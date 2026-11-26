
import csv
import json
import math
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "transactions.json"


def load_transactions():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r") as file:
            transactions = json.load(file)

    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading transactions: {error}")
        raise

    if not isinstance(transactions, list):
        raise ValueError("Invalid transaction data format. Expected a list.")

    required_fields = {
        "type",
        "amount",
        "category",
        "description",
        "date"
    }

    for transaction in transactions:

        # Check whether each transaction is a dictionary
        if not isinstance(transaction, dict):
            raise ValueError("Invalid transaction record.")

        # Check whether all required fields exist
        if not required_fields.issubset(transaction):
            raise ValueError("Transaction is missing required fields.")

        # Validate transaction type
        if transaction["type"] not in ("income", "expense"):
            raise ValueError("Invalid transaction type.")

        # Validate transaction amount
        amount = transaction["amount"]

        if (
            not isinstance(amount, (int, float))
            or isinstance(amount, bool)
            or not math.isfinite(amount)
            or amount <= 0
        ):
            raise ValueError("Invalid transaction amount.")

        # Validate category and description
        if (
            not isinstance(transaction["category"], str)
            or not isinstance(transaction["description"], str)
            or not transaction["category"].strip()
            or not transaction["description"].strip()
        ):
            raise ValueError("Invalid category or description.")

        # Validate date
        try:
            transaction_date = datetime.strptime(
                transaction["date"], "%Y-%m-%d"
            )

            if transaction_date.strftime("%Y-%m-%d") != transaction["date"]:
                raise ValueError("Invalid transaction date format.")

        except (ValueError, TypeError):
            raise ValueError("Invalid transaction date. Use YYYY-MM-DD.")

    return transactions


def save_transactions(transactions):
    temp_file = DATA_FILE.with_suffix(".tmp")

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)
            file.flush()

        temp_file.replace(DATA_FILE)
        return True

    except OSError:
        print("Error: Could not save transactions.")

        if temp_file.exists():
            try:
                temp_file.unlink()
            except OSError:
                pass

        return False
    
        

def add_transaction(transactions, transaction_type):
    print(f"\n--- Add {transaction_type.title()} ---")

    try:
        amount = float(input("Enter amount: ₹"))

        if not math.isfinite(amount):
            print("Amount must be a valid finite number.")
            return

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    if not category or not description:
        print("Category and description cannot be empty.")
        return

    transaction = {
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    transactions.append(transaction)

    if save_transactions(transactions):
        print(f"{transaction_type.title()} added successfully!")
    else:
        transactions.pop()
        print("Transaction was not added because saving failed.")


def view_transactions(transactions):
    print("\n--- Transaction History ---")

    if not transactions:
        print("No transactions found.")
        return

    for index, transaction in enumerate(transactions, start=1):
        print(
            f"{index}. {transaction['date']} | "
            f"{transaction['type'].title()} | "
            f"₹{transaction['amount']:.2f} | "
            f"{transaction['category']} | "
            f"{transaction['description']}"
        )


def show_summary(transactions):
    income = sum(
        t["amount"] for t in transactions if t["type"] == "income"
    )

    expenses = sum(
        t["amount"] for t in transactions if t["type"] == "expense"
    )

    balance = income - expenses

    print("\n--- Financial Summary ---")
    print(f"Total Income:  ₹{income:.2f}")
    print(f"Total Expense: ₹{expenses:.2f}")
    print(f"Balance:       ₹{balance:.2f}")


def filter_transactions(transactions):
    category = input("Enter category to search: ").strip().lower()

    results = [
        t for t in transactions
        if t["category"].lower() == category
    ]

    print("\n--- Filtered Transactions ---")
    view_transactions(results)


def delete_transaction(transactions):
    view_transactions(transactions)

    if not transactions:
        return

    try:
        choice = int(input("\nEnter transaction number to delete: "))

        if 1 <= choice <= len(transactions):
            removed = transactions.pop(choice - 1)

            if save_transactions(transactions):
                print(f"Deleted: {removed['description']}")
            else:
                transactions.insert(choice - 1, removed)
                print("Deletion failed. Original transaction restored.")

        else:
            print("Invalid transaction number.")

    except ValueError:
        print("Please enter a valid number.")


def edit_transaction(transactions):
    view_transactions(transactions)

    if not transactions:
        return

    try:
        choice = int(input("\nEnter transaction number to edit: "))

        if 1 <= choice <= len(transactions):
            transaction = transactions[choice - 1]
            original_transaction = transaction.copy()

            print("\nLeave a field blank to keep its current value.")

            new_amount = input(
                f"Amount [{transaction['amount']}]: "
            ).strip()

            new_category = input(
                f"Category [{transaction['category']}]: "
            ).strip()

            new_description = input(
                f"Description [{transaction['description']}]: "
            ).strip()

            if new_amount:
                try:
                    amount = float(new_amount)

                    if not math.isfinite(amount):
                        print("Amount must be a valid finite number.")
                        return

                    if amount <= 0:
                        print("Amount must be greater than zero.")
                        return

                    transaction["amount"] = amount

                except ValueError:
                    print("Please enter a valid amount.")
                    return

            if new_category:
                transaction["category"] = new_category

            if new_description:
                transaction["description"] = new_description

            if save_transactions(transactions):
                print("Transaction updated successfully!")
            else:
                transactions[choice - 1] = original_transaction
                print("Edit cancelled because saving failed. Original transaction restored.")
            print("Invalid transaction number.")

    except ValueError:
        print("Please enter a valid number.")


def monthly_summary(transactions):
    month = input("Enter month (YYYY-MM), e.g. 2026-11: ").strip()

    if len(month) != 7 or month[4] != "-":
        print("Invalid format. Use YYYY-MM.")
        return

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month.")
        return

    monthly_transactions = [
        t for t in transactions if t["date"].startswith(month)
    ]

    income = sum(
        t["amount"] for t in monthly_transactions
        if t["type"] == "income"
    )

    expenses = sum(
        t["amount"] for t in monthly_transactions
        if t["type"] == "expense"
    )

    print(f"\n--- Summary for {month} ---")
    print(f"Income:  ₹{income:.2f}")
    print(f"Expense: ₹{expenses:.2f}")
    print(f"Balance: ₹{income - expenses:.2f}")
    print(f"Transactions: {len(monthly_transactions)}")


def export_transactions(transactions):
    if not transactions:
        print("No transactions to export.")
        return

    csv_file = Path(__file__).parent / "transactions.csv"

    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "date",
                    "type",
                    "amount",
                    "category",
                    "description"
                ]
            )

            writer.writeheader()
            writer.writerows(transactions)

        print(f"\nTransactions exported successfully!")
        print(f"File saved at: {csv_file}")

    except OSError:
        print("Error: Could not export transactions.")
        