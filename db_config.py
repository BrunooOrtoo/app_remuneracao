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
        driver = 'ODBC Driver 17 for SQL Server'

        # Adicione os parâmetros de timeout à string de conexão
        conn_str = (
            'DRIVER=' + driver + ';'
            'SERVER=' + server + ';'
            'DATABASE=' + database + ';'
            'UID=' + username + ';'
            'PWD=' + password + ';'
            'TIMEOUT=30;'  # Defina o tempo limite da conexão para 30 segundos
            'QUERY_TIMEOUT=60;'  # Defina o tempo limite da consulta para 60 segundos
        )

        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as ex:
        # Em vez de retornar render_template, registre o erro para depuração
        print("Erro ao conectar ao banco de dados:", ex)
        return None



