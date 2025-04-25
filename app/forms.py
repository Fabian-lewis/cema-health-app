from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp


# Client Registration Form
# This form is used to register a new client
# Form validators are used to validate the form data before it is submitted to the database
class ClientRegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    date_of_birth = DateField("Date of Birth", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female")])
    # phone number is validated to ensure it is a valid phone number with 10-15 digits and + allowed at start 
    phone = StringField("Phone Number", validators=[DataRequired(),Regexp(r'^\+?\d{10,15}+$', message="Enter digits only, + allowed at start, 10-15 digits allowed")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")
    

# Login Form
# This form is used to login a user
# The form validators used here are DataRequired and Length
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")
