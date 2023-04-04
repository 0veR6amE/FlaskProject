from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SERVER_NAME'] = "127.0.0.1:5000"


@app.route('/test')
def test():
    return render_template('test.html')


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/en/")
def en_home():
    return render_template('en/main.html')


@app.route("/en/phhot/about")
def en_phhot_about():
    return render_template("en/phhot/about.html")


@app.route("/en/phhot/home")
def en_phhot_home():
    return render_template("en/phhot/index.html")


@app.route("/ru/")
def ru_home():
    return render_template('ru/main.html')


@app.route("/ru/phhot/about")
def ru_phhot_about():
    return render_template("ru/about.html")


@app.route("/ru/phhot/home")
def ru_phhot_home():
    return render_template("ru/base.html")


def main():
    app.run(debug=True)


"""<form class="d-flex" role="search">
                <input class="form-control me-2" type="search"
                       placeholder="Search" aria-label="Search">
            </form>"""
if __name__ == '__main__':
    main()
