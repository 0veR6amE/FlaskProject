import os

from flask import Flask, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm
from data.inventory import Value

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_for_flask_project'
app.config['SERVER_NAME'] = "127.0.0.1:5000"
app.config['UPLOAD_FOLDER'] = \
    'C:/Users/4444/PycharmProjects/FlaskProject_Git_Hub/user/download/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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


@app.route("/en/")
def en_home():
    return render_template('en/main.html')


@app.route("/en/casino/")
def en_casino_startscreen():
    return render_template("en/casino/startscreen.html", username='lox', balance='0')


@app.route("/en/casino/slots")
def en_casino_slots():
    return render_template("en/casino/slots.html", username='lox', balance='0')


@app.route("/en/paint/home")
def painter_paint():
    return render_template('en/paint/index.html')


@app.route("/en/phhot/about")
def en_phhot_about():
    return render_template("en/phhot/about.html")


@app.route("/en/phhot/home")
def en_phhot_home():
    return render_template("en/phhot/index.html")


@app.route("/en/phhot/redactor", methods=['GET', 'POST'])
@login_required
def login_en_phhot_redactor():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл
        if 'file' not in request.files:
            return render_template("en/phhot/photo_redact.html", message='Не могу прочитать файл')
        file = request.files['file']
        if file.filename == '':
            return render_template("en/phhot/photo_redact.html", message='Нет выбранного файл')
        if allowed_file(file.filename):
            if file:
                # безопасно извлекаем оригинальное имя файла
                filename = secure_filename(file.filename)
                # сохраняем файл
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # если все прошло успешно, то перенаправляем
                # на функцию-представление `download_file`
                # для скачивания файла
                return render_template("en/phhot/photo_redact.html", message='Файл загружен')
        else:
            return render_template("en/phhot/photo_redact.html",
                                   message='Файл не того типа')
    return render_template("en/phhot/photo_redact.html", message='')


@app.route("/en/phhot/redactor", methods=['GET', 'POST'])
def en_phhot_redactor():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл
        if 'file' not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            # сохраняем файл
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # если все прошло успешно, то перенаправляем
            # на функцию-представление `download_file`
            # для скачивания файла
            return render_template("en/phhot/index.html")
    return render_template("en/phhot/redactor.html")


# noinspection PyTypeChecker,PyArgumentList
@app.route('/en/phhot/register', methods=['GET', 'POST'])
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
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/en/phhot/login')
    return render_template('en/phhot/register.html', title='Регистрация',
                           form=form)


# noinspection PyTypeChecker
@app.route('/en/phhot/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User
                             ).filter(User.email == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/en/phhot/home")
        return render_template('/en/phhot/login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('/en/phhot/login.html', form=form)


@app.route('/en/shop/home')
def shop_home():
    return render_template('/en/shop/base.html')


@app.route('/en/shop/home/success', methods=['POST'])
def shop_success():
    db_sess = db_session.create_session()
    if 'Free' in request.POST:
        name = 'Free'
    elif 'Amateur' in request.POST:
        name = 'Amateur'
    elif 'Professional' in request.POST:
        name = 'Professional'

    value = Value(
        name=name,
    )
    db_sess.add(value)
    db_sess.commit()
    print('1')
    return render_template('НЕ ЗАБЫТЬ РАЗРАБОТАТЬ ДИЗАЙН ДЕБИЛЫ')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/en/")


@app.route("/ru/")
def ru_home():
    return render_template('ru/main.html')


@app.route("/ru/phhot/about")
def ru_phhot_about():
    return render_template("ru/phhot/about.html")


@app.route("/ru/phhot/home")
def ru_phhot_home():
    return render_template("ru/phhot/base.html")


def main():
    db_session.global_init("databases/phhot.db")
    app.run(debug=True)


"""<form class="d-flex" role="search">
                <input class="form-control me-2" type="search"
                       placeholder="Search" aria-label="Search">
            </form>"""

if __name__ == '__main__':
    main()
