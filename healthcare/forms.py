from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError

class Registrationform(FlaskForm):
    username = StringField("User_name", validators=[DataRequired(), length(min=4, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=6, max=20)])
    confirm_password = PasswordField("Confirm_password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class Loginform(FlaskForm):
    username = StringField("User_name", validators=[DataRequired(), length(min=4, max=15)]) 
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")   