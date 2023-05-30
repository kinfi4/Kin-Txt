from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, UniqueConstraint, Enum, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base

from kin_news_api.constants import PossibleRating
from kin_news_core.database import metadata


Base = declarative_base(metadata=metadata)


user_channel_association_table = Table(
    "user_channel",
    metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("channel_id", Integer, ForeignKey("channel.id"))
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    subscriptions = relationship("Channel", secondary=user_channel_association_table)
    ratings = relationship("ChannelRatings")
    is_fetching = Column(Boolean, default=False)


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255), unique=True, index=True)
    subscribers = relationship("User", secondary=user_channel_association_table)
    ratings = relationship("ChannelRatings")


class ChannelRatings(Base):
    __tablename__ = "channel_rating"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rate = Column(Integer, CheckConstraint(f'rate IN ({", ".join(str(e.value) for e in PossibleRating)})'))
    user_id = Column(Integer, ForeignKey("user.id"))
    channel_id = Column(Integer, ForeignKey("channel.id"))

    __table_args__ = (UniqueConstraint("user_id", "channel_id"), )
