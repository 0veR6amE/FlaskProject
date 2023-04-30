import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from sqlalchemy import update, select
from werkzeug.utils import secure_filename

from data import db_session
from data.users import User
from forms.login import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_for_flask_project'
app.config['SERVER_NAME'] = "127.0.0.1:5000"
app.config['UPLOAD_FOLDER'] = \
    'C:/Users/ASUS/PycharmProjects/FlaskProject/user/download/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CURRENT_USER = None

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/test')
def test():
    return render_template('test.html')


@app.route("/")
def home():
    return render_template("main.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/en_log/")


@app.route("/en/")
@login_required
def en_home_reg():
    if CURRENT_USER:
        return render_template('en/main.html', username=CURRENT_USER)
    else:
        return redirect('/en_log/')


@app.route("/en_log/")
def en_home_non_reg():
    return render_template('en/main_non_reg.html')


# noinspection PyTypeChecker,PyArgumentList
@app.route('/en_log/register/', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('en/phhot/register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('en/phhot/register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if not form.username.data:
            username = form.name.data
        else:
            username = form.username.data
        user = User(
            name=form.name.data,
            username=username,
            email=form.email.data,
            about=form.about.data,
            balance=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/en/login/')
    return render_template('en/register.html', title='Регистрация',
                           form=form)


# noinspection PyTypeChecker
@app.route('/en_log/login/', methods=['GET', 'POST'])
def login():
    global CURRENT_USER
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User
                             ).filter(User.email == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            CURRENT_USER = form.login.data
            print(CURRENT_USER)
            return redirect("/en/")
        return render_template('/en/login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('/en/login.html', form=form)


@app.route("/en/casino/")
def en_casino_startscreen():
    return render_template("en/casino/startscreen.html", username='lox',
                           balance='0')


def slots_prokrutka(balance, bet):
    from random import choice

    print('begin')
    im = '../../../static/img/casino/'
    cells = {'7': im + '7.png', 'b': im + 'banana.png', 'B': im + 'bigwin.png',
             'c': im + 'cherry.png', 'd': im + 'drain.png',
             'l': im + 'lemon.png',
             'o': im + 'orange.png', 's': im + 'strawberry.png',
             'w': im + 'watermelon.png'}
    combos = {'ccc': 10, 'bbb': 15, 'ddd': 20, 'lll': 25, 'ooo': 30, 'sss': 35,
              'www': 40, '777': 50, 'BBB': 100}
    drawings = ['7', 'b', 'B', 'c', 'd', 'l', 'o', 's', 'w']
    win = 0
    result = ''
    pics = []
    if 0 < bet <= balance:  # прокрутка
        count = 0
        while count < 3:  # иконочка
            result += choice(drawings)
            count += 1
        for i in result:
            pics.append(cells.get(i))  # картиночка
        if result in combos.keys():  # проверка результата на коэф
            win = bet * combos.get(result)
        elif 'BB' in result:
            win = bet * 5
        elif 'B' in result:
            win = bet * 2
        else:
            win = -bet
    else:
        result = 'неверная ставка или недостаточно средств'
    balance += win
    return (result, pics, win, balance)


@app.route("/en/casino/slots/", methods=['POST', 'GET'])
def en_casino_slots():
    if CURRENT_USER:
        price = 0
        for key, value in request.form.items():
            if key == 'price':
                price = int(value)
        print(price)
        db_sess = db_session.create_session()
        user_balance = db_sess.execute(select(User.balance).filter(
            User.email == CURRENT_USER)).first()[0]
        if price:
            result, pics, win, balance = slots_prokrutka(user_balance, price)
            db_sess.query(User).filter_by(email=CURRENT_USER).update(
                {"balance": balance})
            db_sess.commit()
            return render_template("en/casino/slots.html", username=CURRENT_USER,
                                   balance=balance, win=win, result=result,
                                   first=pics[0], second=pics[1], thrid=pics[2])
        db_sess.commit()
        return render_template("en/casino/slots.html", username=CURRENT_USER,
                               balance=user_balance, win=0, result='',
                               first='../../../static/img/casino/7.png',
                               second='../../../static/img/casino/7.png',
                               thrid='../../../static/img/casino/7.png  ')
    return redirect('/en_log/login/')


@app.route("/en/casino/roulette/")
def en_casino_roulette():
    return render_template("en/casino/roulette.html", username='lox',
                           balance='0')


@app.route("/en/casino/crash/")
def en_casino_crash():
    return render_template("en/casino/crash.html", username='lox', balance='0')


@app.route("/en/phhot/home")
def en_phhot_home():
    return render_template("en/phhot/index.html")


@app.route("/en_log/phhot/home")
def en_log_phhot_home():
    return render_template("en/phhot/index.html")


@app.route("/en/phhot/about")
def en_phhot_about():
    return render_template("en/phhot/about.html")


@app.route("/en_log/phhot/about")
def en_log_phhot_about():
    return render_template("en/phhot/about.html")


@login_required
@app.route("/en/phhot/redactor", methods=['GET', 'POST'])
def login_en_phhot_redactor():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл
        if 'file' not in request.files:
            return render_template("en/phhot/photo_redact.html",
                                   message='Не могу прочитать файл')
        file = request.files['file']
        if file.filename == '':
            return render_template("en/phhot/photo_redact.html",
                                   message='Нет выбранного файл')
        if allowed_file(file.filename):
            if file:
                # безопасно извлекаем оригинальное имя файла
                filename = secure_filename(file.filename)
                # сохраняем файл
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # если все прошло успешно, то перенаправляем
                # на функцию-представление `download_file`
                # для скачивания файла
                return render_template("en/phhot/photo_redact.html",
                                       message='Файл загружен')
        else:
            return render_template("en/phhot/photo_redact.html",
                                   message='Файл не того типа')
    return render_template("en/phhot/photo_redact.html", message='')


@app.route("/en/phhot/redactor", methods=['GET'])
def en_phhot_paint():
    print(request.values)
    return render_template("en/paint/index.html")


@app.route("/en_log/phhot/redactor", methods=['GET'])
def en_log_phhot_paint():
    print(request.values)
    return render_template("en/paint/index.html")


@app.route('/en/shop/home')
def shop_home():
    return render_template('/en/shop/base.html')


@app.route('/en_log/shop/home')
def log_shop_home():
    return render_template('/en/shop/base.html')


@app.route('/en_log/game')
def en_game():
    return render_template('en/game/index.html')


def add_balance(balance):
    if CURRENT_USER:
        db_sess = db_session.create_session()
        user_balance = db_sess.execute(select(User.balance).filter(User.email == CURRENT_USER)).first()
        b = balance + user_balance[0]
        db_sess.query(User).filter_by(email=CURRENT_USER).update({"balance":b})
        db_sess.commit()
    else:
        return redirect('/en_log/login/')


@app.route('/en_log/shop/free/unsuccess')
def log_free_shop_success0():
    return redirect('/en_log/login')


@app.route('/en_log/shop/amature/unsuccess')
def log_amature_shop_success0():
    return redirect('/en_log/login')


@app.route('/en_log/shop/profession/unsuccess')
def log_profession_shop_success0():
    return redirect('/en_log/login')


@app.route('/en/shop/free/unsuccess')
def free_shop_success0():
    return redirect('/en_log/login')


@app.route('/en/shop/amature/unsuccess')
def amature_shop_success0():
    return redirect('/en_log/login')


@app.route('/en/shop/profession/unsuccess')
def profession_shop_success0():
    return redirect('/en_log/login')


@app.route('/en/shop/free/success')
@login_required
def free_shop_success1():
    print(1)
    add_balance(1500)
    return '<h1>НЕ ЗАБЫТЬ РАЗРАБОТАТЬ ДИЗАЙН</h1>'


@app.route('/en/shop/amature/success')
@login_required
def amature_shop_success1():
    add_balance(3000)
    return '<h1>НЕ ЗАБЫТЬ РАЗРАБОТАТЬ ДИЗАЙН</h1>'


@app.route('/en/shop/profession/success')
@login_required
def profession_shop_success1():
    add_balance(5000)
    return '<h1>НЕ ЗАБЫТЬ РАЗРАБОТАТЬ ДИЗАЙН</h1>'


@app.route("/ru/")
def ru_home():
    return "<h1>Пока не поддерживается</h1>"


def main():
    db_session.global_init("databases/db.db")
    app.run(debug=True)


"""<form class="d-flex" role="search">
                <input class="form-control me-2" type="search"
                       placeholder="Search" aria-label="Search">
            </form>"""

if __name__ == '__main__':
    main()
