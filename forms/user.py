from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Позиция', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])

    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobAdd(FlaskForm):
    title = StringField('Название работы', validators=[DataRequired()])
    leader_id = IntegerField('ID капитана команды', validators=[DataRequired()])
    work_size = IntegerField('Количество работы в часах', validators=[DataRequired()])
    collaborators = StringField('ID работников', validators=[DataRequired()])
    is_finished = BooleanField('Работа закончена?')
    submit = SubmitField('Добавить')


class DepAdd(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    chief = IntegerField('Капитан', validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    email= EmailField('Почта', validators=[DataRequired()])

    submit = SubmitField('Добавить')
