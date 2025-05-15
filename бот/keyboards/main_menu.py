from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon import LEXICON

# Формируем клавиатуру с кнопками (2 ряда: первый с одной кнопкой, второй с двумя)
main_menu_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=LEXICON['btn_add'])],
        [KeyboardButton(text=LEXICON['btn_show']), KeyboardButton(text=LEXICON['btn_today'])]
    ],
    resize_keyboard=True
)
