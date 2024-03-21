FROM python:3.8-slim

# Atualize o índice de pacotes e instale as dependências necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Instale o driver ODBC do SQL Server 17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copie o código-fonte da sua aplicação para o contêiner
COPY . /app

# Defina o diretório de trabalho como /app
WORKDIR /app

# Instale as dependências do Python
RUN pip install -r requirements.txt

# Comando padrão para iniciar o servidor
CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]