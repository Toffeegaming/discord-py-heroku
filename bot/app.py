from flask import Flask
from threading import Thread
from werkzeug.serving import make_server

app = Flask('')

@app.route('/')
def index():
    return "Bot is ready"

def run():
    app.run(host='0.0.0.0',port=8000)

class ServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server('0.0.0.0', 8000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def start_server():
    global server
    server = ServerThread(app)
    server.start()
    print('server started')

def stop_server():
    global server
    server.shutdown()