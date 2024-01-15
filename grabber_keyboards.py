from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

kb=[[InlineKeyboardButton(text='Опубликовать', callback_data='post'), InlineKeyboardButton(text='Не опубликовывать', callback_data='pass')]]
keyboard_commit=InlineKeyboardMarkup(inline_keyboard=kb)

kb=[[KeyboardButton(text='Добавить связку'), KeyboardButton(text='Мои связки')]]
keyboard_start=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb=[[KeyboardButton(text='Назад')]]
keyboard_back=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)