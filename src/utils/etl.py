import sqlite3
import json
from os import path

filepath = path.dirname(path.abspath(__file__))
LEGAL_DATA_PATH = f"{filepath}/../data/legal_data_online.json"
USERS_DATA_PATH = f"{filepath}/../data/users_data_online.json"

class ETL:
    def __init__ (self) -> None:
        self.connector = sqlite3.connect('etl.db')
        self.cursor = self.connector.cursor()

        if self.__create_tables():
            self.__insert_data()
            self.connector.commit()


    def __create_tables(self) -> bool:
        """
        Private: Create the tables if they are not created
        """
        query_find_tables = "SELECT name FROM sqlite_master WHERE \
            name='usuarios';"
        res = self.cursor.execute(query_find_tables)
        if res.fetchone() is None:
            self.cursor.execute('''CREATE TABLE legal (
                            web TEXT PRIMARY KEY,
                            cookies INTEGER,
                            aviso INTEGER,
                            proteccion_de_datos INTEGER,
                            creacion INTEGER
                            )''')

            # Tabla usuarios
            self.cursor.execute('''CREATE TABLE usuarios (
                            username TEXT PRIMARY KEY,
                            telefono INTEGER,
                            contrasena TEXT,
                            provincia TEXT,
                            permisos INTEGER,
                            fechas TEXT,
                            ips TEXT
                            )''')

            # Tabla emails
            self.cursor.execute('''CREATE TABLE emails (
                            usuario TEXT PRIMARY KEY,
                            total INTEGER,
                            phishing INTEGER,
                            cliclados INTEGER,
                            FOREIGN KEY (usuario) REFERENCES usuarios(username)
                            )''')
            return True
        else:
            return False

    def __insert_data(self) -> None:
            """
            Private: Insert the data from the json files
            """
            with open(LEGAL_DATA_PATH, 'r') as legal_data_online:
                legal = json.load(legal_data_online)['legal']

                for item in legal:
                    for website, data in item.items():
                        self.cursor.execute('''INSERT INTO legal (web, \
                            cookies, aviso, proteccion_de_datos, creacion)
                            VALUES (?, ?, ?, ?, ?);''',
                            (website, data['cookies'], data['aviso'], \
                             data['proteccion_de_datos'], data['creacion'])
                        )

            with open(USERS_DATA_PATH, 'r') as users_data_online:
                users = json.load(users_data_online)['usuarios']
                for item in users:
                    for username, data in item.items():
                        self.cursor.execute('''INSERT INTO usuarios (username, \
                            telefono, contrasena, provincia, permisos)
                            VALUES (?, ?, ?, ?, ?);''',
                            (username, data['telefono'], data['contrasena'],
                             data['provincia'], data['permisos'])
                        )

                        self.cursor.execute('''INSERT INTO emails (usuario, \
                            total, phishing, cliclados)
                            VALUES (?, ?, ?, ?);''',
                            (username, data['emails']['total'], \
                             data['emails']['phishing'], \
                             data['emails']['cliclados'])
                        )

                        for fecha in data['fechas']:
                            self.cursor.execute('''INSERT INTO fechas (usuario, \
                                fecha)
                                VALUES (?, ?);''',
                                (username, fecha)
                            )

                        if data['ips'] != "None":
                            for ip in data['ips']:
                                self.cursor.execute('''INSERT INTO ips\
                                    (usuario, ip)
                                    VALUES (?, ?);''',
                                    (username, ip)
                                )