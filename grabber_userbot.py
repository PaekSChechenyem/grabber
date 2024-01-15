from pyrogram import Client, filters
from pyrogram.raw import functions
import re
import grabber
from grabber_db import pyro_on_start, update_private_source
from grabber_time import *
import aiosqlite
from pyrogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation
)

async def fill_last_msg_id():
    async for message in grabber.userbot.get_chat_history('@grabbet_test283bot', limit=1, offset_id=-1):
        await pyro_on_start(message.id)

@grabber.userbot.on_raw_update()
async def test(app, update, a, b):
    false, true = (0, 0)
    if eval(str(update))['_'] == "types.UpdateChannel":
        await update_private_source(eval(str(b[update.channel_id]))['title'], update.channel_id)
    if eval(str(update))['_'] == "types.UpdateNewChannelMessage":
        chat_id = int(('-100'+str(update.message.peer_id.channel_id)))
        try:
            await grabber.bot.get_chat_member(chat_id=chat_id, user_id=grabber.userbot_id)
        except:
            b = await app.forward_messages(
                '@grabbet_test283bot',
                int('-100'+str(eval(str(update))['message']['peer_id']["channel_id"])),
                eval(str(update))['message']['id']
            )
            print(b.id)

async def schedule_msg(text):
    msg_ids = text.split()[-1].split(':')
    msg_ids = list(map(int, msg_ids))
    msgs = await grabber.userbot.get_messages(6420020475, msg_ids)
    group_elements = []
    for element in msgs:
        caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}
        if element.photo:
            input_media = InputMediaPhoto(media=element.photo.file_id, **caption_kwargs)
        elif element.video:
            input_media = InputMediaVideo(media=element.video.file_id, **caption_kwargs)
        elif element.document:
            input_media = InputMediaDocument(media=element.document.file_id, **caption_kwargs)
        elif element.audio:
            input_media = InputMediaAudio(media=element.audio.file_id, **caption_kwargs)
        elif element.animation:
            input_media = InputMediaAnimation(media=element.animation.file_id, **caption_kwargs)
        else:
            pass     
        try:     
            group_elements.append(input_media)
        except:
            pass

    for target_time in text.split()[:-1]:
        chat_id = int(target_time.split('!')[0])
        schedule_date = get_datetime(target_time.split('!')[1].replace('_', ' '))
        if group_elements!=[]:
            await grabber.userbot.send_media_group(chat_id=chat_id, media=group_elements, schedule_date=schedule_date)
        else:
            await grabber.userbot.send_message(chat_id=chat_id, text=msgs[0].text, schedule_date=schedule_date)



