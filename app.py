from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from tools import import_csv, allowed_file, add_trade, get_coin_ids, get_current_price
from models import Trade, Position, db, setup_db, db_drop_and_create
from forms import AddTradeForm
import os
from sqlalchemy import desc, func, case


app = Flask(__name__)
app.secret_key = '12345'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000 #sets max filesize to 1mb


#routes
@app.route('/', methods=['POST', 'GET'])
def dashboard():
    if request.method == "POST":
        return "HELLO"
    else:
        trades = Trade.query.order_by(Trade.date).all()
        positions = Position.query.order_by(case([(Position.status=='Open', 0)], else_=1), desc(Position.date_open)).all()
        columns = [
            {
                'field': 'status',
                'title': 'Status'
            },
            {
                'field': 'date_open',
                'title': 'Date Opened'
            },
            {
                'field': 'symbol',
                'title': 'Symbol'
            },
            {
                'field': 'entry',
                'title': 'Entry'
            },
            {
                'field': 'exit',
                'title': 'Exit'
            },
            {
                'field': 'pnl',
                'title': 'Return'
            },
            {
                'field': 'price',
                'title': 'Price'
            },
            {
                'field': 'direction',
                'title': 'Direction'
            }
        ]
        pos_data = []
        if trades:
            current_prices =  get_current_price()
        for count, p in enumerate(positions):
            pos_data.append(
                {
                    'status': p.status,
                    'date_open': p.date_open,
                    'symbol': p.symbol,
                    'entry': p.entry,
                    'exit': p.exit,
                    'pnl': p.pnl,
                    'price': p.qty * (p.current_price - p.entry),
                    'direction': p.direction
                }
            )
        return render_template('dashboard.html', trades=trades, positions=positions, data=pos_data)

@app.route('/importcsv', methods=['POST', 'GET'])
def importcsv():
    if request.method == "POST":
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

# app.context_processor enables auto injecting variables or functions into all templates.
# https://flask.palletsprojects.com/en/2.0.x/templating/#context-processors
@app.context_processor
def inject_addtradeForm():
    return dict(addtradeForm=AddTradeForm())

@app.route('/add', methods=["POST"])
def add():
    form = AddTradeForm()
    if form.validate_on_submit():
        print('FORM VALIDATED')

        new_trade = Trade(
            date=form.date.data,
            type=form.type.data,
            symbol=form.symbol.data.upper(),
            price=form.price.data,
            qty=form.qty.data,
            value=form.value.data,
            img=form.img.data
        )

        print(type(new_trade.date), type(new_trade.type), type(new_trade.symbol), type(new_trade.price), type(new_trade.qty), type(new_trade.value))
        add_trade(new_trade)
        db.session.add(new_trade)
        db.session.commit()
        flash('New trade added.')
        return redirect(url_for('dashboard'))
    print('FORM NOT VALIDATED')
    return redirect(url_for('dashboard'))

@app.route('/test', methods=["GET"])
def test():
    if request.method == "POST":
        return 'REQUEST ERROR /TEST'

    print(get_coin_ids())
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    setup_db(app)
    # db_drop_and_create(app) #clear and initialize new db on app start
    app.run(debug=True)



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
