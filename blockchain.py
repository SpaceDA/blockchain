from cryptography.hazmat.primitives import hashes


class SomeBlock:
    def __init__(self, mystring):
        self.string = mystring

    def __repr__(self):
        return self.string


class CBlock:
    data = None
    previousHash = None
    previousBlock = None

    def __init__(self, data, previousBlock):
        self.previousBlock = previousBlock
        self.data = data
        if previousBlock is not None:
            self.previousHash = previousBlock.compute_hash()

    def __repr__(self):
        if self.previousBlock is not None:
            return "Prev Block: " + str(self.previousBlock) + "\n" + "Prev Hash: " + str(self.previousHash) + "\n" + "Current block: " + str(self.data)
        else:
            return "Prev Block: " + str(self.previousBlock) + "\n" + str(self.data)

    def compute_hash(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data), 'utf-8'))
        if self.previousBlock is not None:
            digest.update(self.previousHash)
        return digest.finalize()

    def is_valid(self):
        if not self.previousBlock:
            return True
        return self.previousBlock.compute_hash() == self.previousHash


if __name__ == "__main__":
    root = CBlock("I am root", None)
    B1 = CBlock("I am child", root)
    B2 = CBlock("I am B1's brother", root)
    B3 = CBlock(12345, B1)
    B4 = CBlock(SomeBlock("Hello there!"), B3)
    B5 = CBlock("Top block", B4)

    for block in [B1, B2, B3, B4, B5]:
        if block.previousBlock.compute_hash() == block.previousHash:
            print("SUCCESS! Hash is good!")
        else:
            print("ERROR, Hash is bad")


    B3.data = "This is an attack"

    digest = hashes.Hash(hashes.SHA256())
    digest.update(bytes(str(B3.data), 'utf-8'))
    digest.update(B3.previousHash)
    fake_hash = digest.finalize()

    B4.previousHash = fake_hash


    if B4.previousBlock.compute_hash() == B4.previousHash:
        print("Error, tampering not detected!")
    else:
        print("Success, tampering detected!")






