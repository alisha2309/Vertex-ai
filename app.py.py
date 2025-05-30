from flask import Flask, request, jsonify, render_template
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from google.cloud import discoveryengine_v1 as discoveryengine
import os

app = Flask(__name__)

# Initialize Vertex AI
PROJECT_ID = os.environ.get("PROJECT_ID", "your-project-id")  # Set your project ID
LOCATION = "us-central1"  # Adjust to your region
DATA_STORE_ID = os.environ.get("DATA_STORE_ID", "company-data-store")  # Optional: for RAG
vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_chat_session():
    chat_model = ChatModel.from_pretrained("chat-bison@002")  # Or use "gemini-1.5-pro"
    context = "You are a helpful customer support chatbot for YourCompany. Answer queries politely and accurately."
    examples = [
        InputOutputTextPair(
            input_text="What are your business hours?",
            output_text="Our business hours are 9 AM to 5 PM, Monday to Friday."
        )
    ]
    chat = chat_model.start_chat(context=context, examples=examples)
    return chat

def query_data_store(user_message):
    """Query Vertex AI Data Store for RAG (optional)."""
    try:
        client = discoveryengine.DocumentServiceClient()
        parent = f"projects/{PROJECT_ID}/locations/global/dataStores/{DATA_STORE_ID}"
        request = discoveryengine.SearchRequest(
            query=user_message,
            page_size=5,
            serving_config=f"{parent}/servingConfigs/default_config"
        )
        response = client.search(request)
        return [result.document.content for result in response.results]
    except Exception as e:
        print(f"Data store query failed: {e}")
        return []

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Optional: Query data store for RAG context
    context_results = query_data_store(user_message)
    context = "Relevant information: " + " ".join(context_results[:3]) if context_results else ""

    # Initialize chat session and send message
    chat_session = create_chat_session()
    parameters = {
        "temperature": 0.7,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    try:
        response = chat_session.send_message(user_message + "\n" + context, **parameters)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": f"Chatbot error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))