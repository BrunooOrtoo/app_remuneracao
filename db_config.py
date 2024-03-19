# db_config.py

import pyodbc
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_database_connection():
    try:
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_DATABASE')
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        driver = '{ODBC Driver 17 for SQL Server}'
        conn_str = 'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as ex:
        # Em vez de retornar render_template, registre o erro para depuração
        print("Erro ao conectar ao banco de dados:", ex)
        return None


