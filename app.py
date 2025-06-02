from flask import Flask, request, jsonify, send_from_directory
import os
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

app = Flask(__name__, static_folder='.', static_url_path='')

# Initialize Vertex AI
project_id = "black-cirrus-461305-f6"
location = "us-central1"
vertexai.init(project=project_id, location=location)

# Load Gemini model
model = GenerativeModel("gemini-1.5-flash")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Please provide a message"}), 400
    
    user_message = data['message']
    
    # Start a chat session with Gemini
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": ["What is the capital of France?"]},
            {"role": "model", "parts": ["The capital of France is Paris."]}
        ]
    )
    
    # Send user input to Gemini and get response
    try:
        response = chat.send_message(
            content=user_message,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 256,
                "top_p": 0.8,
                "top_k": 40
            }
        )
        bot_response = response.text
    except Exception as e:
        bot_response = f"Error: {str(e)}"
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
