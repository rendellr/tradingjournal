from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateTimeField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class AddTradeForm(FlaskForm):
    date = DateTimeLocalField('date', default=datetime.now(), validators=[DataRequired()])
    type = SelectField('type', choices=['Buy', 'Sell'], validators=[DataRequired()])
    symbol = StringField('symbol', validators=[DataRequired(), Length(max=10)])
    price = FloatField('price', validators=[DataRequired()])
    qty = FloatField('qty', validators=[DataRequired()])
    value = FloatField('value', validators=[DataRequired()])
    img = StringField('symbol')
