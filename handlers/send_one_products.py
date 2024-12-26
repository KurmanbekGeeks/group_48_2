# send_one_products.py

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import buttons
from db import main_db


def fetch_all_products():
    conn = main_db.get_db_connection()
    products = conn.execute("""
    SELECT * FROM store s 
    INNER JOIN store_details sd ON s.product_id = sd.product_id
    """).fetchall()
    conn.close()
    return [dict(row) for row in products]


def fetch_products_by_id(product_id):
    conn = main_db.get_db_connection()
    product = conn.execute("""
    SELECT s.id, s.name_product, s.size, s.price, s.product_id, s.photo, 
    sd.category, sd.info_product FROM store s 
    INNER JOIN store_details sd ON s.product_id = sd.product_id 
    WHERE s.product_id = ?
    """, (product_id, )).fetchone()
    conn.close()
    return product


async def start_sending_products(message: types.Message):
    products = fetch_all_products()

    if products:
        await send_product(message, products[0]['product_id'])

    else:
        await message.answer('Товары не найдены!')


async def send_product(message: types.Message, product_id):
    product = fetch_products_by_id(product_id)

    if product:
        caption = (f'Название товара - {product["name_product"]}\n'
                   f'Информация о товаре - {product["info_product"]}\n'
                   f'Категория - {product["category"]}\n'
                   f'Размер - {product["size"]}\n'
                   f'Цена - {product["price"]}\n'
                   f'Артикул - {product["product_id"]}\n')


        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        next_buttons = InlineKeyboardButton("Далее",
                                            callback_data=f'next_{product_id}')
        keyboard.add(next_buttons)

        await message.answer_photo(photo=product['photo'], caption=caption,
                                   reply_markup=keyboard)
    else:
        await message.answer('Товаров нет!')


async def next_product(call: types.CallbackQuery):
    current_prodducts_id = int(call.data.split('_')[1])

    products = fetch_all_products()

    current_index = None

    for index, product in enumerate(products):
        if int(product['product_id']) == current_prodducts_id:
            current_index = index
            break

    if current_index is not None and current_index + 1 < len(products):
        next_product_id = products[current_index + 1]['product_id']
        await send_product(call.message, next_product_id)

    else:
        await call.message.answer('Больше товаров нет!')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_sending_products, commands=['products_one'])
    dp.register_callback_query_handler(next_product, Text(startswith='next_'))