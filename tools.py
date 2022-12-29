import csv
from datetime import datetime
from models import Trade, Position, db

ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def import_csv(filename):

    with open(filename, 'r') as csvfile:

        csvreader = csv.DictReader(csvfile)

        trades = []  # date, type, symbol, price, qty
        for row in csvreader:
            trades.append(row)

        header = ['date', 'type', 'symbol', 'price', 'qty']
        # print(header)
        # print(trades[0].keys())

        # If list is empty or keys do not match header, return error string
        if len(trades) == 0:
            return 'csv file is empty'
        if list(trades[0]) != header:
            return 'data format incorrect'

        # process data and save to database
        for trade in trades:
            # convert values to correct data type
            price = float(trade['price'])
            qty = float(trade['qty'])
            value = round(price * qty, 2)
            # notes = 'notes text'
            # img = 'https://s3.tradingview.com/g/G1EOg7dj_mid.png'

            #print(price, qty, value)

            # create db entry
            entry = Trade(
                date=datetime.strptime(trade['date'], "%Y-%m-%d"),
                type=trade['type'],
                symbol=trade['symbol'].upper(),
                price=price,
                qty=qty,
                value=value
            )


            #print(entry.symbol)
            add_trade(entry)
            db.session.add(entry)
            db.session.commit()

    return

# Add trade new trade to position, update position id with new data
def add_trade(trade):

    direction = {'Buy': 1, 'Sell': -1}

    # if no open trades exist, create new position, commit to db, return
    if not Position.query.filter_by(symbol=trade.symbol, status='Open').all():
        position = Position(
            date_open=trade.date,
            status='Open',
            symbol=trade.symbol,
            cost_basis=trade.price,
            qty=trade.qty*direction[trade.type],
            net_cost=trade.price*trade.qty,
            notes='',
            img=trade.img,
        )

        print(f'No trade exists, creating {position}, {position.symbol}, qty: {position.qty} ')
        db.session.add(position)
        db.session.commit()
        trade.position_id = position._id #add position relationship to trade entry
        db.session.commit()

        return

    # else an open trade exists, link new trade to position, update position data, return
    else :
        # if open pos != 1, return error msg
        if Position.query.filter_by(symbol=trade.symbol, status='Open').count() != 1:
            print('error, open position qty mismatch')

        openpos = Position.query.filter_by(symbol=trade.symbol, status='Open').first()

        # If new trade reduces qty past 0, throw error about selling/buying more than available

        # If new trade reduces qty to 0 or , update position data and set status to "Closed"
        if openpos.qty + trade.qty * direction[trade.type] == 0:
            print(f'Trade quantity zero, closing position {openpos}')
            openpos.qty = 0
            openpos.cost_basis = 0
            openpos.status = 'Closed'
        else:
            print(f'Adding {trade} to {openpos}')
            openpos.cost_basis = (openpos.cost_basis * openpos.qty + trade.price * trade.qty) / (openpos.qty + trade.qty)
            openpos.qty += trade.qty * direction[trade.type] # adjust pos qty based on trade direction

        openpos.net_cost = trade.price * trade.qty * direction[trade.type]
        trade.position_id = openpos._id # add trade as child to open position
        db.session.commit()
        return

    # trades = db.relationship('Trade', backref='trade')
    # date_open = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # status = db.Column(db.String(10), default='Open', nullable=False)
    # symbol = db.Column(db.String(200), nullable=False)
    # cost_basis = db.Column(db.Float, nullable=False)
    # qty = db.Column(db.Float, nullable=False)
    # notes = db.Column(db.String(1000), default='')
    # img = db.Column(db.String(200), default='')
