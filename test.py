from app import app
from models import setup_db, db_drop_and_create, db, Trade
from tools import import_csv

setup_db(app)
db_drop_and_create(app)

with app.app_context():
    import_csv('./data/dbtest.csv')
    trades = Trade.query.filter_by(symbol='BTC', type='Buy').first()
    print(trades)
    if not Trade.query.filter_by(symbol='BTC', type='Sell'):
        print('Add Sell')
    else:
        print('Add Sell')


def new_position(symbol):
    pass
    # if symbol in Trade.query.filter_by(symbol=symbol):
