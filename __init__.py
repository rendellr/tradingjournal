from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #config test.db file at relative location
db = SQLAlchemy(app) #initialize database with settings from app


#models
class Trades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#routes
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        pass
        return "Hello"
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

