from txblock import TxBlock
from transactions import Tx
from signatures import generate_keys
from socket_utils import SendObject
import socket
import pickle

TCP_PORT = 5005
local_ip = '10.0.1.27'


if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    tx1 = Tx()
    tx1.add_input(pu1, 2.3)
    tx1.add_output(pu2, 1.0)
    tx1.add_output(pu3, 1.1)
    tx1.sign(pr1)

    tx1 = Tx()
    tx1.add_input(pu1, 2.3)
    tx1.add_output(pu2, 1.0)
    tx1.add_output(pu3, 1.1)
    tx1.sign(pr1)

    tx2 = Tx()
    tx2.add_input(pu3, 2.3)
    tx2.add_input(pu2, 1.0)
    tx2.add_output(pu1, 3.1)
    tx2.sign(pr3)
    tx2.sign(pr2)

    B1 = TxBlock(None)
    B1.add_tx(tx1)
    B1.add_tx(tx2)

    send_server = SendObject([B1, tx2])
    conn = send_server.connect('localhost', TCP_PORT)
    send_server.send_object(conn)





