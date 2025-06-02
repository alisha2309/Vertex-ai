from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Simple chatbot logic
def get_bot_response(message):
    message = message.lower().strip()
    responses = {
        "hello": "Hi there!",
        "how are you": "I'm doing great, thanks for asking!",
        "bye": "Goodbye! Have a great day!",
        "help": "I'm a simple chatbot. Try saying 'hello', 'how are you', or 'bye'."
    }
    return responses.get(message, "Sorry, I didn't understand that. Try something else!")

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Chatbot API! Use POST /chat to interact."})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Please provide a message"}), 400
    user_message = data['message']
    bot_response = get_bot_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
