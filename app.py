from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #config test.db file at relative location
db = SQLAlchemy(app) #initialize database with settings from app

#models
class Trade(db.Model):
    __tablename__ = 'trades'
    _id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    asset = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    img = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Trade> %r' % self._id

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
