# echo.py
from aiogram import types, Dispatcher

async def echo_handler(message: types.Message):
    await message.answer("Я не понимаю твое сообщение")
    await message.delete()


def register_echo_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_handler)