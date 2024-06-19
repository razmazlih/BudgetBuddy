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
        with open(file_path, 'r') as file:
            all_records = json.load(file)
    except Exception as err:
        print(f"file loading error for {file_path}:", err)
        all_records = []

    all_records.append(record)

    with open(file_path, "w") as file_to_update:
        json.dump(all_records, file_to_update, indent=4)


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
        "description": description
    }
    add_record(expenses_file_location, expense_to_add)


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
        "description": description
    }
    add_record(income_file_location, income_to_add)


