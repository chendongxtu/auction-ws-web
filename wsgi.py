import os

from websocket import create_app
from websocket.event import auction_event # noqa
from websocket.event import test_event # noqa

application = create_app()
