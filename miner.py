from socket_utils import GetObject, SendObject
from transactions import Tx
from txblock import TxBlock, longest_blockchain
from signatures import generate_keys

WALLET_LIST = ['localhost']
WALLET_PORT = 5006
MINER_PORT = 5005
BLOCK_REWARD = 25.0

head_blocks = []

class Miner:

    def __init__(self):
        self.transactions = None
        self.miner_address = None

    def check_incoming(self, object_list: list[Tx]):
            for tx in object_list:
                if isinstance(tx, Tx):
                    self.transactions.append(tx)

    def create_block(self) -> TxBlock:
        """Takes tx's from self.transactions, forms into block"""
        if len(self.transactions) >= 2:
            new_block = TxBlock(longest_blockchain(head_blocks))
            for tx in self.transactions:
                new_block.add_tx(tx)
                self.transactions.remove(tx)
        return new_block


    def mine_block(self, new_block: TxBlock):
            """Mine block, remove old, longest chain and replace with new chain """
            print("Finding nonce")
            new_block.get_nonce()
            print("Found nonce!")
            if new_block.check_nonce():
                head_blocks.remove(new_block.previousBlock)
                head_blocks.append(new_block)
                return block.check_nonce()
            else:
                return False


if __name__ == "__main__":

    my_pr, my_pu = generate_keys()

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

    rec_server = GetObject()
    rec_conn = rec_server.connect('localhost', MINER_PORT)
    incoming_data = rec_server.receive_object(rec_conn)

    miner = Miner('')
    miner.check_incoming(incoming_data)
    block = miner.create_block()
    block_with_rewards = block.extract_rewards(my_pu, BLOCK_REWARD)
    if miner.mine_block(block_with_rewards):
        send_server = SendObject(block_with_rewards)
        send_conn = send_server.connect('localhost', WALLET_PORT)
        send_server.send_object(send_conn)
        print("Success, block sent to wallets")
    else:
        print("Error, nonce is invalid")








