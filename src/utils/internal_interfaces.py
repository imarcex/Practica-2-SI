import sqlite3 
import hashlib
import requests
import pandas as pd
from os import path


FILEPATH = path.dirname(path.abspath(__file__))
LEGAL_DATA_PATH = f"{FILEPATH}/../data/legal_data_online.json"
USERS_DATA_PATH = f"{FILEPATH}/../data/users_data_online.json"
ROCKYOU_PATH = f"{FILEPATH}/../data/rockyou-20.txt"
DB_PATH = f"{FILEPATH}/../db/etl.db"
API_URL = 'https://api.pwnedpasswords.com/range'

connector = sqlite3.connect(DB_PATH, check_same_thread=False)

def __create_rainbow_table(fname: str):
    rainbowtable = {}
    md5 = hashlib.md5
    with open(fname,"r") as file:
        for line in file:
            hash= md5(line.strip().encode()).hexdigest()
            rainbowtable[hash] = line.strip()
    return rainbowtable

RAINBOWTABLE = __create_rainbow_table(ROCKYOU_PATH)

def __get_all_users():
    users = pd.read_sql_query("SELECT usuarios.username, usuarios.contrasena, emails.total, emails.cliclados FROM emails INNER JOIN usuarios ON emails.usuario = usuarios.username ORDER BY emails.cliclados DESC",connector)
    if users.empty == True:
        print("La query ha fallado bro")
        exit(-1)
    return users


def __get_all_critical_users():
    users = __get_all_users()
    critical_users = users[users['contrasena'].isin(RAINBOWTABLE.keys())]

    return critical_users


def __get_n_outdated_webs(sampleLength):
    webs = pd.read_sql_query("SELECT * FROM legal", connector)
    webs['politicas_desactualizadas'] = (webs[['cookies', 'aviso', 'proteccion_de_datos']] == 0).sum(axis=1).astype(int)
    top_webs_politicas_desactualizadas = webs.sort_values(['politicas_desactualizadas','creacion'], ascending=False).head(sampleLength)

    return top_webs_politicas_desactualizadas


def times_password_been_leaked(password: str):
    password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    url = f"{API_URL}/{password_hash[:5]}"
    print(url)
    response = requests.get(url)
    print(response.text)

    if response.status_code == 200:
        for line in response.text.splitlines():
            leaked_hash, ntimes = line.split(':')
            if leaked_hash == password_hash[5:]:
              return ntimes

    return 0
