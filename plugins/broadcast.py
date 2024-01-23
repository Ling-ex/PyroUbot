import asyncio
import config
from pyrogram import (
  Client,
  filters,
  types,
  enums,
  errors,
)



def get_msg(m):
    msg = (
        m.reply_to_message
        if m.reply_to_message
        else ""
        if len(m.command) < 2
        else " ".join(m.command[1:])
    )
    return msg


@Client.on_message(filters.command(["broadcast", "gcast"], config.prefix) & filters.me)
async def broadcast_group(c: Client, m: types.Message):
    msg = get_msg(m)
    if not msg:
        return await m.reply("Give me a message or reply to a message!")
    load = await m.reply("Broadcast Group processing....")
    done = error = 0
    chat_ids = []

    async for dialog in c.get_dialogs():
        if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            chat_ids.append(dialog.chat.id)

    async def send_broadcast(chat_id):
        nonlocal done, error
        try:
            if m.reply_to_message:
                await msg.copy(chat_id)
            else:
                await c.send_message(chat_id, msg)
            done += 1
            await asyncio.sleep(0.5)
        except errors.FloodWait as f:
            await asyncio.sleep(f.value + 1)
            await send_broadcast(chat_id)
        except Exception:
            error += 1

    for chat_id in chat_ids: # loop
        await send_broadcast(chat_id)
    return await load.edit(f"<i>Broadcast was sent to {done} groups, failed to send to {error} groups(s)</i>")


@Client.on_message(filters.command("ucast", config.prefix) & filters.me)
async def broadcast_users(c: Client, m: types.Message):
    msg = get_msg(m)
    if not msg:
        return await m.reply("Give me a message or reply to a message!")
    load = await m.reply("Broadcast users processing.....")
    done = error = 0
    chat_ids = []

    async for dialog in c.get_dialogs():
        if dialog.chat.type in enums.ChatType.PRIVATE:
            chat_ids.append(dialog.chat.id)

    async def send_broadcast(chat_id):
        nonlocal done, error
        try:
            if m.reply_to_message:
                await msg.copy(chat_id)
            else:
                await c.send_message(chat_id, msg)
            done += 1
            await asyncio.sleep(0.5)
        except errors.FloodWait as f:
            await asyncio.sleep(f.value + 1)
            await send_broadcast(chat_id)
        except Exception:
            error += 1

    for chat_id in chat_ids: # loop
        await send_broadcast(chat_id)
    return await load.edit(f"<i>Broadcast was send to {done} users, failed to send to {error} users(s)</i>")


@Client.on_message(filters.command("fwdcast", config.prefix) & filters.me)
async def broadcast_forward(c: Client, m: types.Message):
    if not (reply := m.reply_to_message):
        return await m.reply("Reply to messages you want to continue posting")
    load = await m.reply("Broadcast forward processing....")
    done = error = 0
    chat_ids = []

    async for dialog in c.get_dialogs():
        if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            chat_ids.append(dialog.chat.id)

    async def send_broadcast(chat_id):
        nonlocal done, error
        try:
            await m.reply_to_message.forward(chat_id)
            done += 1
            await asyncio.sleep(0.5)
        except errors.FloodWait as f:
            await asyncio.sleep(f.value + 1)
            await send_broadcast(chat_id)
        except Exception:
            error += 1

    for chat_id in chat_ids: # loop
        await send_broadcast(chat_id)
    return await load.edit(f"<i>Broadcast was send to {done} forward, failed to send to {error} forward(s)")
