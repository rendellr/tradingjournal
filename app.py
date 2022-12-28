from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from tools import import_csv, allowed_file
from datetime import datetime
from models import Trade, setup_db, db_drop_and_create
import os


app = Flask(__name__)
#db = SQLAlchemy(app) #initialize database with settings from app
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #config test.db file at relative location
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '12345'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000 #sets max filesize to 1mb


#routes
@app.route('/', methods=['POST', 'GET'])
def dashboard():
    if request.method == "POST":
        return "Hello"
    else:
        trades = Trade.query.order_by(Trade.date).all()
        return render_template('dashboard.html', trades=trades)

@app.route('/importcsv', methods=['POST', 'GET'])
def importcsv():

    if request.method == "POST":
        # check to see if post request has the file part form form input, else
        if 'formFile' not in request.files:
            flash('Form lacking File part')
            return redirect(request.url)

        file = request.files['formFile']

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if '.' in file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            import_csv(filename)
            os.remove(filename)
            flash('Trade data uploaded')
            return redirect(url_for('dashboard'))

    return render_template('importcsv.html')


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
    setup_db(app)
    db_drop_and_create(app)
    app.run(debug=True)

