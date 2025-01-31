# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Instale o Git LFS
RUN apt-get update && apt-get install -y git-lfs

# Configure o Git LFS
RUN git lfs install

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Baixe os arquivos grandes rastreados pelo Git LFS
RUN git lfs pull

# Comando para iniciar o servidor Django
CMD ["gunicorn", "autou.wsgi:application", "--bind", "0.0.0.0:$PORT"]