import asyncio
import aiosqlite
from aiogram.types import Message
from aiogram.filters import BaseFilter
from datetime import datetime, timedelta
from grabber_time import *
import grabber
from grabber_keyboards import keyboard_back

async def connect_2db():
    db = await aiosqlite.connect('grabber.db')
    await db.execute('CREATE TABLE IF NOT EXISTS adm (target_id int, target_title text, next_time text, frequency int, invite_link text)')
    await db.commit()
    await db.execute('CREATE TABLE IF NOT EXISTS bunches (source_id int, source_title text, source_username text, target_id int, target_title text)')
    await db.commit()
    await db.execute('CREATE TABLE IF NOT EXISTS state (state int)')
    await db.commit()
    await db.execute('CREATE TABLE IF NOT EXISTS private_counter (id int)')
    await db.commit()
    '''await db.execute('INSERT INTO adm VALUES (-1001934976692, "технический", "14.01.24 11:50", 60)')
    await db.commit()'''

    await db.execute('CREATE TABLE IF NOT EXISTS posts (source_id int, message_id int, group_id int)')
    await db.commit()
    if await db.execute_fetchall('SELECT state FROM state') == []:
        await db.execute('INSERT INTO state VALUES (0)')
        await db.commit()
    return db

loop = asyncio.get_event_loop() 
task = connect_2db()
db = (loop.run_until_complete(asyncio.gather(task)))[0]

class StateFilter(BaseFilter):  
    def __init__(self, mode: int):
        self.mode = mode
    async def __call__(self, msg: Message) -> bool: 
        return await get_state() == self.mode

async def get_state():
    cur = await db.execute(f'SELECT state FROM state')
    mode = await cur.fetchone()
    return mode[0]

async def set_state(state):
    await db.execute(f'UPDATE state SET state = {state}')
    await db.commit()
    
async def save_target(target_id, target_title):
    s = await db.execute_fetchall('SELECT source_id, source_title, source_username FROM bunches WHERE target_id = 0')
    await db.execute(f'UPDATE bunches SET target_id = {target_id} WHERE target_id = 0')
    await db.commit()
    await db.execute(f'UPDATE bunches SET target_title = "{target_title}" WHERE target_title = 0')
    await db.commit()
    return s

async def save_source(channel_id, channel_title, channel_username):
    l = await db.execute_fetchall(f'SELECT source_id FROM bunches WHERE source_title = "{channel_title}"')
    for i in l:
        if i[0]!='0':
            channel_id = i[0]
    await db.execute(f'INSERT INTO bunches VALUES ({channel_id}, "{channel_title}", "{channel_username}", 0, 0)')
    await db.commit()

async def del_half_filled():
    await db.execute(f'DELETE FROM bunches WHERE target_id = 0 AND target_title = 0')
    await db.commit()

async def save_adm(target_id, target_title, link):
    await db.execute(f'INSERT INTO adm VALUES ({target_id}, "{target_title}", "{get_now()}", 60, "{link}")')
    await db.commit()

async def get_link(target_id):
    link = await db.execute_fetchall(f'SELECT invite_link FROM adm WHERE target_id = {target_id}')
    return link[0][0]

async def del_adm(target_id, target_title):
    await db.execute(f'DELETE FROM adm WHERE target_id = {target_id} AND target_title = "{target_title}"')
    await db.commit()

async def check_adm(title):
    cur = await db.execute_fetchall(f'SELECT target_id, target_title FROM adm WHERE target_title = "{title}"')
    return cur
    
async def get_bunches():
    bunches = list(set(await db.execute_fetchall('SELECT source_title, source_id FROM bunches')))
    text = ''
    for source_title in bunches:
        targets = ", ".join([i[0] for i in await db.execute_fetchall(f'SELECT target_title FROM bunches WHERE source_title = "{source_title[0]}"')])
        if source_title[1] != 0:
            text+=f'<b>{source_title[0]} ---> {targets}</b>\n'
        else:
            text+=f'<i>{source_title[0]} ---> {targets}</i>\n'
    if text!='':
        return text
    else:
        return 'Связок пока нет!'

async def add_private(source_id, source_title):
    try:
        await db.execute(f'UPDATE bunches SET source_id = {source_id} WHERE source_title = "{source_title}"')
        await db.commit()
    except:
        pass

async def get_bunch(source_id):
    print(source_id)
    text = ''
    bunch = await db.execute_fetchall(f'SELECT source_title, target_title FROM bunches WHERE source_id = {str(source_id)[4:]}')
    if bunch == []:
        bunch = await db.execute_fetchall(f'SELECT source_title, target_title FROM bunches WHERE source_id = {str(source_id)}')
    print(bunch)
    text += bunch[0][0]
    text += ' ---> '
    for i in bunch:
        text += f'{i[1]}, '
    return text[:-2]

async def save_post(source_id, message_id, group_id):
    await db.execute(f'INSERT INTO posts VALUES ({source_id}, {message_id}, {group_id})')
    await db.commit()

async def get_frequency(id):
    return await db.execute_fetchall(f'SELECT frequrncy FROM schedule WHERE id = {id}')[0][0]

async def get_ids(group_id):
    return await db.execute_fetchall(f'SELECT message_id FROM posts WHERE group_id = {group_id}')

async def del_post(group_id):
    await db.execute(f'DELETE from posts WHERE group_id = {group_id}')
    await db.commit()

async def get_id(s_t):
    source_id = await db.execute(f'SELECT source_id FROM bunches WHERE source_title = "{s_t}"')
    return (await source_id.fetchone())[0]

async def change_freq(target_title, new_freq):
    print(target_title, new_freq)
    await db.execute(f'UPDATE adm SET frequency = {new_freq} WHERE target_title = "{target_title}"')
    await db.commit()

async def get_info(source_id):
    '''await db.execute(f'UPDATE adm SET next_time = "09.01.24 06:07" WHERE target_title = "тото"')
    await db.commit()
    await db.execute(f'UPDATE adm SET next_time = "09.01.24 07:17" WHERE target_title = "закрытый по ссылке"')
    await db.commit()
    print('готово бро')'''

    target_ids = await db.execute_fetchall(f'SELECT target_id FROM bunches WHERE source_id = {source_id}') 
    to_send = [] 
    for target_id in target_ids:
        next_time = await db.execute_fetchall(f'SELECT next_time, frequency FROM adm WHERE target_id = {target_id[0]}')
        if get_datetime(get_now()) > get_datetime(next_time[0][0]):
            to_send.append((target_id[0], get_new_time(get_now(), 1)))
            await db.execute(f'UPDATE adm SET next_time = "{get_new_time(get_now(), int(next_time[0][1]))}" WHERE target_id = {target_id[0]}')
            await db.commit()
        else:
            to_send.append((target_id[0], next_time[0][0]))
            await db.execute(f'UPDATE adm SET next_time = "{get_new_time(next_time[0][0], int(next_time[0][1]))}" WHERE target_id = {target_id[0]}')
            await db.commit()
    text = ''
    for i in to_send:
        text += str(i[0])+'!'+i[1].replace(' ', '_')+' '
    return text

async def update_counter():
    await db.execute('UPDATE private_counter SET id = id + 1')
    await db.commit()

async def set_private_id(private_id):
    await db.execute(f'UPDATE private_counter SET id = {private_id}')
    await db.commit()

async def get_private_id():
    return int((await db.execute_fetchall('SELECT id FROM private_counter'))[0][0])

async def get_adm():
    adm_list = await db.execute_fetchall(f'SELECT target_id FROM adm')
    await db.close()
    return list(map(str, adm_list))

async def pyro_on_start(new_id):
    c = await db.execute_fetchall('SELECT id FROM private_counter')
    if c == []:
        await db.execute(f'INSERT INTO private_counter VALUES ({new_id})')
        await db.commit()
    else:
        await db.execute(f'UPDATE private_counter SET id = {new_id}')
        await db.commit()


async def get_freq():
    text = ''
    freqs = await db.execute_fetchall('SELECT target_title, frequency FROM adm')
    for i in freqs:
        text += i[0] + ' - ' + str(i[1]) + ' минут\n'
    return text

async def update_private_source(source_title, source_id):
    await db.execute(f'UPDATE bunches SET source_id = {source_id} WHERE source_id = 0 AND source_title = "{source_title}"')
    await db.commit()

'''async def join_chat(chat_id, text, title):
    try:
        await grabber.userbot.join_chat(text)
        await save_source(0, title, text)
        await set_state(3)
        await grabber.bot.send_message(chat_id=chat_id, text='Запрос на вступление подан. Введи название канала-цели', reply_markup=keyboard_back)
    except:
        await grabber.userbot.join_chat(text)
        await save_source(0, title, text)
        await set_state(3)
        await grabber.bot.send_message(chat_id=chat_id, text='Запрос на вступление подан. Введи название канала-цели', reply_markup=keyboard_back)'''