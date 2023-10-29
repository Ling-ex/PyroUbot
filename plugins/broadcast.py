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
        m.reply_to_message.text
        if m.reply_to_message and m.reply_to_message.text
        else ""
        if len(m.command) < 2
        else " ".join(m.command[1:])
    )
    return msg

async def send_broadcast_message(c, group, msg):
    try:
        await c.send_message(group, msg)
        return True
    except errors.FloodWait as f:
        await asyncio.sleep(f.value)
    except Exception as e:
        return False

@Client.on_message(filters.command(["broadcast", "gcast"], config.prefix) & filters.me)
async def broadcast(c: Client, m: types.Message):
    msg = get_msg(m)
    if not msg:
        return await m.reply("Give me a message or reply to a message!")
    load = await m.reply("Broadcast processing....")
    done = 0
    error = 0
    async for dialog in c.get_dialogs():
        if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            group = dialog.chat.id
            if m.reply_to_message:
                if await send_broadcast_message(c, group, msg):
                    done += 1
                else:
                    error += 1
            else:
                if await send_broadcast_message(c, group, msg):
                    done += 1
                else:
                    error += 1
            await asyncio.sleep(0.5)
    await load.edit(f"<i>Broadcast was sent to {done} groups, failed to send to {error} groups</i>")
