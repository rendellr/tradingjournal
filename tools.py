import csv
from datetime import datetime


def import_csv(filename):

    with open(filename, 'r') as csvfile:

        csvreader = csv.DictReader(csvfile)

        trades = [] # date, type, asset, price, qty
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

            # convert entries to correct data type
            price = float(trade['price'])
            qty = float(trade['qty'])
            date = datetime.strptime(trade['date'], "%Y-%m-%d")
            value = round(price * qty, 2)

            print (date, price, qty, value)
            # _id
            # date
            # asset
            # price
            # qty
            # value
            # notes
            # img





