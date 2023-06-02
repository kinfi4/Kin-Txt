from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base, Mapped

from kin_news_api.constants import PossibleRating
from kin_news_core.database import metadata


Base = declarative_base(metadata=metadata)


class UserChannel(Base):
    __tablename__ = "user_channel"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"), primary_key=True)
    channel_id: Mapped[int] = Column(Integer, ForeignKey("channel.id"), primary_key=True)


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = Column(String, unique=True)
    password: Mapped[str] = Column(String)
    is_fetching: Mapped[bool] = Column(Boolean, default=False)
    subscriptions: Mapped[list["Channel"]] = relationship("UserChannel")
    ratings: Mapped[list["ChannelRatings"]] = relationship("ChannelRatings", back_populates="user")


class Channel(Base):
    __tablename__ = "channel"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    link: Mapped[str] = Column(String(255), unique=True, index=True)
    subscribers: Mapped[list["User"]] = relationship("UserChannel")
    ratings: Mapped[list["ChannelRatings"]] = relationship("ChannelRatings", back_populates="channel")


class ChannelRatings(Base):
    __tablename__ = "channel_rating"
    __table_args__ = (UniqueConstraint("user_id", "channel_id"), {"extend_existing": True})

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    rate: Mapped[int] = Column(Integer, CheckConstraint(f'rate IN ({", ".join(str(e.value) for e in PossibleRating)})'))
    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"))
    channel_id: Mapped[int] = Column(Integer, ForeignKey("channel.id"))

    user: Mapped[User] = relationship(back_populates="ratings")
    channel: Mapped[Channel] = relationship(back_populates="ratings")
