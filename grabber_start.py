from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message, BotCommand
from grabber_keyboards import keyboard_start
import grabber
from grabber_db import *

router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer('Что нужно сделать?', reply_markup=keyboard_start)

@router.message(Command('freq'))
async def start_handler(msg: Message, command: BotCommand):
    try:
        await change_freq(' '.join(command.args.split()[:-1]), command.args.split()[-1])
        await msg.answer(text='Частота постинга изменена!')
    except:
        await msg.answer('Что-то пошло не так, попробуй отправить команду еще раз')

@router.message(Command('get_freq'))
async def start_handler(msg: Message, command: BotCommand):
    await msg.answer(await get_freq())