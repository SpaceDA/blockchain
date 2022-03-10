import socket
import pickle
import select
from abc import ABC, abstractmethod

TCP_PORT = 5005
BUFFER_SIZE = 1024
local_ip = '10.0.1.27'


class Connection(ABC):
    @abstractmethod
    def connect(self, ip_addr, port):
        pass


class GetObject(Connection):

    def connect(self, ip_addr, port):
        """open connection and listen"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_addr, port))
        s.listen()
        print("server: waiting for data")
        return s

    def receive_object(self, server):
        """receive and de-serialize incoming data in chunks of BUFFER_SIZE"""
        inputs = [server]
        print(inputs)
        while inputs:
            readable, writable, exceptional = select.select(
                inputs, [], [], 0.5
            )
            for s in readable:
                data = b""
                 # accept connections from external
                new_sock, addr = s.accept()
                while True:
                    d = new_sock.recv(BUFFER_SIZE)
                    if not d:
                        break
                    data += d
                print("Data Received")
                return pickle.loads(data)

        return None


class SendObject(Connection):

    def __init__(self, object_list):
        self.object_list = object_list

    def connect(self, ip_addr, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_addr, port))
        return s

    def send_object(self, s):
        """serialize using pickle and send to server"""
        send_bytes = pickle.dumps(self.object_list)
        s.send(send_bytes)
        print("Object list sent to server")
        s.close()
        return None


if __name__ == "__main__":
    """test non-blocking server"""
    server = GetObject()
    conn = server.connect('localhost', TCP_PORT)
    incoming_data = server.receive_object(conn)


    print("new object", incoming_data,"end object")
    print("SUCCESS, server is non-blocking")

    server.close()

