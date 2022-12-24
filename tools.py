import csv
from datetime import datetime
from app import Trade, db


def import_csv(filename):
    with open(filename, 'r') as csvfile:

        csvreader = csv.DictReader(csvfile)

        trades = []  # date, type, asset, price, qty
        for row in csvreader:
            trades.append(row)

        # If list is empty or keys do not match header, return error string
        header = ['date', 'type', 'asset', 'price', 'qty']
        print(header)
        print(trades[0].keys())

        if len(trades) == 0: return 'csv file is empty'
        if list(trades[0]) != header: return 'data format incorrect'

        # process data and save to database
        for trade in trades:
            # convert values to correct data type
            price = float(trade['price'])
            qty = float(trade['qty'])
            value = round(price * qty, 2)
            notes = 'notes text'
            img = 'https://s3.tradingview.com/g/G1EOg7dj_mid.png'

            # print (date, price, qty, value)

            # create db entry
            entry = Trade(
                date=datetime.strptime(trade['date'], "%Y-%m-%d"),
                type=trade['type'],
                asset=trade['asset'].upper(),
                price=price,
                qty=qty,
                value=value,
                notes=notes,
                img=img,
            )

            db.session.add(entry)
            db.session.commit()