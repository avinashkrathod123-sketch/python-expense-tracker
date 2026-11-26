from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from tracker import (
    export_transactions,
    load_transactions,
    add_transaction,
    view_transactions,
    show_summary,
    filter_transactions,
    delete_transaction,
    edit_transaction,
    monthly_summary
)

from budget import (
    set_budget,
    load_budget,
    show_budget
)


console = Console()


def show_dashboard(transactions):
    total_income = sum(
        t["amount"] for t in transactions
        if t["type"] == "income"
    )

    total_expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "expense"
    )

    balance = total_income - total_expenses

    current_month = datetime.now().strftime("%Y-%m")
    budgets = load_budget()
    current_budget = budgets.get(current_month, 0)

    dashboard = Table.grid(expand=True)
    dashboard.add_column(justify="center")
    dashboard.add_column(justify="center")
    dashboard.add_column(justify="center")

    dashboard.add_row(
        Text(f"INCOME\n₹{total_income:,.2f}", style="bold green"),
        Text(f"EXPENSES\n₹{total_expenses:,.2f}", style="bold red"),
        Text(f"BALANCE\n₹{balance:,.2f}", style="bold cyan")
    )

    if current_budget:
        dashboard.add_row(
            Text(f"\nMONTHLY BUDGET\n₹{current_budget:,.2f}", style="bold yellow"),
            Text(f"TRANSACTIONS\n{len(transactions)}", style="bold magenta"),
            Text(f"MONTH\n{current_month}", style="bold white")
        )

    console.print(
        Panel(
            dashboard,
            title="[bold white]💰 EXPENSE TRACKER[/bold white]",
            subtitle="[dim]Personal Finance Manager[/dim]",
            border_style="cyan",
            padding=(0, 1)
        )
    )

def show_menu():
    menu = Table(
        title="MAIN MENU",
        border_style="blue",
        header_style="bold cyan",
        show_lines=False,
        expand=True
    )

    menu.add_column("No.", style="bold yellow", justify="center", width=5)
    menu.add_column("Action", style="white")
    menu.add_column("No.", style="bold yellow", justify="center", width=5)
    menu.add_column("Action", style="white")

    menu.add_row("1", "Add Income", "7", "Edit")
    menu.add_row("2", "Add Expense", "8", "Monthly Summary")
    menu.add_row("3", "Transactions", "9", "Export CSV")
    menu.add_row("4", "Financial Summary", "10", "Set Budget")
    menu.add_row("5", "Category Search", "11", "View Budget")
    menu.add_row("6", "Delete", "12", "Exit")
    console.print(menu)

def main():
    transactions = load_transactions()

    while True:
        console.clear()

        show_dashboard(transactions)
        show_menu()

        choice = console.input(
            "\n[bold cyan]Choose an option (1-12): [/bold cyan]"
        ).strip()

        if choice == "1":
            add_transaction(transactions, "income")

        elif choice == "2":
            add_transaction(transactions, "expense")

        elif choice == "3":
            view_transactions(transactions)

        elif choice == "4":
            show_summary(transactions)

        elif choice == "5":
            filter_transactions(transactions)

        elif choice == "6":
            delete_transaction(transactions)

        elif choice == "7":
            edit_transaction(transactions)

        elif choice == "8":
            monthly_summary(transactions)

        elif choice == "9":
            export_transactions(transactions)

        elif choice == "10":
            set_budget()

        elif choice == "11":
            show_budget(transactions)

        elif choice == "12":
            console.print(
                Panel(
                    "[bold green]Thank you for using Expense Tracker![/bold green]\n"
                    "[white]Your transactions have been saved.[/white]",
                    border_style="green"
                )
            )
            break

        else:
            console.print("[bold red]Invalid choice. Select from 1 to 12.[/bold red]")

        if choice != "12":
            console.input("\n[dim]Press Enter to return to the dashboard...[/dim]")


if __name__ == "__main__":
    main()
