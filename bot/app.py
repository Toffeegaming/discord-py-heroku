from flask import Flask
from threading import Thread
from werkzeug.serving import make_server

class ServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server('0.0.0.0', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def start_server():
    global server
    app = Flask(__name__)
    # App routes defined here
    @app.route('/')
    def index():
        return "Bot is ready"
    server = ServerThread(app)
    server.start()
    print('server started')

def stop_server():
    global server
    server.shutdown()