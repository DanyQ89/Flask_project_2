import json
from random import randint

from flask import Flask, render_template, redirect, request, make_response, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# from Forms import LoginForm
from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm, LoginForm, JobAdd, DepAdd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init('./db/mars_explorer.sqlite')
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index0():
    db_sess = db_session.create_session()
    users = db_sess.query(User, Jobs).join(User, Jobs.team_leader == User.id).all()
    print(users)
    leaders = []

    for i in users:
        leader = db_sess.query(User).filter(User.id == i[1].team_leader).first()
        leaders.append(f'{leader.name} {leader.surname}')

    return render_template("index.html", users=users, leaders=leaders)


@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<profession>')
def training(profession):
    arr_tr = ['инженер', 'строитель']
    if any([i in profession.lower() for i in arr_tr]):
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


@app.route('/login_old', methods=['GET', 'POST'], endpoint='login_old')
def login_old():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            f = form.data
        except Exception:
            pass
        return redirect('/success')

    return render_template('login_old.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(form.password.data, user.hashed_password)
        if user and form.password.data == user.hashed_password:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/success')
def success():
    return 'Поздравляем с отправкой формы'


@app.route('/distribution')
def distribution():
    arr_distr = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']
    return render_template('distr.html', arr=arr_distr)


@app.route('/table_param/<sex>/<int:age>')
def table_param(sex, age):
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
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(form.email.data == User.email).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()

        user.name = form.name.data
        user.email = form.email.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.hashed_password = form.password.data

        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobAdd()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Jobs).filter(form.title.data == Jobs.job).first():
            render_template('add_job.html', form=form, message='Такая работа уже существует')
        job = Jobs(
            team_leader=form.leader_id.data,
            job=form.title.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            hazard=form.hazard.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    # print(form.cs)
    return render_template('add_job.html', form=form)


@app.route('/edit_job/<int:id_job>', methods=['GET', 'POST'])
@login_required
def edit_job(id_job):
    form = JobAdd()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
        if job and current_user.id in [1, form.leader_id.data]:
            form.title.data = job.job
            form.leader_id.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.hazard.data = job.hazard
            form.is_finished.data = job.is_finished
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
        if job.job == form.title.data:
            job.team_leader = form.leader_id.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.hazard = form.hazard.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        return render_template('add_job.html', form=form, message='Название работы не должно изменяться')

    return render_template('add_job.html', form=form)


@app.route('/delete_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job and current_user.id in [1, job.team_leader]:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():
    db_sess = db_session.create_session()
    dep = db_sess.query(User, Department).join(User, Department.chief == User.id).all()

    return render_template('departments.html', deps=dep)


@app.route('/add_dep', methods=['GET', 'POST'])
@login_required
def add_dep():
    form = DepAdd()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if db_sess.query(Department).filter(form.email.data == Department.email).first():
            return render_template('add_dep.html', form=form, message='Такой департамент уже существует')
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )

        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')

    return render_template('add_dep.html', form=form)


@app.route('/edit_dep/<int:id_dep>', methods=['GET', 'POST'])
@login_required
def edit_dep(id_dep):
    form = DepAdd()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        old_dep = db_sess.query(Department).filter(Department.id == id_dep).first()
        if old_dep:
            form.title.data = old_dep.title
            form.chief.data = old_dep.chief
            form.members.data = old_dep.members
            form.email.data = old_dep.email

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id_dep).first()
        if dep.title == form.title.data:
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        return render_template('add_dep.html', form=form, message='Название департамента не должно изменяться')

    return render_template('add_dep.html', form=form)


@app.route('/delete_dep/<int:dep_id>')
@login_required
def delete_dep(dep_id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == dep_id).first()
    db_sess.delete(dep)
    db_sess.commit()
    return redirect('/departments')


if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1', debug=True)
