from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_main_menu():
    buttons = [
        [types.InlineKeyboardButton(text="Отправить резюме", callback_data="отправить резюме")],

        [
            types.InlineKeyboardButton(text="Вакансии", callback_data="вакансии"),
            types.InlineKeyboardButton(text="Отзывы", callback_data="num_incr")
        ],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
