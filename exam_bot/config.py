import os

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
PATH = os.getenv("FILES_PATH")
DB_NAME = os.getenv("DB_NAME")
PORT = int(os.getenv("PORT"))
HOST = os.getenv("HOST")
SEND_ERRORS = bool(os.getenv("SEND_ERRORS"))
