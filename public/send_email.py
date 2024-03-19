from flask import Flask, render_template_string, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def send_email(nome, email, password):
    try:
        # Configrações do servidor de email
        email_host = 'smtp.gmail.com'
        email_port = 587
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')

        # configurações do e-mail
        destinatario = email
        assunto = 'Nova Senha Portal Andrade'

        # Corpo do email com o link amigável para página HTML
        corpo_email = f"<p><strong>Olá, {nome}</strong></p><p>Segue sua nova senha gerada pelo Sistema: <strong>{password}</strong></p><p>Clique no link abaixo para alterar a senha de acesso:</p><p><a href='http://127.0.0.1:5000/alterar_senha' target='_blank'>Clique aqui</a></p><p>Atenciosamente,</p><p>Portal Andrade</p>"

        # Conectar-se ao servidor de e-mail e enviar o e-mail
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)

        mensagem = MIMEMultipart()
        mensagem['From'] = email_user
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto

        mensagem.attach(MIMEText(corpo_email, 'html'))

        server.sendmail(email_user, destinatario, mensagem.as_string())
        server.quit()

        return "E-mail enviado com sucesso!"

    except Exception as e:
        return render_template('erro.html', mensagem_de_erro=e)
