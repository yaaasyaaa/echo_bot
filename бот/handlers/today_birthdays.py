from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from services.birthday_service import register_user, get_today_birthdays

router: Router = Router()

@router.message(Command("today_birthdays"))
@router.message(F.text == LEXICON['btn_today'])
async def process_today_command(message: Message) -> None:
    """Обработчик команды /today_birthdays - показать именинников сегодня."""
    user_id = message.from_user.id
    register_user(birthdays, user_id)
    user_data = birthdays[user_id]
    if not user_data:
        # Нет ни одной записи
        await message.answer(LEXICON['no_birthdays'])
    else:
        today_names = get_today_birthdays(user_data)
        if not today_names:
            await message.answer(LEXICON['no_today'])
        else:
            # Формируем сообщение со списком именинников
            lines: list[str] = [LEXICON['today_list']]
            for name in today_names:
                lines.append(name)
            await message.answer("\n".join(lines))