from dotenv import load_dotenv
import os


load_dotenv("init.env")

api_id = os.getenv("API_ID", "2040")
api_hash = os.getenv("API_HASH", "b18441a1ff607e10a989891a5462e627")
prefix = os.getenv("PREFIX", "! . * ^").split()
