FROM python:3.14.0a3-alpine3.20

WORKDIR /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/src

RUN pip install pytelegrambotapi

CMD ["python", "bot.py"]
