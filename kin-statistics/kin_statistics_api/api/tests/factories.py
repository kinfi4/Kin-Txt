from datetime import datetime
from random import choice

from faker import Faker

from api.domain.entities import GenerateReportEntity
from config.constants import MessageCategories, SentimentTypes
from kin_news_core.telegram.entities import TelegramChannelEntity, TelegramMessageEntity

faker = Faker()


def build_telegram_channel_entity() -> TelegramChannelEntity:
    return TelegramChannelEntity(
        link=faker.words(0),
        title=faker.words(0),
        description=faker.sentence(),
        participants_count="300 K"
    )


def build_generate_report_entity() -> GenerateReportEntity:
    return GenerateReportEntity(
        start_date=datetime.now(),
        end_date=datetime.now(),
        channels=["ChannelName"]
    )


def build_telegram_message_entity():
    return TelegramMessageEntity(
        text=faker.text(),
        channel_title=faker.word(),
        message_link=faker.word(),
        created_at=faker.past_datetime(),
    )


def get_random_sentiment_type() -> SentimentTypes:
    return choice(list(SentimentTypes))


def get_random_message_category() -> MessageCategories:
    return choice(list(MessageCategories))
