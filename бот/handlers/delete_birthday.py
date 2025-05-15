from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from keyboards.friends_kb import create_friends_keyboard

router: Router = Router()

@router.message(Command("delete_birthday"))
async def process_delete_command(message: Message) -> None:
    """Начало удаления: предлагает выбрать друга для удаления."""
    user_id = message.from_user.id
    if user_id not in birthdays or not birthdays[user_id]:
        await message.answer(LEXICON['no_birthdays'])
        return
    names = list(birthdays[user_id].keys())
    await message.answer(LEXICON['prompt_delete'], reply_markup=create_friends_keyboard(names, 'delete'))

@router.callback_query(lambda call: call.data and call.data.startswith('delete:'))
async def process_delete_callback(callback: CallbackQuery) -> None:
    """Обработчик нажатия на кнопку удаления конкретного друга."""
    user_id = callback.from_user.id
    friend_name = callback.data.split(':', 1)[1]
    if friend_name in birthdays.get(user_id, {}):
        # Удаляем запись о дне рождения
        birthdays[user_id].pop(friend_name)
        await callback.message.answer(LEXICON['birthday_deleted'].format(name=friend_name))
    else:
        # Имя уже отсутствует (например, если было удалено ранее)
        await callback.message.answer(LEXICON['no_birthdays'])
    await callback.answer()
