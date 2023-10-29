import config

from pyrogram import Client, idle as idling


client = Client(
     "SolidUbot",
     api_id=config.api_id,
     api_hash=config.api_hash,
     device_model="SolidUbot",
     plugins=dict(root="plugins"),
     in_memory=False,
)

idle = idling
