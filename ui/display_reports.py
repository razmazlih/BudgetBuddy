from logic.report_generation import filter_expense_by_date, filter_income_by_date
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from flask import send_file, request


def show_income_graph(start_date: str = "0000-00-00", end_date: str = "9999-00-00"):
    start_date = request.args.get('start_date', '2024-06-01')
    end_date = request.args.get('end_date', '2024-06-30')

    data = filter_income_by_date(start_date, end_date)
    df = pd.DataFrame(data)

    if df.empty:
        return "No data available for the specified date range."

    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(10, 6))
    plt.bar(df["date"], df["total_amount"], color="green")
    plt.xlabel("Date")
    plt.ylabel("Income")
    plt.title("Total Income per Date")
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


def show_expense_graph():
    start_date = request.args.get('start_date', '2024-06-01')
    end_date = request.args.get('end_date', '2024-06-30')

    data = filter_expense_by_date(start_date, end_date)
    df = pd.DataFrame(data)

    if df.empty:
        return "No data available for the specified date range."

    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(10, 6))
    plt.bar(df["date"], df["total_amount"], color="red")
    plt.xlabel("Date")
    plt.ylabel("Expense")
    plt.title("Total Expense per Date")
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


