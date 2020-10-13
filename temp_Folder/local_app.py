from waitress import serve
import socket

from app import app

if __name__ == '__main__':
    DASHBOARD_PORT = 80
    IP_ADDRESS = socket.gethostbyname(socket.gethostname())

    serve(app, host=IP_ADDRESS, threads=20)        # port=DASHBOARD_PORT,
    