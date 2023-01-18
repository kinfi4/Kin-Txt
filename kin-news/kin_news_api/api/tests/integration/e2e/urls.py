from django.urls import reverse


class APIUrls:
    channels_url = reverse('channels')
    rate_channel_url = reverse('channels-rates')
    messages_url = reverse('messages')

    @staticmethod
    def channel_details_url(channel_link: str):
        return reverse('single-channel', args=(channel_link,))

    @staticmethod
    def channel_exists_url(channel_link: str):
        return reverse('channel-exists', args=(channel_link,))
