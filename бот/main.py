from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_config
from handlers import (start_help, add_birthday, show_birthdays,
                      today_birthdays, edit_birthday, delete_birthday, admin)
from services.storage_json import save_birthdays
from database.birthday_db import birthdays


# Загружаем конфигурацию (.env)
config = load_config()

# Инициализируем объекты Bot и Dispatcher
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=MemoryStorage())

# Подключаем роутеры с хендлерами
dp.include_router(start_help.router)
dp.include_router(add_birthday.router)
dp.include_router(show_birthdays.router)
dp.include_router(today_birthdays.router)
dp.include_router(edit_birthday.router)
dp.include_router(delete_birthday.router)
dp.include_router(admin.router)

# Запуск поллинга бота
if __name__ == "__main__":
   try:
       dp.run_polling(bot)
   finally:                 # блок выполнится и при Ctrl-C, и при ошибке
       save_birthdays(birthdays)

