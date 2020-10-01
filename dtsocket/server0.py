from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import logging 
import datetime
from concurrent.futures import ThreadPoolExecutor

class TimeServer:
    def __init__(self, host, port):
        self.logger = self.setup_logger()
        self.sock = self.setup_socket(host, port)
        self.connections=[]

    def run(self):
        self.logger.info('TimerServer is running.')
        with ThreadPoolExecutor() as executor:           
            while True:
                conn, addr = self.sock.accept()
                self.logger.debug(f'New Connection: {addr}')
                self.connections.append(conn)
                self.logger.debug(f'Connections: {self.connections}')
                executor.submit(self.relay_messages, conn, addr)

    def relay_messages(self, conn, addr):
        while True:
            data = conn.recv(4096)            
            self.logger.info(data)
            now = datetime.datetime.now()
            my_bytes = bytearray(6)
            my_bytes[0] = (int(now.strftime("%y")))
            my_bytes[1] = (int(now.strftime("%m")))            
            my_bytes[2] = (int(now.strftime("%d")))
            my_bytes[3] = (int(now.strftime("%w")))
            my_bytes[4] = (int(now.strftime("%H")))
            my_bytes[5] = (int(now.strftime("%M")))
            for connection in self.connections:
                connection.send(my_bytes)
            if not data:
                self.logger.warning("No data. Exiting.")
                break


    @staticmethod
    def setup_logger():
        logger = logging.getLogger('TimerServer')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def setup_socket(host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        #sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
        return sock

if __name__ == "__main__":
    server = TimeServer('localhost', 4333)
    server.run()