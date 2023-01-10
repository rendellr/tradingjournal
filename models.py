from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() #initialize database

# Database setup
def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///positions.db' #config test.db file at relative location
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def db_drop_and_create(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

#models
class Position(db.Model):
    __tablename__ = 'position'
    _id = db.Column(db.Integer, primary_key=True)
    trades = db.relationship('Trade', backref='trade')
    date_open = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(10), default='Open', nullable=False)  # Open, Closed
    symbol = db.Column(db.String(50), nullable=False)  # Asset symbol
    coin_id = db.Column(db.String(50))  # coin_id is the id used by coin gecko; needed for scraping live prices
    entry = db.Column(db.Float, nullable=False)  # Average entry price
    size = db.Column(db.Float, nullable=False) #  total position size in shares/contract before any profit taking
    # net_cost = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Float, nullable=False)  # current position quantity
    exit = db.Column(db.Float)  # Average exit price
    pnl = db.Column(db.Float)  # Average profit or loss
    direction = db.Column(db.String(10))
    current_price = db.Column(db.Float)
    notes = db.Column(db.String(1000), default='')
    img = db.Column(db.String(200), default='')

    #def __init__(self):
    def __repr__(self):
        return f'<{self.symbol} Position {self._id}>'

    def to_dict(self):
        return {
            'status': self.status,
            'date_open': self.date_open,
            'symbol': self.symbol,
            'entry': self.entry,
            'exit': self.exit,
            'current_price': self.current_price,
            'pnl': self.pnl,
            'direction': self.direction
        }

class Trade(db.Model):
    __tablename__ = 'trade'
    _id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position._id'))
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(200), default='')

    def __repr__(self):
        return f'<{self.symbol} Trade {self._id}>'



