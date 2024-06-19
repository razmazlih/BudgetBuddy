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


def get_data(file_path):
    """
    טוען נתונים מקובץ JSON נתון.

    פרמטרים:
        file_path (str): הנתיב לקובץ ה-JSON.

    מחזיר:
        list: רשימת נתונים מהקובץ.

    זורק:
        Exception: אם יש שגיאה בטעינת הקובץ.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def add_expense(date, category, amount, description):
    """
    מוסיף הוצאה חדשה לקובץ ההוצאות JSON.

    פרמטרים:
        date (str): התאריך של ההוצאה.
        category (str): הקטגוריה של ההוצאה.
        amount (float): סכום ההוצאה.
        description (str): תיאור ההוצאה.

    תיאור:
        הפונקציה יוצרת מילון של ההוצאה החדשה עם התאריך, קטגוריה, סכום ותיאור.
        היא טוענת את כל ההוצאות הקיימות מקובץ ה-JSON. אם יש שגיאה בטעינת הקובץ,
        היא יוצרת רשימה ריקה. לאחר מכן, הפונקציה מוסיפה את ההוצאה החדשה לרשימה
        ושומרת את הרשימה המעודכנת בחזרה לקובץ ה-JSON.

    """
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
        json.dump(all_expenses, expenses_file, indent=4)
