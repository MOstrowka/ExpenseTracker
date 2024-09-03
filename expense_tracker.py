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

    # Placeholder commands (will be implemented in next steps)
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    list_parser = subparsers.add_parser('list', help='List all expenses')
    delete_parser = subparsers.add_parser('delete', help='Delete an expense by ID')
    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    summary_parser = subparsers.add_parser('summary', help='Show a summary of expenses')
    help_parser = subparsers.add_parser('help', help='Show help information')

    args = parser.parse_args()

    # Check if no command was given or help command was invoked
    if not args.command or args.command == 'help':
        parser.print_help()

# Entry point for the script
if __name__ == '__main__':
    initialize_expenses_file()
    main()
