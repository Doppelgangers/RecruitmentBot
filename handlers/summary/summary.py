import asyncio
import datetime

from aiogram import Router, types, Bot
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F

import config
from keyboards.admin_kb import get_keyboard_admin_choose_resume
from keyboards.any import make_row_keyboard
import keyboards.menu
from handlers.summary.vacancy import get_vacancy
router = Router()

bool_keyboard = ["Да", "Нет"]
education_keyboard = ["Высшее", "Неполное высшее", "Среднее профессиональное"]


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
    agreement = State()


@router.callback_query(text="вакансии")
async def give_vacancy(callback: types.CallbackQuery):
    await callback.answer(show_alert=True)
    vacancy_list = [{'title': 'Рабочие специальности', 'vacancy_list': ['Бетонщик', 'Гибщик труб', 'Кровельщик', 'Машинист козлового / мостового крана (5,6 разряд)', 'Оператор станков с ЧПУ (5 разряд)', 'Плотник', 'Слесарь по сборке металлоконструкций (3 4, 5, 6 разряд)', 'Токарь-карусельщик\xa0(5,6 разряд)', 'Токарь-расточник\xa0(5,6 разряд)', 'Токарь-универсал\xa0(5,6 разряд)', 'Фрезеровщик (5,6 разряд)', 'Штукатур-маляр']}, {'title': 'Инженерно-технические специальности', 'vacancy_list': ['Ведущий специалист (ценообразование)', 'Диспетчер производства', 'Инженер-технолог', 'Инженер по подготовке производства', 'Инспектор технического контроля', 'Мастер (мехобработка)', 'Мастер по сварке', 'Специалист по переводу', 'Техник по инсрументу']}]
    for group in vacancy_list:
        buttons = [ [types.InlineKeyboardButton(text=name, callback_data=f"qwe")] for name in group['vacancy_list']]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        print(buttons)
        await callback.message.answer(text=f"{group['title']}", reply_markup=keyboard)


@router.callback_query(text="отправить резюме")
async def start_fsm_summary(callback: types.CallbackQuery, state: FSMContext):
    """ Начало опроса, запрос желаемой должности. """
    await callback.answer(show_alert=True)

    await callback.message.answer("Отлично, на какую должность вы желаете устроиться?")

    await state.set_state(OrderSummary.working_position)


@router.message(OrderSummary.working_position)
async def choose_working_position(message: Message, state: FSMContext):
    """Запрос опыта работы"""

    await state.update_data(working_position=message.text.lower().strip())

    await message.answer(text="Отлично, какой у вас опыт работы по желаемой должности?")

    await state.set_state(OrderSummary.work_experience)


@router.message(OrderSummary.work_experience)
async def choose_work_experience(message: Message, state: FSMContext):
    """Ловим и проверяем опыт работы и запрашиваем ФИО"""
    if not message.text.isnumeric():
        await message.answer(text="Укажите ваш опыт работы в виде числа. Например 0 или 4")
        return

    if not 0 <= (age := int(message.text)) <= 50:
        await message.answer(text=
                             f"""Вы действительно проработали {age} лет? Извените но я не могу в это поверить. 

Введите ваш настоящий опыт работы.
""")
        return

    await state.update_data(work_experience=age)

    await message.answer(text=f"""Давайте знакомиться дальше, укажите ваше ФИО?""")

    await state.set_state(OrderSummary.full_name)


@router.message(OrderSummary.full_name)
async def set_full_name(message: Message, state: FSMContext):
    """Проверяем ФИО и запрашиваем дату рождения"""

    full_name = [value for value in message.text.strip().split(" ") if value != '']

    if full_name.__len__() != 3:
        await message.answer(text="ФИО указанно не правильно, укажите Фамилию Имя Отчество через пробел\nНапример Иван Иванович Иванов")
        return

    await message.answer(text=f"Отлично, {full_name[1]} {full_name[2]}, укажите вашу дату рождения.\n\nДату необходимо указать в следующем формате {datetime.date.today().strftime('%d.%m.%Y')}")
    await state.update_data(full_name=" ".join(full_name))
    await state.set_state(OrderSummary.birthday)


@router.message(OrderSummary.birthday)
async def set_birthday(message: Message, state: FSMContext):
    birthday = None
    try:
        birthday = datetime.datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
    except ValueError:
        await message.answer(f"Вы указали дату в неправильном формате, дата должна быть указана подобным образом:\n {datetime.date.today().strftime('%d.%m.%Y')} ")

    if birthday is None:
        print(birthday)
        return

    await message.answer(text="Укажите ваше текущее место жительства.")
    await state.update_data(birthday=birthday)
    await state.set_state(OrderSummary.place_of_residence)


@router.message(OrderSummary.place_of_residence)
async def set_place_of_residence(message: Message, state: FSMContext):
    await state.update_data(place_of_residence=message.text)

    await message.answer(text="Укажите ваше Гражденство.")
    await state.set_state(OrderSummary.citizenship)


@router.message(OrderSummary.citizenship)
async def set_citizenship(message: Message, state: FSMContext):
    await state.update_data(citizenship=message.text)

    await message.answer(text="Укажите ваш номер телефона.")
    await state.set_state(OrderSummary.phone)


@router.message(OrderSummary.phone)
async def set_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await message.answer(text="Укажите ваш адрес электронной почты.")
    await state.set_state(OrderSummary.email)


@router.message(OrderSummary.email, )
async def set_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    await message.answer(text="Укажите ваш уровень образования.", reply_markup=make_row_keyboard(education_keyboard))
    await state.set_state(OrderSummary.education_lvl)


@router.message(OrderSummary.education_lvl, F.text.in_(education_keyboard))
async def choose_education(message: Message, state: FSMContext):
    await state.update_data(education_lvl=message.text)

    await message.answer(text="Где вы обучалиь? Укажите учебное заведение.", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(OrderSummary.educational_institution)


@router.message(OrderSummary.education_lvl)
async def choose_education(message: Message, state: FSMContext):
    await message.answer(text="Выберете элемент из списка.")


@router.message(OrderSummary.educational_institution)
async def set_educational_institution(message: Message, state: FSMContext):
    await state.update_data(educational_institution=message.text)

    await message.answer(text="Укажите спецальность по которой вы обучались.")
    await state.set_state(OrderSummary.specialization)


@router.message(OrderSummary.specialization)
async def set_specialization(message: Message, state: FSMContext):
    await state.update_data(specialization=message.text)

    await message.answer(text="Укажите год окончания обучения.")
    await state.set_state(OrderSummary.year_of_graduation)


@router.message(OrderSummary.year_of_graduation)
async def set_specialization(message: Message, state: FSMContext):
    await state.update_data(year_of_graduation=message.text)

    await message.answer(text="Если именются проф. аттестации то перечислите их.")
    await state.set_state(OrderSummary.attestations)


@router.message(OrderSummary.attestations)
async def set_specialization(message: Message, state: FSMContext):
    await state.update_data(attestations=message.text)

    await message.answer(text="Чо бы отправить ваше резюме мне нужно ваше согласее на обработку персональных данных.\n\nВы даёте согласие на обработку персональных данных?",
                         reply_markup=make_row_keyboard(bool_keyboard)

                         )
    await state.set_state(OrderSummary.agreement)


@router.message(OrderSummary.agreement, F.text.in_(bool_keyboard))
async def set_specialization(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(agreement=message.text)
    await state.update_data(chat_id=message.chat.id)

    data = await state.get_data()

    await message.answer(text="Вы успешно отправили резюме роботадателю.", reply_markup=types.ReplyKeyboardRemove())
    log_text = f""" Вам было отправленно новое резюме на рассмотрение
    
Желаемая вакансия: {data['working_position']}
ФИО: {data["full_name"]}
Возрамт: {calculate_age(data["birthday"])}

<b>Место жительства</b>
Прожимвает в : {data['place_of_residence']}
Имеет гражданство: {data['citizenship']}

<b>Контактные данные</b>
Номер тедефона: {data['phone']}
Почта: {data['email']}

<b>Образование</b>
Уровень образования: {data['education_lvl']}
Учился в: {data['educational_institution']}
По спецальности: {data['specialization']}
Окончил обучение: {data['year_of_graduation']}

<b>Дополнительные аттестации</b>
Атестации: {data['attestations']}
"""

    for admin_chat_id in config.ADMIN_CHATS:
        await bot.send_message(chat_id=admin_chat_id, text=log_text, parse_mode="HTML", reply_markup=get_keyboard_admin_choose_resume())
    await state.clear()


def calculate_age(born):
    today = datetime.date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, month=born.month + 1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year
    