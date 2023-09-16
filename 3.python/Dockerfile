FROM python:3.8-slim

RUN pip install flask

WORKDIR /app
COPY . .

ENTRYPOINT ["python", "app.py"]