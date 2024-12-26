import telebot
from telebot.types import ReactionTypeEmoji
import os
import json


with open(os.path.dirname(os.path.abspath(__file__)) + '/../conf/app_settings.json', encoding = 'utf-8') as settings_file:
  settings = json.load(settings_file)

bot = telebot.TeleBot(settings['bot_id'])

print('FISModelBot is running.')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id, settings['response_messages']['start_message'])

@bot.message_handler(content_types=['text'])
def forward_message(message):
  for chat_id in settings['chats_ids']:
    if message.text.startswith(settings['trigger_tag']) and message.chat.id != chat_id:
      try:
        bot.forward_message(chat_id, message.chat.id, message.message_id)
      except:
        bot.send_message(message.chat.id, settings['response_messages']['send_error'])
        return
  if settings['response_types']['emoji']:
    try:
      bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(settings['response_messages']['response_emoji'])], is_big = False)
    except:
      bot.send_message(message.chat.id, settings['response_messages']['emoji_response_error'])
      return
  if settings['response_types']['text']:
    try:
      bot.send_message(message.chat.id, settings['response_messages']['send_success'])
    except:
      bot.send_message(message.chat.id, settings['response_messages']['text_response_error'])
      return

bot.infinity_polling()
