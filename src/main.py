from utils.etl import ETL
etl = ETL()

import random
import numpy as np
from flask import Flask, render_template, session, request, redirect, jsonify
from utils.ejercicio1 import get_n_crtitical_users, get_n_outdated_webs
from utils.ejercicio2 import get_critical_users_clicked_spam
from utils.ejercicio4 import times_hash_been_leaked, times_password_been_leaked
from utils.ejercicio3 import get_latest_vulns
from utils.ejercicio5 import linearRegression, decisionTree, randomForest
from utils.internal_interfaces import __get_user_passwd_hash
from functools import wraps

app = Flask(__name__)

app.secret_key = random.randbytes(32)

def is_arg_true(value):
    return value.lower() == 'true'

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


@app.route('/api/ejercicio1', methods=['POST'])
@login_required
def api_ej1():
    sample_len = int(request.form.get("length", default=5))
    data = {}
    data['users'] = get_n_crtitical_users(sample_len)
    data['webs'] = get_n_outdated_webs(sample_len)
    return jsonify(data)


@app.route('/api/ejercicio2', methods=['POST'])
@login_required
def api_ej2():
    sample_len = request.form.get("length", default=5)
    above_fifty = request.form.get("above_fifty", type=is_arg_true, default=True)

    data = get_critical_users_clicked_spam(int(sample_len), bool(above_fifty))
    return jsonify(data)


@app.route('/api/ejercicio3', methods=['GET'])
@login_required
def api_ej3():
    return jsonify(get_latest_vulns())


@app.route('/api/ejercicio4', methods=['POST'])
@login_required
def api_ej4():
    passwd = request.form.get('password')
    data = times_password_been_leaked(passwd)
    return jsonify(data)
    

@app.route('/ejercicio1')
@login_required
def ejercicio1():
    return render_template('ejercicio1.html')

@app.route('/ejercicio2')
@login_required
def ejercicio2():
    return render_template('ejercicio2.html')

@app.route('/ejercicio3')
@login_required
def ejercicio3():
    return render_template('ejercicio3.html')

@app.route('/ejercicio4')
@login_required
def ejercicio4():
    passw_hash = __get_user_passwd_hash(session.get('username'))
    data = times_hash_been_leaked(passw_hash)
    return render_template('ejercicio4.html', data=data)

@app.route('/ejercicio5')
@login_required
def ejercicio5_get():
    return render_template('ejercicio5.html')

@app.route('/ejercicio5', methods=['POST'])
@login_required
def ejercicio5():
    if request.method == 'POST':
        username = request.form['username']
        totalEmails = int(request.form['totalMails'])
        phishingEmails = int(request.form['phishingMails'])
        clickedEmails = int(request.form['clickedMails'])
        iamodel = request.form['iamodel']

        if iamodel == 'linear':
            model = linearRegression()
            prediction = model.predict(np.array([[float(clickedEmails/phishingEmails)]]))

        elif iamodel == 'tree':
            model = decisionTree()
            prediction = model.predict(np.array([[totalEmails, phishingEmails, clickedEmails]]))

        elif iamodel == 'forest':
            model = randomForest()
            prediction = model.predict(np.array([[totalEmails, phishingEmails, clickedEmails]]))
        
        if prediction == 1:
            return render_template('ejercicio5_data.html', prediction=f'Usuario {username} critico')

        return render_template('ejercicio5_data.html', prediction=f'Usuario {username} no critico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)