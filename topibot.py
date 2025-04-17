import asyncio
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from config import BOT_TOKEN
load_dotenv()

dp = Dispatcher()
bot = Bot(BOT_TOKEN)

BAD_WORDS = {'сука', 'блять', 'мат'}


async def handle_caps(message: types.Message) -> None:
    if message.text and len(message.text.split()) > 1:
        text = ' '.join(message.text.split()[1:])
        await message.reply(text.upper())
    else:
        await message.reply("Используйте: /caps ваш текст")


async def handle_reverse(message: types.Message) -> None:
    if message.text and len(message.text.split()) > 1:
        text = ' '.join(message.text.split()[1:])
        await message.reply(text[::-1])
    else:
        await message.reply("Используйте: /reverse ваш текст")


# Обработчики сообщений
async def echo_text(message: types.Message) -> None:
    if has_numbers(message.text):
        await message.reply("Ваше сообщение содержит цифры!")
    elif contains_bad_words(message.text):
        await message.reply("Пожалуйста, не используйте нецензурную лексику")
    else:
        await message.reply(text=message.text)


async def echo_photo(message: types.Message) -> None:
    caption = "Принято фото!"
    if message.caption:
        caption += f"\nПодпись: {message.caption}"
    await message.reply_photo(photo=message.photo[0].file_id, caption=caption)


# Фильтры
def has_numbers(text: str) -> bool:
    return any(char.isdigit() for char in text)


def contains_bad_words(text: str) -> bool:
    return any(word.lower() in text.lower() for word in BAD_WORDS)


async def echo_video(message: types.Message) -> None:
    await message.reply_video(video=message.video.file_id)


async def echo_animation(message: types.Message) -> None:
    await message.reply_animation(animation=message.animation.file_id)


async def echo_audio(message: types.Message) -> None:
    await message.reply_audio(audio=message.audio.file_id)


async def echo_voice(message: types.Message) -> None:
    await message.reply_voice(voice=message.voice.file_id)


async def echo_sticker(message: types.Message) -> None:
    await message.reply_sticker(sticker=message.sticker.file_id)


async def echo_document(message: types.Message) -> None:
    await message.reply_document(document=message.document.file_id)


# Регистрация обработчиков
async def main() -> None:
    dp.message.register(handle_caps, Command("caps"))
    dp.message.register(handle_reverse, Command("reverse"))
    dp.message.register(echo_text, F.text)
    dp.message.register(echo_photo, F.photo)

    # Остальные обработчики медиа
    dp.message.register(echo_video, F.video)
    dp.message.register(echo_animation, F.animation)
    dp.message.register(echo_audio, F.audio)
    dp.message.register(echo_voice, F.voice)
    dp.message.register(echo_sticker, F.sticker)
    dp.message.register(echo_document, F.document)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())