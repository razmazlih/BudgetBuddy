from datetime import datetime
from . import (
    BUDGET_FILE_LOCATION,
    INCOME_FILE_LOCATION,
    EXPENSES_FILE_LOCATION,
    _open_read_file,
    _open_write_file,
)


def add_record(file_path: str, record: dict):
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


def add_expense(date: str, category: str, amount, description: str):
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
    try:
        float_amount = float(amount)
    except:
        print("amount isn't a number")
        return

    if not _check_valid_budget(float_amount):
        print("Amount is bigger then budget!")
        return

    expense_to_add = {
        "date": date,
        "category": category,
        "amount": float_amount,
        "description": description,
    }
    add_record(EXPENSES_FILE_LOCATION, expense_to_add)


def add_income(date: str, source: str, amount, description: str):
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
    try:
        float_amount = float(amount)
    except:
        print("amount isn't a number")
        return

    income_to_add = {
        "date": date,
        "source": source,
        "amount": float_amount,
        "description": description,
    }
    add_record(INCOME_FILE_LOCATION, income_to_add)


def search_expense(wey_search: str, string_search: str) -> list:
    my_expenses = _open_read_file(EXPENSES_FILE_LOCATION)
    filter_expenses = [expense for expense in my_expenses if string_search in expense[wey_search]]
    return filter_expenses


def search_incomes(wey_search: str, string_search: str) -> list:
    my_incomes = _open_read_file(INCOME_FILE_LOCATION)
    filter_incomes = [income for income in my_incomes if string_search in income[wey_search]]
    return filter_incomes


def delete_expense_by_index(idx: int):
    """
    הפונקציה delete_expense משמשת למחיקת הוצאה מתוך רשימת ההוצאות בקובץ נתון.

    פרמטרים:
    - idx (int): אינדקס ההוצאה שברצונך למחוק מתוך הרשימה.

    שלבים:
    1. קריאה של כל ההוצאות מקובץ הנתונים באמצעות _open_read_file ואחסונן במשתנה all_expenses.
    2. מחיקת ההוצאה במיקום הנתון לפי האינדקס idx באמצעות pop.
    3. כתיבת הרשימה המעודכנת חזרה לקובץ באמצעות _open_write_file.
    """
    all_expenses = _open_read_file(EXPENSES_FILE_LOCATION)

    all_expenses.pop(idx)

    _open_write_file(EXPENSES_FILE_LOCATION, all_expenses)


def delete_income_by_index(idx: int):
    """
    הפונקציה delete_income משמשת למחיקת הכנסה מתוך רשימת ההכנסות בקובץ נתון.

    פרמטרים:
    - idx (int): אינדקס ההכנסה שברצונך למחוק מתוך הרשימה.

    שלבים:
    1. קריאה של כל ההכנסות מקובץ הנתונים באמצעות _open_read_file ואחסונן במשתנה all_incomes.
    2. מחיקת ההכנסה במיקום הנתון לפי האינדקס idx באמצעות pop.
    3. כתיבת הרשימה המעודכנת חזרה לקובץ באמצעות _open_write_file.
    """
    all_incomes = _open_read_file(INCOME_FILE_LOCATION)

    all_incomes.pop(idx)

    _open_write_file(INCOME_FILE_LOCATION, all_incomes)


def _check_valid_budget(new_expense: float) -> bool:
    """
    בודק האם הוצאה חדשה תקפה לפי התקציב החודשי הקיים.

    פרמטרים:
    new_expense (str): ההוצאה החדשה לבדיקה

    מחזיר:
    bool: True אם ההוצאה החדשה תקפה לפי התקציב החודשי, אחרת False
    """
    my_budget = _open_read_file(BUDGET_FILE_LOCATION)

    is_valid_expense = new_expense <= my_budget["monthly_budget"]

    if is_valid_expense:
        return True
    else:
        return False


def _create_budget(categories: list) -> dict:
    """
    יוצר מילון תקציב מקטגוריות וסכומים נתונים.

    פרמטרים:
        categories (list): רשימת טאפלות שכל אחת מכילה שם קטגוריה וסכום (כגון [("Food", 500.0), ("Transport", 200.0)]).

    מחזיר:
        dict: מילון עם קטגוריות וסכומים, ותקציב חודשי כולל.

    תיאור:
        הפונקציה יוצרת מילון עם הקטגוריות והסכומים הנתונים. היא מחשבת את הסכום הכולל של כל הקטגוריות
        ומוסיפה אותו למילון תחת המפתח "monthly_budget".
    """
    budget_dict = {"categories": {}}

    total_budget = 0.0
    for category, amount in categories:
        if amount == 0:
            continue
        budget_dict["categories"][category] = amount
        total_budget += amount

    budget_dict["monthly_budget"] = total_budget

    return budget_dict


def update_budget(new_category: str, new_amount):
    """
    מעדכן את התקציב הקיים עם קטגוריה חדשה או מעודכנת.

    פרמטרים:
        new_category (str): שם הקטגוריה לעדכון או להוספה.
        new_amount (float or str): הסכום החדש עבור הקטגוריה. אם זהו מחרוזת, היא תומר למספר.

    תיאור:
        הפונקציה קוראת את התקציב הקיים מקובץ ה-JSON המוגדר במיקום `BUDGET_FILE_LOCATION`.
        היא בודקת אם הסכום החדש הוא מספר תקין. אם הקטגוריה החדשה כבר קיימת בתקציב, היא מעדכנת את הסכום שלה.
        אם הקטגוריה החדשה לא קיימת, היא מוסיפה את הקטגוריה עם הסכום החדש.
        לבסוף, הפונקציה מעדכנת את התקציב הכולל ושומרת את התקציב המעודכן בחזרה לקובץ ה-JSON.
    """
    budget = _open_read_file(BUDGET_FILE_LOCATION)

    tuple_budget = budget["categories"]

    try:
        float_amount = float(new_amount)
    except:
        print("category value isn't a number")
        return

    if new_category in tuple_budget:
        for category in tuple_budget.items():
            if category[0] == new_category:
                tuple_budget[category[0]] = float_amount
                break
    else:
        budget["categories"][new_category] = float_amount

    updated_budget = _create_budget(tuple_budget.items())
    _open_write_file(BUDGET_FILE_LOCATION, updated_budget)


def get_full_budget():
    return _open_read_file(BUDGET_FILE_LOCATION)


def get_total_expense() -> float:
    """
    פונקציה זו מחשבת את סך כל ההוצאות.

    היא קוראת את קובץ ההוצאות מהמיקום המוגדר במשתנה EXPENSES_FILE_LOCATION,
    מחשבת את סכום כל ההוצאות ומחזירה את התוצאה כסוג נתון float.

    החזרת ערך:
    float: סכום כל ההוצאות.
    """
    all_expenses = _open_read_file(EXPENSES_FILE_LOCATION)

    total_expenses = 0.0

    if all_expenses:
        for expense in all_expenses:
            total_expenses += expense["amount"]
        return total_expenses
    else:
        return total_expenses


def get_total_income() -> float:
    """
    פונקציה זו מחשבת את סך כל ההכנסות.

    היא קוראת את קובץ ההכנסות מהמיקום המוגדר במשתנה INCOME_FILE_LOCATION,
    מחשבת את סכום כל ההכנסות ומחזירה את התוצאה כסוג נתון float.

    החזרת ערך:
    float: סכום כל ההכנסות.
    """
    all_incomes = _open_read_file(INCOME_FILE_LOCATION)

    total_incomes = 0.0

    if all_incomes:
        for income in all_incomes:
            total_incomes += income["amount"]
        return total_incomes
    else:
        return total_incomes


def get_budget() -> float:
    """
    פונקציה זו מחזירה את התקציב החודשי.

    היא קוראת את קובץ התקציב מהמיקום המוגדר במשתנה BUDGET_FILE_LOCATION,
    ומחזירה את הערך של התקציב החודשי כסוג נתון float.

    החזרת ערך:
    float: התקציב החודשי.
    """
    budget = _open_read_file(BUDGET_FILE_LOCATION)

    return budget["monthly_budget"]


def get_budget_categories() -> dict:
    """
    פונקציה להחזרת קטגוריות התקציב.

    Returns:
        dict: קטגוריות התקציב מתוך קובץ התקציב.
    """
    return _open_read_file(BUDGET_FILE_LOCATION)["categories"]


def get_expenses() -> list:
    """
    פונקציה להחזרת כל ההוצאות.

    Returns:
        list: רשימת ההוצאות מתוך קובץ ההוצאות.
    """
    return _open_read_file(EXPENSES_FILE_LOCATION)


def get_incomes() -> list:
    """
    פונקציה להחזרת כל ההכנסות.

    Returns:
        list: רשימת ההכנסות מתוך קובץ ההכנסות.
    """
    return _open_read_file(INCOME_FILE_LOCATION)


def get_expense_categories() -> set:
    """
    פונקציה להחזרת קטגוריות ההוצאות.

    Returns:
        set: סט של קטגוריות ההוצאות מתוך קובץ ההוצאות.
    """
    # all_expenses = _open_read_file(EXPENSES_FILE_LOCATION)
    # categories_set = {expense["category"] for expense in all_expenses}
    # return categories_set

    my_budget = _open_read_file(BUDGET_FILE_LOCATION)
    return my_budget["categories"]


def get_income_categories() -> set:
    """
    פונקציה להחזרת קטגוריות ההכנסות.

    Returns:
        set: סט של קטגוריות ההכנסות מתוך קובץ ההכנסות.
    """
    all_incomes = _open_read_file(INCOME_FILE_LOCATION)
    categories_set = {income["category"] for income in all_incomes}
    return categories_set


def get_total_expenses_now_month() -> float:
    """
    פונקציה זו מחזירה את סך כל ההוצאות בחודש הנוכחי.

    Returns:
        float: סך כל ההוצאות בחודש הנוכחי.
    """
    all_expenses = get_expenses()

    now_month = datetime.now().month
    now_year = datetime.now().year

    list_on_now_month = [
        expense["amount"]
        for expense in all_expenses
        if int(expense["date"][5:7]) == now_month
        and int(expense["date"][:4]) == now_year
    ]

    return sum(list_on_now_month)


def get_total_income_now_month() -> float:
    """
    פונקציה זו מחזירה את סך כל ההכנסות בחודש הנוכחי.

    Returns:
        float: סך כל ההכנסות בחודש הנוכחי.
    """
    all_income = get_incomes()

    now_month = datetime.now().month
    now_year = datetime.now().year

    list_on_now_month = [
        income["amount"]
        for income in all_income
        if int(income["date"][5:7]) == now_month
        and int(income["date"][:4]) == now_year
    ]

    return sum(list_on_now_month)
