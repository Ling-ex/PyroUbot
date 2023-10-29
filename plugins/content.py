import config
import os

from pyrogram import Client, filters, types
from .broadcast import get_msg


async def download_copy(get, c, infomsg, m, chatid, msgid):
    msg = m.reply_to_message or m
    get = await c.get_messages(chatid, msgid)
    text = get.caption or ""
    if get.text:
        await c.send_message(
            m.chat.id,
            get.text,
            reply_to_message_id=msg.id,
        )
    elif get.photo:
        media = await c.download_media(get)
        await c.send_photo(
            m.chat.id,
            media,
            caption=text,
            reply_to_message_id=msg.id,
        )
    elif get.animation:
        media = await c.download_media(get)
        await c.send_animation(
            m.chat.id,
            animation=media,
            caption=text,
            reply_to_message_id=msg.id,
        )
    elif get.voice:
        media = await c.download_media(get)
        await c.send_voice(
            m.chat.id,
            voice=media,
            caption=text,
            reply_to_message_id=msg.id,
        )
    elif get.audio:
        media = await c.download_media(get)
        await c.send_audio(
            m.chat.id,
            audio=media,
            duration=get.audio.duration,
            caption=text,
            reply_to_message_id=msg.id,
        )
    elif get.document:
        media = await c.download_media(get)
        await c.send_document(
            m.chat.id,
            document=media,
            caption=text,
            reply_to_message_id=msg.id,
        )
    elif get.video:
        media = await c.download_media(get)
        await c.send_video(
            m.chat.id,
            video=media,
            duration=get.video.duration,
            caption=text,
            reply_to_message_id=msg.id,
        )
    await infomsg.delete()
    os.remove(media)


@Client.on_message(filters.command("copy", config.prefix) & filters.me)
async def copy_content(c: Client, m: types.Message):
    link = m.reply_to_message or get_msg(m)
    if not link:
        return await m.reply(
            f"<b><code>{m.text}</code> [link konten]</b>"
        )
    infomsg = await m.reply("Processing....")
    if m.reply_to_message:
        try:
            await m.reply_to_message.copy(m.chat.id, reply_to_message_id=m.id)
            await infomsg.delete()
        except Exception as e:
            await infomsg.edit(f"{e}")
    elif "https://t.me/" in link:
        datas = link.split("/")
        msgid = int(datas[-1].split("?")[0])
        if "https://t.me/c/" in link:
            chatid = int("-100" + datas[-2])
            try:
                get = await c.get_messages(chatid, msgid)
                try:
                    await get.copy(m.chat.id, reply_to_message_id=msg.id)
                    await infomsg.delete()
                except Exception:
                    await download_copy(get, c, infomsg, m, chatid, msgid)
            except Exception as e:
                await infomsg.edit(f"{e}")
        else:
            username = datas[-2]
            try:
                get = await c.get_messages(username, msgid)
                try:
                    await get.copy(m.chat.id, reply_to_message_id=msg.id)
                    await infomsg.delete()
                except Exception:
                    await download_copy(get, c, infomsg, m, username, msgid)
            except Exception as e:
                await infomsg.edit(f"{e}")
    else:
        return await infomsg.edit("Link invalid!")
