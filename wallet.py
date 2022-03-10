from signatures import generate_keys
from transactions import Tx
from socket_utils import send_object, new_server_connection, receive_object
from txblock import TxBlock, longest_blockchain, enumerate_blockchain
import threading
import time
from miner import miner_server, nonce_finder, break_now

WALLET_PORT = 5006
MINER_PORT = 5005
WALLET_LIST = ['localhost']
break_now = False
head_blocks = []


class Server:
    def __init__(self):
        self.open = False

    def listen(self, ip, port):
        """Create server connection, receive objects"""
        try:
            server = new_server_connection(ip, port)
            print("WALLET SERVER CONNECTED")
            self.open = True
        except Exception as e:
            print(f"ERROR CONNECTING WALLET SERVER: {e}")
        while self.open:
            # receive TX list
            object_list = receive_object(server)


class MessageHandler:

    def message_in(self, object_list: list):
        pass

    def message_out(self, ):



MessageHandler.message_in(Server.listen)



def wallet_server(wallet_ip, port):
    """open a socket, receive incoming blocks, pass to check_blocks for placement on head_blocks"""
    global head_blocks
    global break_now

    head_blocks = []

    # open server connection
    try:
        server = new_server_connection(wallet_ip, port)
        print("WALLET SERVER CONNECTED")
    except Exception as e:
        print(f"ERROR CONNECTING WALLET SERVER: {e}")
    while not break_now:
        # receive TX list
        object_list = receive_object(server)
        for i, block in enumerate(object_list):
            if isinstance(block, TxBlock):
                print(f"WALLET RECEIVED BLOCK {i+1}/{len(object_list)}: {block}")
                check_blocks(block)


def check_blocks(new_block):
    """check blocks for placement in head blocks by comparing previousHash and hash of current blocks"""
    print("check blocks executing")
    if not head_blocks and new_block.is_valid():
        new_block.previousBlock = None
        head_blocks.append(new_block)

    elif not new_block.is_valid():
        print("ERROR, new_block is not valid")

    else:
        for b in head_blocks:
            print("PROCESSING BLOCK...")
            if not new_block.is_valid():
                print("ERROR, new_block is not valid")
            else:
                print("NEW BLOCK IS VALID")
                b.compute_hash == new_block.previousHash
                new_block.previousBlock = b
                head_blocks.remove(b)
                head_blocks.append(new_block)
                print(head_blocks)


def check_balance(public_key):
    long_chain = enumerate_blockchain(longest_blockchain())
    bal = 0.0
    for block in long_chain:
        for tx in block.data:
            for addr, amt in tx.inputs:
                if addr == public_key:
                    bal -= amt
            for addr, amt in tx.outputs:
                if addr == public_key:
                    bal += amt
    return bal

    long_chain = longest_blockchain(head_blocks)
    this_block = long_chain

    while this_block != None:
        for tx in this_block.data:
            for addr, amt in tx.inputs:
                if addr == public_key:
                    bal -= amt
            for addr, amt in tx.outputs:
                if addr == public_key:
                    bal += amt
        this_block = this_block.previousBlock
    return bal


def send_coins(sender_public, sender_amt, sender_private, rec_public, rec_amt):
    tx = Tx()
    tx.add_input(sender_public, sender_amt)
    tx.add_output(rec_public, rec_amt)
    tx.sign(sender_private)
    try:
        send_object([tx], 'localhost')
        print(f"Suceesfully sent {rec_amt} coins from {sender_public} to {rec_public}")
    except Exception as e:
        print(f"ERROR SENDING COINS TO MINER SERVER {e}")

    return None


if __name__ == "__main__":

    miner_pr, miner_pu = generate_keys()

    t1 = threading.Thread(target=miner_server, args=('localhost', MINER_PORT))
    t2 = threading.Thread(target=nonce_finder, args=(WALLET_LIST, miner_pu))
    t3 = threading.Thread(target=wallet_server, args=('localhost', WALLET_PORT))

    t1.start()
    t2.start()
    t3.start()

    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    # check account balances
    bal1 = check_balance(pu1)

    bal2 = check_balance(pu2)

    bal3 = check_balance(pu3)

    # send coins
    send_coins(pu1, 1.0, pr1, pu2, 1.0)
    send_coins(pu1, 1.0, pr1, pu2, 0.3)

    time.sleep(30)

    # re-check balances
    new_bal1 = check_balance(pu1)
    print(f"New bal 1 {new_bal1}")
    new_bal2 = check_balance(pu2)
    print(f"New bal 2 {new_bal2}")
    new_bal3 = check_balance(pu3)
    print(f"New bal 3 {new_bal3}")

    print(f"HEAD BLOCKS = {head_blocks}")


    #re-verify balances

    if abs(bal1 - new_bal1 + 1.3) > 0.00000001:
        print("ERROR, wrong balance for pu1")
    else:
        print("Success, good balance for pu1")

    if abs(bal2 - new_bal2 - 1.0) > 0.00000001:
        print("ERROR, wrong balance for pu2")
    else:
        print("Success, good balance for pu2")

    if abs(bal3 - new_bal3 - 0.3) > 0.00000001:
        print("ERROR, wrong balance for pu3")
    else:
        print("Success, good balance for pu3")



    t1.join()
    t2.join()
    t3.join()

    print("Exit successful")



