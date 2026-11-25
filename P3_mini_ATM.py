import json
import os
from datetime import datetime

FILE_NAME = "atm_data.json"
DAILY_LIMIT = 20000


def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Data file error. Starting with default account.")

    return {
        "pin": "1234",
        "balance": 5000,
        "history": [],
        "daily_withdrawals": 0,
        "withdrawal_date": datetime.now().strftime("%Y-%m-%d"),
        "locked": False
    }


def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_transaction(transaction_type, amount):
    transaction = {
        "type": transaction_type,
        "amount": amount,
        "balance": data["balance"],
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    data["history"].append(transaction)
    save_data()


def login():
    if data["locked"]:
        print("Account is locked!")
        return False

    for attempt in range(3):
        pin = input("Enter your 4-digit ATM PIN: ")

        if pin == data["pin"]:
            print("\nLogin successful!")
            return True

        remaining = 2 - attempt
        print(f"Incorrect PIN! Attempts remaining: {remaining}")

    data["locked"] = True
    save_data()
    print("Account locked after 3 incorrect attempts!")
    return False


def check_balance():
    print(f"\nCurrent Balance: Rs. {data['balance']}")


def deposit():
    try:
        amount = int(input("Enter deposit amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

        data["balance"] += amount
        add_transaction("Deposit", amount)

        print("Deposit successful!")
        check_balance()

    except ValueError:
        print("Invalid input! Please enter a number.")


def withdraw():
    try:
        amount = int(input("Enter withdrawal amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

        today = datetime.now().strftime("%Y-%m-%d")

        if data["withdrawal_date"] != today:
            data["daily_withdrawals"] = 0
            data["withdrawal_date"] = today

        if amount > data["balance"]:
            print("Insufficient balance!")
            return

        if data["daily_withdrawals"] + amount > DAILY_LIMIT:
            print("Daily withdrawal limit exceeded!")
            return

        data["balance"] -= amount
        data["daily_withdrawals"] += amount

        add_transaction("Withdrawal", amount)

        print("Withdrawal successful!")
        check_balance()

    except ValueError:
        print("Invalid input! Please enter a number.")


def mini_statement():
    history = data["history"]

    if not history:
        print("No transactions available.")
        return

    print("\n========== MINI STATEMENT ==========")

    for transaction in history[-5:][::-1]:
        print(f"\nType: {transaction['type']}")
        print(f"Amount: Rs. {transaction['amount']}")
        print(f"Balance: Rs. {transaction['balance']}")
        print(f"Date: {transaction['date']}")

    print("\n====================================")


def change_pin():
    old_pin = input("Enter your current PIN: ")

    if old_pin != data["pin"]:
        print("Incorrect current PIN!")
        return

    new_pin = input("Enter your new 4-digit PIN: ")

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must contain exactly 4 digits!")
        return

    confirm_pin = input("Confirm your new PIN: ")

    if new_pin != confirm_pin:
        print("PIN does not match!")
        return

    data["pin"] = new_pin
    save_data()

    print("PIN changed successfully!")


def main():
    print("\n===== WELCOME TO PYTHON ATM =====")

    if not login():
        return

    while True:
        print("""
========== ATM MENU ==========
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Mini Statement
5. Change PIN
6. Exit
==============================
""")

        try:
            choice = int(input("Enter your choice: "))

        except ValueError:
            print("Invalid choice! Enter a number.")
            continue

        if choice == 1:
            check_balance()

        elif choice == 2:
            deposit()

        elif choice == 3:
            withdraw()

        elif choice == 4:
            mini_statement()

        elif choice == 5:
            change_pin()

        elif choice == 6:
            print("\nThank you for using Python ATM!")
            print("Have a nice day!")
            break

        else:
            print("Invalid choice! Select 1 to 6.")


if __name__ == "__main__":
    data = load_data()
    main()