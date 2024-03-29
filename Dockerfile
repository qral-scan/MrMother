FROM python:3.12.2
WORKDIR /usr/app/bot
COPY . ./
RUN ["pip", "install", "-r", "requirements.txt"]
ENV telegram_token telegram_token
ENV github_token github_token
ENV telegram_group_chat_id telegram_group_chat_id   
ENTRYPOINT ["python", "main.py"]