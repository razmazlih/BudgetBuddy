import json
import os


budget_file_location = os.path.join(
    os.path.dirname(__file__), "..", "data", "budget.json"
)
income_file_location = os.path.join(
    os.path.dirname(__file__), "..", "data", "income.json"
)
expenses_file_location = os.path.join(
    os.path.dirname(__file__), "..", "data", "expenses.json"
)


def get_data(file_location):
    with open(file_location, "r") as budget_data:
        json_data = json.load(budget_data)

    return json_data


def add_expense(date, category, amount, description):
    expense_to_add = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }
    try:
        all_expenses = get_data(expenses_file_location)
    except Exception as err:
        print("file loading error:", err)
        all_expenses = []

    all_expenses.append(expense_to_add)

    with open(expenses_file_location, "w") as expenses_file:
        json.dump(all_expenses, expenses_file)
