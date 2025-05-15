from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from keyboards.main_menu import main_menu_kb
from database.birthday_db import birthdays
from services.birthday_service import register_user

router: Router = Router()

@router.message(Command("start"))
async def process_start_command(message: Message) -> None:
    # Регистрируем пользователя в базе (если уже есть, функция ничего не сделает)
    register_user(birthdays, message.from_user.id)
    # Отправляем приветственное сообщение и отображаем клавиатуру меню
    await message.answer(LEXICON['start'], reply_markup=main_menu_kb)

@router.message(Command("help"))
async def process_help_command(message: Message) -> None:
    # Отправляем текст справки
    await message.answer(LEXICON['help'])
