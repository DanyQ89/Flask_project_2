from flask import Flask, render_template, redirect

from Forms import LoginForm

app = Flask(__name__, static_folder='./static')


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
        except Exception():
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
    return render_template('kauta.html')

if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1', debug=True)
