document.getElementById("send-button").onclick = async function() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    // Display user's message
    addMessage(userInput, "user");
    document.getElementById("user-input").value = ""; // Clear input

    // Show "Bot is typing..." before the bot's message
    const messagesDiv = document.getElementById("messages");
    const botTypingDiv = document.createElement("div");
    botTypingDiv.className = "message bot typing"; // Add typing class
    const typingText = document.createElement("div");
    typingText.className = "typing-text";
    typingText.textContent = "Bot is typing...";
    botTypingDiv.appendChild(typingText);
    messagesDiv.appendChild(botTypingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll to the bottom

    // Send the message to the Flask backend
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    const botMessage = data.response;

    // Remove typing message and show the bot's actual response
    setTimeout(() => {
        botTypingDiv.remove(); // Remove the typing message
        addMessage(botMessage, "bot"); // Add the bot's actual response
    }, 1500); // Simulate typing delay (adjustable)
};

function addMessage(text, sender) {
    const messagesDiv = document.getElementById("messages");
    const messageElement = document.createElement("div");
    messageElement.className = `message ${sender}`;

    // Add message text
    const messageTextElement = document.createElement("div");
    messageTextElement.className = "message-text";
    messageTextElement.textContent = text;

    // Add timestamp
    const timestampElement = document.createElement("div");
    timestampElement.className = "timestamp";
    timestampElement.textContent = new Date().toLocaleTimeString();

    // Append text and timestamp to the message
    messageElement.appendChild(messageTextElement);
    messageElement.appendChild(timestampElement);

    // Append the message to the chat
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll to the bottom
}
