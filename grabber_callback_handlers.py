from aiogram import F, Router
from aiogram.types import CallbackQuery
from grabber_db import *
import grabber
import re
import grabber_userbot

router = Router()

@router.callback_query(F.data == 'post')
async def cb_post(callback: CallbackQuery):
    ids = await get_ids(callback.message.text.split()[0])
    text = ''
    for i in ids:
        text += str(i[0])+':'
    text = text[:-1]
    source_id = await get_id((re.findall(r'(?<=\d\s).*?\s--->', callback.message.text)[0])[:-5])
    targets_info = await get_info(source_id)
    await grabber_userbot.schedule_msg(f'{targets_info} {text}')
    await del_post(callback.message.text.split()[0])
    await grabber.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()

@router.callback_query(F.data == 'pass')
async def cb_post(callback: CallbackQuery):
    await del_post(callback.message.text.split()[0])
    ids = await get_ids(callback.message.text.split()[0])
    for i in ids:
        await grabber.bot.delete_message(chat_id=callback.from_user.id, message_id=i[0])
    await grabber.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()
