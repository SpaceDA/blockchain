import socket
import pickle
import select

TCP_PORT = 5050
BUFFER_SIZE = 1024
local_ip = '10.0.1.27'


def new_server_connection(ip_addr, port):
    """open connection"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr, port))
    s.listen()
    print("server: waiting for data")
    return s


def receive_object(s):
    """receive and de-serialize incoming data in chunks of BUFFER_SIZE"""

    inputs = [s]
    outputs = [s]
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


def send_object(object_list, ip_address, port):
    """serialize using pickle and send to server"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_address, port))
    send_bytes = pickle.dumps(object_list)
    s.send(send_bytes)
    print("Object list sent to server")
    s.close()
    return None


if __name__ == "__main__":
    """test non-blocking server"""
    server = new_server_connection('localhost')

    test_obj = receive_object(server)
    print("new object", test_obj,"end object")
    print("SUCCESS, server is non-blocking")

    server.close()

