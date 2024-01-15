from aiogram import Router, F
from grabber_db import *
from grabber_keyboards import *
from grabber_filters import *

router = Router()
router.message.filter(ChatTypeFilter(chat_type='private'))

@router.message(F.text=='Добавить связку')
async def set_bunch(msg: Message):
    await set_state(1)
    await msg.answer('Введи юзернейм/линк на вступление канала-источника', reply_markup=keyboard_back)

@router.message(F.text=='Мои связки')
async def my_bunches(msg: Message):
    text = await get_bunches()
    await msg.answer(str(text), reply_markup=keyboard_back)