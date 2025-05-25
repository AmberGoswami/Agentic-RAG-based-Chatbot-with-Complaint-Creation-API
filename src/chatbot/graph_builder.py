from state_schema import ChatState
from langgraph.graph import StateGraph, END
from nodes import GraphNodes
from typing import Dict
from langchain.memory import ConversationBufferMemory

user_sessions: Dict[str, ChatState] = {}

workflow = StateGraph(ChatState)
workflow.add_node("classify_intent", GraphNodes().classify_intent)
workflow.add_node("search_kb_node", GraphNodes().search_kb)
workflow.add_node("other_node", GraphNodes().other)
workflow.add_node("create_complaint_node", GraphNodes().create_complaint)
workflow.add_node("create_complaint_api", GraphNodes().create_complaint_api)
workflow.add_node("retrieve_complaint_api", GraphNodes().retrieve_complaint_api)
workflow.add_node("retrieve_complaint_node", GraphNodes().retrieve_complaint)

workflow.set_entry_point("classify_intent")
workflow.add_conditional_edges("classify_intent", lambda s: s["intent"], {
    "create_complaint": "create_complaint_node",
    "retrieve_complaint": "retrieve_complaint_node",
    "search_kb": "search_kb_node",
    "other": "other_node",
})

workflow.add_edge("create_complaint_node", "create_complaint_api")
workflow.add_edge("retrieve_complaint_node", "retrieve_complaint_api")
workflow.add_edge("create_complaint_api", END)
workflow.add_edge("retrieve_complaint_api", END)
workflow.add_edge("search_kb_node", END)
workflow.add_edge("other_node", END)
graph = workflow.compile()



def handle_user_input(user_id: str, user_input: str) -> str:
    print("User sessions:", user_sessions.keys())
    state = user_sessions.get(user_id)

    if not state:
        memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
        state = ChatState(user_input="", intent=None, memory=memory)
        user_sessions[user_id] = state
    memory = state["memory"]
    memory.chat_memory.add_user_message(user_input)
    state["user_input"] = user_input
    state["chat_history"] = memory.chat_memory.messages
    updated_state = graph.invoke(state)
    bot_reply = updated_state.get("bot_response", "[No response]")
    memory.chat_memory.add_ai_message(bot_reply)
    updated_state["memory"] = memory
    user_sessions[user_id] = updated_state
    return bot_reply

