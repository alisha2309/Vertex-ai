import gradio as gr
import requests

BACKEND_URL = "http://backend:8000/chat"
#BACKEND_URL = "http://localhost:8000/chat"

def chat_with_llm(message, history):
    try:
        response = requests.post(BACKEND_URL, json={"message": message})
        bot_message = response.json()["response"]
        return bot_message
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"

# Create Gradio interface with chat
demo = gr.ChatInterface(
    fn=chat_with_llm,
    chatbot=gr.Chatbot(height=600),
    textbox=gr.Textbox(placeholder="Ask me anything...", container=False, scale=7),
    title="AI Chat Assistant",
    description="Chat with an AI using ChatGPT API",
    theme="soft",
    examples=["Tell me a joke", "What is the meaning of life?", "Write a short poem"],
    cache_examples=False,
    retry_btn="Retry ↺",
    undo_btn="Undo ↶",
    clear_btn="Clear 🗑️"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860) 