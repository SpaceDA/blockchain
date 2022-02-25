from txblock import TxBlock
import socket
import pickle

TCP_PORT = 5005
BUFFER_SIZE = 1024

def new_connection(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr, TCP_PORT))
    s.listen()
    return s

def receive_object(s):
    data = b""
    new_sock, addr = s.accept()
    while True:
        d = new_sock.recv(BUFFER_SIZE)
        if not d:
            break
        data += d
    return pickle.loads(data)

    return pickle.loads(d)

if __name__ == "__main__":
    s = new_connection('10.0.1.27')
    newB = receive_object(s)
    if newB.is_valid():
        print("SUCCESS, new TX is valid")
    else:
        print("ERROR, new Tx invalid")

    if newB.data[0].inputs[0][1] == 2.3:
        print("SUCCESS, black 1 input 1 matches")
    else:
        print("ERROR, block 1 input 1 does not match")

    if newB.data[0].outputs[0][1] == 1.0:
        print("SUCCESS, block 1 output 1 matches")
    else:
        print("ERROR, block 1 output 1 does not match")

    if newB.data[0].outputs[1][1] == 1.1:
        print("SUCCESS, block 1 output 2 matches")
    else:
        print("ERROR, block 1 output 2 does not match")

    if newB.data[1].inputs[0][1] == 2.3:
        print("SUCCESS, block 2 input 1 matches")
    else:
        print("ERROR, block 2 input 1 does not match")

    if newB.data[1].inputs[1][1] == 1.0:
        print("SUCCESS, block 2 input 2 matches")
    else:
        print("ERROR, block 2 input 2 does not match")

    if newB.data[1].outputs[0][1] == 3.1:
        print("SUCCESS, block 2 output 1 matches")
    else:
        print("ERROR, block 2 output 1 does not match")

    newtx = receive_object(s)

    print(f"NewTx Input 1: {newtx.inputs[0][1]} coins")

