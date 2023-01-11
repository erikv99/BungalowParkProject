from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired

class ChangeWeekForm(FlaskForm):
    
    reservation_id = HiddenField(validators=[DataRequired()])
    date = DateField("Select week: ", validators=[DataRequired()])
    submit = SubmitField("Change")