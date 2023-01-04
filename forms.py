from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateTimeField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class AddTradeForm(FlaskForm):
    date = DateTimeLocalField('Date', default=datetime.now(), validators=[DataRequired()])
    type = SelectField('Type', choices=['Buy', 'Sell'], validators=[DataRequired()], default="Buy")
    symbol = StringField('Symbol', validators=[DataRequired(), Length(max=10)], default="ETH")
    price = FloatField('Price', validators=[DataRequired()], default=1000)
    qty = FloatField('Quantity', validators=[DataRequired()], default=1)
    value = FloatField('Value', validators=[DataRequired()], default=1000)
    img = StringField('Image')
