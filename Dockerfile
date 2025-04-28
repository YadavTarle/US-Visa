FROM python:3.8-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r reuirements.txt

CMD ["python3","app.py"]
