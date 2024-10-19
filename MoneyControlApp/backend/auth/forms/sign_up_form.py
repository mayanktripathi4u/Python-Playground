from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from models.user import User

class RegisterForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    # Custom email validation to check if email is already in use
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("This email is already registered. Please choose another one.")
