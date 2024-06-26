
import requests
import urllib3
from dotenv import load_dotenv
from send_email import send_email
from realiza_cadastro import insert_data_into_db, select_data_primary_key, select_data_email, update_data_password, select_data_nome, select_data_key, select_data_operacao,select_data_unidade
from datetime import datetime
from password_generator import generate_random_password  # Importa a função para geração da senha aleatória
from validate_docbr import CPF
from services.pbiembedservice import PbiEmbedService
from utils import Utils
from flask import Flask, render_template, send_from_directory,request, redirect, url_for, jsonify
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Desativar warnings de certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

# Página de login
@app.route('/')
def index():
    return render_template('index.html')

# Verificação do login
@app.route('/index', methods=['POST'])
def do_login():
    if request.method == 'POST':
        recaptcha_response = request.form['g-recaptcha-response']
        secret_key = os.getenv('SECRET_KEY')  # Certifique-se de configurar a variável de ambiente
        response = requests.post('https://www.google.com/recaptcha/api/siteverify',
                                 data={'secret': secret_key, 'response': recaptcha_response})
        result = response.json()

        if result['success']:
            cpf = request.form['cpf']
            senha = request.form['password']

            # Verificar as credenciais do usuário (substitua pela sua lógica)
            busca_senha = select_data_key(cpf=cpf)
            operacao = select_data_operacao(cpf=cpf)
            unidade = select_data_unidade(cpf=cpf)

            if busca_senha == senha:
                def remover_zeros_esquerda(cpf):
                    return cpf.lstrip('0')
                cpf_sem_pontos = cpf.replace('.', '').replace('-', '')
                cpf_sem_zeros = remover_zeros_esquerda(cpf_sem_pontos)
                return render_template('home_page.html', cpf=cpf_sem_zeros, operacao=operacao, unidade=unidade)
            else:
                mensagem_de_erro = "Senha inválida."
                return render_template('erro.html', mensagem_de_erro=mensagem_de_erro)
        else:
            mensagem_de_erro = "Falha na validação do reCAPTCHA."
            return render_template('erro.html', mensagem_de_erro=mensagem_de_erro)
    else:
        return render_template('index.html')  # Renderizar o formulário de login

# Página de Cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Verificação do Cadastro
@app.route('/cadastro', methods=['POST'])
def do_cadastro():
    matricula = request.form['matricula']
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    senha = request.form['password']
    data_cadastro = datetime.now()
    data_alteracao = datetime.now()
    operacao = request.form['campo_selecao']
    unidade = request.form['campo_selecao_unidade']
    # Procura se o CPF está cadastrado
    search_primary_key = select_data_primary_key(cpf)

    cpf_validator = CPF()

    if cpf_validator.validate(cpf):
        if search_primary_key == cpf:
            mensagem_de_erro = "CPF já cadastrado"
            return render_template('erro.html', mensagem_de_erro=mensagem_de_erro)
        else:
            # Chama a função para inserir no banco de dados
            try:
                success = insert_data_into_db(matricula, nome, cpf, email, senha, data_cadastro, data_alteracao, operacao, unidade)
                return redirect(url_for('procedimento_concluido'))
            except Exception as ex:
                return render_template('erro.html', mensagem_de_erro=ex)
    else:
        mensagem_de_erro = "CPF Inválido"
        return render_template('erro.html', mensagem_de_erro=mensagem_de_erro)

# Envio Senha
@app.route('/envio_senha', methods=['POST'])
def envio_senha():
    cpf = request.form['cpf_alt']
    cpf_validator = CPF()
    nova_senha = generate_random_password()
    data_alteracao = datetime.now()
    nome = select_data_nome(cpf=cpf)
    email = select_data_email(cpf=cpf)

    if cpf_validator.validate(cpf):
        try:
            success = update_data_password(nova_senha=nova_senha,data_alterado=data_alteracao,cpf=cpf)
            #adicionar a função para envio de e-mail
            send_email(nome=nome,email=email,password=nova_senha)
            return redirect(url_for('procedimento_concluido'))
        except Exception as ex:
            return render_template('erro.html', mensagem_de_erro=ex)
    else:
        mensagem_de_erro = "CPF Inválido"
        return render_template('erro.html', mensagem_de_erro=mensagem_de_erro)

#Executado com Sucesso
@app.route('/procedimento_concluido')
def procedimento_concluido():
    return render_template('procedimento_concluido.html')

# Página Alterar Senha
@app.route('/alterar_senha')
def alterar_senha():
    return render_template('alterar_senha.html')

# Página Alterar Senha buscar nome
@app.route('/verifica_nome', methods=['POST'])
def do_verifica_nome():
    data = request.json['data']
    cpf_validator = CPF()
    if cpf_validator.validate(data):
        nome = select_data_nome(cpf=data)
        processed_data = nome
        return jsonify({'result': processed_data})
    else:
        mensagem_de_erro = "CPF não cadastrado. Realize o cadastro ou verifique o cpf informado."
        return render_template('erro.html', mensagem_de_erro=mensagem_de_erro)

#Página Alterar Senha
@app.route('/alterar_senha', methods=['POST'])
def do_alterar_senha():
    cpf = request.form['cpf']
    senha_ant = request.form['antpassword']
    busca_senha = select_data_key(cpf=cpf)
    if busca_senha != senha_ant:
        mensagem_de_erro = "Senha incorreta."
        return render_template('erro.html', mensagem_de_erro=mensagem_de_erro)
    else:
        nova_senha = request.form['password']
        data_alterado = datetime.now()
        update_data_password(nova_senha=nova_senha,data_alterado=data_alterado,cpf=cpf)
        return render_template('procedimento_concluido.html')

# Load configuration
app.config.from_object('config.BaseConfig')

#Página do Usuário
@app.route('/home_page')
def home_page():
    return render_template('home_page.html')

from flask import request, jsonify

# No código existente...

@app.route('/getembedinfo', methods=['GET'])
def get_embed_info():
    '''Returns report embed configuration'''
    config_result = Utils.check_config(app)
    if config_result is not None:
        return jsonify({'errorMsg': config_result}), 500
    try:
        # Obtenha os parâmetros de incorporação ajustados para o layout móvel
        embed_info = PbiEmbedService().get_embed_params_for_single_report(app.config['WORKSPACE_ID'], app.config['REPORT_ID'])

        # Modifique o embed_info para ajustar para layout móvel
        embed_info = json.loads(embed_info)
        embed_info['config'] = embed_info.get('config', '')
        embed_info['config'] += '&config=embedToolbarEnabled=true&navContentPaneEnabled=false&toolbarEnabled=false&mobile=true'

        return jsonify(embed_info)
    except Exception as ex:
        return jsonify({'errorMsg': str(ex)}), 500


# Página chat
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
if __name__ == '__main__':
    app.run(debug=True)