from socket import socket, AF_INET, SOCK_STREAM
import logging
from threading import Thread

class TestClient:

    def __init__(self, host, port):
        self.logger = self.setup_logger()
        self.sock = self.setup_socket(host, port)

        thread = Thread(target=self.send_message)
        thread.daemon = True
        thread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            self.logger.info(data.hex())

    def send_message(self):
        while True:
            user_message = input('Enter test message: ')
            self.sock.send(user_message.encode('utf-8', 'backslashreplace'))

    @staticmethod
    def setup_logger():
        logger = logging.getLogger('TestClient')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def setup_socket(host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))        
        return sock

if __name__ == "__main__":
    from dtsocket.settings import SERVER_HOST, SERVER_PORT
    client = TestClient(SERVER_HOST, SERVER_PORT)