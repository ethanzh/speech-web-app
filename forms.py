from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class CreateAccountForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "New Password",
        [DataRequired(), EqualTo("confirm_password", message="Passwords must match")],
    )
    confirm_password = PasswordField("Confirm Password")
    gender = SelectField(
        "Gender",
        choices=["Male", "Female", "Prefer not to say"],
        validators=[DataRequired()],
    )
    age_range = SelectField(
        "Age Range",
        default="18-25",
        choices=["Under 18", "18-25", "25-40", "40-60", "Above 60"],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create Account")
