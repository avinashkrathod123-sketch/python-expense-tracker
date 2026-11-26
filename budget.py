
import json
import math
from pathlib import Path
from datetime import datetime

BUDGET_FILE = Path(__file__).parent / "budget.json"


def load_budget():
    if not BUDGET_FILE.exists():
        return {}

    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as file:
            budgets = json.load(file)

    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading budgets: {error}")
        raise

    if not isinstance(budgets, dict):
        raise ValueError("Invalid budget data format. Expected a dictionary.")

    for month, amount in budgets.items():

        # Validate month
        try:
            parsed_month = datetime.strptime(month, "%Y-%m")

            if parsed_month.strftime("%Y-%m") != month:
                raise ValueError("Invalid month format.")

        except (ValueError, TypeError):
            raise ValueError(f"Invalid budget month: {month}")

        # Validate amount
        if (
            not isinstance(amount, (int, float))
            or isinstance(amount, bool)
            or not math.isfinite(amount)
            or amount <= 0
        ):
            raise ValueError(f"Invalid budget amount for {month}.")

    return budgets


def set_budget():
    try:
        month = input("Enter month (YYYY-MM): ").strip()

        # Validate month
        try:
            parsed_month = datetime.strptime(month, "%Y-%m")

            if parsed_month.strftime("%Y-%m") != month:
                print("Invalid month. Use YYYY-MM.")
                return

        except ValueError:
            print("Invalid month. Use YYYY-MM.")
            return

        # Get budget amount
        amount = float(input("Enter monthly budget: ₹"))

        # Validate amount
        if not math.isfinite(amount):
            print("Budget must be a valid finite number.")
            return

        if amount <= 0:
            print("Budget must be greater than zero.")
            return

        budgets = load_budget()
        budgets[month] = amount

        # Save safely using a temporary file
        temp_file = BUDGET_FILE.with_suffix(".tmp")

        try:
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(budgets, file, indent=4)
                file.flush()

            temp_file.replace(BUDGET_FILE)

        except OSError:
            print("Error: Could not save budget.")

            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass

            return

        print(f"Budget set successfully for {month}: ₹{amount:.2f}")

    except ValueError:
        print("Invalid input. Please enter a valid month and amount.")

    except OSError:
        print("Error: Could not save budget.")


def show_budget(transactions):
    month = input("Enter month (YYYY-MM): ").strip()

    # Validate month
    try:
        parsed_month = datetime.strptime(month, "%Y-%m")

        if parsed_month.strftime("%Y-%m") != month:
            print("Invalid month. Use YYYY-MM.")
            return

    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    budgets = load_budget()

    if month not in budgets:
        print(f"No budget set for {month}.")
        return

    monthly_budget = budgets[month]

    # Calculate monthly expenses
    monthly_expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "expense" and t["date"].startswith(month)
    )

    remaining = monthly_budget - monthly_expenses
    percentage = (monthly_expenses / monthly_budget) * 100

    # Display budget report
    print(f"\n--- Budget Report: {month} ---")
    print(f"Monthly Budget: ₹{monthly_budget:.2f}")
    print(f"Total Spent:   ₹{monthly_expenses:.2f}")
    print(f"Remaining:      ₹{remaining:.2f}")
    print(f"Budget Used:    {percentage:.1f}%")

    # Budget warnings
    if remaining < 0:
        print("⚠️ You have exceeded your budget!")

    elif percentage >= 80:
        print("⚠️ Warning: You have used 80% or more of your budget.")

    else:
        print("✅ You are within your budget.")
