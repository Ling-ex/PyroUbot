from userbot import UserBot as ubot

from hydrogram import filters
from hydrogram.types import Message
from hydrogram.enums import ParseMode


@ubot.on_message(filters.command("hello", ".") & filters.me)
async def hello_world(ubot, msg: Message):
    return await msg.edit("**Hello World**", parse_mode=ParseMode.MARKDOWN)