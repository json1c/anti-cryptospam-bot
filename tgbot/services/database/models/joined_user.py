from sqlalchemy import Column, DateTime, Integer, func

from tgbot.services.database.engine import Base


class JoinedUser(Base):
    __tablename__ = "joined_users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    chat_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
