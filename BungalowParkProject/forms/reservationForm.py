from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired, Length

class ReservationForm(FlaskForm):
    
    bungalow_id = HiddenField(validators=[DataRequired()])
    date = DateField("Reservation week: ", validators=[DataRequired()])
    submit = SubmitField("Book")