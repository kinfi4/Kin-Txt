import os
import csv

from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types import Channel

from .utils import cut_channel_link, export_post_to_csv, get_or_create_channel_file
from .fetch_config import LoadPostsConfig


_WORDS_MUST_BE = ["корупц", "розкрад", "присво", "шахрай", "злочин", "втручан", "втручання", "зловжив", "коррупц", "расхищ", "присво", "мошен", "преступ", "вмешательство", "вмешательства", "присвоил"]


client = TelegramClient("session-1", api_id=int(os.getenv("API_KEY")), api_hash=os.getenv("API_HASH"))


def fetch(config: LoadPostsConfig) -> None:
    with client:
        client.loop.run_until_complete(collect_posts(config))


async def collect_posts(config: LoadPostsConfig) -> None:
    counter = 0
    channels_to_export_cut = map(cut_channel_link, config.channels)

    for channel_name in channels_to_export_cut:
        print(f"Starting collecting data from {channel_name}...")

        entity: Channel = await client.get_entity(channel_name)

        with get_or_create_channel_file(config.output_file_path) as destination_file_obj:
            csv_writer = csv.writer(destination_file_obj)
            csv_writer.writerow(["channel_name", "text", "date"])

            message: Message
            async for message in client.iter_messages(entity, offset_date=config.start_date, reverse=True):
                if not message.text:
                    continue

                if not any(word in message.text.lower() for word in _WORDS_MUST_BE):
                    continue

                from random import random
                if random() < 0.3:
                    continue

                if message.date.date() > config.end_date.date():
                    break

                print("Exporting message...")
                export_post_to_csv(csv_writer, message)
                destination_file_obj.flush()
                counter += 1

    print(f"Collected {counter} posts.")
