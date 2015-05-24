from __future__ import print_function
import logging
from threading import Timer
from collections import deque

import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

try:
    import simplejson as json
except ImportError:
    import json

cherrypy.config.update({'server.socket_port': 9001})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.DEBUG)
logger = logging.getLogger()

fake_data = deque(range(101) + range(99, 0, -1))


class Faker(object):
    def __init__(self):
        self.connections = []
        t = Timer(0.1, self.send_data)
        t.start()

    def new_connection(self, con):
        self.connections.append(con)

    def closed_connection(self, con):
        self.connections.remove(con)

    def handle_request(self, con, msg):
        logger.log("Received: " + repr(msg))

    def send_data(self):
        data = fake_data.popleft()
        fake_data.append(data)
        logger.debug("Now data: " + repr(data))
        for con in self.connections:
            con.send('{"data":' + repr(data) + '}')
        t = Timer(0.1, self.send_data)
        t.start()


app = Faker()


class WebSocketHandler(WebSocket):
    def opened(self):
        app.new_connection(self)
        print('WS connection opened from', self.peer_address)

    def closed(self, code, reason=None):
        app.closed_connection(self)
        print('WS connection closed with code', code, reason)

    def received_message(self, message):
        try:
            request = json.loads(message.data)
        except ValueError as e:
            logger.exception("JSON not correctly formatted")
            return
        except Exception as e:
            logger.exception('JSON decode failed for message')
            return
        app.handle_request(self, request)

    def send(self, payload, binary=False):
        logger.debug("Answer: " + str(payload))
        super(WebSocketHandler, self).send(payload, binary)


class Root(object):
    @cherrypy.expose
    def index(self):
        handler = cherrypy.request.ws_handler


cherrypy.quickstart(Root(), '/', config={
    '/': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': WebSocketHandler,
    },
})
