import pyodbc
from flask import render_template
from db_config import get_database_connection


def select_data_key(cpf):
    conn = get_database_connection()
    cursor = conn.cursor()
    # Executa o INSERT na tabela tb_login
    cursor.execute("SELECT c_senha FROM tb_login WHERE c_cpf = ?",cpf)
    try:
        results = cursor.fetchall()
        return results[0][0]
        conn.commit()
        conn.close()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)

def select_data_nome(cpf):
    conn = get_database_connection()
    cursor = conn.cursor()
    # Executa o INSERT na tabela tb_login
    cursor.execute("SELECT c_nome FROM tb_login WHERE c_cpf = ?",cpf)
    try:
        results = cursor.fetchall()
        return results[0][0]
        conn.commit()
        conn.close()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)

def update_data_password(nova_senha, data_alterado, cpf):
    conn = get_database_connection()
    cursor = conn.cursor()
    # Executa o UPDATE na tabela tb_login
    cursor.execute("UPDATE tb_login SET [c_senha] = ?, [c_alterado] = ? WHERE c_cpf = ?",nova_senha, data_alterado, cpf)
    try:
        conn.commit()
        conn.close()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)

def select_data_email(cpf):
    conn = get_database_connection()
    cursor = conn.cursor()
    # Executa o INSERT na tabela tb_login
    cursor.execute("SELECT c_email FROM tb_login WHERE c_cpf = ?",cpf)
    try:
        results = cursor.fetchall()
        return results[0][0]
        conn.commit()
        conn.close()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)

def select_data_primary_key(cpf):
    conn = get_database_connection()
    cursor = conn.cursor()
    # Executa o INSERT na tabela tb_login
    cursor.execute("SELECT c_cpf FROM tb_login WHERE c_cpf = ?",cpf)
    try:
        results = cursor.fetchall()
        return results[0][0]
        conn.commit()
        conn.close()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)

def insert_data_into_db(matricula, nome, cpf, email, senha, data_criacao, data_alteracao):
    conn = get_database_connection()
    cursor = conn.cursor()
    #Executa o INSERT na tabela tb_login
    cursor.execute("INSERT INTO tb_login (c_matricula,c_nome,c_cpf,c_email,c_senha,c_criado,c_alterado) \
                   VALUES (?, ?, ?, ?, ?, ?, ?)",matricula, nome, cpf, email, senha, data_criacao, data_alteracao)
    try:
        conn.commit()
        conn.close()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)

