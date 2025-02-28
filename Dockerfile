# (Imagem para o crawler)
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão de execução do crawler
CMD ["python", "crawler/main.py"]