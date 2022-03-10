from socket_utils import receive_object, new_server_connection, send_object
from transactions import Tx
from txblock import TxBlock, longest_blockchain
from signatures import generate_keys
import threading


WALLET_LIST = ['localhost']
WALLET_PORT = 5006
MINER_PORT = 5005
BLOCK_REWARD = 25.0

head_blocks = []
tx_list = []
break_now = False


class MinerServer:
    def __init__(self):
        self.open = False

    def new_connection(self, server_ip, port) -> list:
        """Open server connection and receive object"""
        try:
            server = new_server_connection(server_ip, port)
            self.open = True
            print("SUCCESS MINER SERVER STARTED")

        except Exception as e:
            print(f"ERROR STARTING MINER SERVER {e}")

        while len(object)
        object_list = receive_object(server)

        return object_list

    def add_tx(self, object_list):



def miner_server(server_ip, port):
    """ open server conn, receive incoming transactions,
    combine into block, mine block, return block
    """
    global tx_list
    global break_now

    # open server connection
    try:
        server = new_server_connection(server_ip, port)
        print("SUCCESS MINER SERVER STARTED")

    except Exception as e:
        print(f"ERROR STARTING MINER SERVER {e}")

    while not break_now:
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
    global head_blocks
    head_blocks = [None]

    # turn into block
    while not break_now:
        if tx_list:
            new_block = TxBlock(longest_blockchain(head_blocks))
            for tx in tx_list:
                new_block.add_tx(tx)
                tx_list.remove(tx)
            # extract block rewards + mining fees
            total_in, total_out = new_block.count_totals()
            fee_tx = Tx()
            fee_tx.add_output(my_address, BLOCK_REWARD + total_in - total_out)

            # add mining rewards + fees to block
            new_block.add_tx(fee_tx)

            # mine block
            print("Finding nonce")
            new_block.get_nonce()
            print("Found nonce!")
            if new_block.check_nonce():
                # return block to wallets
                for address in wallet_list:
                    send_object([new_block], address, WALLET_PORT)
                    print("New Block sent to wallet")

                head_blocks.remove(new_block.previousBlock)
                head_blocks.append(new_block)
    return True



if __name__ == "__main__":

    my_pr, my_pu = generate_keys()

    t1 = threading.Thread(target=miner_server, args=('localhost', MINER_PORT))
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
        send_object([tx1, tx2], 'localhost', MINER_PORT)

    except Exception as e:
        print(e)

    server = new_server_connection('localhost', WALLET_PORT)

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

    break_now = True




