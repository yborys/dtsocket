from socket import socket, AF_INET, SOCK_STREAM
import logging 
import selectors
import types


class TimeServer:
    def __init__(self, host, port):
        self.logger = self.setup_logger()
        self.lsock = self.setup_socket(host, port)
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

    def run(self):
        self.logger.info('TimerServer is running.')
        while True:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        self.logger.info(f'accepted connection from :{addr}')
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                self.logger.info(f'closing connection to {data.addr}')
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                self.logger.info(f'echoing {repr(data.outb)} to {data.addr}')
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]



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
        sock.setblocking(False)
        return sock

if __name__ == "__main__":
    from dtsocket.settings import SERVER_HOST, SERVER_PORT
    server = TimeServer(SERVER_HOST, SERVER_PORT)
    server.run()