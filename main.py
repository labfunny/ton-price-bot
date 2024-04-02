import sys
import logging
import asyncio
import aiohttp

from config import TOKEN

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

logger = logging.getLogger(__file__)

dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    price = await get_toncoin_price()
    await message.answer(text=f'TON Price: ${price}')

async def get_toncoin_price():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://tonapi.io/v2/rates?tokens=ton&currencies=usd') as response:
            if response.status == 200:
                data = await response.json()
                result = data["rates"]["TON"]["prices"]["USD"]
                return result
            else:
                return False


async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # skip_updates = True
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')