from aiogram import Router, types
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

import keyboards.menu

router = Router()


class OrderSummary(StatesGroup):
    working_position = State()
    work_experience = State()
    full_name = State()
    birthday = State()
    place_of_residence = State()
    citizenship = State()
    phone = State()
    email = State()
    education_lvl = State()
    educational_institution = State()
    specialization = State()
    year_of_graduation = State()
    attestations = State()
    send = State()


@router.message(commands=["трудоустроиться"])
async def welcome(message: Message):
    await message.answer(text="Выберете действие", reply_markup=keyboards.menu.get_keyboard_main_menu())


@router.callback_query(text = "трудоустроиться")
async def start_fsm_summary(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("ВВедите желаемую должность")
    await callback.answer(show_alert=True)

    await state.set_state(OrderSummary.working_position)


@router.message(OrderSummary.working_position)
async def choose_working_position(message: Message, state: FSMContext):
    await state.update_data(working_position=message.text.lower().strip())

    await message.answer(text="Отлично, какой у вас опыт работы по желаемой должности?")

    await state.set_state(OrderSummary.work_experience)


@router.message(OrderSummary.work_experience)
async def choose_work_experience(message: Message, state: FSMContext):

    await message.answer("Хмм... Опыт не такой большой. Давайте знакомиться дальше.")
    datas = await state.get_data()
    await message.answer(f"""Напомню вы выбрали вакансию {datas["working_position"]}, и у вас опыт работы {message.text} лет.""")

    await state.clear()

