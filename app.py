from flask import Flask, request, jsonify, send_from_directory
import os
import vertexai
from vertexai.generative_models import GenerativeModel
import logging

app = Flask(__name__, static_folder='.', static_url_path='')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vertex AI
project_id = "black-cirrus-461305-f6"
location = "us-central1"
vertexai.init(project=project_id, location=location)

# Load Gemini model
try:
    model = GenerativeModel("gemini-1.5-pro")
    logger.info("Successfully loaded Gemini model: gemini-1.5-pro")
except Exception as e:
    logger.error(f"Failed to load Gemini model: {str(e)}")
    raise

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        logger.error("Invalid request: No message provided")
        return jsonify({"error": "Please provide a message"}), 400
    
    user_message = data['message']
    logger.info(f"Received user message: {user_message}")
    
    # Start a chat session with Gemini
    try:
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": ["What is the capital of France?"]},
                {"role": "model", "parts": ["The capital of France is Paris."]}
            ]
        )
        logger.info("Successfully started chat session")
    except Exception as e:
        logger.error(f"Failed to start chat session: {str(e)}")
        return jsonify({"response": f"Error starting chat: {str(e)}"}), 500
    
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
        logger.info(f"Gemini response: {bot_response}")
    except Exception as e:
        logger.error(f"Failed to get Gemini response: {str(e)}")
        bot_response = f"Error: {str(e)}"
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
