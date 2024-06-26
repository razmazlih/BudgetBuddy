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
        date = entry['date']
        amount = entry['amount']
        if date in grouped_data:
            grouped_data[date] += amount
        else:
            grouped_data[date] = amount

    result = [{'date': date, 'total_amount': total_amount} for date, total_amount in grouped_data.items()]
    return result

def filter_expense_by_date(start_date: str = "0000-00-00", end_date: str = "9999-00-00") -> list:
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
        entry for entry in _group_and_sum_by_date(all_expense)
        if start_date <= entry['date'] <= end_date
    ]

    return filtered_data

def filter_income_by_date(start_date: str = "0000-00-00", end_date: str = "9999-00-00") -> list:
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
        entry for entry in _group_and_sum_by_date(all_incomes)
        if start_date <= entry['date'] <= end_date
    ]

    return filtered_data
