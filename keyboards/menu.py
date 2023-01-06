from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_main_menu():
    buttons = [
        [types.InlineKeyboardButton(text="Отправить резюме", callback_data="send_resume")],

        [
            types.InlineKeyboardButton(text="Вакансии", callback_data="трудоустроиться"),
            types.InlineKeyboardButton(text="Отзывы", callback_data="num_incr")
        ],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
