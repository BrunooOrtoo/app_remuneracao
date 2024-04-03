import pyodbc
from flask import render_template
from db_config import get_database_connection


def select_data_key(cpf):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o SELECT na tabela tb_login
        cursor.execute("SELECT c_senha FROM tb_login WHERE c_cpf = ?", (cpf,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except Exception as ex:
        # Em vez de retornar o template HTML, registre o erro para depuração
        print("Erro ao buscar senha no banco de dados:", ex)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def select_data_nome(cpf):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o SELECT na tabela tb_login
        cursor.execute("SELECT c_nome FROM tb_login WHERE c_cpf = ?", (cpf,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_data_password(nova_senha, data_alterado, cpf):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o UPDATE na tabela tb_login
        cursor.execute("UPDATE tb_login SET [c_senha] = ?, [c_alterado] = ? WHERE c_cpf = ?", (nova_senha, data_alterado, cpf))
        conn.commit()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def select_data_email(cpf):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o SELECT na tabela tb_login
        cursor.execute("SELECT c_email FROM tb_login WHERE c_cpf = ?", (cpf,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def select_data_primary_key(cpf):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o SELECT na tabela tb_login
        cursor.execute("SELECT c_cpf FROM tb_login WHERE c_cpf = ?", (cpf,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_data_into_db(matricula, nome, cpf, email, senha, data_criacao, data_alteracao, operacao, unidade):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o INSERT na tabela tb_login
        cursor.execute("INSERT INTO tb_login (c_matricula,c_nome,c_cpf,c_email,c_senha,c_criado,c_alterado,c_operacao,c_unidade) \
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (matricula, nome, cpf, email, senha, data_criacao, data_alteracao, operacao, unidade))
        conn.commit()
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def select_data_operacao(cpf):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o SELECT na tabela tb_login
        cursor.execute("SELECT c_operacao FROM tb_login WHERE c_cpf = ?", (cpf,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def select_data_unidade(cpf):
    conn = None
    cursor = None
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        # Executa o SELECT na tabela tb_login
        cursor.execute("SELECT c_unidade FROM tb_login WHERE c_cpf = ?", (cpf,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except Exception as ex:
        return render_template('erro.html', mensagem_de_erro=ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()