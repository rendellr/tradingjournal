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
    status = db.Column(db.String(10), default='Open', nullable=False)
    symbol = db.Column(db.String(200), nullable=False)
    cost_basis = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    net_cost = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(1000), default='')
    img = db.Column(db.String(200), default='')

    #def __init__(self):
    def __repr__(self):
        return f'<{self.symbol} Position {self._id}>'


class Trade(db.Model):
    __tablename__ = 'trade'
    _id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position._id'))
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    symbol = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(200), default='')

    def __repr__(self):
        return f'<{self.symbol} Trade {self._id}>'



