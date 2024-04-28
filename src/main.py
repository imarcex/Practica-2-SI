import random
from flask import Flask, render_template, session, request, redirect
from utils.etl import ETL

app = Flask(__name__)
etl = ETL()

app.secret_key = random.randbytes(32)

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
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)