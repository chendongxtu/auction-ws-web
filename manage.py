#!/usr/bin/env python

import sys

from flask_script import Manager

from websocket import create_app, socketio
from websocket.event import auction_event # noqa
from websocket.event import test_event # noqa

app = create_app()
manager = Manager(app)

manager.add_command('run', socketio.run(app))

if __name__ == '__main__':
    manager.run()
