from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username_astr = StringField('Id астронавта', validators=[DataRequired()])
    password_astr = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username_cap = StringField('Id капитана', validators=[DataRequired()])
    password_cap = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')
