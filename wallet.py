from signatures import generate_keys
from transactions import Tx
from socket_utils import send_object, new_server_connection, receive_object
from txblock import TxBlock

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


send_object(tx1, 'localhost')
send_object(tx2, 'localhost')

server = new_server_connection('localhost')


for i in range(10):
    new_block = receive_object(server)
    if new_block:
        break
server.close()

if new_block.is_valid:
    print("Success, new block is valid")
else:
    print("ERROR, new block is not valid")

if new_block.get_nonce:
    print("Success, nonce is good")

for tx in new_block.data:
    if tx == tx1:
        print("tx1 is present")

    if tx == tx2:
        print("tx2 is present")





