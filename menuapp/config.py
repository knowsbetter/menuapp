import os
from typing import cast

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
REDIS_HOST = cast(str, os.getenv("REDIS_HOST"))
REDIS_PORT = cast(int, os.getenv("REDIS_PORT"))
SPECIAL_PASSWORD = os.getenv("SPECIAL_PASSWORD")
