from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    nickname = StringField('Имя', [DataRequired()])
    email = StringField('Электронная почта', [DataRequired(), Email()])
    password = StringField('Пароль', [DataRequired()])
    submit = SubmitField('Зарегистрироваться')

class AuthorizationForm(FlaskForm):
    email = StringField('Электронная почта', [DataRequired(), Email()])
    password = StringField('Пароль', [DataRequired()])
    submit = SubmitField('Войти')