from dotenv import load_dotenv
import os


load_dotenv("init.env")

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
prefix = os.getenv("PREFIX", "! . * ^").split()
