FROM python:3.8

WORKDIR /usr/src/app/
COPY . /usr/src/app/

RUN pip install pytelegrambotapi

CMD ["python", "bot.py"]
