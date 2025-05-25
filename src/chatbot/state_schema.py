from typing import Optional, List, Tuple, TypedDict, Dict
from langchain.memory import ConversationBufferMemory

class ComplaintChatState(TypedDict):
    userInput: Optional[str]
    conversationHistory: List[Tuple[str, str]]
    intent: Optional[str]
    knowledgeBaseResponse: Optional[str]
    userName: Optional[str]
    userPhone: Optional[str]
    userEmail: Optional[str]
    complaintDetails: Optional[str]
    missingFields: List[str]
    complaintIdToRetrieve: Optional[str]
    createdComplaintId: Optional[str]
    apiResponse: Optional[dict]
    lastBotMessage: Optional[str]
    
# ---- Define State ----
class ChatState(TypedDict):
    user_input: Optional[str]
    intent: Optional[str]
    bot_response: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    complaint_description: Optional[str]
    memory: Optional[ConversationBufferMemory]
    complaint_id: Optional[str]
    