import os
import json


def get_thread_id(message):
  try:
    thread_id = message.reply_to_message.message_thread_id
  except AttributeError:
    thread_id = None
  return thread_id

def is_reciever(message, chat_settings):
  thread_id = get_thread_id(message)
  for reciever in chat_settings['recievers']:
    if (
      reciever['chat_id'] == message.chat.id
      and reciever['thread_id'] == thread_id
    ):
      return True
  return False

def is_forwarder(message, chat_settings):
  thread_id = get_thread_id(message)
  for forwarder in chat_settings['forwarders']:
    if (
      forwarder['chat_id'] == message.chat.id
      and forwarder['thread_id'] == thread_id
    ):
      return True
  return False

def can_control_bot(message, settings, chat_settings):
  try:
    if (
      message.from_user.id in chat_settings['superuser_ids']
      or not settings['superuser_access']
    ):
      return True
  except:
    return False
  return False

def is_superuser(user_id, chat_settings):
  try:
    if (
      user_id in chat_settings['superuser_ids']
    ):
      return True
  except:
    return False
  return False

def is_default_superuser(user_id, settings):
  try:
    if (
      user_id in settings['default_superuser_ids']
    ):
      return True
  except:
    return False
  return False

def update_chat_settings(chat_settings):
  with open(
    os.path.dirname(os.path.abspath(__file__)) + '/../conf/chat_settings.json',
    'w',
    encoding = 'utf-8'
  ) as chat_settings_file:
    json.dump(chat_settings, chat_settings_file)
