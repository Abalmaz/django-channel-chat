# from channels.routing import route
# from example.consumers import ws_connect, ws_disconnect
#
# channel_routing = [
#     route('websocket.connect', ws_connect),
#     route('websocket.disconnect', ws_disconnect),
# ]

from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]