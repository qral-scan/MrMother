FROM python:3.9.6
WORKDIR /usr/app/bot
COPY . ./
RUN ["pip", "install", "-r", "requirements.txt"]
ENTRYPOINT ["python", "MrMother.py"]