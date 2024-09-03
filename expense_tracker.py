#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Define the path for the expenses JSON file
EXPENSES_FILE: str = 'expenses.json'


def initialize_expenses_file() -> None:
    """
    Initialize the expenses JSON file if it doesn't exist.
    Creates an empty list in the JSON file to store expenses.
    """
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'w') as file:
            json.dump([], file)  # Start with an empty list of expenses


def load_expenses() -> List[Dict[str, Any]]:
    """
    Load expenses from the JSON file.
    Returns a list of expenses.
    """
    with open(EXPENSES_FILE, 'r') as file:
        return json.load(file)


def save_expenses(expenses: List[Dict[str, Any]]) -> None:
    """
    Save expenses to the JSON file.
    Overwrites the file with the provided list of expenses.
    """
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)


def add_expense(description: str, amount: float) -> None:
    """
    Add a new expense with a description and amount.
    Assigns a unique ID and records the current date and time.
    """
    expenses = load_expenses()
    new_id = max((expense['id'] for expense in expenses), default=0) + 1
    new_expense = {
        "id": new_id,
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")


def list_expenses() -> None:
    """
    List all expenses in a readable format.
    Displays the ID, date, description, and amount for each expense.
    """
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.")
    else:
        print(f"{'ID':<5} {'Date':<20} {'Description':<30} {'Amount':<10}")
        print("-" * 70)
        for expense in expenses:
            print(f"{expense['id']:<5} {expense['date']:<20} {expense['description']:<30} ${expense['amount']:<10.2f}")


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

    # List command to display all expenses
    list_parser = subparsers.add_parser('list', help='List all expenses')

    # Delete command to remove an expense by ID
    delete_parser = subparsers.add_parser('delete', help='Delete an expense by ID')
    delete_parser.add_argument('--id', required=True, type=int, help='ID of the expense to delete')

    # Placeholder commands for future implementation
    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    summary_parser = subparsers.add_parser('summary', help='Show a summary of expenses')
    help_parser = subparsers.add_parser('help', help='Show help information')

    args = parser.parse_args()

    # Execute based on the command provided
    if args.command == 'add':
        add_expense(args.description, args.amount)
    elif args.command == 'list':
        list_expenses()
    elif args.command == 'delete':
        delete_expense(args.id)
    elif not args.command or args.command == 'help':
        parser.print_help()


# Entry point for the script
if __name__ == '__main__':
    initialize_expenses_file()
    main()
