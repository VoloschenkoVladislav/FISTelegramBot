# Telegram-бот FISModelBot

## Цели бота

Бот создан в рамках необходимости передачи отмеченных тегом сообщений в груповых чатах в другие заданные чаты.

## Загрузка и установка бота

> **Внимание!** Перед установкой и запуском бота зарегистрируйте бота в Telegram при помощи бота *BotFather* и получите его ID, т.к. это понадобится в последующих шагах.

### Загрузка

Введите в консоли:

```
>>> git clone https://github.com/VoloschenkoVladislav/FISTelegramBot
```

Дождитесь загрузки бота с репозитория.

### Настройка

Создайте конфиграционный файл командой:

```
>>> cp ./FISTelegramBot/conf/app_settings.json.example ./FISTelegramBot/conf/app_settings.json
```

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

При установке опции `superuser_access: true` для ограниченного доступа к настройке бота следует указать в конфигурации список ID пользователей в опции `default_superuser_ids`:

```
{
  "bot_id": "<ID вашего бота>",
  ...
  "superuser_access": true,
  "default_superuser_ids": [
    <ID суперпользователя 1>,
    <ID суперпользователя 2>,
    ...
  ],
  ...
}
```

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

Для работы бота добавьте его в целевые чаты. Проверить работспособность бота и узнать его возможности можно командой `/start` или `/help`.

Отправка сообщения начинающегося с заданного в конфигурации триггер-тега (по умолчанию `"#изменение_модели\n"`) спровоцирует пересылку сообщения в чаты с настроенным на приём ботом за исключением чата, в которого произошла отправка сообщения.

После успешной пересылки бот проставит реакцию на сообщение, заданную в конфигурации (также бота можно настроить на отправку текстового подтверждения отправки). 
