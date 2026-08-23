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

REDIS_HOST=os.getenv("REDIS_HOST","redis")

REDIS_PORT=os.getenv("REDIS_PORT","6379")

RATE_LIMIT_REQUESTS=int(os.getenv("RATE_LIMIT_REQUESTS","10"))

RATE_LIMIT_WINDOW=int(os.getenv("RATE_LIMIT_WINDOW","60"))