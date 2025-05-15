from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from services.birthday_service import register_user

router: Router = Router()

@router.message(Command("show_birthdays"))
@router.message(F.text == LEXICON['btn_show'])
async def process_show_command(message: Message) -> None:
    """Обработчик команды /show_birthdays - показать все дни рождения."""
    user_id = message.from_user.id
    register_user(birthdays, user_id)
    user_data = birthdays[user_id]
    if not user_data:
        # Если список пуст
        await message.answer(LEXICON['no_birthdays'])
    else:
        # Формируем текст со списком друзей и дат
        lines: list[str] = [LEXICON['show_list']]
        for name, date in user_data.items():
            lines.append(LEXICON['birthday_entry'].format(name=name, date=date))
        # Отправляем одним сообщением, строки разделены переносом
        await message.answer("\n".join(lines))
