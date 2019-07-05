from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(Form):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField("Usuário", validators=[DataRequired()])

    password = PasswordField("Senha", validators=[DataRequired()])

    password2 = PasswordField("Confirmar senha", validators=[
        DataRequired(), EqualTo('password',
        message='-- Senhas não conferem! --')])

    name = StringField("Nome", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired()])


class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
