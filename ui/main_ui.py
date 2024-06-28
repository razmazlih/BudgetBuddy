from .display_reports import show_expense_graph, show_income_graph
from flask import Flask, render_template, request, redirect, url_for
from logic.data_management import (
    add_record,
    add_expense,
    add_income,
    search_expense,
    search_income,
    update_budget,
    delete_expense,
    delete_income,
    get_total_expense,
    get_total_income,
    get_budget,
    get_expenses,
    get_incomes,
    get_budget_categories
)


app = Flask(__name__)


# דף הבית
@app.route("/")
def index():
    return render_template("index.html", total_expenses= get_total_expense(), total_incomes=get_total_income(), my_budget=get_budget())


# דף ניהול הוצאות
@app.route("/expenses")
def expenses():
    my_expenses = get_expenses()
    return render_template("expenses.html", expenses=my_expenses)


@app.route("/add_expenses", methods=["POST"])
def add_new_expense():
    year_date = request.form.get("yearDate")
    month_date = request.form.get("monthDate")
    day_date = request.form.get("dayDate")

    if len(month_date) != 2:
        month_date = "0" + month_date

    if len(day_date) != 2:
        day_date = "0" + day_date

    input_date = f"{year_date}-{month_date}-{day_date}"

    input_category = request.form.get("category")
    input_amount = request.form.get("amount")
    input_description = request.form.get("description")

    add_expense(input_date, input_category, input_amount, input_description)
    return render_template("index.html", total_expenses= get_total_expense(), total_incomes=get_total_income(), my_budget=get_budget())

@app.route("/income")
def income():
    my_incomes = get_incomes()
    return render_template("income.html", incomes=my_incomes)


@app.route("/add_income", methods=["POST"])
def add_new_income():
    year_date = request.form.get("yearDate")
    month_date = request.form.get("monthDate")
    day_date = request.form.get("dayDate")

    if len(month_date) != 2:
        month_date = "0" + month_date

    if len(day_date) != 2:
        day_date = "0" + day_date

    input_date = f"{year_date}-{month_date}-{day_date}"

    input_source = request.form.get("source")
    input_amount = request.form.get("amount")
    input_description = request.form.get("description")

    add_income(input_date, input_source, input_amount, input_description)
    return render_template("index.html", total_expenses= get_total_expense(), total_incomes=get_total_income(), my_budget=get_budget())


@app.route("/budget")
def budget():
    return render_template("budget.html", categories=get_budget_categories(), total=get_budget())


@app.route("/expense-graph")
def expense_graph():
    return show_expense_graph()


@app.route("/income-graph")
def income_graph():
    return show_income_graph()
