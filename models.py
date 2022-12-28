from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() #initialize database

# Database setup
def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #config test.db file at relative location
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

#models
class Trade(db.Model):
    __tablename__ = 'trades'
    _id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    asset = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(1000), default='')
    img = db.Column(db.String(200), default='')

    def __repr__(self):
        return '<Trade> %r' % self._id

