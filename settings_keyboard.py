import telebot
from enum import Enum

CHANGE_LEN_CALLBACK = "change_len"
CHANGE_NUMBER_TYPE_CALLBACK = "change_number_type"


def get_keyboard(num_len, is_integer):
    kb = telebot.types.InlineKeyboardMarkup()
    kb.row(
        telebot.types.InlineKeyboardButton(
            "Длина числа: {}".format(num_len),
            callback_data=CHANGE_LEN_CALLBACK
        ),
        telebot.types.InlineKeyboardButton(
            "Целое" if is_integer else "Дробное",
            callback_data=CHANGE_NUMBER_TYPE_CALLBACK
        )
    )

    return kb
