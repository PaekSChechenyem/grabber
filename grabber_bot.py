from aiogram import Dispatcher
import grabber_db
import asyncio
import grabber
from grabber_userbot import fill_last_msg_id
import grabber_start
import grabber_states_handlers
import grabber_commands
import grabber_adm
import grabber_userbot_msgs_handler
import grabber_callback_handlers

#bot.id = 6420020475

async def main():
    await grabber.userbot.start()
    await fill_last_msg_id()
    dp = Dispatcher()
    dp.include_routers(grabber_userbot_msgs_handler.router, 
                       grabber_adm.router, 
                       grabber_start.router, 
                       grabber_states_handlers.router, 
                       grabber_commands.router,
                       grabber_callback_handlers.router
                       )
    await dp.start_polling(grabber.bot)

if __name__ == '__main__':
    grabber.userbot.run(main())