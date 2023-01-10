from aiogram import Router
from aiogram.types import Message

import keyboards.menu

router = Router()


@router.message(commands=["start", "hello"])
async def welcome(message: Message):
    await message.answer(text="Выберете действие", reply_markup=keyboards.menu.get_keyboard_main_menu())


@router.message(commands=["info"])
async def info(message: Message):
    from aiogram import types
    await message.answer(text=f"{message.chat.id}", reply_markup=types.ReplyKeyboardRemove())