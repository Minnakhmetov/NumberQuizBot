import telebot
import random
import oddcast_downloader
import number_generator
import settings_keyboard
import requests
import config

bot = telebot.TeleBot(config.token)
telebot.apihelper.proxy = {'https': 'socks5://127.0.0.1:9050'}

chat_data = {}


def start_new_round(chat_id):
    chat_data[chat_id]['state'] = 'in_game'
    number = number_generator.get_number(
        chat_data[chat_id]['length'],
        chat_data[chat_id]['is_integer']
    )
    chat_data[chat_id]['number'] = number
    try:
        file_path = oddcast_downloader.get_audio(str(number))
        audio = open(file_path, 'rb')
        bot.send_audio(chat_id, audio)
    except requests.RequestException:
        bot.send_message(chat_id, 'Хмммммм, что-то пошло не так. Попробуйте еще раз.')


@bot.message_handler(commands=['start'])
def greet_new_user(msg):
    bot.send_message(msg.chat.id, 'Привеееет!\n'
                                  'Вы готовы напрячь свои мозги?!\n'
                                  'Напишите /round для начала тренировки!')
    if msg.chat.id not in chat_data:
        chat_data[msg.chat.id] = {'length': 4, 'is_integer': True, 'state': 'in_game'}


@bot.message_handler(func=lambda msg: msg.chat.id not in chat_data)
def send_user_not_found_message(msg):
    bot.send_message(msg.chat.id, 'Напишите /start, чтобы запустить бота!')


@bot.message_handler(commands=['round'])
def handle_start_command(msg):
    start_new_round(msg.chat.id)


@bot.message_handler(func=lambda msg: chat_data[msg.chat.id]['state'] == 'entering_len')
def change_length(msg):
    chat_data[msg.chat.id]['number'] = None
    try:
        new_len = int(msg.text)
        if new_len < 1 or new_len > 10:
            raise ValueError
        chat_data[msg.chat.id]['length'] = new_len
        chat_data[msg.chat.id]['state'] = 'in_game'
        bot.send_message(msg.chat.id, 'Замечательно! Настройки изменены.')
    except ValueError:
        bot.send_message(msg.chat.id, 'Что-то не то вы вводите! Мне нужно число от 1 до 10.')


@bot.message_handler(commands=['settings'])
def handle_start_command(msg):
    kb = settings_keyboard.get_keyboard(
        chat_data[msg.chat.id]['length'],
        chat_data[msg.chat.id]['is_integer']
    )
    bot.send_message(msg.chat.id, "Настройте все по вашему вкусу!",
                     reply_markup=kb)


@bot.callback_query_handler(lambda cbq: cbq.data == settings_keyboard.CHANGE_LEN_CALLBACK)
def switch_to_change_len_state(cbq):
    chat_data[cbq.message.chat.id]['state'] = 'entering_len'
    bot.send_message(cbq.message.chat.id, 'Отлично! Теперь введите число от 1 до 10.')


@bot.callback_query_handler(lambda cbq: cbq.data == settings_keyboard.CHANGE_NUMBER_TYPE_CALLBACK)
def change_number_type(cbq):
    chat_data[cbq.message.chat.id]['is_integer'] = not chat_data[cbq.message.chat.id]['is_integer']
    kb = settings_keyboard.get_keyboard(
        chat_data[cbq.message.chat.id]['length'],
        chat_data[cbq.message.chat.id]['is_integer']
    )
    bot.edit_message_reply_markup(cbq.message.chat.id,
                                  cbq.message.message_id,
                                  reply_markup=kb)


@bot.message_handler(content_types=['text'])
def handle_answer(msg):
    if chat_data[msg.chat.id].get('number') is not None:
        if chat_data[msg.chat.id]['number'] == msg.text:
            bot.send_message(msg.chat.id, 'Вы совершенно правы!')
            chat_data[msg.chat.id]['number'] = None
            start_new_round(msg.chat.id)
        else:
            bot.send_message(msg.chat.id, 'Неверно! Попробуйте еще раз.')
    else:
        bot.send_message(msg.chat.id, 'Чтобы начать игру напишите /round!')


if __name__ == "__main__":
    bot.polling()

