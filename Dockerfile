FROM python:3.9-slim
EXPOSE 8000

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install poppler-utils -y

CMD python3 app.py
