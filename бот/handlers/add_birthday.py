from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from services.birthday_service import register_user

router: Router = Router()

# Определяем группу состояний для добавления дня рождения
class AddBirthdayState(StatesGroup):
    name = State()  # ожидание ввода имени друга
    date = State()  # ожидание ввода даты рождения

@router.message(Command("add_birthday"))
@router.message(F.text == LEXICON['btn_add'])
async def process_add_command(message: Message, state: FSMContext) -> None:
    """Начало добавления: запрос имени друга."""
    register_user(birthdays, message.from_user.id)
    # Устанавливаем состояние на ввод имени
    await state.set_state(AddBirthdayState.name)
    await message.answer(LEXICON['add_name'])

@router.message(AddBirthdayState.name)
async def process_name_step(message: Message, state: FSMContext) -> None:
    """Первый шаг FSM: получено имя друга."""
    name = message.text.strip()
    if not name:
        # Если имя пустое, просим ввести снова (остаемся в том же состоянии)
        await message.answer(LEXICON['add_name'])
        return
    # Проверяем, нет ли уже такого имени у пользователя
    if name in birthdays[message.from_user.id]:
        await message.answer(LEXICON['name_exists'])
        return
    # Сохраняем имя во временном хранилище FSM
    await state.update_data(name=name)
    # Переходим к следующему шагу (ожидание даты)
    await state.set_state(AddBirthdayState.date)
    await message.answer(LEXICON['add_date'])

@router.message(AddBirthdayState.date)
async def process_date_step(message: Message, state: FSMContext) -> None:
    """Второй шаг FSM: получена дата рождения."""
    date_text = message.text.strip()
    # Проверяем формат даты ДД.ММ
    try:
        datetime.strptime(date_text, "%d.%m")  # пытаемся распознать дату
    except ValueError:
        # Неверный формат - сообщаем и остаемся в том же состоянии
        await message.answer(LEXICON['invalid_date'])
        return
    # Загружаем ранее сохраненное имя из FSM
    data = await state.get_data()
    friend_name = data.get("name")
    # Сохраняем новую запись в словарь (базу данных)
    birthdays[message.from_user.id][friend_name] = date_text
    # Очищаем состояние (выходим из FSM)
    await state.clear()
    # Отправляем подтверждение пользователю
    await message.answer(LEXICON['birthday_added'].format(name=friend_name, date=date_text))
