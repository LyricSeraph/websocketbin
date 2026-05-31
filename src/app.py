from flask import Flask
from flask_sock import Sock
from src.routes import register_routes
from src.websockets import register_websockets

app = Flask(__name__)
sock = Sock(app)

# Register routes and websockets from separate files
register_routes(app)
register_websockets(sock)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
