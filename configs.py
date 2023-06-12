import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
STANDART_URL = os.environ.get("STANDART_URL")
