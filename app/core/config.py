import os
from dotenv import load_dotenv


load_dotenv()


API_KEY=os.getenv("API_KEY")

BASE_URL=os.getenv("BASE_URL")

MODEL=os.getenv("MODEL")

SECRET_KEY=os.getenv("SECRET_KEY")

DATABASE=os.getenv("DATABASE","ai_chat.db")


