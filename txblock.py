from blockchain import CBlock
from signatures import generate_keys, sign
from transactions import Tx
import pickle
from cryptography.hazmat.primitives import hashes
from time import time
from random import randint


reward = 25.0

leading_zeroes = 2
next_char_limit = 50


class TxBlock(CBlock):
    nonce = None

    def __init__(self, previousBlock):
        super().__init__([], previousBlock)

    def add_tx(self, tx_in):
        self.data.append(tx_in)

    def __count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr, amt in tx.inputs:
                total_in += amt
            for addr, amt in tx.outputs:
                total_out += amt
        return total_in, total_out

    def is_valid(self):
        if not self.previousBlock:
            return True
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        total_in, total_out = self.__count_totals()
        if total_out - total_in - reward > 0.00000000001:
            return False

        return True

    def check_nonce(self):
        """Check (hashed nonce + hashed data + hased previous block's hash) for correct # of leading zeroes"""
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previousBlock), 'utf-8'))
        digest.update(bytes(str(self.nonce), 'utf-8'))
        current_hash = digest.finalize()

        if current_hash[:leading_zeroes] != bytes(''.join(['\x00' for i in range(leading_zeroes)]), 'utf-8'):
            return False
        return int(current_hash[leading_zeroes]) < next_char_limit

    def get_nonce(self):
        """Generates random nonce to check feed check_nonce """
        for i in range(1000000):
            self.nonce = "".join([
                chr(randint(0, 255)) for i in range(10*leading_zeroes)
            ])
            if self.check_nonce():
                return self.nonce
        return None




if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()
    pr4, pu4 = generate_keys()

    tx1 = Tx()
    tx1.add_input(pu1, 1)
    tx1.add_output(pu2, 1)
    tx1.sign(pr1)

    message = b"Test message"
    sig = sign(message, pr1)

    if tx1.is_valid():
        print("Success, Tx is valid")


    with open("save.dat", "wb") as savefile:
        pickle.dump(tx1, savefile)

    with open("save.dat", "rb") as loadfile:
        new_tx = pickle.load(loadfile)

    if new_tx.is_valid():
        print("Success, loaded Tx is valid")


    root = TxBlock(None)
    root.add_tx((tx1))

    tx2 = Tx()
    tx2.add_input(pu2, 1.1)
    tx2.add_output(pu3, 1)
    tx2.sign(pr2)
    root.add_tx(tx2)

    B1 = TxBlock(root)

    tx3 = Tx()
    tx3.add_input(pu3, 1.1)
    tx3.add_output(pu1, 1)
    tx3.sign(pr3)
    B1.add_tx(tx3)

    tx4 = Tx()
    tx4.add_input(pu1, 1)
    tx4.add_output(pu2, 1)
    tx4.add_reqd(pu3)
    tx4.sign(pr1)
    tx4.sign(pr3)
    B1.add_tx(tx4)

    # check mining time
    start = time()
    B1.get_nonce()
    stop = time()
    print(f"Time to mine is {stop - start}")

    #print and check hash w/ nonce

    if B1.check_nonce():
        print("Success, nonce is good")
    else:
        print("ERROR, nonce is not good")


    with open("block.dat", "wb") as savefile:
        pickle.dump(B1, savefile)

    with open("block.dat", "rb") as loadfile:
        load_B1 = pickle.load(loadfile)

    if load_B1.check_nonce():
        print("Success, nonce is good after load")
    else: print("ERROR, nonce is not good after load")


    for b in [root, B1, load_B1, load_B1.previousBlock]:
        if b.is_valid():
            print("Success, valid block")
        else:
            print("Error, bad block")


    B2 = TxBlock(B1)
    tx5 = Tx()
    tx5.add_input(pu3, 1)
    tx5.add_output(pu1, 100)
    tx5.sign(pr3)
    B2.add_tx(tx5)

    load_B1.previousBlock.add_tx(tx4)

    for b in [B2, load_B1]:
        if b.is_valid():
            print("Error, bad block verified")
        else:
            print("Success, bad block detected")
    #test mining rewards
    B3 = TxBlock(B2)
    B3.add_tx(tx2)
    B3.add_tx(tx3)
    B3.add_tx(tx4)
    tx6 = Tx()
    tx6.add_output(pu4, 25)
    if B3.is_valid():
        print("Success, block reward good")
    else:
        print("ERROR, block reward fail")

    #test tx fees
    B4 = TxBlock(B3)
    B4.add_tx(tx2)
    B4.add_tx(tx3)
    B4.add_tx(tx4)
    tx7 = Tx()
    tx7.add_output(pu4, 25.2)
    if B4.is_valid():
        print("Success, tx fee good")
    else:
        print("ERROR, tx fee fail")

    #greedy miner
    B5 = TxBlock(B4)
    B5.add_tx(tx2)
    B5.add_tx(tx3)
    B5.add_tx(tx4)
    tx8 = Tx()
    tx8.add_output(pu4, 26.2)
    B5.add_tx(tx8)
    if not B5.is_valid():
        print("Success, greedy miner detected")
    else:
        print("ERROR, greedy miner not detected")

