import os
import json

BUDGET_FILE_LOCATION = os.path.join(
    os.path.dirname(__file__), "..", "data", "budget.json"
)
INCOME_FILE_LOCATION = os.path.join(
    os.path.dirname(__file__), "..", "data", "income.json"
)
EXPENSES_FILE_LOCATION = os.path.join(
    os.path.dirname(__file__), "..", "data", "expenses.json"
)

def _open_read_file(file_path: str):
    """
    קורא נתוני JSON מקובץ ומחזיר אותם.

    פרמטרים:
    file_path (str): הנתיב לקובץ לקריאה ממנו.

    מחזיר:
    dict: הנתונים שנקראו מהקובץ.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        raise Exception("Error reading the file") from e


def _open_write_file(file_path: str, data):
    """
    כותב נתוני JSON לקובץ.

    פרמטרים:
    file_path (str): הנתיב לקובץ לכתיבה אליו.
    data (dict): הנתונים לכתיבה לקובץ.
    """
    try:
        with open(file_path, "w") as write_file:
            json.dump(data, write_file, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")
