import sys

class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def authenticate(self, user_id, pin):
        return self.user_id == user_id and self.pin == pin

class ATM:
    def __init__(self):
        self.users = []
        self.current_user = None

    def add_user(self, user):
        self.users.append(user)

    def authenticate_user(self, user_id, pin):
        for user in self.users:
            if user.authenticate(user_id, pin):
                self.current_user = user
                return True
        return False

    def transaction_history(self):
        if self.current_user:
            return self.current_user.transaction_history
        else:
            return None

    def withdraw(self, amount):
        if self.current_user:
            if amount <= 0:
                return "Amount must be positive."
            if amount <= self.current_user.balance:
                self.current_user.balance -= amount
                self.current_user.transaction_history.append(f"Withdraw: -${amount}")
                return f"Successfully withdrew ${amount}"
            else:
                return "Insufficient balance."
        else:
            return "No user authenticated."

    def deposit(self, amount):
        if self.current_user:
            if amount <= 0:
                return "Amount must be positive."
            self.current_user.balance += amount
            self.current_user.transaction_history.append(f"Deposit: +${amount}")
            return f"Successfully deposited ${amount}"
        else:
            return "No user authenticated."

    def transfer(self, target_user_id, amount):
        if self.current_user:
            if amount <= 0:
                return "Amount must be positive."
            target_user = next((user for user in self.users if user.user_id == target_user_id), None)
            if target_user and self.current_user.balance >= amount:
                self.current_user.balance -= amount
                target_user.balance += amount
                self.current_user.transaction_history.append(f"Transfer: -${amount} to User {target_user_id}")
                target_user.transaction_history.append(f"Transfer: +${amount} from User {self.current_user.user_id}")
                return f"Successfully transferred ${amount} to User {target_user_id}"
            elif not target_user:
                return "Target user not found."
            else:
                return "Insufficient balance."
        else:
            return "No user authenticated."

    def quit(self):
        self.current_user = None
        return "Logged out successfully."

def main():
    atm = ATM()

    # Sample Users
    user1 = User(user_id="user1", pin="1234", balance=1000)
    user2 = User(user_id="user2", pin="5678", balance=2000)
    atm.add_user(user1)
    atm.add_user(user2)

    print("Welcome to the ATM")
    user_id = input("Enter your User ID: ").strip()
    pin = input("Enter your PIN: ").strip()

    if atm.authenticate_user(user_id, pin):
        print("Authentication successful!")

        while True:
            print("\nOptions:")
            print("1. Transaction History")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer")
            print("5. Quit")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                history = atm.transaction_history()
                if history:
                    print("Transaction History:")
                    for transaction in history:
                        print(transaction)
                else:
                    print("No transactions found.")
            elif choice == '2':
                try:
                    amount = float(input("Enter amount to withdraw: ").strip())
                    message = atm.withdraw(amount)
                    print(message)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            elif choice == '3':
                try:
                    amount = float(input("Enter amount to deposit: ").strip())
                    message = atm.deposit(amount)
                    print(message)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            elif choice == '4':
                target_user_id = input("Enter target User ID: ").strip()
                try:
                    amount = float(input("Enter amount to transfer: ").strip())
                    message = atm.transfer(target_user_id, amount)
                    print(message)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            elif choice == '5':
                message = atm.quit()
                print(message)
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
    else:
        print("Authentication failed. Please check your User ID and PIN.")

if __name__ == "__main__":
    main()
