FROM ubuntu:latest
LABEL authors="blackthunder"

ENTRYPOINT ["top", "-b"]


FROM python:3.10-slim

WORKDIR app


COPY . .

EXPOSE 3000


RUN pip install -r requirements.txt


CMD ["python", "bot.py"]