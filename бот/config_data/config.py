from dataclasses import dataclass
from environs import Env


# Описываем структуру с данными о Telegram-боте
@dataclass
class TgBot:
    token: str  # Токен доступа к боту
    admin_id: int  # ID администратора бота


@dataclass
class Config:
    tg_bot: TgBot  # Настройки бота (в будущем можно добавить другие секции конфигурации)


def load_config(path: str | None = None) -> Config:
    """Функция для загрузки конфигурации из .env файла."""
    env = Env()
    env.read_env(path)  # Читаем файл .env
    return Config(tg_bot=TgBot(
        token=env.str("BOT_TOKEN"),  # Получаем токен бота
        admin_id=env.int("ADMIN_ID")  # Получаем ID администратора (целое число)
    ))
