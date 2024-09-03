
# Expense Tracker CLI

Expense Tracker is a command-line application for managing personal expenses. The application allows users to add, update, delete, and view expenses, as well as set a monthly budget and export expenses to a CSV file.

## Features

- **Add Expenses:** You can add an expense with a description, amount, and optional category.
- **Update Expenses:** Ability to edit existing expenses.
- **Delete Expenses:** Remove expenses by their ID.
- **View Expenses:** Display all expenses or filter by category.
- **Expense Summary:** Show a summary of all expenses or expenses for a specific month.
- **Set Monthly Budget:** Get a warning when expenses exceed the set budget.
- **Export to CSV:** Export the list of expenses to a CSV file.
- **Filter by Date Range:** View expenses within a specific date range.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/YourUsername/ExpenseTracker.git
    cd ExpenseTracker
    ```

2. Make sure you have Python 3 installed.

3. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
    ```

4. Run the application from the command line:

    ```bash
    python expense_tracker.py
    ```

## Usage

### Adding a New Expense

```bash
expense-tracker add --description "Lunch" --amount 20 --category "Food"
```

### Updating an Expense

```bash
expense-tracker update --id 1 --description "Dinner" --amount 30 --category "Food"
```

### Deleting an Expense

```bash
expense-tracker delete --id 1
```

### Viewing All Expenses

```bash
expense-tracker list
```

### Filtering Expenses by Category

```bash
expense-tracker list --category "Food"
```

### Filtering Expenses by Date Range

```bash
expense-tracker list --start-date 2024-09-01 --end-date 2024-09-03
```

### Showing an Expense Summary

```bash
expense-tracker summary
expense-tracker summary --month 9  # Summary for September
```

### Setting a Monthly Budget

```bash
expense-tracker set-budget --amount 100
```

### Exporting Expenses to a CSV File

```bash
expense-tracker export-csv --filename expenses.csv
```

### Displaying Help

```bash
expense-tracker help
```

## Requirements

- Python 3.7 or later

## Contributing

If you would like to contribute to this project, please clone the repository, create a new feature branch, and then create a pull request.


## Source

[Expense Tracker on roadmap.sh](https://roadmap.sh/projects/expense-tracker)
