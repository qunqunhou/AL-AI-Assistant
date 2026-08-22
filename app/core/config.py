import os
from dotenv import load_dotenv


load_dotenv()


API_KEY=os.getenv("API_KEY")

BASE_URL=os.getenv("BASE_URL")

MODEL=os.getenv("MODEL")

SECRET_KEY=os.getenv("SECRET_KEY")

DATABASE=os.getenv("DATABASE","ai_chat.db")

DB_HOST=os.getenv("DB_HOST","localhost")

DB_PORT=os.getenv("DB_PORT","3306")

DB_NAME=os.getenv("DB_NAME","al_ai")

DB_USER=os.getenv("DB_USER","ai_user")

DB_PASSWORD=os.getenv("DB_PASSWORD","")
