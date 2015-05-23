from __future__ import print_function, unicode_literals
import logging

try:
    import simplejson as json
except ImportError:
    import json

__author__ = 'javier'

logger = logging.getLogger()


class Application:
    def __init__(self):
        self.connections = {}

    def send_error(self, connection, content):
        self.send('error', connection, content)

    def send(self, type, connection, content):
        try:
            text = json.dumps(content)
        except Exception as e:
            logger.exception("JSON loading failed")
            connection.send('{"type": "' + type + '", "message": "' + repr(
                content) + '"}')
            return
        connection.send('{"type": "' + type + '", "message": ' + text + '}')

    def new_connection(self, con):
        self.connections[con] = {'status': 'uninit'}
        logger.debug("Adding new connection " + repr(con))

    def closed_connection(self, con):
        self.connections.pop(con)
        logger.debug("Removing closed connection " + repr(con))

    def handle_request(self, connection, message):
        logger.debug('Handling', message)
        if not message.get('type', False):
            self.send_error(connection, message)
        if message['type'] == 'initialize':
            self.handle_initialize(connection, message)

    def handle_initialize(self, con, msg):
        init_msg = {
            'displays': [
                {
                    'id': 1,
                    'axis': [0, 10, 0, 1],
                    'signals': [
                        {
                            'id': 0,
                            'name': 'Reference',
                        },
                        {
                            'id': 1,
                            'name': 'Plant',
                        },
                    ],
                },
            ],
        }
        self.send('initialize', con, init_msg)
