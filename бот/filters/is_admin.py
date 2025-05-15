from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    """Фильтр для проверки, является ли пользователь администратором."""
    def __init__(self, admin_id: int) -> None:
        self.admin_id = admin_id

    async def __call__(self, message: Message) -> bool:
        # Вернет True, если ID пользователя совпадает с заданным admin_id
        return message.from_user.id == self.admin_id
