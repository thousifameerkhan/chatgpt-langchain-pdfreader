docker build -t ai-chat-app .

docker run -p 8000:8000 --env-file .env my-python-app

docker save -o ai-chat-app.tar ai-chat-app


docker load -i ai-chat-app.tar