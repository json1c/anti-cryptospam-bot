from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from tgbot.config import parse_config

Base = declarative_base()

config = parse_config("config.toml")
engine = create_async_engine(f"sqlite+aiosqlite:///{config.database.db_path}")
