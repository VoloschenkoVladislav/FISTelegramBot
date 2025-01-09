import telebot
from telebot.types import ReactionTypeEmoji
import os
import json
from utils import (
  get_thread_id,
  is_reciever,
  is_forwarder,
  can_control_bot,
  is_superuser,
  is_default_superuser,
  update_chat_settings
)


if not os.path.exists(
  os.path.dirname(os.path.abspath(__file__)) + '/../conf/chat_settings.json'
):
  with open(
    os.path.dirname(os.path.abspath(__file__)) + '/../conf/chat_settings.json', 'w'
  ): pass

with open(
  os.path.dirname(os.path.abspath(__file__)) + '/../conf/app_settings.json',
  encoding = 'utf-8'
) as settings_file:
  settings = json.load(settings_file)

with open(
  os.path.dirname(os.path.abspath(__file__)) + '/../conf/chat_settings.json',
  'r+',
  encoding = 'utf-8'
) as chat_settings_file:
  try:
    chat_settings = json.load(chat_settings_file)
  except json.decoder.JSONDecodeError:
    json.dump(
      {
        'recievers': [],
        'forwarders': [],
        'superuser_ids': settings['default_superuser_ids']
      },
      chat_settings_file
    )
    chat_settings = json.loads(
      '{"recievers": [], "forwarders": [], "superuser_ids": ' + str(settings['default_superuser_ids']) + '}'
    )

keyErr = False
try:
  chat_settings['recievers']
except KeyError:
  chat_settings['recievers'] = []
  keyErr = True
try:
  chat_settings['forwarders']
except KeyError:
  chat_settings['forwarders'] = []
  keyErr = True
try:
  chat_settings['superuser_ids']
except KeyError:
  chat_settings['superuser_ids'] = settings['default_superuser_ids']
  keyErr = True
if keyErr:
  update_chat_settings(chat_settings)


bot = telebot.TeleBot(settings['bot_id'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(
    message.chat.id,
    settings['response_messages']['start_message'],
    message_thread_id = get_thread_id(message)
  )


@bot.message_handler(commands=['status'])
def status(message):
  reciever_status = 'вкл. ⬇️' if is_reciever(message, chat_settings) else 'выкл. ⏸'
  forwarder_status = 'вкл. ⬆️' if is_forwarder(message, chat_settings) else 'выкл. ⏸'
  bot.send_message(
    message.chat.id,
    'Статус чата:\nОтправка сообщений ' + forwarder_status + '\nПриём сообщений ' + reciever_status,
    message_thread_id = get_thread_id(message)
  )


@bot.message_handler(commands=['enable_recieve'])
def enable_recieve(message):
  thread_id = get_thread_id(message)
  if can_control_bot(message, settings, chat_settings):
    if is_reciever(message, chat_settings):
      bot.send_message(
        message.chat.id,
        settings['response_messages']['already_in_recievers'],
        message_thread_id = thread_id
      )
    else:
      chat_settings['recievers'].append({
        'chat_id': message.chat.id,
        'thread_id': thread_id
      })
      update_chat_settings(chat_settings)
      bot.send_message(
        message.chat.id,
        settings['response_messages']['added_to_recievers'],
        message_thread_id = thread_id
      )
  else:
    bot.send_message(
      message.chat.id,
      settings['response_messages']['not_enough_rights'],
      message_thread_id = thread_id
    )


@bot.message_handler(commands=['disable_recieve'])
def disable_recieve(message):
  thread_id = get_thread_id(message)
  if can_control_bot(message, settings, chat_settings):
    if not is_reciever(message, chat_settings):
      bot.send_message(
        message.chat.id,
        settings['response_messages']['already_excluded_from_recievers'],
        message_thread_id = thread_id
      )
    else:
      chat_settings['recievers'].remove({
        'chat_id': message.chat.id,
        'thread_id': thread_id
      })
      update_chat_settings(chat_settings)
      bot.send_message(
        message.chat.id,
        settings['response_messages']['excluded_from_recievers'],
        message_thread_id = thread_id
      )
  else:
    bot.send_message(
      message.chat.id,
      settings['response_messages']['not_enough_rights'],
      message_thread_id = thread_id
    )


@bot.message_handler(commands=['enable_forward'])
def enable_forward(message):
  thread_id = get_thread_id(message)
  if can_control_bot(message, settings, chat_settings):
    if is_forwarder(message, chat_settings):
      bot.send_message(
        message.chat.id,
        settings['response_messages']['already_in_forwarders'],
        message_thread_id = thread_id
      )
    else:
      chat_settings['forwarders'].append({
        'chat_id': message.chat.id,
        'thread_id': thread_id
      })
      update_chat_settings(chat_settings)
      bot.send_message(
        message.chat.id,
        settings['response_messages']['added_to_forwarders'],
        message_thread_id = thread_id
      )
  else:
    bot.send_message(
      message.chat.id,
      settings['response_messages']['not_enough_rights'],
      message_thread_id = thread_id
    )


@bot.message_handler(commands=['disable_forward'])
def disable_forward(message):
  thread_id = get_thread_id(message)
  if can_control_bot(message, settings, chat_settings):

    if not is_forwarder(message, chat_settings):
      bot.send_message(
        message.chat.id,
        settings['response_messages']['already_excluded_from_forwarders'],
        message_thread_id = thread_id
      )
    else:
      chat_settings['forwarders'].remove({
        'chat_id': message.chat.id,
        'thread_id': thread_id
      })
      update_chat_settings(chat_settings)
      bot.send_message(
        message.chat.id,
        settings['response_messages']['excluded_from_forwarders'],
        message_thread_id = thread_id
      )
  else:
    bot.send_message(
      message.chat.id,
      settings['response_messages']['not_enough_rights'],
      message_thread_id = thread_id
    )


@bot.message_handler(commands=['add_superuser'])
def add_superuser(message):
  thread_id = get_thread_id(message)
  if can_control_bot(message, settings, chat_settings):
    try:
      new_superuser_id = int(message.text.split()[1:][0])
    except ValueError:
      bot.send_message(
        message.chat.id,
        settings['response_messages']['invalid_superuser_id'],
        message_thread_id = thread_id
      )
      return
    except IndexError:
      bot.send_message(
        message.chat.id,
        settings['response_messages']['user_is_not_specified'],
        message_thread_id = thread_id
      )
      return
    if is_superuser(new_superuser_id, chat_settings):
      bot.send_message(
        message.chat.id,
        settings['response_messages']['already_superuser'],
        message_thread_id = thread_id
      )
    else:
      chat_settings['superuser_ids'].append(new_superuser_id)
      update_chat_settings(chat_settings)
      bot.send_message(
        message.chat.id,
        settings['response_messages']['added_to_superusers'],
        message_thread_id = thread_id
      )
  else:
    bot.send_message(
      message.chat.id,
      settings['response_messages']['not_enough_rights'],
      message_thread_id = thread_id
    )


@bot.message_handler(commands=['remove_superuser'])
def remove_superuser(message):
  thread_id = get_thread_id(message)
  if can_control_bot(message, settings, chat_settings):
    try:
      superuser_to_delete_id = int(message.text.split()[1:][0])
    except ValueError:
      bot.send_message(
        message.chat.id,
        settings['response_messages']['invalid_superuser_id'],
        message_thread_id = thread_id
      )
      return
    except IndexError:
      bot.send_message(
        message.chat.id,
        settings['response_messages']['user_is_not_specified'],
        message_thread_id = thread_id
      )
      return
    if not is_superuser(superuser_to_delete_id, chat_settings):
      bot.send_message(
        message.chat.id,
        settings['response_messages']['already_not_superuser'],
        message_thread_id = thread_id
      )
    else:
      if not is_default_superuser(superuser_to_delete_id, settings):
        chat_settings['superuser_ids'].remove(superuser_to_delete_id)
        update_chat_settings(chat_settings)
        bot.send_message(
          message.chat.id,
          settings['response_messages']['removed_from_superusers'],
          message_thread_id = thread_id
        )
      else:
        bot.send_message(
          message.chat.id,
          settings['response_messages']['cannot_remove_default_superuser'],
          message_thread_id = thread_id
        )
  else:
    bot.send_message(
      message.chat.id,
      settings['response_messages']['not_enough_rights'],
      message_thread_id = thread_id
    )


@bot.message_handler(content_types=['text'])
def forward_message(message):
  thread_id = get_thread_id(message)
  
  if is_forwarder(message, chat_settings):
    for chat in chat_settings['recievers']:
      if (
        message.text.startswith(settings['trigger_tag'])
        and (
          message.chat.id == chat['chat_id']
          and thread_id != chat['thread_id']
          and settings['send_to_same_chat']
          or
          message.chat.id != chat['chat_id']
        ) 
      ):
        try:
          bot.forward_message(
            chat['chat_id'],
            message.chat.id,
            message.message_id,
            message_thread_id = chat['thread_id']
          )
          if settings['response_types']['emoji']:
            try:
              bot.set_message_reaction(
                message.chat.id,
                message.id,
                [ReactionTypeEmoji(settings['response_messages']['response_emoji'])],
                is_big = False
              )
            except:
              bot.send_message(
                message.chat.id,
                settings['response_messages']['emoji_response_error'],
                message_thread_id = thread_id
              )
              break
          if settings['response_types']['text']:
            try:
              bot.send_message(
                message.chat.id,
                settings['response_messages']['send_success'],
                message_thread_id = thread_id
              )
            except:
              bot.send_message(
                message.chat.id,
                settings['response_messages']['text_response_error'],
                message_thread_id = thread_id
              )
              break
        except Exception as error:
          if settings['show_error_details']:
            bot.send_message(
              message.chat.id,
              settings['response_messages']['send_error'] + '\n\n' + f'Unexpected {error=}, {type(error)=}',
              message_thread_id = thread_id
            )
          else:
            bot.send_message(
              message.chat.id,
              settings['response_messages']['send_error'],
              message_thread_id = thread_id
            )
          break

bot.infinity_polling()
