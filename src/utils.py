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

def can_control_bot(message, settings):
  try:
    if (
      message.from_user.id in settings['superuser_ids']
      or not settings['superuser_access']
    ):
      return True
  except:
    return False
  return False
