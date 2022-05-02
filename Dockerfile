FROM python:3.9-slim
EXPOSE 8000

WORKDIR /app

RUN apt-get update \
    && apt-get install poppler-utils -y

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD python3 app.py
