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

    # Placeholder commands for future implementation
    list_parser = subparsers.add_parser('list', help='List all expenses')
    delete_parser = subparsers.add_parser('delete', help='Delete an expense by ID')
    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    summary_parser = subparsers.add_parser('summary', help='Show a summary of expenses')
    help_parser = subparsers.add_parser('help', help='Show help information')

    args = parser.parse_args()

    # Execute based on the command provided
    if args.command == 'add':
        add_expense(args.description, args.amount)
    elif not args.command or args.command == 'help':
        parser.print_help()


# Entry point for the script
if __name__ == '__main__':
    initialize_expenses_file()
    main()
