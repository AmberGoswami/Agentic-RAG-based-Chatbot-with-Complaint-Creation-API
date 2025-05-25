import gradio as gr
import uuid
from graph_builder import handle_user_input  # Replace with your actual module path

user_ids = {}

def gradio_chat(message, history, session_id=None):
    if session_id is None or session_id not in user_ids:
        session_id = str(uuid.uuid4())
        user_ids[session_id] = session_id

    reply = handle_user_input(user_ids[session_id], message)
    history = history + [{"role": "user", "content": message}, {"role": "assistant", "content": reply}]
    return history, session_id, ""  # clear input

with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Comprehensive Customer Support and Service Policy for electronics")

    with gr.Column():
        chatbot = gr.Chatbot(label="Bot", type="messages")
        session_state = gr.State()

        with gr.Row():
            txt = gr.Textbox(
                show_label=False,
                placeholder="Type your message here...",
                container=True,
                scale=10
            )
            send_btn = gr.Button("Send", scale=2)

    txt.submit(gradio_chat, [txt, chatbot, session_state], [chatbot, session_state, txt])
    send_btn.click(gradio_chat, [txt, chatbot, session_state], [chatbot, session_state, txt])

demo.launch()
