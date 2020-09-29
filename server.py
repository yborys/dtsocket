from socket import socket, AF_INET, SOCK_STREAM
import logging

class TimeServer:
    def __init__(self, host, port):
        self.logger = self.setup_logger()
        self.sock = self.setup_socket(host, port)

    def run(self):
        self.logger.info('TimerServer is running.')
        while True:
            conn, addr = self.sock.accept()
            self.logger.info(f'New Connection: {addr}')

    @staticmethod
    def setup_logger():
        logger = logging.getLogger('TimerServer')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def setup_socket(host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
        return sock

if __name__ == "__main__":
    server = TimeServer('localhost', 4333)
    server.run()