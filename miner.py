from socket_utils import receive_object, new_server_connection, send_object
from transactions import Tx
from txblock import TxBlock
from signatures import generate_keys


WALLET_LIST = ['localhost']
IN_PORT = 6000
OUT_PORT = 6050
BLOCK_REWARD = 25.0

def miner_server(server_ip, wallet_list):
    """
    open server conn, receive incoming tx's,
    combine into block, mine block, return block
    """
    # open server connection
    server = new_server_connection(server_ip, IN_PORT)

    # receive TX list
    object_list = receive_object(server)

    # turn into block
    new_block = TxBlock(None)
    for object in object_list:
        new_block.add_tx(object)

    # extract block rewards + mining fees
    total_in, total_out = new_block.count_totals()
    fee_tx = Tx()
    fee_tx.add_output(my_pu, BLOCK_REWARD + total_in-total_out)

    # add mining rewards + fees to block
    new_block.add_tx(fee_tx)

    # mine block
    new_block.get_nonce()

    # return block to wallets
    for address in wallet_list:
        send_object([new_block], address, OUT_PORT)


my_pr, my_pu = generate_keys()

miner_server('localhost', WALLET_LIST)


