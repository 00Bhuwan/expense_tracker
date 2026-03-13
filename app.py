import os

from datetime import datetime, UTC
from enum import unique

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
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
    amount = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10))
    date = db.Column(db.String(20), default=datetime.now(UTC))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)