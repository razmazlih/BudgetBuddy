from data_management import (
    BUDGET_FILE_LOCATION,
    _open_read_file,
    _open_write_file,
)


def check_budget(new_expense: str) -> bool:
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
