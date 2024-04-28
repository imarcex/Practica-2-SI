import random
from flask import Flask, render_template, session, request
from utils.etl import ETL

app = Flask(__name__)
etl = ETL()

app.secret = random.randbytes(16)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    error = request.args.get('error')
    return render_template('login.html', error=error)


@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'admin':
        session['username'] = username
        return 'Login success'
    else:
        return 'Login failed'


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']

    etl.register(username, password)
    return 'Register success'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'Logout success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)