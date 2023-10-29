import config
import asyncio

from pyrogram import Client, filters, types


@Client.on_message(filters.command("del", config.prefix) & filters.me)
async def delete(c: Client, m: types.Message):
    reply = m.reply_to_message
    await asyncio.gather(reply.delete(), m.delete())


@Client.on_message(filters.command("purge", config.prefix) & filters.me)
async def purge(c: Client, m: types.Message):
    reply = m.reply_to_message
    if not reply:
        return await m.reply("Reply to the message you want to delete next")
    await m.delete()
    chat = m.chat.id
    msgid = []
    for msgids in range(
        reply.id,
        m.id
    ):
        msgid.append(msgids)
        if len(msgid) == 100:
            await c.delete_messages(
                chat_id=chat,
                message_ids=msgid,
                revoke=True,
            )
            msgid = []
    if len(msgid) > 0:
        await c.delete_messages(
            chat_id=chat,
            message_ids=msgid,
            revoke=True,
        )
