# Telegram-бот FISModelBot

## Цели бота

Бот создан в рамках необходимости передачи отмеченных тегом сообщений в груповых чатах в другие заданные чаты.

## Загрузка и установка бота

> **Внимание!** Перед установкой и запуском бота зарегистрируйте бота в Telegram при помощи бота *BotFather* и получите его ID, т.к. это понадобится в последующих шагах. Также узнайте ID чатов, которые будут задействованы в работе бота.

### Загрузка

Введите в консоли:

```
>>> git clone https://github.com/VoloschenkoVladislav/FISTelegramBot
```

Дождитесь загрузки бота с репозитория.

### Настройка

Отредактируйте конфигурационный файл бота любым удобным для вас текстовым редактором, например, с помощью Vim:

```
>>> vim ./FISTelegramBot/conf/app_settings.json
```

Задайте в файле ID бота, зарегистрированного в Telegram:

```
{
  "bot_id": "<ID вашего бота>",
  ...
  ...
}
```

Задайте ID чатов, по которым должна осуществляться рассылка:

```
{
  "bot_id": "7702867423:AAHqYvz-LzBv4UCUPSNImRl8trsA4u_K-xE",
  "chats_ids": [
    <ID чата №1>,
    <ID чата №2>,
    ...
  ],
  ...
  ...
}
```

> Обратите внимание на то, что ID чатов должны быть **отрицательными числами**. ID вашего бота должен быть строковым значением.

Прочие настройки можно оставить без изменений.

### Установка и запуск

Перейдите в загруженную с репозитория директорию и введите в консоли:

```
>>> cd ./FISTelegramBot
>>> docker build -t fis_model_telegram_bot .
```

Дождитесь создания образа. Затем запустите контейнер с помощью команды:

```
>>> docker run -d fis_model_telegram_bot
```

Готово!

## Использование бота

Для работы бота добавьте его в целевые чаты. Проверить работспособность бота можно командой `/start`.

Отправка сообщения начинающегося с заданного в конфигурации триггер-тега спровоцирует пересылку ботом сообщения в чаты указанные в конфигурации (по умолчанию `"#изменение_модели\n"`) за исключением чата, в которого произошла отправка сообщения.

После успешной пересылки бот проставит реакцию на сообщение, заданную в конфигурации (также бота можно настроить на отправку текстового подтверждения отправки). 
