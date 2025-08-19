import datetime

# User database with ghost names and initial data
users_db = {
    'Sydnor Nana Adwoa': {
        'pin': '1234',
        'balance': 500.00,
        'transactions': [],
    },
    'Kwabena KB': {
        'pin': '4199',
        'balance': 5200.00,
        'transactions': [],
    },
    'Mark Anim': {
        'pin': '5678',
        'balance': 1500.00,
        'transactions': [],
    },
    'Efua Kobi': {
        'pin': '9012',
        'balance': 75.00,
        'transactions': [],
    },
    'Gifty Dannah': {
        'pin': '8653',
        'balance': 6450.00,
        'transactions': [],
    }
}

daily_withdrawal_limit = 10000.00

def check_balance(user_data):
    """Displays the user's current balance."""
    print(f"\nYour current balance is: GHS{user_data['balance']:.2f}")

def deposit_money(user_data):
    """Handles depositing money into the account."""
    try:
        amount = float(input("Enter amount to deposit: GHS"))
        if amount > 0:
            user_data['balance'] += amount
            # This record the transaction
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_data['transactions'].append({
                'type': 'Deposit',
                'amount': amount,
                'balance': user_data['balance'],
                'timestamp': timestamp
            })
            print("\nDeposit successful!")
            generate_receipt(user_data['transactions'][-1])
        else:
            print("Invalid amount. Please enter a positive number.") # Takes care of the edge cases.
    except ValueError:
        print("Invalid input. Please enter a number.") # Takes care of value error

def withdraw_money(user_data):
    """Handles withdrawing money from the account with a daily limit."""
    try:
        amount = float(input("Enter amount to withdraw: GHS"))
        
        # Calculate daily withdrawal total
        today = datetime.date.today().strftime("%Y-%m-%d") # Use to check daily withdrawal limit.
        daily_withdrawal_total = sum(
            t['amount'] for t in user_data['transactions']
            if t['type'] == 'Withdrawal' and t['timestamp'].startswith(today)
        ) # This sums up the total transactions for today and used to check withdrawal limit.
        
        if amount <= 0:
            print("Invalid amount. Please enter a positive number.") #Checks edge case if the user inputs a negative number or zero
        elif user_data['balance'] < amount:
            print("Insufficient funds.")
        elif daily_withdrawal_total + amount > daily_withdrawal_limit:
            remaining_limit = daily_withdrawal_limit - daily_withdrawal_total
            print(f"Daily withdrawal limit of GHS{daily_withdrawal_limit:.2f} exceeded. You can still withdraw up to GHS{remaining_limit:.2f} today.")
        else:
            user_data['balance'] -= amount
            # Record the transaction
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_data['transactions'].append({
                'type': 'Withdrawal',
                'amount': amount,
                'balance': user_data['balance'],
                'timestamp': timestamp
            })
            print("\nWithdrawal successful!")
            generate_receipt(user_data['transactions'][-1])
            
    except ValueError:
        print("Invalid input. Please enter a number.")


def show_transaction_history(user_data):
    """Displays the user's transaction history."""
    if not user_data['transactions']:
        print("No transactions yet.")
        return

    print("\n--- Transaction History ---")
    for transaction in user_data['transactions']:
        print(f"Type: {transaction['type']}")
        print(f"Amount: GHS{transaction['amount']:.2f}")
        print(f"Balance: GHS{transaction['balance']:.2f}")
        print(f"Date: {transaction['timestamp']}")
        print("---------------------------")

def generate_receipt(transaction):
    """Prints a formatted receipt for a transaction."""
    print("\n--------------------------")
    print("      ATM RECEIPT")
    print(f"Transaction: {transaction['type']}")
    print(f"Amount: GHS{transaction['amount']:.2f}")
    print(f"Balance: GHS{transaction['balance']:.2f}")
    print(f"Date: {transaction['timestamp'].split(' ')[0]}")
    print("--------------------------\n")

def show_menu():
    """Displays the main menu options."""
    print("\n--- ATM Main Menu ---")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Transaction History")
    print("5. Exit")
    return input("Enter your choice (1-5): ")

def main():
    while True:
        """This code runs first and calls the rest of the functions"""
        # This is the User Authentication section
        user_name = input("Please enter your name: ").strip() # The strip functions checks for edge cases were the user types a space before or after their name
        pin = input("Input your pin number: ")

        if user_name in users_db and users_db[user_name]['pin'] == pin:
            print("\nWelcome, {user_name}!")
            current_user = users_db[user_name]
            break
        else:
            print("Invalid name or PIN. Please try again.")

    while True:
        choice = show_menu()
        if choice == '1':
            check_balance(current_user)
        elif choice == '2':
            deposit_money(current_user)
        elif choice == '3':
            withdraw_money(current_user)
        elif choice == '4':
            show_transaction_history(current_user)
        elif choice == '5':
            print("Get out of here!")
            break
        else:
            print("Invalid. Please select a number from the menu.")

if __name__ == '__main__':
    main()