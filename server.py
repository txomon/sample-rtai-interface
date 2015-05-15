import cherrypy
from os.path import abspath
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

cherrypy.config.update({'server.socket_port': 9000})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()


class WebSocketHandler(WebSocket):
    def received_message(self, message):
        return 'ok'

class Root(object):
    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler


cherrypy.quickstart(Root(), '/', config={
    '/': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': abspath('./index.html')
    },
    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': abspath('./js')
    },
    '/ws': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': WebSocketHandler,
    },
})
