from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class TaskNotifier:
    def __init__(self, channel_layer_alias=None) -> None:
        if channel_layer_alias is None:
            # default channel layer
            self.channel_layer = get_channel_layer()
        else:
            self.channel_layer = get_channel_layer(channel_layer_alias)

    def send_notification(self, group_name, type, **kwargs):
        payload = dict({"type": type}, **kwargs)
        async_to_sync(self.channel_layer.group_send)(group_name, payload)
