from services.storage_json import load_birthdays
# database/birthday_db.py
# Глобальный словарь для хранения дней рождения.
# Формат: { user_id: { friend_name: "DD.MM", ... }, ... }
birthdays: dict[int, dict[str, str]] = load_birthdays()


