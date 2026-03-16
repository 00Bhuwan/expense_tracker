import os

from datetime import datetime, UTC

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

uri = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float(100), nullable=False)
    type = db.Column(db.String(10))
    category = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    transactions = Transaction.query.order_by(Transaction.id.desc()).all()

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expense

    return render_template(
        "index.html",
        transactions=transactions,
        income=total_income,
        expense=total_expense,
        balance=balance
    )

@app.route("/add")
def add_transaction():
    return render_template("add.html", transactions=Transaction.query.all())

@app.route("/transactions/add", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        t_type = request.form["type"]
        category = request.form["category"]

        new_transaction = Transaction(title=title, amount=amount, type=t_type, category=category)
        try:
            db.session.add(new_transaction)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return f"Error: Title must be unique."

    return redirect(url_for("home"))

# delete
@app.route("/transactions/delete/<int:transaction_id>", methods=["POST"])
def del_transaction(transaction_id):
    delete_trans = Transaction.query.get_or_404(transaction_id)
    try:
        db.session.delete(delete_trans)
        db.session.commit()
        return redirect(url_for("home"))
    except Exception as e:
        return f"Error: {e}"

# edit
@app.route("/transactions/edit", methods=["POST"])
def update_transaction():
    txn_id = request.form["id"]
    transaction = db.session.get(Transaction, txn_id)

    if transaction:
        transaction.title = request.form["title"]
        transaction.amount = float(request.form["amount"])
        transaction.type = request.form["type"]
        transaction.category = request.form["category"]
        db.session.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)