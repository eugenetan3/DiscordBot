FROM python:3.6

RUN apt-get update && python3 -m pip install discord.py==0.16.12 

COPY . /app
WORKDIR /app
CMD ["python3", "./bot.py"]

