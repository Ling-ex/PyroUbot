import os
import sys
import logging

from dotenv import load_dotenv

from hydrogram import Client


load_dotenv("config.env", override=True)


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")


class UserBot(Client):
    def __init__(self):
        super().__init__(
            "userbot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING,
            in_memory=True,
            plugins=dict(root="plugins")
        )
        
    
    async def start(self):
        logging.basicConfig(level=logging.INFO)
        try:
            await super().start()
            logging.info("Client Started!")
        except Exception as e:
            logging.error(str(e))