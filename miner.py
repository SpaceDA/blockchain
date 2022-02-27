from socket_utils import receive_object, new_server_connection, send_object
from transactions import Tx
from txblock import TxBlock

WALLET_LIST = ['localhost']
IN_PORT = 6000
OUT_PORT = 6050

def miner_server(server_ip, wallet_list):
    """
    open server conn, recveive incoming tx's,
    combine into block, mine block, return block
    """
    # open server connection
    server = new_server_connection(server_ip, IN_PORT)

    # receive TX
    object_list = receive_object(server)
    print(object_list)

    # turn into block
    B1 = TxBlock(None)
    for object in object_list:
        B1.add_tx(object)
    # mine block
    B1.get_nonce()
    # return block to wallets
    for address in wallet_list:
        send_object([B1], address, OUT_PORT)

    #extract mining fees



miner_server('localhost', WALLET_LIST)


