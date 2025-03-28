from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    email = EmailField(
        label="Elektronski naslov",
        validators=[
            InputRequired("Vnesi elektronski naslov!"),
            Length(min=6, max=100, message="Elektronski naslov je predolg!"),
        ],
    )

    password = PasswordField(
        label="Geslo",
        validators=[
            InputRequired("Vnesi geslo!"),
            Length(min=8, max=64, message="Geslo je predolgo!"),
        ],
    )
    remember_me = BooleanField(label="Ostani prijavljen", default=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
