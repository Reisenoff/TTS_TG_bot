# Voice Message Translator Bot

## Описание

Этот бот предназначен для обработки голосовых сообщений, их расшифровки и перевода текста на различные языки. Бот поддерживает следующие функции:

- Отправка голосового сообщения для расшифровки.
- Расшифровка голосового сообщения с использованием модели whisper.
- Перевод расшифрованного текста на различные языки с помощью Google Translator.
- Синтезирование голоса на основе переведенного текста и отправка аудиофайла пользователю.

## Инструкция по использованию

1. Отправьте голосовое сообщение боту.
2. Бот расшифрует сообщение и предложит вам выбрать язык для перевода.
3. Выберите желаемый язык перевода.
4. Получите переведенный текст и опцию синтеза голоса.

## Автор

Выполнил: Быстров Г.О. (ПИ22-1В)

## Требования к окружению

Для успешного запуска этой программы, убедитесь, что у вас установлены следующие зависимости:

- Python 3.11
- Библиотека OpenAI Whisper
    [Инструкция установки](https://github.com/openai/whisper/blob/main/README.md)
- Библиотека telebot
- Библиотека pyttsx3
- Библиотека deep_translator
- Доступ к API Telegram (токен Telegram Bot)

## Запуск программы

1. Зарегистрируйте бота в Telegram и получите токен.
2. Замените значение переменной `TOKEN` в коде программы на свой токен Telegram Bot.
3. Убедитесь, что у вас установлены все необходимые библиотеки и зависимости.
4. Запустите программу с помощью команды `python имя_файла.py`.

## Лицензия

Этот проект распространяется под лицензией [MIT License](LICENSE).

