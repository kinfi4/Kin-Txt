from faker import Faker

from api.domain.entities import RatePostEntity
from api.models import Channel, PossibleRating
from kin_news_core.telegram.entities import TelegramChannelEntity, TelegramMessageEntity

faker = Faker()


def build_orm_channel():
    return Channel(
        link=faker.word(),
    )


def build_telegram_channel_entity(link: str = None):
    return TelegramChannelEntity(
        link=link if link is not None else faker.word(),
        title=faker.word(),
        description=faker.text(),
        participants_count="300K",
    )


def build_telegram_message():
    return TelegramMessageEntity(
        text=faker.text(),
        channel_title=faker.word(),
        message_link=faker.word(),
        created_at=faker.past_datetime(),
    )


def build_rate_post_entity():
    return RatePostEntity(
        channel_link=faker.word(),
        rating=faker.random.randint(1, 5),
    )
