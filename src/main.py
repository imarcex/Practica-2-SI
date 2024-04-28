from flask import Flask, render_template, session, request

from utils.etl import ETL

app = Flask(__name__)
etl = ETL()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)