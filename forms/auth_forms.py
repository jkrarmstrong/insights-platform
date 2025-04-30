# --- Imports ---
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    """
    Form for user authentication.
    Contains fields for email, password and verification of password.
    """
    
    # Email and password with validation (i.e. mandatory)
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])


class LoginForm(FlaskForm):
    """
    Form for login. Contains fields for email and password.
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])