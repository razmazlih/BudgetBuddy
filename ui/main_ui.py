from flask import Flask
from .display_reports import show_expense_graph, show_income_graph

app = Flask(__name__)

@app.route('/expense-graph')
def expense_graph():
    return show_expense_graph()

@app.route('/income-graph')
def income_graph():
    return show_income_graph()

if __name__ == '__main__':
    app.run(debug=True)