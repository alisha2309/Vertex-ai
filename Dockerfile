FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT 8080
CMD exec gunicorn --bind :$PORT app:app