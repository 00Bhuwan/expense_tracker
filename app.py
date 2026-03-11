from flask import Flask
from db import db

app = Flask(__name__)

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/home")
def home():
    ...