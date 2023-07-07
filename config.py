from dotenv import load_dotenv
import os

load_dotenv()
REDIS_URL = os.environ.get("REDIS_URL")
TOKEN = os.environ.get("TOKEN")
