from flask_wtf import FlaskForm, RecaptchaField
from wtforms import EmailField, PasswordField
from wtforms.validators import EqualTo, InputRequired, Length


class RegisterForm(FlaskForm):
    email = EmailField(
        "Elektronski naslov",
        validators=[InputRequired(), Length(min=6, max=40)],
    )
    password = PasswordField(
        "Geslo", validators=[InputRequired(), Length(min=8, max=64)]
    )
    password_confirm = PasswordField(
        "Geslo (ponovno)",
        validators=[
            InputRequired(),
            EqualTo("password", message="Gesli se ne ujemata!"),
        ],
    )
    recaptcha = RecaptchaField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
