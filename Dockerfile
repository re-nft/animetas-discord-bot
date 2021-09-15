FROM python:3.8.3-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev && \
    apt-get clean


COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY src .

CMD ["python", "main.py"]
