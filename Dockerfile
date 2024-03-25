FROM python:3.12.2
WORKDIR /usr/app/bot
COPY . ./
RUN ["pip", "install", "-r", "requirements.txt"]
ENTRYPOINT ["python", "main.py"]