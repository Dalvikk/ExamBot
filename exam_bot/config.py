import os

TOKEN = os.environ["TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])
PATH = os.environ["FILES_PATH"]
DB_NAME = os.environ["DB_NAME"]
PORT = int(os.environ["PORT"])
HOST = os.environ["HOST"]
SEND_ERRORS = bool(os.environ["SEND_ERRORS"])
