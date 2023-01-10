from aiogram import types


def get_keyboard_admin_choose_resume():
    buttons = [


        [
            types.InlineKeyboardButton(text="Одобрить", callback_data="accept_resume"),
            types.InlineKeyboardButton(text="Отказать", callback_data="not_accept_resume")
        ],

        [types.InlineKeyboardButton(text="Открыть чат", callback_data="answer_chat")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
