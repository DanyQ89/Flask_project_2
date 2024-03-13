import json
from random import randint

from Forms import LoginForm
from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
# from data.news import News
from data.jobs import Jobs
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('./db/mars_explorer.sqlite')

# d = {'1': {'n_s': 'Энди Уир', 'prof': 'Астрогеолог'}, '2': {'n_s': 'Леша', 'prof': 'пчела'}}
# with open('./templates/data.json', 'wt', encoding='utf8') as file:
#     json.dump(d, file, ensure_ascii=False, indent=4)

users_array = []
@app.route("/")
def index0():
    db_sess = db_session.create_session()
    users = db_sess.query(User, Jobs).join(User, Jobs.team_leader == User.id).all()
    leaders = []

    for i in users:
        leader = db_sess.query(User).filter(User.id == i[1].team_leader).first()
        leaders.append(f'{leader.name} {leader.surname}')
        print(users)

    return render_template("index.html", users=users, leaders=leaders)


@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<profession>')
def training(profession):
    arr = ['инженер', 'строитель']
    if any([i in profession.lower() for i in arr]):
        heading = 'Инженерные тренажеры'
    else:
        heading = 'Научные симуляторы'

    return render_template('index_training.html', text=heading)


@app.route('/list_prof/<arr_type>')
def list_prof(arr_type):
    arr_prof = ['1', '2', '3']
    return render_template('prof_list.html', el=arr_type, arr=arr_prof)


@app.route('/answer')
def answer():
    title = 'Анкета'
    d = {'surname': 'Watny', 'name': 'Mark', 'education': 'выше среднего',
         'profession': "Штурман марсохода", 'sex': 'male', 'motivation': 'Всегда мечтал застрять на Марсе!',
         'ready': 'Да'}
    return render_template('auto_answer.html', d=d, title=title)


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            f = form.data
            print(f)
        except Exception:
            pass
        return redirect('/success')

    return render_template('login.html', form=form)


@app.route('/success')
def success():
    return 'Поздравляем с отправкой формы'


@app.route('/distribution')
def distribution():
    arr = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']
    return render_template('distr.html', arr=arr)


@app.route('/table_param/<sex>/<int:age>')
def table_param(sex, age):
    print(sex, age)
    color = 'white'
    photo = '../../static/img/'

    if age < 21:
        if sex == 'male':
            color = 'lightgrey'
        elif sex == 'female':
            color = '#FFDAB9'
    else:
        if sex == 'male':
            color = 'blue'
        elif sex == 'female':
            color = 'red'
    if sex == 'male':
        photo += 'male.png'
    elif sex == 'female':
        photo += 'female.png'
    return render_template('kauta.html', color=color, photo=photo)


@app.route('/member')
def member():
    with open('./templates/data.json', encoding='utf8') as file:
        a = json.load(file)
    rand_member = dict(sorted(list(a[str(randint(1, len(a)))].items())))

    return render_template('member.html', **rand_member)


arr = ['male.png', 'female.png']


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        file = request.files['filename']
        arr.append(file.filename)
    return render_template('carousel.html', arr=arr)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # db_sess = db_session.create_session()
        if db_sess.query(User).filter(form.email.data == User.email).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1', debug=True)
