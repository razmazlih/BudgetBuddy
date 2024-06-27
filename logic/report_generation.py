import datetime
from . import (
    INCOME_FILE_LOCATION,
    EXPENSES_FILE_LOCATION,
    _open_read_file,
)


def _group_and_sum_by_date(data: list) -> list:
    """
    מקבץ סכומים לפי תאריך.

    פרמטרים:
    data (list): רשימת נתונים עם תאריך וסכום.

    מחזיר:
    list: רשימה של מילונים עם תאריך והסכום הכולל עבור אותו תאריך.
    """
    grouped_data = {}

    for entry in data:
        date = entry["date"]
        amount = entry["amount"]
        if date in grouped_data:
            grouped_data[date] += amount
        else:
            grouped_data[date] = amount

    result = [
        {"date": date, "total_amount": total_amount}
        for date, total_amount in grouped_data.items()
    ]
    return result


def _fill_missing_dates(data: list, start_date: str, end_date: str) -> list:
    """
    ממלא תאריכים חסרים עם ערך 0.

    פרמטרים:
    data (list): רשימה של מילונים עם תאריך והסכום הכולל.
    start_date (str): תאריך התחלה לטווח (בפורמט "שששש-חח-יי").
    end_date (str): תאריך סיום לטווח (בפורמט "שששש-חח-יי").

    מחזיר:
    list: רשימה מלאה של תאריכים עם הסכומים הכוללים, כולל תאריכים חסרים עם ערך 0.
    """
    date_format = "%Y-%m-%d"
    start = datetime.datetime.strptime(start_date, date_format)
    end = datetime.datetime.strptime(end_date, date_format)
    date_set = {entry["date"] for entry in data}
    current = start

    while current <= end:
        date_str = current.strftime(date_format)
        if date_str not in date_set:
            data.append({"date": date_str, "total_amount": 0})
        current += datetime.timedelta(days=1)

    data.sort(key=lambda x: x["date"])
    return data


def filter_expense_by_date(start_date: str, end_date: str) -> list:
    """
    מסנן הוצאות לפי טווח תאריכים.

    פרמטרים:
    start_date (str): תאריך התחלה לטווח (בפורמט "שששש-חח-יי").
    end_date (str): תאריך סיום לטווח (בפורמט "שששש-חח-יי").

    מחזיר:
    list: רשימה מסוננת של הוצאות המקובצות לפי תאריך והסכום הכולל עבור כל תאריך בטווח שנבחר.
    """
    all_expense = _open_read_file(EXPENSES_FILE_LOCATION)

    filtered_data = [
        entry
        for entry in _group_and_sum_by_date(all_expense)
        if start_date <= entry["date"] <= end_date
    ]

    if filtered_data:
        oldest_date = min(entry["date"] for entry in filtered_data)
        newest_date = max(entry["date"] for entry in filtered_data)
        filled_data = _fill_missing_dates(filtered_data, oldest_date, newest_date)
    else:
        filled_data = []

    return filled_data


def filter_income_by_date(start_date: str, end_date: str) -> list:
    """
    מסנן הכנסות לפי טווח תאריכים.

    פרמטרים:
    start_date (str): תאריך התחלה לטווח (בפורמט "שששש-חח-יי").
    end_date (str): תאריך סיום לטווח (בפורמט "שששש-חח-יי").

    מחזיר:
    list: רשימה מסוננת של הכנסות המקובצות לפי תאריך והסכום הכולל עבור כל תאריך בטווח שנבחר.
    """
    all_incomes = _open_read_file(INCOME_FILE_LOCATION)

    filtered_data = [
        entry
        for entry in _group_and_sum_by_date(all_incomes)
        if start_date <= entry["date"] <= end_date
    ]

    if filtered_data:
        oldest_date = min(entry["date"] for entry in filtered_data)
        newest_date = max(entry["date"] for entry in filtered_data)
        filled_data = _fill_missing_dates(filtered_data, oldest_date, newest_date)
    else:
        filled_data = []

    return filled_data
