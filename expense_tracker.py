#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import csv

# Define the paths for the expenses and budget JSON files
EXPENSES_FILE: str = 'expenses.json'
BUDGET_FILE: str = 'budget.json'


# Initialization functions
def initialize_expenses_file() -> None:
    """
    Initialize the expenses JSON file if it doesn't exist.
    Creates an empty list in the JSON file to store expenses.
    """
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'w') as file:
            json.dump([], file)  # Start with an empty list of expenses


def initialize_budget_file() -> None:
    """
    Initialize the budget JSON file if it doesn't exist.
    Sets an initial monthly budget to zero.
    """
    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'w') as file:
            json.dump({"monthly_budget": 0}, file)


# Load and save functions
def load_expenses() -> List[Dict[str, Any]]:
    """
    Load expenses from the JSON file.
    Returns a list of expenses.
    If the JSON file is empty or contains invalid JSON, it initializes an empty list.
    """
    try:
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # If JSON is invalid or file is not found, return an empty list
        return []


def save_expenses(expenses: List[Dict[str, Any]]) -> None:
    """
    Save expenses to the JSON file.
    Overwrites the file with the provided list of expenses.
    """
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)


def load_budget() -> float:
    """
    Load the monthly budget from the JSON file.
    Returns the monthly budget amount.
    """
    try:
        with open(BUDGET_FILE, 'r') as file:
            return json.load(file).get("monthly_budget", 0)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0


def save_budget(monthly_budget: float) -> None:
    """
    Save the monthly budget to the JSON file.
    """
    with open(BUDGET_FILE, 'w') as file:
        json.dump({"monthly_budget": monthly_budget}, file)


# Expense functions
def add_expense(description: str, amount: float, category: Optional[str] = None) -> None:
    """
    Add a new expense with a description, amount, and optional category.
    Assigns a unique ID and records the current date and time.
    """
    expenses = load_expenses()
    new_id = max((expense['id'] for expense in expenses), default=0) + 1
    new_expense = {
        "id": new_id,
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category if category else "Uncategorized"
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")
    check_budget()


def list_expenses(category: Optional[str] = None, start_date: Optional[str] = None,
                  end_date: Optional[str] = None) -> None:
    """
    List all expenses, filter by category, or by a date range.
    Displays the ID, date, description, amount, and category for each expense.
    """
    expenses = load_expenses()

    if category:
        expenses = [expense for expense in expenses if expense.get('category') == category]

    if start_date:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        expenses = [expense for expense in expenses if
                    datetime.strptime(expense['date'], "%Y-%m-%d %H:%M:%S") >= start_date_obj]

    if end_date:
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        expenses = [expense for expense in expenses if
                    datetime.strptime(expense['date'], "%Y-%m-%d %H:%M:%S") <= end_date_obj]

    if not expenses:
        print_no_expenses_message(category)
    else:
        print(f"{'ID':<5} {'Date':<20} {'Description':<30} {'Amount':<10} {'Category':<20}")
        print("-" * 90)
        for expense in expenses:
            print(f"{expense['id']:<5} {expense['date']:<20} {expense['description']:<30} "
                  f"${expense['amount']:<10.2f} {expense['category']:<20}")


def delete_expense(expense_id: int) -> None:
    """
    Delete an expense by ID.
    Removes the expense with the given ID from the list and updates the JSON file.
    """
    expenses = load_expenses()
    updated_expenses = [expense for expense in expenses if expense['id'] != expense_id]
    if len(updated_expenses) == len(expenses):
        print(f"No expense found with ID: {expense_id}")
    else:
        save_expenses(updated_expenses)
        print(f"Expense with ID {expense_id} deleted successfully.")


def update_expense(expense_id: int, description: str = None, amount: float = None, category: Optional[str] = None) \
        -> None:
    """
    Update an existing expense by ID.
    Allows updating the description, amount, category, or all for the specified expense.
    """
    expenses = load_expenses()
    for expense in expenses:
        if expense['id'] == expense_id:
            if description:
                expense['description'] = description
            if amount:
                expense['amount'] = amount
            if category:
                expense['category'] = category
            expense['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Update date to current time
            save_expenses(expenses)
            print(f"Expense with ID {expense_id} updated successfully.")
            return
    print(f"No expense found with ID: {expense_id}")


def show_summary(month: int = None) -> None:
    """
    Show a summary of expenses.
    If a month is provided, shows the summary for that month of the current year.
    Otherwise, shows the total summary of all expenses.
    """
    expenses = load_expenses()
    total = 0.0
    current_year = datetime.now().year

    for expense in expenses:
        expense_date = datetime.strptime(expense['date'], "%Y-%m-%d %H:%M:%S")
        if month and expense_date.month == month and expense_date.year == current_year:
            total += expense['amount']
        elif not month:
            total += expense['amount']

    if month:
        print(f"Total expenses for {datetime(1900, month, 1).strftime('%B')}: ${total:.2f}")
    else:
        print(f"Total expenses: ${total:.2f}")


def print_no_expenses_message(category: Optional[str] = None) -> None:
    """
    Print a message when there are no expenses recorded.
    Optionally mentions the category if provided.
    """
    if category:
        print(f"No expenses found in category '{category}'.")
    else:
        print("No expenses recorded.")


def check_budget() -> None:
    """
    Check if the total expenses exceed the monthly budget.
    Displays a warning if the budget is exceeded.
    """
    total_expenses = sum(expense['amount'] for expense in load_expenses())
    monthly_budget = load_budget()
    if total_expenses > monthly_budget:
        print(f"Warning: You have exceeded your monthly budget of ${monthly_budget:.2f}!")


def set_budget(amount: float) -> None:
    """
    Set the monthly budget to the specified amount.
    """
    save_budget(amount)
    print(f"Monthly budget set to ${amount:.2f}")


def export_to_csv(filename: str) -> None:
    """
    Export all expenses to a CSV file with the given filename.
    """
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return

    # Define the header for CSV file
    headers = ["ID", "Date", "Description", "Amount", "Category"]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write the header
        for expense in expenses:
            writer.writerow([expense['id'], expense['date'], expense['description'],
                             f"${expense['amount']:.2f}", expense['category']])

    print(f"Expenses have been exported to {filename}")


def main() -> None:
    """
    Main function to handle CLI commands.
    Sets up command line argument parsing and initializes expenses file.
    """
    parser = argparse.ArgumentParser(
        description="Expense Tracker CLI - A tool to manage your personal expenses."
    )

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command to add a new expense
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--description', required=True, type=str, help='Description of the expense')
    add_parser.add_argument('--amount', required=True, type=float, help='Amount of the expense')
    add_parser.add_argument('--category', type=str, help='Category of the expense')

    # List command to display all expenses or filter by category or date range
    list_parser = subparsers.add_parser('list', help='List all expenses or filter by category or date range')
    list_parser.add_argument('--category', type=str, help='Category to filter expenses by')
    list_parser.add_argument('--start-date', type=str, help='Start date to filter expenses by (YYYY-MM-DD)')
    list_parser.add_argument('--end-date', type=str, help='End date to filter expenses by (YYYY-MM-DD)')

    # Delete command to remove an expense by ID
    delete_parser = subparsers.add_parser('delete', help='Delete an expense by ID')
    delete_parser.add_argument('--id', required=True, type=int, help='ID of the expense to delete')

    # Update command to update an existing expense by ID
    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    update_parser.add_argument('--id', required=True, type=int, help='ID of the expense to update')
    update_parser.add_argument('--description', type=str, help='New description of the expense')
    update_parser.add_argument('--amount', type=float, help='New amount of the expense')
    update_parser.add_argument('--category', type=str, help='New category of the expense')

    # Summary command to show a summary of expenses
    summary_parser = subparsers.add_parser('summary', help='Show a summary of expenses')
    summary_parser.add_argument('--month', type=int, help='Month number to filter the summary by (1-12)')

    # Set budget command to set a monthly budget
    budget_parser = subparsers.add_parser('set-budget', help='Set a monthly budget')
    budget_parser.add_argument('--amount', required=True, type=float, help='Amount of the monthly budget')

    # Export command to export expenses to a CSV file
    export_parser = subparsers.add_parser('export-csv', help='Export all expenses to a CSV file')
    export_parser.add_argument('--filename', required=True, type=str, help='Name of the CSV file to export expenses to')

    args = parser.parse_args()

    # Execute based on the command provided
    if args.command == 'add':
        add_expense(args.description, args.amount, args.category)
    elif args.command == 'list':
        list_expenses(args.category)
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'update':
        update_expense(args.id, args.description, args.amount, args.category)
    elif args.command == 'summary':
        show_summary(args.month)
    elif args.command == 'set-budget':
        set_budget(args.amount)
    elif args.command == 'export-csv':
        export_to_csv(args.filename)
    elif not args.command or args.command == 'help':
        parser.print_help()


# Entry point for the script
if __name__ == '__main__':
    initialize_expenses_file()
    initialize_budget_file()
    main()
