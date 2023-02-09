FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py", "--id", "1", "--target", "ws://actuatorserver:8765","--actuator_type","water_sprinkler"]