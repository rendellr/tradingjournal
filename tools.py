import csv
import json
from datetime import datetime
from models import Trade, Position, db
from bs4 import BeautifulSoup
import requests
import json

ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def import_csv(filename):
    dateformat = "%Y-%m-%d"
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
            price = float(trade['price'].replace("$", ""))
            qty = float(trade['qty'])
            value = round(price * qty, 2)
            # notes = 'notes text'
            # img = 'https://s3.tradingview.com/g/G1EOg7dj_mid.png'

            # create db entry
            new_trade = Trade(
                date=datetime.strptime(trade['date'], dateformat),
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

    with open('./data/coin_ids.json', 'r', encoding='utf-8') as file:
        coin_ids = json.loads(file.read())

    if coin_ids.get(trade.symbol.lower()):
        coin_id = coin_ids[trade.symbol.lower()]
    else:
        coin_id = ''

    # if no open positions exist, create new position, commit to db, return
    if not Position.query.filter_by(symbol=trade.symbol, status='Open').all():

        position = Position(
            date_open=trade.date,
            status='Open',
            symbol=trade.symbol,
            coin_id=coin_id,
            entry=trade.price,
            size=trade.qty,
            # net_cost=trade.price*trade.qty,
            qty=trade.qty,
            exit=0,
            pnl=0,
            direction=dir[trade.type],
            notes='',
            img=trade.img,
        )

        # print(f'No trade exists, creating {position}, {position.symbol}, qty: {position.qty} ')
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

        # If trade direction == position direction, recalc size and avg entry
        if dir[trade.type] == openpos.direction:
            openpos.entry = (openpos.entry * openpos.size + trade.price * trade.qty) / (openpos.size + trade.qty)
            openpos.size += trade.qty  # total position size !! assumes open and close trades happen in succession
            openpos.qty += trade.qty  # current pos qty remaining
            # openpos.net_cost += trade.qty * trade.price
            # print(f'Adding {trade.qty} {trade.symbol} to {openpos}')

        # If trade direction != position direction, recalc avg exit and pnl, check if position closed
        else:
            pnl_dir = {'Long': 1, 'Short': -1}
            sold_qty = openpos.size - openpos.qty
            openpos.exit = (openpos.exit * sold_qty + trade.price * trade.qty) / (sold_qty + trade.qty)
            openpos.pnl += trade.qty * (trade.price - openpos.entry) * pnl_dir[openpos.direction]
            openpos.qty -= trade.qty  # current pos qty remaining
            # print(f'Reducing {openpos} by {trade.qty} {trade.symbol}. Return of {openpos.pnl}')

            # If new trade reduces qty to "effective 0", update position data and set status to "Closed"
            # due to trading fees we often see mismatch b/w in & out qtys, i.e qty may not equal exact 0
            # if remaining position value is less than threshold_value, position is closed
            threshold_value = 20  # USD

            if openpos.qty * trade.price < threshold_value:
                # print(f'Trade quantity zero, closing position {openpos}')
                openpos.qty = 0
                if openpos.pnl > 0:
                    openpos.status = 'Win'
                else:
                    openpos.status = 'Loss'

            # TODO: If new trade reduces qty past 0, throw error about selling/buying more than available

        trade.position_id = openpos._id # add trade as child to open position
        db.session.commit()
        return

def get_coin_ids():
    # Takes asset symbols from positions db and finds corresponding coin gecko ids used for scraping live prices

    url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
    json_data = requests.get(url).json()
    coin_ids = {}

    for i in json_data:
        coin_ids[i['symbol']] = i['id']

    file = open('./data/coin_ids.json', 'w', encoding='utf-8')
    file.write(json.dumps(coin_ids))
    file.close()

    # COINMARKETCAP ATTEMPT - COULDN'T easily extract get a list of coin names
    # cmc = requests.get('https://coinmarketcap.com/')
    # print(cmc.status_code)  # 200
    # soup = BeautifulSoup(cmc.content, 'html.parser')
    #
    # data = soup.find('script', id="__NEXT_DATA__", type="application/json")  #CMC data stored as json in script tag
    # json_data = json.loads(data.contents[0])
    #
    # # cmc obfuscates their coin data, requiring some extraction and mapping list indexes with keys
    # # coin_list returns a list where entry 0 is a dict of key arrays: coin_list[0] = {'keysArr': [price, name, etc]}
    # # remaining entries are lists of values, matching the index of the keysArr. We need slug, symbol, and  keys.
    # json_table_data = json.loads(json_data['props']['initialState'])
    # coin_list = json_table_data['cryptocurrency']['listingLatest']['data']
    # slug_index = coin_list[0]['keysArr'].index('slug')
    # symbol_index = coin_list[0]['keysArr'].index('symbol')
    #
    # for i in range(len(coin_list))
    #
    # coins = {}
    #
    # for i in coin_data:
    #     coin_data['symbol']

def get_current_price():
    # Query list of coin_ids from open positions - convert to string and pass to CoinGecko API
    # Get prices using CoinGecko API https://www.coingecko.com/en/api/documentation

    open_pos = Position.query.all()
    ids = list(filter(None, [d.coin_id for d in open_pos]))
    ids_str = ','.join(ids)

    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=USD'
    gecko = requests.get(url).json()

    for i in open_pos:
        if i.coin_id and i.coin_id in ids_str:
            i.current_price = gecko[i.coin_id]['usd']
        else:
            i.current_price = 0
        db.session.commit()

    # #if open positions exist, scrape coingecko for prices and return dict of {symbol:price}, else return empty list?
    # if open_pos:
    #     for i in open_pos:
    #         if i.coin_id:
    #             gecko = requests.get(url + i.coin_id)
    #             print(f'Scraping data from {i.symbol} at {url + i.coin_id}')
    #             soup = BeautifulSoup(gecko.content, 'html.parser')
    #             price = soup.find(attrs={'data-target': 'price.price'})
    #             print(price.text)
    #             prices[i.coin_id] = price.text
    #
    # return prices


    # soup = BeautifulSoup(cmc.content, 'html.parser')
    #
    # data = soup.find('script', id="__NEXT_DATA__", type="application/json")  #CMC data stored as json in script tag
    # json_data = json.loads(data.contents[0])


