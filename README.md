# LLM Chatbot with Microservices Architecture and Docker Containerization.

## Overview

This project demonstrates building a simple yet scalable LLM chat application using microservices architecture and Docker for containerization. It provides a user-friendly web interface to interact with OpenAI's GPT models through a chat interface.

## Technical Blog or Article explaninig the project

[Technical Blog Link: Code](https://shaktiwadekar.medium.com/learning-to-build-scalable-llm-chat-application-microservices-architecture-and-docker-93ea1335871e)

[Technical Blog Link: AWS](https://shaktiwadekar.medium.com/understanding-scalable-deployment-tools-on-aws-aws-ecr-ecs-alb-iam-and-secrets-manager-8869c937de88)


## Files information

### Components

- **Frontend Service**
  - Built with Gradio for an interactive chat interface
  - Runs on port 7860
  - Communicates with the backend service

- **Backend Service**
  - Built with FastAPI
  - Handles API requests to OpenAI
  - Runs on port 8000
  - Requires OpenAI API key

## Prerequisites

1. Docker and Docker Compose installed on your system
2. OpenAI API key
3. Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create the `.env` file with your OpenAI API key as shown above

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Open your browser and go to: `http://localhost:7860`
   - The chat interface will be ready to use

## Testing the Application

1. The frontend will be available at: `http://localhost:7860`
2. The backend API will be available at: `http://localhost:8000`
3. Try the example prompts provided in the interface:
   - "Tell me a joke"
   - "What is the meaning of life?"
   - "Write a short poem"

## Development

- Frontend modifications can be made in `frontend/app.py`
- Backend modifications can be made in `backend/app.py`
- After making changes, rebuild the containers:
  ```bash
  docker-compose down
  docker-compose up --build
  ```

## Troubleshooting

1. If you see API key errors, ensure your `.env` file is properly configured
2. If containers fail to start, check if ports 7860 and 8000 are available
3. For connection issues, ensure both services are running:
   ```bash
   docker-compose ps
   ```


