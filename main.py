"""
Этот бот предназначен для обработки голосовых сообщений, их расшифровки и перевода текста
на различные языки. Бот поддерживает следующие функции:

- Отправка голосового сообщения для расшифровки.
- Расшифровка голосового сообщения с использованием модели whisper.
- Перевод расшифрованного текста на различные языки с помощью Google Translator.
- Синтезирование голоса на основе переведенного текста и отправка аудиофайла пользователю.

Инструкция по использованию:
1. Отправьте голосовое сообщение боту.
2. Бот расшифрует сообщение и предложит вам выбрать язык для перевода.
3. Выберите желаемый язык перевода.
4. Получите переведенный текст и опцию синтеза голоса.
"""
import os
import telebot
from telebot import types
import whisper
import pyttsx3
from deep_translator import GoogleTranslator

TOKEN = "<YOUR_TOKEN>"

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Сохранение обработанной информации пользователя
user_status = {}

# Инициализация синтесайзера
synthesizer = pyttsx3.init()


@bot.message_handler(commands=["start"])
def start_message(message):
    """
    Обработчик команды /start

    Эта функция отправляет пользователю сообщение, которое 
    просит отправить голосовое сообщение.
    """
    bot.send_message(message.chat.id, 'Отправьте голосовое сообщение')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    """
    Обработчик голосовых сообщений.

    Эта функция скачивает и сохраняет голосовое сообщение, добавляет 
    клавиатуру для запроса расшифровки сообщения и устанавливает статус 
    ожидания расшифровки для пользователя.
    """
    # Сохранение голосового сообщения файлом
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'voice_messages/{message.chat.id}_rawVoice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    # Создание кнопки для обработки голосового сообщения
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_transcript = types.KeyboardButton("Получить расшифровку сообщения")
    markup.add(button_transcript)

    bot.reply_to(message, 'Для получения расшифровки нажмите кнопку\nили отправьте другое голосовое сообщение', reply_markup=markup)

    # Ограничитель функций, чтобы работала только функция получения расшифровки
    user_status[message.chat.id] = 'waiting_transcript'


@bot.message_handler(func=lambda message: user_status.get(message.chat.id) == 'waiting_transcript')
def handle_transcript_request(message):
    """
    Обработчик запроса на расшифровку голосового сообщения и последующий перевод текста.

    Эта функция обрабатывает запрос на расшифровку голосового сообщения, 
    сохраняет расшифрованный текст, и предоставляет пользователю опцию 
    выбора языка для перевода.
    """
    markup = types.ReplyKeyboardRemove()
    bot.reply_to(message, 'Сообщение обрабатывается...', reply_markup=markup)

    model = whisper.load_model("small")
    result = model.transcribe(f"voice_messages/{message.chat.id}_rawVoice.ogg")
    transcript = result['text']

    bot.send_message(message.chat.id, f'Расшифровка сообщения: {transcript}')

    markup_translate = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_english = types.KeyboardButton("Перевести на английский")
    button_spanish = types.KeyboardButton("Перевести на испанский")
    button_italian = types.KeyboardButton("Перевести на итальянский")
    button_russian = types.KeyboardButton("Перевести на русский")
    markup_translate.add(button_english, button_spanish, button_italian, button_russian)

    bot.send_message(message.chat.id, "Выберите язык для перевода:", reply_markup=markup_translate)

    user_status[message.chat.id] = {'transcript': transcript, 'language': None, 'translated_text': None}


@bot.message_handler(func=lambda message: isinstance(user_status.get(message.chat.id), dict) and message.text == "Перевести на английский")
def handle_translation_choice_english(message):
    """
    Обработчик выбора пользователем перевода на английский язык.

    Эта функция выполняет перевод текста на английский язык и сохраняет 
    результат, предоставляя дополнительные опции для пользователя.
    """
    user_data = user_status[message.chat.id]
    transcript = user_data['transcript']
    translated_text = ""

    translated_text = GoogleTranslator(source='auto', target='en').translate(transcript)
    user_data['language'] = 'en'
    user_data['translated_text'] = translated_text

    markup = types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, f"Перевод:\n{user_data['translated_text']}", reply_markup=markup)

    markup_actions = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton("Выбрать другой перевод")
    button_synthesize = types.KeyboardButton("Синтезировать голос")
    markup_actions.add(button_back, button_synthesize)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup_actions)


@bot.message_handler(func=lambda message: isinstance(user_status.get(message.chat.id), dict) and message.text == "Перевести на испанский")
def handle_translation_choice_spanish(message):
    """
    Обработчик выбора пользователем перевода на испанский язык.

    Эта функция выполняет перевод текста на испанский язык и сохраняет 
    результат, предоставляя дополнительные опции для пользователя.
    """
    user_data = user_status[message.chat.id]
    transcript = user_data['transcript']
    translated_text = ""

    translated_text = GoogleTranslator(source='auto', target='es').translate(transcript)
    user_data['language'] = 'es'
    user_data['translated_text'] = translated_text

    markup = types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, f"Перевод:\n{user_data['translated_text']}", reply_markup=markup)

    markup_actions = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton("Выбрать другой перевод")
    button_synthesize = types.KeyboardButton("Синтезировать голос")
    markup_actions.add(button_back, button_synthesize)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup_actions)


@bot.message_handler(func=lambda message: isinstance(user_status.get(message.chat.id), dict) and message.text == "Перевести на итальянский")
def handle_translation_choice_italian(message):
    """
    Обработчик выбора пользователем перевода на итальянский язык.

    Эта функция выполняет перевод текста на итальянский язык и сохраняет 
    результат, предоставляя дополнительные опции для пользователя.
    """
    user_data = user_status[message.chat.id]
    transcript = user_data['transcript']
    translated_text = ""

    translated_text = GoogleTranslator(source='auto', target='it').translate(transcript)
    user_data['language'] = 'it'
    user_data['translated_text'] = translated_text

    markup = types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, f"Перевод:\n{user_data['translated_text']}", reply_markup=markup)

    markup_actions = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton("Выбрать другой перевод")
    button_synthesize = types.KeyboardButton("Синтезировать голос")
    markup_actions.add(button_back, button_synthesize)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup_actions)


@bot.message_handler(func=lambda message: isinstance(user_status.get(message.chat.id), dict) and message.text == "Перевести на русский")
def handle_translation_choice_russian(message):
    """
    Обработчик выбора пользователем перевода на русский язык.

    Эта функция выполняет перевод текста на русский язык и сохраняет 
    результат, предоставляя дополнительные опции для пользователя.
    """
    user_data = user_status[message.chat.id]
    transcript = user_data['transcript']
    translated_text = ""

    translated_text = GoogleTranslator(source='auto', target='ru').translate(transcript)
    user_data['language'] = 'ru'
    user_data['translated_text'] = translated_text

    markup = types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, f"Перевод:\n{user_data['translated_text']}", reply_markup=markup)

    markup_actions = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton("Выбрать другой перевод")
    button_synthesize = types.KeyboardButton("Синтезировать голос")
    markup_actions.add(button_back, button_synthesize)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup_actions)


@bot.message_handler(func=lambda message: isinstance(user_status.get(message.chat.id), dict) and message.text == "Синтезировать голос")
def handle_synthesize_button(message):
    """
    Обработчик запроса пользователя на синтезирование голоса на основе переведенного текста.

    Эта функция синтезирует голос на основе текста, предоставленного пользователем,
    сохраняет его как аудиофайл и отправляет пользователю.
    """
    markup_actions = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Синтезирование выполняется...", reply_markup=markup_actions)

    user_data = user_status[message.chat.id]
    translated_text = user_data['translated_text']
    
    synthesizer.save_to_file(translated_text, f'synthesized_messages/{message.chat.id}_synthesized.ogg')
    synthesizer.runAndWait()

    with open(f'synthesized_messages/{message.chat.id}_synthesized.ogg', 'rb') as audio:
        bot.send_audio(message.chat.id, audio, caption=user_data['translated_text'])

    os.remove(f'synthesized_messages/{message.chat.id}_synthesized.ogg')

    user_status[message.chat.id] = None

    bot.send_message(message.chat.id, "Для продолжения отправьте новое голосовое или перешлите предыдущее")


@bot.message_handler(func=lambda message: isinstance(user_status.get(message.chat.id), dict) and message.text == "Выбрать другой перевод")
def handle_back_button(message):
    """
    Обработчик запроса пользователя на выбор другого языка для перевода.

    Эта функция предоставляет пользователю опцию выбора другого языка для перевода текста.
    """
    markup_translate = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_english = types.KeyboardButton("Перевести на английский")
    button_spanish = types.KeyboardButton("Перевести на испанский")
    button_italian = types.KeyboardButton("Перевести на итальянский")
    button_russian = types.KeyboardButton("Перевести на русский")
    markup_translate.add(button_english, button_spanish, button_italian, button_russian)

    bot.send_message(message.chat.id, "Выберите язык для перевода:", reply_markup=markup_translate)

    user_data = user_status[message.chat.id]
    user_data['language'] = None


bot.polling()
