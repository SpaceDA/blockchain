from socket_utils import receive_object, new_server_connection, send_object
from transactions import Tx
from txblock import TxBlock
from signatures import generate_keys
import threading


WALLET_LIST = ['localhost']
IN_PORT = 7000
OUT_PORT = 7050
BLOCK_REWARD = 25.0

head_blocks = []
tx_list = []
break_now = False


def longest_block():
    """checks each head block to determine longest chain"""
    longest_len = -1
    longest_head = None
    for b in head_blocks:
        current = b
        this_len = 0
        while current != None:
            current = b.previousBlock
            this_len += 1
        if this_len > longest_len:
            longest_head = b
            longest_len = this_len

    return longest_head


def miner_server(server_ip, port):
    """
    open server conn, receive incoming tx's,
    combine into block, mine block, return block
    """
    while not break_now:

        # open server connection
        server = new_server_connection(server_ip, port)

        # receive TX list
        object_list = receive_object(server)
        for tx in object_list:
            if isinstance(tx, Tx):
                tx_list.append(tx)


def nonce_finder(wallet_list, my_address):
    """Takes tx's from tx_list, forms into block, mines block """
    # ensure nonce_finder can see same tx_list and break_now as server
    global tx_list
    global break_now
    # turn into block
    new_block = TxBlock(longest_block())
    for tx in tx_list:
        new_block.add_tx(tx)

    # extract block rewards + mining fees
    total_in, total_out = new_block.count_totals()
    fee_tx = Tx()
    fee_tx.add_output(my_address, BLOCK_REWARD + total_in - total_out)

    # add mining rewards + fees to block
    new_block.add_tx(fee_tx)

    # mine block
    new_block.get_nonce()

    # return block to wallets
    for address in wallet_list:
        send_object([new_block], address, OUT_PORT)

    break_now = True


if __name__ == "__main__":

    my_pr, my_pu = generate_keys()

    t1 = threading.Thread(target=miner_server, args=('localhost', IN_PORT))
    t2 = threading.Thread(target=nonce_finder, args=(WALLET_LIST, my_pu))

    t1.start()
    t2.start()

    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    tx1 = Tx()
    tx1.add_input(pu1, 1.1)
    tx1.add_input(pu2, 1.1)
    tx1.add_output(pu3, 2.0)
    tx1.sign(pr1)
    tx1.sign(pr2)

    tx2 = Tx()
    tx2.add_input(pu1, 2.1)
    tx2.add_input(pu2, 2.1)
    tx2.add_output(pu3, 4.0)
    tx2.sign(pr1)
    tx2.sign(pr2)

    try:
        send_object([tx1, tx2], 'localhost', IN_PORT)

    except Exception as e:
        print(e)

    server = new_server_connection('localhost', OUT_PORT)

    for i in range(10):
        new_block = receive_object(server)[0]
        if new_block:
            break
    server.close()

    if new_block.is_valid:
        print("Success, new block is valid")
    else:
        print("ERROR, new block is not valid")

    if new_block.check_nonce:
        print("Success, nonce is good")
        print(new_block)






