from flask import Flask, request, jsonify, send_from_directory
import os
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import storage
import csv
from io import StringIO
import logging

app = Flask(__name__, static_folder='.', static_url_path='')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vertex AI
project_id = "black-cirrus-461305-f6"
location = "us-central1"
vertexai.init(project=project_id, location=location)

# Initialize Cloud Storage client
storage_client = storage.Client(project=project_id)

# Load Gemini model
try:
    model = GenerativeModel("gemini-1.5-pro")
    logger.info("Successfully loaded Gemini model: gemini-1.5-pro")
except Exception as e:
    logger.error(f"Failed to load Gemini model: {str(e)}")
    raise

# Function to load CSV from Cloud Storage
def load_csv_from_storage(bucket_name, file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data = blob.download_as_text()
        csv_file = StringIO(data)
        csv_reader = csv.DictReader(csv_file)
        data_list = [row for row in csv_reader]
        logger.info(f"Successfully loaded CSV file: {file_name}")
        return data_list
    except Exception as e:
        logger.error(f"Failed to load CSV from {bucket_name}/{file_name}: {str(e)}")
        return None

# Load your CSV file (replace with your bucket and file name)
BUCKET_NAME = "your-bucket-name"  # Replace with your Cloud Storage bucket name
CSV_FILE_NAME = "your-file.csv"  # Replace with your CSV file name
csv_data = load_csv_from_storage(BUCKET_NAME, CSV_FILE_NAME)

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
    
    # Check if CSV data was loaded successfully
    if csv_data is None:
        logger.error("CSV data not available")
        return jsonify({"response": "Error: Unable to access CSV data"}), 500

    # Search CSV data for relevant context
    context = ""
    for row in csv_data:
        # Example: Search for user_message in any column (customize this logic)
        if any(user_message.lower() in str(value).lower() for value in row.values()):
            context += f"Found in CSV: {row}\n"
    
    # If no relevant data found, provide a default message
    if not context:
        context = "No relevant data found in the CSV for your query."

    # Combine user message with CSV context for Gemini
    prompt = f"User query: {user_message}\nContext from CSV: {context}\nProvide a response based on the query and context."

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
    
    # Send user input and CSV context to Gemini and get response
    try:
        response = chat.send_message(
            content=prompt,
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
