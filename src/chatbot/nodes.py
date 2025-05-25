from state_schema import ChatState
from chains import ChatbotChains
from tools import Tools
import json

class GraphNodes:

    @classmethod
    def classify_intent(cls, state: ChatState) -> ChatState:
        memory= state.get("memory")
        print(state.get("intent"))
        user_input = state.get("user_input") 
        intent=ChatbotChains.classify_intent_chain(memory).invoke({"user_input": user_input})
        return {"intent": intent.intent}
    

    
    @classmethod
    def create_complaint(cls,state: ChatState) -> ChatState:
        user_input = state.get("user_input")
        history = ""
        if state.get("name"):
            history += f"Name: {state['name']}\n"
        if state.get("email"):
            history += f"Email: {state['email']}\n"
        if state.get("phone"):
            history += f"Phone Number: {state['phone']}\n"
        if state.get("complaint_description"):
            history += f"Complaint: {state['complaint_description']}\n"
            
        res = ChatbotChains.create_complaint_chain().invoke({"history": history, "user_input": user_input})
        print(res)
        return {
            "name": res.name ,
            "email": res.email ,
            "phone": res.phone ,
            "complaint_description": res.complaint_description ,
            "bot_response": res.response ,
        }

    
    @classmethod
    def create_complaint_api(cls,state: ChatState) -> ChatState:
        if state.get("name") and state.get("email") and state.get("phone") and state.get("complaint_description"):
            response = Tools.create_complaint_tool.invoke({
            "name": state.get("name") ,
            "phone_number": state.get("phone"),
            "email": state.get("email"),
            "complaint_details": state.get("complaint_description"),
        })
            return {"intent":None,"name":None, "email":None, "phone":None,
                    "complaint_description":None,
                    "bot_response": f'''Your complaint has been registered with ID: {response.get("complaint_id")}. You'll hear back soon.''',
                    "complaint_id": None}
        else:
            return
    
    @classmethod
    def retrieve_complaint(cls, state: ChatState) -> ChatState:
        user_input = state.get("user_input")
        res = ChatbotChains.retrieve_complaint_chain().invoke({"user_input": user_input})
        print(res)
        return {
            "complaint_id": res.complaint_id,
            "bot_response": res.response
        }
        
    @classmethod
    def retrieve_complaint_api(cls, state: ChatState) -> ChatState:
        if state.get("complaint_id"):
            result = Tools.retrieve_complaint_tool.invoke({
                "complaint_id": state.get("complaint_id")
            })

            status_code = result.get("status_code")
            data = result.get("data")
            error = result.get("error")

            if status_code == 200 and data:
                bot_message = json.dumps(data, indent=2)
            elif status_code == 404:
                bot_message = f"No complaint found with the id: {state.get('complaint_id')}"
            else:
                bot_message = error or "Something went wrong"

            return {
                "intent": None,
                "name": None,
                "email": None,
                "phone": None,
                "complaint_description": None,
                "bot_response": bot_message,
                "complaint_id": None
            }
        else:
            return
    
        
    @classmethod
    def search_kb(cls,state: ChatState) -> ChatState:
        user_input = state.get("user_input") 
        memory= state.get("memory")
        res = ChatbotChains.rag_chain(memory).invoke({"question": user_input})
        return {"intent":None, "bot_response": res.content,
                "name": None, "email": None, "phone": None,
                "complaint_description": None, "complaint_id": None}
    
    @classmethod
    def other(cls,state: ChatState) -> ChatState:
        user_input = state.get("user_input")
        memory= state.get("memory")
        res = ChatbotChains.other_chain(memory).invoke({"message": user_input})
        return {"intent":None, "bot_response": res,
                "name": None, "email": None, "phone": None,
                "complaint_description": None, "complaint_id": None}