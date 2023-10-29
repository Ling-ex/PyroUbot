import config
from datetime import datetime

from pyrogram import Client, filters, types


@Client.on_message(filters.command("ping", config.prefix) & filters.me)
async def ping(c: Client, m: types.Message):
    start = m.date
    msg = await m.reply("ping...")
    end = datetime.now()
    return await msg.edit(
        f"<b>Pong!</b>\n<code>{round((end - start).microseconds / 1000)}ms</code>")
