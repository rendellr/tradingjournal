from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #config test.db file at relative location
db = SQLAlchemy(app) #initialize database with settings from app


#models
class Trades(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    asset = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float)
    notes = db.Column(db.String(1000))
    img = db.Column(db.String(200))

    def __init__(self):
        self.value = price * size

#routes
@app.route('/', methods=['POST', 'GET'])
def dashboard():
    if request.method == "POST":
        return "Hello"
    else:
        return render_template('dashboard.html')

# Example of redirect
# @app.route('/admin')
# def admin():
#     return redirect(url_for('dashboard')) #enter name of function to redirect to

# Example of passing variable via URL
# @app.route("/<name>")
# def user(name):
#    return f"Hello {name}!"

# Example of passing variable via URL
# @app.route('/admin')
# def admin():
#     return redirect(url_for('user', name="Admin!")) # redirects to user and passes name to user function


if __name__ == "__main__":
    app.run(debug=True)

