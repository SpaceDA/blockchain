import socket
import pickle
import select

TCP_PORT = 5050
BUFFER_SIZE = 1024
local_ip = '10.0.1.27'


def new_server_connection(ip_addr):
    """open connection"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr, TCP_PORT))
    s.listen()
    print("server: waiting from data")
    return s


def receive_object(s):
    """receive and de-serialize incoming data in chunks of BUFFER_SIZE"""
    inputs = [s]
    outputs = [s]

    readable, writable, exceptional = select.select(
        inputs, outputs, inputs, 10
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


        return pickle.loads(data)

    return None

def send_block(blk, socket):
    """serialize using pickle and send to server"""
    send_bytes = pickle.dumps(blk)
    socket.send(send_bytes)


if __name__ == "__main__":
    """test non-blocking server"""
    server = new_server_connection('localhost')
    test_obj = receive_object(server)
    print("SUCCESS, server is non-blocking")
    print(test_obj)
    server.close()

