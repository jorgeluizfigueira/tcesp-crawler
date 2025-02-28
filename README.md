# 👨‍💻⚖️tcesp-crawler

## Autor
**Jorge Luiz Figueira**  
[LinkedIn](https://www.linkedin.com/in/jorgeluizfigueira/)

## 📌 Contexto
Este projeto foi desenvolvido como parte do desafio técnico para a vaga de **Desenvolvedor Python Jr. (Crawler/RPA)** na [Turivius](https://turivius.com/). O objetivo principal é criar um **robô de automação de processos (RPA)** capaz de extrair dados do site do **TCE-SP**. Embora o site ofereça diversos parâmetros de busca para os processos, este desafio focou especificamente no parâmetro *"Todas essas palavras" (txtTdPalvs)*, utilizando como exemplo o termo: *"fraude em escolas"*. 

## 📜 Desafio e Critérios de Avaliação
O robô deve:
- Extrair corretamente os dados do site do **TCE-SP**.
- Utilizar **requests_html, Selenium ou Scrapy**.
- Salvar os dados em um banco de dados **(MongoDB, PostgreSQL, MySQL, etc.)**.
- Garantir boa performance na raspagem e recuperação de informações.
- Ser estruturado para ambiente de produção, utilizando **Docker e Docker Compose**.
- Seguir boas práticas de código (**PEP8**), documentação clara e tratamento de exceções.
- Diferenciais: uso de **requests_html ou bs4**, entrega containerizada e armazenamento em **MongoDB**.

## 📂 Estrutura do Repositório
```
/
├── crawler/                # Módulo principal do Crawler
│   ├── main.py             # Código de extração de dados
│   ├── __init__.py         # Arquivo de inicialização do módulo
│
├── db/                     # Configuração do banco de dados
│   ├── db_config.py        # Configuração do MongoDB
│
├── .env                    # Variáveis de ambiente
├── Dockerfile              # Definição do container
├── docker-compose.yml      # Orquestração de serviços
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
```

## 🔍 Solução Implementada
- O projeto foi **containerizado** com **Docker e Docker Compose**.
- Utiliza **MongoDB** para armazenamento dos dados extraídos.
- O web crawler está configurado para buscar automaticamente processos com o termo **"fraude em escolas"**.

## 🚀 Como Executar o Projeto

### 1️⃣ Configurar Variáveis de Ambiente
Crie um arquivo **.env** na raiz do projeto com as seguintes configurações:

```ini
MONGO_USER=YOUR-USER-NAME
MONGO_PASSWORD=YOUR-DB-PASSWORD
MONGO_HOST=YOUR-HOST
MONGO_PORT=27017
MONGO_DB=YOUR-DB-NAME
MONGO_COLLECTION=YOUR-COLLECTION
```

### 2️⃣ Construir e Rodar os Containers
Execute os comandos abaixo no terminal:

```sh
docker-compose up --build
```
Isso iniciará tanto o banco de dados **MongoDB** quanto o **crawler**.

### 3️⃣ Iniciar a Raspagem Manualmente (Opcional)
Caso queira rodar manualmente o crawler dentro do container:

```sh
docker exec -it tcesp-crawler python crawler/main.py
```

O script buscará processos com o termo **"fraude em escolas"** e armazenará os dados no MongoDB.

---
