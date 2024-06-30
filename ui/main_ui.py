from .display_reports import show_expense_graph, show_income_graph
from flask import Flask, render_template, request, redirect, url_for, jsonify
from logic.data_management import (
    add_record,
    add_expense,
    add_income,
    search_expense,
    search_income,
    update_budget,
    delete_expense_by_index,
    delete_income_by_index,
    get_total_expense,
    get_total_income,
    get_budget,
    get_expenses,
    get_incomes,
    get_budget_categories,
    get_full_budget,
    get_expense_categories,
    get_income_categories,
    get_total_expenses_now_month,
    get_total_income_now_month,
)


app = Flask(__name__)


# דף הבית
@app.route("/")
def index():
    total_expenses = get_total_expense()
    total_incomes = get_total_income()
    total_budget = get_budget()
    expenses_now_month = get_total_expenses_now_month()
    incomes_now_month = get_total_income_now_month()
    return render_template(
        "index.html",
        total_expenses=total_expenses,
        total_incomes=total_incomes,
        my_budget=total_budget,
        expenses_now_month=expenses_now_month,
        incomes_now_month=incomes_now_month
    )


# דף ניהול הוצאות
@app.route("/expenses", methods=["GET", "POST"])
def expenses():
    sorted_expenses = enumerate(sorted(get_expenses(), key=lambda item: item["date"]))
    return render_template(
        "expenses.html",
        my_expenses=sorted_expenses,
        all_expense_categories=get_expense_categories(),
    )


@app.route("/add_expenses", methods=["POST"])
def add_new_expense():
    input_date = request.form.get("fullDate")
    input_category = request.form.get("category")
    input_amount = request.form.get("amount")
    input_description = request.form.get("description")

    add_expense(input_date, input_category, input_amount, input_description)

    return render_template("expense_confirmation.html")


@app.route("/delete_expense/<int:idx>", methods=["POST"])
def delete_expense(idx):
    delete_expense_by_index(idx)
    return redirect(url_for("expenses"))


@app.route("/income")
def income():
    sorted_incomes = enumerate(sorted(get_incomes(), key=lambda item: item["date"]))
    return render_template("income.html", incomes=sorted_incomes)


@app.route("/add_income", methods=["POST"])
def add_new_income():
    input_date = request.form.get("fullDate")
    input_source = request.form.get("source")
    input_amount = request.form.get("amount")
    input_description = request.form.get("description")

    add_income(input_date, input_source, input_amount, input_description)

    return render_template("income_confirmation.html")


@app.route("/delete_income/<int:idx>", methods=["POST"])
def delete_income(idx):
    delete_income_by_index(idx)
    return redirect(url_for("income"))


@app.route("/budget", methods=["GET", "POST"])
def budget():
    if request.method == "POST":
        new_category = request.form["new_category"]
        new_amount = request.form["new_amount"]
        update_budget(new_category, new_amount)
        return redirect(url_for("budget"))
    now_budget = get_full_budget()
    categories = now_budget.get("categories", {})
    total = now_budget.get("monthly_budget", 0)
    return render_template("budget.html", categories=categories, total=total)


@app.route("/expense-graph")
def expense_graph():
    return show_expense_graph()


@app.route("/income-graph")
def income_graph():
    return show_income_graph()
