"""
Abstraction means hiding the unnecessary details from the user and showing only the essential features.
"""

class Payment:
    def pay_with_card(self, amount):
        # print(f"Paid ${amount} using Card.")
        print(f"Processing card payment of ${amount}...")


    def pay_with_upi(self, amount):
        # print(f"Paid ${amount} using UPI.")
        print(f"Processing UPI payment of ${amount}...")

    def pay_with_cash(self, amount):
        # print(f"Paid ${amount} using Cash.")
        print(f"Processing cash payment of ${amount}...")

p = Payment()
p.pay_with_card(100)
p.pay_with_upi(200)
p.pay_with_cash(300)

