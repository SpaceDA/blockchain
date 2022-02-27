from socket_utils import receive_object, new_server_connection
from transactions import Tx

WALLET_LIST = ['localhost']


def miner_server(server_ip, wallet_list):
    # open server connection
    server = new_server_connection(server_ip)

    # receive TX

    # turn into block
    # mine block
    # return block to wallets

