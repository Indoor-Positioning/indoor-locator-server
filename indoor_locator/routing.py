from channels.routing import route
from locator.consumers import ws_receive, analytics_receive


channel_routing = [
    route('websocket.receive', ws_receive, path=r"^/realtime$"),
    # new route specific for analytics
    route('websocket.receive', analytics_receive, path=r"^/analytics$")

]
