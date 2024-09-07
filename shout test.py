from typing import List, Union
from contextlib import suppress
from aiogram.utils.exceptions import ChatNotFound

import logging

from app.loader import dp

API_TOKEN = '5119758921:AAER4wLBOY6bbEChecbjGyTzqcP4vYMQ_WA'

#переменные для удобной работы с ботом
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def notify_admins(admins: Union[List[int], List[str], int, str]):
    count = 0
    for admin in admins:
        with suppress(ChatNotFound):
            await dp.bot.send_message(admin, "The bot is running")
            count += 1
    logging.info(f"{count} admins received messages")
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)