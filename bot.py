import telebot
from telebot.types import ReactionTypeEmoji
from dotenv import load_dotenv
import os


load_dotenv()
BOTID = os.getenv('BOTID')
CHATID = os.getenv('CHATID')
TRIGGER_TAG = os.getnev('TRIGGER_TAG')
EMOJI_REACTION = os.getenv('EMOJI_REACTION').lower() in ('true', '1', 't')
TEXT_REACTION = os.getenv('TEXT_REACTION').lower() in ('true', '1', 't')
TEXT_REACTION_VALUE = os.getenv('TEXT_REACTION_VALUE')

bot = telebot.TeleBot(BOTID)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id, 'FISModelBot активен. Версия 1.0.0.')

@bot.message_handler(content_types=['text'])
def forward_message(message):
  if message.text.startswith(TRIGGER_TAG) and message.chat.id != CHATID:
    try:
      bot.forward_message(CHATID, message.chat.id, message.message_id)
    except:
      bot.send_message(message.chat.id, 'Не удалось доставить сообщение, проверьте настройки бота')
      return
    if EMOJI_REACTION:
      bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
    if TEXT_REACTION:
      bot.send_message(message.chat.id, TEXT_REACTION_VALUE)

bot.infinity_polling()
