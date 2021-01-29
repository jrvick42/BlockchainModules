

class Wallet():
    def __init__(self, currency="coins", count=100):
        self.funds = {}
        self.funds['currency'] = count

    def deposit(self, count, currency="coins"):
        try:
            starting_count = self.funds['currency']
            deposit = int(count)
            assert deposit > 0, "Deposit must be a positive value"

            self.funds['currency'] += deposit
            assert self.funds['currency'] == starting_count + \
                deposit, "An unknown error was encounder while making the deposit"

            return self.funds['currency']

        except Exception as e:
            print("Unable to make deposit due to the following circumstances ...")
            print(e)

            # Reset the funds to the starting value
            self.funds['currency'] = starting_count

    def withdrawal(self, count, currency="coins"):
        try:
            starting_count = self.funds['currency']
            withdrawal = int(count)
            assert withdrawal > 0, "Deposit must be a positive value"

            self.funds['currency'] -= withdrawal
            assert self.funds['currency'] == starting_count - \
                withdrawal, "An unknown error was encountered when making this withdrawal"

            return self.funds['currency']

        except Exception as e:
            print("Unable to make withdrawal due to the following circumstances ...")
            print(e)

            # Reset the funds to the starting value
            self.funds['currency'] = starting_count

    def getBalance(self, currency="coins"):
        return self.funds['currency']


if __name__ == "__main__":
    wallet = Wallet()
    print("Starting Balance:", str(wallet.getBalance()))

    val = wallet.deposit(0)
    print("New Balance:", str(wallet.getBalance()))

    val = wallet.deposit(50)
    print("New Balance:", str(wallet.getBalance()))

    val = wallet.withdrawal(0)
    print("New Balance:", str(wallet.getBalance()))

    val = wallet.withdrawal(25)
    print("New Balance:", str(wallet.getBalance()))
