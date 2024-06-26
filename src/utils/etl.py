import json
import hashlib
from utils.internal_interfaces import LEGAL_DATA_PATH, USERS_DATA_PATH, connector

class ETL:
    def __init__ (self) -> None:
        self.connector = connector
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
                            ips TEXT,
                            esCritico INTEGER
                            )''')

            # Tabla emails
            self.cursor.execute('''CREATE TABLE emails (
                            usuario TEXT PRIMARY KEY,
                            total INTEGER,
                            phishing INTEGER,
                            cliclados INTEGER,
                            FOREIGN KEY (usuario) REFERENCES usuarios(username)
                            )''')
            
            self.cursor.execute('''CREATE TABLE login (
                            username TEXT PRIMARY KEY,
                            password TEXT
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
                            telefono, contrasena, provincia, permisos, fechas, ips, esCritico)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                            (username, data['telefono'], data['contrasena'],
                             data['provincia'], data['permisos'], ' '.join(data['fechas']), \
                                ' '.join(data['ips']), data['critico'])
                        )

                        self.cursor.execute('''INSERT INTO emails (usuario, \
                            total, phishing, cliclados)
                            VALUES (?, ?, ?, ?);''',
                            (username, data['emails']['total'], \
                             data['emails']['phishing'], \
                             data['emails']['cliclados'])
                        )
    
    def register(self, username: str, password: str) -> bool:
        """
        Register a new user, returns false if the usernam is in use, using prepared statements
        """
        query = "INSERT INTO login (username, password) VALUES (?, ?);"
        try:
            self.cursor.execute(query, (username, hashlib.sha1(password.encode()).hexdigest().upper()))
            self.connector.commit()
            return True
        except:
            return False
        
    def login(self, username: str, password: str) -> bool:
        """
        Check if the user and password are correct
        """
        query = "SELECT username FROM login WHERE username = ? AND password = ?;"
        res = self.cursor.execute(query, (username, hashlib.sha1(password.encode()).hexdigest().upper()))
        return res.fetchone() is not None