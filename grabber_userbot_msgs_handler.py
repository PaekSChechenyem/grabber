from aiogram import Router, F, filters
from grabber_db import *
from grabber_keyboards import *
import grabber
import random
from typing import Any, Awaitable, Callable, Dict, List, Union
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    Message
)

DEFAULT_DELAY = 5

class AlbumMiddleware(BaseMiddleware):
    ALBUM_DATA: Dict[str, List[Message]] = {}

    def __init__(self, delay: Union[int, float] = DEFAULT_DELAY):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        '''if not event.media_group_id:
            return await handler(event, data)'''
        #ran_id = random.randint(0,99999)
        await update_counter()
        print(await get_private_id())
        try:
            self.ALBUM_DATA['media_group_id'].append(event)
            self.ALBUM_DATA['msg_ids'].append(await get_private_id())
            #print(await get_private_id())
            return
        except KeyError:
            self.ALBUM_DATA['media_group_id'] = [event]
            self.ALBUM_DATA['msg_ids']=[await get_private_id()]
            #print(await get_private_id())
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop('media_group_id')
            data["msg_ids"] = self.ALBUM_DATA.pop('msg_ids')
            data['forward_from'] = event.forward_from_chat.id
            data['group_id'] = random.randint(0,999999999)

        return await handler(event, data)


album_router = Router()
album_router.message.middleware(AlbumMiddleware())

router = Router()
router.include_router(album_router)
router.message.filter(F.from_user.id==grabber.userbot_id)

@album_router.message()
async def userbot_post_handler(msg: Message, album: List[Message], forward_from: Any, group_id: Any, msg_ids: Any,):
    group_elements = []
    for element in album:
        caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}
        if element.photo:
            input_media = InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs)
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

    #forward_from - в переменной id (int) группы, из которой этот пост

    if group_elements!=[]:
        await grabber.bot.send_media_group(chat_id=grabber.admin_id, media=group_elements)
        for i in msg_ids:
            commit_msg_id = i
            await save_post(forward_from, commit_msg_id, group_id) 
        await grabber.bot.send_message(chat_id=grabber.admin_id, text = f'{group_id}\n' + await get_bunch(forward_from), reply_markup=keyboard_commit)
    else:
        await grabber.bot.send_message(chat_id=grabber.admin_id, text=album[0].text)
        await save_post(forward_from, msg_ids[0], group_id)
        await grabber.bot.send_message(chat_id=grabber.admin_id, text = f'{group_id}\n' + await get_bunch(forward_from), reply_markup=keyboard_commit)