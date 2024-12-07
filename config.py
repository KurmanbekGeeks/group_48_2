# config.py
from aiogram import Bot, Dispatcher
from decouple import config

Admins = [995712956, ]

token = config("TOKEN")

bot = Bot(token=token)
dp = Dispatcher(bot)