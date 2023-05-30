def truncate_channel_link_to_username(channel_link: str) -> str:
    if '/' in channel_link:
        return channel_link.split('/')[-1]

    return channel_link
