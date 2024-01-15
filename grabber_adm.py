from aiogram import Router
from aiogram.types import ChatMember
from grabber_db import save_adm, del_adm, check_adm
from aiogram.filters import BaseFilter
import grabber
import asyncio

router = Router()

class AdminRemoved(BaseFilter):
    async def __call__(self, event: ChatMember) -> bool:
        return str(event.new_chat_member.status) == 'ChatMemberStatus.LEFT'

class AdminAdded(BaseFilter):
    async def __call__(self, event: ChatMember) -> bool:
        return str(event.new_chat_member.status) == 'ChatMemberStatus.ADMINISTRATOR'

@router.my_chat_member(AdminAdded())
async def chat_update(event: ChatMember):
    await asyncio.sleep(1)
    link = await grabber.bot.export_chat_invite_link(chat_id=event.chat.id)
    await save_adm(event.chat.id, event.chat.title, link)


@router.my_chat_member(AdminRemoved())
async def chat_update(event: ChatMember):
    try:
        await del_adm(event.chat.id, event.chat.title)
    except:
        pass