import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv

from db.db import Session, UserMessages, UserTable

dp = Dispatcher()

session = Session()
load_dotenv('.env')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    result = session.query(UserTable).all()
    c = []
    for i in result:
        c.append(i.user_id)
    user_is = int(len(c)) + 1
    if str(message.from_user.id) not in c:
        user_id = str(message.from_user.id)
        username = message.from_user.username
        created = str(message.date)

        user = UserTable(user_telegram_id=user_id,user_id=user_is, username=username, created=created)

        session.add(user)
        session.commit()
        await message.reply(text=message.text)


@dp.message(F.text)
async def message_db(message: Message):

    result = session.query(UserMessages).all()
    c = []
    for i in result:
        c.append(i.user_id)

    message_id = int(len(c)) + 1
    user_id = message.from_user.id
    text = message.text

    chat_time = str(message.date)

    user = UserMessages(message_id=message_id, user_id=user_id, text=text, created=chat_time)
    session.add(user)
    session.commit()
    await message.reply(text=message.text)


async def main() -> None:
    bot = Bot(os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
    commands = [
        BotCommand(command="start", description="touch to start the bot")
    ]

    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
