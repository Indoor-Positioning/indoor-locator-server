from channels.routing import route
from locator.consumers import ws_receive


channel_routing = [
    route('websocket.receive', ws_receive)
]
