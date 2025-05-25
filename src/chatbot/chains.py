import os
from typing import Optional
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from prompts import classify_intent_prompt, create_complaint_prompt, retrieve_complaint_prompt, rag_chat_prompt, default_prompt
from pydantic import BaseModel, Field
from dotenv import load_dotenv

class ChatbotChains:
    load_dotenv()
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    @classmethod
    def classify_intent_chain(cls, memory):
        class Intent(BaseModel):
            intent: str = Field(description="Intent of the text (always one of the following: 'create_complaint', 'retrieve_complaint', 'search_kb', 'other )")
            
        parser = PydanticOutputParser(pydantic_object=Intent)
        prompt = ChatPromptTemplate.from_messages(classify_intent_prompt)
        formatted_prompt = prompt.partial(
                format_instructions=parser.get_format_instructions()
            )
        chain = (
            RunnablePassthrough.assign(
                chat_history=lambda x: memory.load_memory_variables(x)["chat_history"]
            )
            | formatted_prompt
            | cls.model.with_config({
                "temperature": 0.3
            }).with_structured_output(Intent)  
        )
        return chain
    
    @classmethod
    def create_complaint_chain(cls):
        class ComplaintInfo(BaseModel):
            name: Optional[str] = Field(description="User's name")
            email: Optional[str] = Field(description="User's email address")
            phone: Optional[str] = Field(description="User's phone address")
            complaint_description: Optional[str] = Field(description="Complaint description")
            response: Optional[str] = Field(description="Bot response to user")
            
        parser = PydanticOutputParser(pydantic_object=ComplaintInfo)
        prompt = ChatPromptTemplate.from_messages(create_complaint_prompt)
        formatted_prompt = prompt.partial(
                format_instructions=parser.get_format_instructions()
            )
        
        chain =(
            formatted_prompt
            | cls.model.with_config({
                "temperature": 0.3
            }).with_structured_output(ComplaintInfo)  
        )
        return chain
    
    @classmethod
    def retrieve_complaint_chain(cls):
        class ComplaintRetrieved(BaseModel):
            complaint_id: Optional[str] = Field(description="Complaint ID")
            response: Optional[str] = Field(description="Bot response to user")

        parser = PydanticOutputParser(pydantic_object=ComplaintRetrieved)
        prompt = ChatPromptTemplate.from_messages(retrieve_complaint_prompt)
        formatted_prompt = prompt.partial(
                format_instructions=parser.get_format_instructions()
            )

        chain =(
            formatted_prompt
            | cls.model.with_config({
                "temperature": 0.3
            }).with_structured_output(ComplaintRetrieved)
        )
        return chain
    
    @classmethod
    def rag_chain(cls, memory, vectorstore_path="faiss_index", data_path="kb.txt"):
        embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5",
            encode_kwargs={"normalize_embeddings": True}  
        )

        if os.path.exists(vectorstore_path):
            db = FAISS.load_local(vectorstore_path, embedding_model, allow_dangerous_deserialization=True)
        else:
            loader = TextLoader(data_path, encoding="utf-8")
            docs = CharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(loader.load())
            db = FAISS.from_documents(docs, embedding_model)
            db.save_local(vectorstore_path)

        retriever = db.as_retriever(search_kwargs={"k": 3})
        prompt = ChatPromptTemplate.from_messages(rag_chat_prompt)

        def format_docs(docs):
            return "\n\n".join([doc.page_content for doc in docs])

        
        chain = (
            RunnablePassthrough.assign(
                chat_history=lambda x: memory.load_memory_variables(x)["chat_history"],
                context=lambda x: format_docs(retriever.invoke(x["question"]))
            )
            | prompt
            | cls.model.with_config({"max_tokens": 100, "temperature": 0.5})
        )
        return chain
    
    @classmethod
    def other_chain(cls, memory):
        prompt = ChatPromptTemplate.from_messages(default_prompt)
        chain = (
            RunnablePassthrough.assign(
                chat_history=lambda x: memory.load_memory_variables(x)["chat_history"]
            )
            | prompt
            | cls.model.with_config({"max_tokens": 50, "temperature": 1})
            | StrOutputParser()
        )
        return chain