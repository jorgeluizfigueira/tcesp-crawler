# crawler.py
import os
import re
import logging
from tqdm import tqdm
from requests_html import HTMLSession
from dotenv import load_dotenv
from db.db_config import get_mongo_client  

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Boas práticas de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TCESP_Crawler:
    def __init__(self):
        self.session = HTMLSession()
        self.base_url = "https://www.tce.sp.gov.br/jurisprudencia"
        self.logger = logging.getLogger(__name__)

        # Configuração do MongoDB usando a função do arquivo db_config
        self.db = get_mongo_client()
        self.collection = self.db[os.getenv("MONGO_COLLECTION")]

    def search_processes(self, search_phrase: str) -> list:
        """Busca todos os processos relacionados à frase de pesquisa e retorna os links completos."""
        search_url = f"{self.base_url}/pesquisar"
        params = {
            "txtTdPalvs": search_phrase,
            "tipoBuscaTxt": "Documento",
            "acao": "Executa",
            "offset": "0"
        }

        response = self.session.get(url=search_url, params=params)
        if response.status_code != 200:
            self.logger.error("Erro ao carregar a página de pesquisa.")
            return []

        num_results_text = response.html.xpath("//div[@class='page-header largura']/h3[@class='nopadding']/text()", first=True)
        total_results = int(re.search(r"\d+", num_results_text).group())
        self.logger.info(f"Total de resultados encontrados: {total_results}")

        process_links = []
        for offset in tqdm(range(0, total_results + 1, 10), desc="Buscando processos", unit="links"):
            params["offset"] = str(offset)
            if offset != 0:
                response = self.session.get(url=search_url, params=params)
                if response.status_code != 200:
                    self.logger.error(f"Erro ao buscar resultados com offset {offset}.")
                    continue
            
            process_numbers = response.html.xpath("//tr[@class='borda-superior']/td[2][@class='small']/a/text()")
            process_links.extend([f"{self.base_url}/exibir?proc={num}" for num in process_numbers])
        
        return process_links

    def parse_processes_data(self, process_url: str) -> dict:
        """Extrai e parseia os dados de um processo específico."""
        response = self.session.get(url=process_url)
        if response.status_code != 200:
            self.logger.error(f"Erro ao carregar a página do processo: {process_url}")
            return None

        num_processo = process_url.split('=')[1]
        doc = response.html.xpath("//td[3][@class='small linha_arquivo']/text()", first=True)
        doc = doc.strip() if doc else None

        parts_content = response.html.xpath('//td[contains(text(), "Parte")]/following-sibling::td[1]')
        parts = {f"Parte {i}": part.text for i, part in enumerate(parts_content, start=1)}

        filing_date = response.html.xpath('//td[contains(text(), "Autuação:")]/following-sibling::td[1]/text()', first=True)
        filing_date = filing_date.strip() if filing_date else None

        matter = response.html.xpath('//td[contains(text(), "Matéria:")]/following-sibling::td[1]/text()', first=True)

        return {
            "num_processo": num_processo,
            "doc": doc,
            "data_autuacao": filing_date,
            "partes": parts,
            "matéria": matter,
            "url": process_url
        }

    def save_to_mongo(self, process_data: dict):
        """Salva os dados de um processo no MongoDB."""
        try:
            self.collection.update_one(
                {"num_processo": process_data["num_processo"]},
                {"$set": process_data},
                upsert=True
            )
            self.logger.info(f"Dados salvos no MongoDB: {process_data['num_processo']}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar no MongoDB: {e}")

    def run(self, search_phrase: str):
        """Executa o crawler e salva os dados no MongoDB."""
        self.logger.info("Iniciando o crawler...")
        process_links = self.search_processes(search_phrase)

        for link in tqdm(process_links, desc="Extraindo detalhes dos processos", unit="processos"):
            process_data = self.parse_processes_data(link)
            if process_data:
                self.save_to_mongo(process_data)

        self.logger.info("Crawler finalizado com sucesso.")

if __name__ == "__main__":
    crawler = TCESP_Crawler()
    crawler.run("fraude em escolas")
