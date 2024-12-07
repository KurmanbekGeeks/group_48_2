# quiz.py
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot

async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    button = InlineKeyboardButton("Далее", callback_data='quiz_2')

    keyboard.add(button)

    question = 'XBOX or Sony'
    answer = ['XBOX', 'Sony', 'Nintendo']


    await bot.send_poll(
        chat_id=message.from_user.id,   # куда отправить
        question=question,      # сам вопрос
        options=answer,          # Ответы
        is_anonymous=False,     # Анонимный или нет
        type='quiz',            # тип опросника
        correct_option_id=1,    # id правильного ответа
        explanation='Жаль...',  # тест при неправильном ответе
        open_period=60,         # Время работы опросника
        reply_markup=keyboard  # Добавление кнопки
    )



async def quiz_2(call: types.CallbackQuery):

    question = 'Python, JavaScript, Java, PHP and Swift'
    answer = ['Python', 'JavaScript', 'Java', 'PHP', 'Swift']

    await bot.send_poll(
        chat_id=call.from_user.id,   # куда отправить
        question=question,      # сам вопрос
        options=answer,          # Ответы
        is_anonymous=True,     # Анонимный или нет
        type='quiz',            # тип опросника
        correct_option_id=0,    # id правильного ответа
        explanation='Всё с тобой понятно -_- ',  # тест при неправильном ответе
        open_period=180
    )


def register_quiz_handlers(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands='quiz')
    dp.register_callback_query_handler(quiz_2, text='quiz_2')