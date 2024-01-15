from aiogram import Router, F
from grabber_db import *
from grabber_keyboards import *
import grabber
from grabber_filters import *
from aiogram.exceptions import *

router = Router()
router.message.filter(ChatTypeFilter(chat_type='private')) 

@router.message(F.text=='Назад')
async def back(msg: Message):
    await del_half_filled()
    await set_state(0)
    await msg.answer('Что нужно сделать?', reply_markup=keyboard_start)

@router.message(StateFilter(1))
async def state1_handler(msg: Message):
    if msg.text.startswith('@'):
        try:
            await grabber.userbot.join_chat(msg.text)
            channel = await grabber.bot.get_chat(chat_id=msg.text)
            await save_source(channel.id, channel.title, channel.username)
            await set_state(2)
            await msg.answer('Введи название канала-цели', reply_markup=keyboard_back)
        except:
            await msg.answer('Канал не найден, попробуй ввести другой юзернейм', reply_markup=keyboard_back)
    else:
        try:
            private_chat = await grabber.userbot.get_chat(chat_id=msg.text)
        except:
            private_chat = ''
        if private_chat != '':
            try:
                p_id = private_chat.id
            except:
                p_id = 0
            try:
                await grabber.userbot.join_chat(msg.text)
                await save_source(p_id, private_chat.title, msg.text)
                await set_state(2)
                await msg.answer('Запрос на вступление подан. Введи название канала-цели', reply_markup=keyboard_back)
            except:
                await save_source(p_id, private_chat.title, msg.text)
                await set_state(2)
                await msg.answer('Запрос на вступление подан. Введи название канала-цели', reply_markup=keyboard_back)
        else:
            await msg.answer('Ссылка недействительна, попробуй ввести другую', reply_markup=keyboard_back)

@router.message(StateFilter(2))
async def state2_handler(msg: Message):
    if await check_adm(msg.text) != []:
        c_a = await check_adm(msg.text)
        member = await grabber.bot.get_chat_member(chat_id=c_a[0][0], user_id=grabber.userbot_id)
        if str(member.status) == 'ChatMemberStatus.LEFT':
            link = await get_link(c_a[0][0])#await grabber.bot.export_chat_invite_link(chat_id=c_a[0][0])#, creates_join_request=False)
            await grabber.userbot.join_chat(chat_id=link)#.invite_link)
            await grabber.bot.promote_chat_member(user_id=grabber.userbot_id, chat_id=c_a[0][0], can_post_messages=True)
        if str(member.status) == 'ChatMemberStatus.MEMBER':
            await grabber.bot.promote_chat_member(user_id=grabber.userbot_id, chat_id=c_a[0][0], can_post_messages=True)
        t_id = c_a[0][0]
        t_title = c_a[0][1]
        await set_state(0)
        source_title = await save_target(t_id, t_title)
        await msg.answer(f'Связка:\n\n{source_title[0][1]} ---> {msg.text}\n\nсохранена!', reply_markup=keyboard_start)
    else:
        await msg.answer('Среди администрируемых ботом каналов нет канала с таким названием, попробуй ввести другое название\nЕсли название верное\
 и бот администрирует это сообщество, попробуй переназначть его администратором и еще раз отправить название', reply_markup=keyboard_back)