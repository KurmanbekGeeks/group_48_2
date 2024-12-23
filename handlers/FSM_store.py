from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.dispatcher import FSMContext
from db import main_db

class store_fsm(StatesGroup):
    name_product = State()
    size = State()
    category = State()
    price = State()
    product_id = State()
    info_product = State()
    photo = State()
    submit = State()


async def start_fsm_store(message: types.Message):
    await message.answer('Введите название товара: ',
                         reply_markup=buttons.cancel_markup)
    await store_fsm.name_product.set()


async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text

    await store_fsm.next()
    await message.answer('Введите размер товара: ')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await store_fsm.next()
    await message.answer('Введите ктегорию товара: ')

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await store_fsm.next()
    await message.answer('Введите цена товара: ')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await store_fsm.next()
    await message.answer('Введите артикул товара: ')


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await store_fsm.next()
    await message.answer('Введите информацию о товаре: ')


async def load_info_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text

    await store_fsm.next()
    await message.answer('Отправьте фото товара: ')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await store_fsm.next()
    await message.answer(f'Верные ли данные?', reply_markup=buttons.submit)
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название - {data["name_product"]}\n'
                                       f'Размер - {data["size"]}\n'
                                       f'Категория - {data["category"]}\n'
                                       f'Артикул - {data["product_id"]}\n'
                                       f'Информация о товаре - {data["info_product"]}\n'
                                       f'Цена - {data["price"]}\n')


async def load_submit(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            await main_db.sql_insert_store(
                name_product=data['name_product'],
                size=data['size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )
            await main_db.sql_insert_store_detail(
                category=data['category'],
                info_product=data['info_product'],
                product_id=data['product_id']
            )
            await message.answer('Ваши данные в базе!')
            await state.finish()

    elif message.text == 'Нет':
        await message.answer('Хорошо, отменено!')
        await state.finish()

    else:
        await message.answer('Введите Да или Нет!')


def store_fsm_handlers(dp: Dispatcher):
    dp.register_message_handler(start_fsm_store, commands=['product'])
    dp.register_message_handler(load_name_product, state=store_fsm.name_product)
    dp.register_message_handler(load_size, state=store_fsm.size)
    dp.register_message_handler(load_category, state=store_fsm.category)
    dp.register_message_handler(load_price, state=store_fsm.price)
    dp.register_message_handler(load_product_id, state=store_fsm.product_id)
    dp.register_message_handler(load_info_product, state=store_fsm.info_product)
    dp.register_message_handler(load_photo, state=store_fsm.photo, content_types=['photo'])
    dp.register_message_handler(load_submit, state=store_fsm.submit)