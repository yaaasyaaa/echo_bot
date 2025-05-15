import json
from pathlib import Path
from typing import Dict

DATA_FILE = Path("birthdays.json")


def load_birthdays() -> Dict[int, Dict[str, str]]:
    """Загрузить базу из JSON и привести id-ключи к int."""
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        raw: dict[str, Dict[str, str]] = json.load(f)
    # преобразуем ключи обратно в int
    return {int(user_id): data for user_id, data in raw.items()}


def save_birthdays(data: Dict[int, Dict[str, str]]) -> None:
    """Сохранить словарь в JSON (ключи-id превращаем в строки)."""
    # json требует строковые ключи
    serializable = {str(user_id): bdays for user_id, bdays in data.items()}
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

