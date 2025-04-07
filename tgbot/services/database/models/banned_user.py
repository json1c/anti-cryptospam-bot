from sqlalchemy import Column, Integer

from tgbot.services.database.engine import Base


class BannedUser(Base):
    __tablename__ = "banned_users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
