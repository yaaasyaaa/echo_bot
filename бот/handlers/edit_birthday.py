from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from keyboards.friends_kb import create_friends_keyboard

router: Router = Router()

# Временное хранилище выбора для редактирования: {user_id: friend_name}
pending_edit: dict[int, str] = {}

@router.message(Command("edit_birthday"))
async def process_edit_command(message: Message) -> None:
    """Начало редактирования: предлагает выбрать друга из списка."""
    user_id = message.from_user.id
    # Если нет ни одной записи, сообщаем и завершаем
    if user_id not in birthdays or not birthdays[user_id]:
        await message.answer(LEXICON['no_birthdays'])
        return
    # Генерируем инлайн-клавиатуру со списком имен друзей
    names = list(birthdays[user_id].keys())
    await message.answer(LEXICON['prompt_edit'], reply_markup=create_friends_keyboard(names, 'edit'))

@router.callback_query(lambda call: call.data and call.data.startswith('edit:'))
async def process_edit_callback(callback: CallbackQuery) -> None:
    """Обработчик нажатия на инлайн-кнопку с именем друга (для редактирования)."""
    user_id = callback.from_user.id
    # Извлекаем имя друга из callback_data после префикса "edit:"
    friend_name = callback.data.split(':', 1)[1]
    # Проверяем, что друг существует (на случай, если запись уже удалена или изменена)
    if friend_name not in birthdays.get(user_id, {}):
        await callback.answer()  # просто закрываем всплывающее уведомление
        return
    # Сохраняем выбор пользователя во временное хранилище
    pending_edit[user_id] = friend_name
    # Просим пользователя ввести новую дату для этого друга
    await callback.message.answer(LEXICON['edit_date'].format(name=friend_name))
    await callback.answer()  # подтверждаем нажатие (убирает "часики" на кнопке)

@router.message(lambda message: message.from_user.id in pending_edit)
async def process_new_date(message: Message) -> None:
    """Обрабатывает введенную новую дату для редактируемого друга."""
    user_id = message.from_user.id
    new_date = message.text.strip()
    # Проверяем формат введенной даты
    try:
        datetime.strptime(new_date, "%d.%m")
    except ValueError:
        await message.answer(LEXICON['invalid_date'])
        return
    # Получаем имя друга, которого редактируем, и убираем из ожидания
    friend_name = pending_edit.pop(user_id)
    # Обновляем дату дня рождения в словаре
    birthdays[user_id][friend_name] = new_date
    await message.answer(LEXICON['birthday_updated'].format(name=friend_name, date=new_date))
