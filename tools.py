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
            new_trade = Trade(
                date=datetime.strptime(trade['date'], "%Y-%m-%d"),
                type=trade['type'],
                symbol=trade['symbol'].upper(),
                price=price,
                qty=qty,
                value=value
            )

            #print(entry.symbol)
            add_trade(new_trade)
            db.session.add(new_trade)
            db.session.commit()

    return

# Add trade new trade to position, update position id with new data
def add_trade(trade):

    dir = {'Buy': 'Long', 'Sell': 'Short'}

    # if no open positions exist, create new position, commit to db, return
    if not Position.query.filter_by(symbol=trade.symbol, status='Open').all():
        position = Position(
            date_open=trade.date,
            status='Open',
            symbol=trade.symbol,
            entry=trade.price,
            size=trade.qty,
            net_cost=trade.price*trade.qty,
            qty=trade.qty,
            exit=0,
            pnl=0,
            direction=dir[trade.type],
            notes='',
            img=trade.img,
        )
        print(f'No trade exists, creating {position}, {position.symbol}, qty: {position.qty} ')
        db.session.add(position)
        db.session.commit()
        trade.position_id = position._id #add position relationship to trade entry
        db.session.commit()

        return

    # if an open trade exists, link new trade to position, update position data, return
    else:
        # if open pos != 1, return error msg
        if Position.query.filter_by(symbol=trade.symbol, status='Open').count() != 1:
            print('ERROR: open position qty mismatch')

        openpos = Position.query.filter_by(symbol=trade.symbol, status='Open').first()

        # If trade direction == position direction, update size and calc new avg entry
        if dir[trade.type] == openpos.direction:
            openpos.entry = (openpos.entry * openpos.size + trade.price * trade.qty) / (openpos.size + trade.qty)
            openpos.size += trade.qty
            openpos.qty += trade.qty
            openpos.net_cost += trade.qty * trade.price
            print(f'Adding {trade.qty} {trade.symbol} to {openpos}')

        # If trade direction != position direction, calc new avg exit and return, check if position closed
        else:
            pnl_dir = {'Long': 1, 'Short': -1}
            sold_qty = openpos.size - openpos.qty
            openpos.exit = (openpos.exit * sold_qty + trade.price * trade.qty) / (sold_qty + trade.qty)
            openpos.pnl = trade.qty * (trade.price - openpos.entry) * pnl_dir[openpos.direction]
            openpos.qty -= trade.qty
            print(f'Reducing {openpos} by {trade.qty} {trade.symbol}. Return of {openpos.pnl}')

            # If new trade reduces qty to 0, update position data and set status to "Closed"
            if openpos.qty == 0:
                print(f'Trade quantity zero, closing position {openpos}')
                openpos.status = 'Closed'

            # If new trade reduces qty past 0, throw error about selling/buying more than available

        trade.position_id = openpos._id # add trade as child to open position
        db.session.commit()
        return
