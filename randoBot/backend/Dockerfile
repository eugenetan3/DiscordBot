FROM python:3.6

RUN apt-get update && pip install flask

COPY . /app
WORKDIR /app
CMD ["python3", "./backend.py"]