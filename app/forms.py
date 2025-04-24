from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class ClientRegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    age = IntegerField("Age")
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")
