import random
from flask import Flask, render_template, session, request, redirect
from utils.ejercicio2 import get_critical_users_clicked_spam
from functools import wraps
from utils.etl import ETL

app = Flask(__name__)
etl = ETL()

app.secret_key = random.randbytes(32)

def is_authenticated():
    username = session.get('username')
    return username and len(username.strip()) > 0

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect('/login?error=Unauthenticated')
        return f(*args, **kwargs)
    
    return wrapper

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

    if etl.login(username, password):
        session['username'] = username
        return redirect('/')
    else:
        return redirect('/login?error=Invalid credentials')


@app.route('/register')
def register():
    error = request.args.get('error')
    return render_template('register.html', error=error)


@app.route('/register', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']

    if etl.register(username, password):
        return redirect('/login')
    else:
        return redirect('/register?error=Username already in use')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login?error=Session closed')

def is_it_true(value):
    return value.lower() == 'true'

@app.route('/ejercicio2')
@login_required
def ejercicio2():
    sample_len = request.args.get("amount", required='True', type=int, default=5)
    above_fifty = request.args.get("above_fifty", type=is_it_true, default=True)

    data = get_critical_users_clicked_spam(sample_len, above_fifty)
    return render_template('ejercicio2', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)