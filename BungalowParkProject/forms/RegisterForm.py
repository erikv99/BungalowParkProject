from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    
    user_name = StringField("Username:", validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField("Confirm password:", validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField("Register")