FROM python:3.8-slim

# Instalação do utilitário curl e do pacote gnupg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Adiciona a chave do repositório Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Adiciona o repositório do SQL Server ao sources.list
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Atualiza o índice de pacotes com os novos repositórios e instala o driver ODBC do SQL Server 17
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala o código-fonte da sua aplicação e suas dependências do Python
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para iniciar o servidor
CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]
