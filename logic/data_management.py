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
    """
    מחפש הוצאות לפי מפתח וערך חיפוש.

    פרמטרים:
        wey_search (str): המפתח לחיפוש בהוצאות (כגון "category", "date").
        string_search (str): הערך לחיפוש במפתח הנתון.

    מחזיר:
        list: רשימת הוצאות שמכילות את ערך החיפוש במפתח הנתון, או רשימה ריקה אם לא נמצאו הוצאות.

    תיאור:
        הפונקציה טוענת את כל ההוצאות מקובץ ההוצאות JSON שצויין בנתיב `EXPENSES_FILE_LOCATION`.
        היא בודקת אם המפתח לחיפוש קיים בהוצאות, ולאחר מכן מחפשת את הערך הנתון במפתח הנתון בכל ההוצאות.
        אם נמצאו הוצאות מתאימות, הפונקציה מחזירה רשימה של ההוצאות הללו. אם לא נמצאו הוצאות מתאימות או
        אם המפתח לחיפוש לא קיים, הפונקציה מחזירה רשימה ריקה ומדפיסה הודעה מתאימה.
    """
    my_expenses = _open_read_file(EXPENSES_FILE_LOCATION)

    for expense in my_expenses:
        if wey_search not in expense:
            print("expense not found!")
            return []
        break

    founds = [
        expense for expense in my_expenses if string_search in str(expense[wey_search])
    ]

    if founds:
        return founds
    else:
        print("expense not found!")
        return []


def search_income(wey_search: str, string_search: str) -> list:
    """
    מחפש הכנסות לפי מפתח וערך חיפוש.

    פרמטרים:
        wey_search (str): המפתח לחיפוש בהכנסות (כגון "source", "date").
        string_search (str): הערך לחיפוש במפתח הנתון.

    מחזיר:
        list: רשימת הכנסות שמכילות את ערך החיפוש במפתח הנתון, או רשימה ריקה אם לא נמצאו הכנסות.

    תיאור:
        הפונקציה טוענת את כל ההכנסות מקובץ ההכנסות JSON שצויין בנתיב `INCOME_FILE_LOCATION`.
        היא בודקת אם המפתח לחיפוש קיים בהכנסות, ולאחר מכן מחפשת את הערך הנתון במפתח הנתון בכל ההכנסות.
        אם נמצאו הכנסות מתאימות, הפונקציה מחזירה רשימה של ההכנסות הללו. אם לא נמצאו הכנסות מתאימות או
        אם המפתח לחיפוש לא קיים, הפונקציה מחזירה רשימה ריקה ומדפיסה הודעה מתאימה.
    """
    my_incomes = _open_read_file(EXPENSES_FILE_LOCATION)

    for income in my_incomes:
        if wey_search not in income:
            print("expense not found!")
            return []
        break

    founds = [
        income for income in my_incomes if string_search in str(income[wey_search])
    ]

    if founds:
        return founds
    else:
        print("expense not found!")
        return []


def delete_expense(desc: str):
    """
    מוחק הוצאה מרשימת ההוצאות לפי תיאור ההוצאה.

    פרמטרים:
    desc (str): תיאור ההוצאה למחיקה.
    """
    all_expenses = _open_read_file(EXPENSES_FILE_LOCATION)

    for idx, expense in enumerate(all_expenses):
        if desc.lower() == expense["description"].lower():
            all_expenses.pop(idx)
            break

    _open_write_file(EXPENSES_FILE_LOCATION, all_expenses)


def delete_income(desc: str):
    """
    מוחק הכנסה מרשימת ההכנסות לפי תיאור ההכנסה.

    פרמטרים:
    desc (str): תיאור ההכנסה למחיקה.
    """
    all_incomes = _open_read_file(INCOME_FILE_LOCATION)

    for idx, income in enumerate(all_incomes):
        if desc.lower() == income["description"].lower():
            all_incomes.pop(idx)
            break

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
    return _open_read_file(BUDGET_FILE_LOCATION)["categories"]


def get_expenses() -> list:
    return _open_read_file(EXPENSES_FILE_LOCATION)


def get_incomes() -> list:
    return _open_read_file(INCOME_FILE_LOCATION)