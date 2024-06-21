import json
import os


BUDGET_FILE_LOCATION = os.path.join(
    os.path.dirname(__file__), "..", "data", "budget.json"
)
INCOME_FILE_LOCATION = os.path.join(
    os.path.dirname(__file__), "..", "data", "income.json"
)
EXPENSES_FILE_LOCATION = os.path.join(
    os.path.dirname(__file__), "..", "data", "expenses.json"
)


def _open_read_file(file_path):
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


def _open_write_file(file_path, data):
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


def add_record(file_path, record):
    """
    מוסיף רשומה חדשה לקובץ JSON נתון ומעדכן את הקובץ.

    פרמטרים:
        file_path (str): הנתיב לקובץ ה-JSON.
        record (dict): הרשומה להוספה לקובץ ה-JSON.

    תיאור:
        הפונקציה טוענת את כל הרשומות הקיימות מקובץ ה-JSON שצויין בנתיב `file_path`.
        אם יש שגיאה בטעינת הקובץ, היא יוצרת רשימה ריקה. לאחר מכן, הפונקציה מוסיפה
        את הרשומה החדשה לרשימה ושומרת את הרשימה המעודכנת בחזרה לקובץ ה-JSON.
        הפרמטר `indent=4` משמש להוספת רווחים לכל רמה במבנה ה-JSON כדי להפוך את הקובץ
        לקריא יותר עבור בני אדם.

    """
    try:
        all_records = _open_read_file(file_path)
    except:
        all_records = []

    all_records.append(record)

    _open_write_file(file_path, all_records)


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
        היא קוראת לפונקציה `add_record` עם הנתיב לקובץ ההוצאות והרשומה החדשה כדי
        להוסיף את ההוצאה לקובץ ולעדכן אותו.

    """
    expense_to_add = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description,
    }
    add_record(EXPENSES_FILE_LOCATION, expense_to_add)


def add_income(date, source, amount, description):
    """
    מוסיף הכנסה חדשה לקובץ ההכנסות JSON.

    פרמטרים:
        date (str): התאריך של ההכנסה.
        source (str): מקור ההכנסה.
        amount (float): סכום ההכנסה.
        description (str): תיאור ההכנסה.

    תיאור:
        הפונקציה יוצרת מילון של ההכנסה החדשה עם התאריך, מקור ההכנסה, סכום ותיאור.
        היא קוראת לפונקציה `add_record` עם הנתיב לקובץ ההכנסות והרשומה החדשה כדי
        להוסיף את ההכנסה לקובץ ולעדכן אותו.

    """
    income_to_add = {
        "date": date,
        "source": source,
        "amount": amount,
        "description": description,
    }
    add_record(INCOME_FILE_LOCATION, income_to_add)


def search_expense(wey_search, string_search: str) -> list:
    my_expenses = _open_read_file(EXPENSES_FILE_LOCATION)

    for expense in my_expenses:
        if wey_search not in expense:
            print("expense not found!")
            return []
        break

    founds = [expense for expense in my_expenses if string_search in str(expense[wey_search])]

    if founds:
        return founds
    else:
        print("expense not found!")
        return []


def search_income(wey_search, string_search: str) -> list:
    my_incomes = _open_read_file(EXPENSES_FILE_LOCATION)

    for income in my_incomes:
        if wey_search not in income:
            print("expense not found!")
            return []
        break

    founds = [income for income in my_incomes if string_search in str(income[wey_search])]

    if founds:
        return founds
    else:
        print("expense not found!")
        return []
