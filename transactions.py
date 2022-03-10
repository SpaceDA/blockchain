import signatures


class Tx:
    inputs = None
    outputs = None
    sig = None
    reqd = None
    reqd_input = None

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []
        self.reqd_input = []
        self.msgs = []

    def add_input(self, from_addr, amount):
        # check if address has reqd input pending
        found_ind = -1
        for ind, tpl in enumerate(self.reqd_input):
            addr_reqd, amount_reqd = tpl[0], tpl[1]
            if addr_reqd == from_addr and amount_reqd == amount:
                found_ind = ind
        if found_ind != -1:
            del self.reqd_input[found_ind]
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append((addr))

    def add_reqd_input(self, addr, amount):
        self.reqd_input.append((addr, amount))

    def sign(self, private):
        message = self.__gather()
        newsig = signatures.sign(message, private)
        self.sigs.append((newsig, message))

    def is_valid(self):
        in_amounts = 0
        out_amounts = []
        for addr, amount in self.inputs:
            found = False
            in_amounts += amount
            for sig, message in self.sigs:
                if signatures.verify(message, sig, addr):
                    found = True
                    break
            if not found:
                return False
            if amount < 0:
                return False

        for addr in self.reqd:
            found = False
            for sig, message in self.sigs:
                if signatures.verify(message, sig, addr):
                    found = True
                    break
            if not found:
                return False

        for addr, amount in self.outputs:
            out_amounts.append(amount)
            if amount < 0:
                return False

            if self.reqd_input:
                first_out_amount = out_amounts[0]
                for amt in out_amounts:
                    if amt != first_out_amount:
                        print("ERROR, Out > in or outputs do not agree")
                        return False

        for addr, amount in self.reqd_input:
            out_amounts.append(amount)
            if amount < 0:
                return False

        return True

    def __gather(self):
        message = [self.inputs.copy(), self.outputs.copy(), self.reqd.copy(), self.reqd_input.copy()]
        self.msgs.append(message)
        return message

    def __repr__(self):
        reprstr = "//START//\nINPUTS:\n"
        for addr, amt in self.inputs:
            reprstr = f"{reprstr} {str(amt)} from + {str(addr)} \n"
        reprstr = reprstr + "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr = f"{reprstr} {str(amt)} to + {str(addr)} \n"
        reprstr = reprstr + "REQD INPUTS:\n"
        for addr, amt in self.reqd_input:
            reprstr += f"{str(amt)} from {str(addr)}"
            reprstr += "REQD SIGS:\n"
        for r in self.reqd:
            reprstr = f"{reprstr} {str(r)}\n"
        reprstr = reprstr + "SIGS:\n"
        for s in self.sigs:
            reprstr = f"{reprstr} {str(s)}\n"
        return reprstr + "//END//"


if __name__ == "__main__":
    pr1, pu1 = signatures.generate_keys()
    pr2, pu2 = signatures.generate_keys()
    pr3, pu3 = signatures.generate_keys()
    pr4, pu4 = signatures.generate_keys()

    tx1 = Tx()
    tx1.add_input(pu1, 2)
    tx1.add_output(pu2, 2)
    tx1.sign(pr1)


    tx2 = Tx()
    tx2.add_input(pu1, 2)
    tx2.add_output(pu2, 1)
    tx2.add_output(pu3, 1)
    tx2.sign(pr1)

    tx3 = Tx()
    tx3.add_input(pu3, 1.2)
    tx3.add_output(pu1, 1.1)
    tx3.add_reqd(pu4)
    tx3.sign(pr3)
    tx3.sign(pr4)

    # two inputs
    tx11 = Tx()
    tx11.add_input(pu1, 3)
    tx11.add_output(pu3, 6)
    tx11.add_reqd_input(pu2, 3)
    tx11.sign(pr1)
    tx11.add_input(pu2, 3)
    tx11.add_output(pu3, 6)
    tx11.sign(pr2)





    for t in [tx1, tx2, tx3, tx11]:
        if t.is_valid():
            print("Success, Tx is valid")
        else:
            print("Tx is invalid")

    # wrong signature
    tx4 = Tx()
    tx4.add_input(pu1, 2)
    tx4.add_output(pu2, 1)
    tx4.add_output(pu3, 1)
    tx4.sign(pr2)

    # escrow not signed by arbiter
    tx5 = Tx()
    tx5.add_input(pu3, 1.2)
    tx5.add_output(pu1, 1.1)
    tx5.add_reqd(pu4)
    tx5.sign(pr3)


    # two inputs, only one sig
    tx6 = Tx()
    tx6.add_input(pu3, 1.2)
    tx6.add_input(pu4, 1.2)
    tx6.add_output(pu1, 2.4)
    tx6.sign(pr3)

    # outputs exceed inputs
    tx7 = Tx()
    tx7.add_input(pu3, 1.2)
    tx7.add_output(pu4, 0.2)
    tx7.add_output(pu1, 1.1)
    tx7.sign(pr3)

    # negative coins

    tx8 = Tx()
    tx8.add_input(pu2, -1)
    tx8.add_output(pu1, -1)
    tx8.sign(pr2)

    # modify tx after sig
    tx9 = Tx()
    tx9.add_input(pu1, 2)
    tx9.add_output(pu2, 2)
    tx9.sign(pr1)
    tx9.outputs[0] = (pu3, 2)

    # outputs tampered
    tx10 = Tx()
    tx10.add_input(pu1, 2)
    tx10.add_output(pu2, 2)
    tx10.sign(pr1)
    tx10.outputs[0] = (pu3, 2)
    tx10.sign(pr3)


    for t in [tx4, tx5, tx6, tx7, tx8, tx9]:
        if t.is_valid():
            print("ERROR.  Bad Tx is valid")
        else:
            print(f"Success! Bad TX is invalid")








