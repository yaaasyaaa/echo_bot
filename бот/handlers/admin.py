from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config_data.config import load_config
from filters.is_admin import IsAdmin
from database.birthday_db import birthdays

router: Router = Router()

# Получаем admin_id из конфигурации (файла .env)
ADMIN_ID: int = load_config().tg_bot.admin_id

@router.message(Command("admin"), IsAdmin(admin_id=ADMIN_ID))
async def process_admin_command(message: Message) -> None:
    """Обработчик админ-команды: выводит статистику по ботуу."""
    total_users = len(birthdays)
    total_records = sum(len(b) for b in birthdays.values())
    await message.answer(f"Всего пользователей: {total_users}\nВсего записей: {total_records}")
