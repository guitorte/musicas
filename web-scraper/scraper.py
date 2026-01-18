#!/usr/bin/env python3
"""
Web Scraper - Busca e catalogação de conteúdo web
Permite buscar por queries e extrair conteúdo de múltiplos links
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import argparse
import json
from urllib.parse import urlparse
from typing import List, Dict, Optional
import sys

# Configurações
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
TIMEOUT = 10
DELAY_BETWEEN_REQUESTS = 1  # segundos


class WebScraper:
    """Classe principal para scraping de conteúdo web"""

    def __init__(self, max_results: int = 50, delay: float = 1.0):
        self.max_results = max_results
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def search_duckduckgo(self, query: str) -> List[str]:
        """
        Busca no DuckDuckGo e retorna lista de URLs
        """
        print(f"🔍 Buscando por: '{query}'")
        urls = []

        try:
            # DuckDuckGo HTML search
            search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = self.session.get(search_url, timeout=TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extrai links dos resultados
            for result in soup.find_all('a', class_='result__a'):
                href = result.get('href')
                if href and href.startswith('http'):
                    urls.append(href)
                    if len(urls) >= self.max_results:
                        break

            print(f"✅ Encontrados {len(urls)} links")

        except Exception as e:
            print(f"❌ Erro na busca: {e}")

        return urls

    def search_google_alternative(self, query: str) -> List[str]:
        """
        Busca alternativa usando Google (via scraping simples)
        """
        print(f"🔍 Buscando por: '{query}' (Google)")
        urls = []

        try:
            search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num={self.max_results}"
            response = self.session.get(search_url, timeout=TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extrai links dos resultados
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if '/url?q=' in href:
                    # Extrai URL real
                    url = href.split('/url?q=')[1].split('&')[0]
                    if url.startswith('http') and 'google.com' not in url:
                        urls.append(url)
                        if len(urls) >= self.max_results:
                            break

            print(f"✅ Encontrados {len(urls)} links")

        except Exception as e:
            print(f"❌ Erro na busca: {e}")

        return urls

    def extract_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extrai conteúdo de uma URL específica
        """
        try:
            print(f"📄 Extraindo: {url[:80]}...")
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove scripts, styles, etc
            for script in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                script.decompose()

            # Extrai título
            title = ''
            if soup.title:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text().strip()

            # Extrai conteúdo principal
            # Tenta encontrar o conteúdo principal em tags comuns
            content = ''
            main_selectors = [
                soup.find('article'),
                soup.find('main'),
                soup.find('div', class_='content'),
                soup.find('div', class_='post-content'),
                soup.find('div', id='content'),
                soup.body
            ]

            for selector in main_selectors:
                if selector:
                    content = selector.get_text(separator='\n', strip=True)
                    break

            # Limpa o conteúdo
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            content = '\n'.join(lines)

            return {
                'url': url,
                'title': title,
                'content': content[:50000],  # Limita a 50k caracteres por página
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Erro ao extrair {url}: {e}")
            return None

    def scrape_multiple(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Faz scraping de múltiplas URLs
        """
        results = []
        total = len(urls)

        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{total}] Processando...")

            content = self.extract_content(url)
            if content:
                results.append(content)

            # Delay entre requisições para não sobrecarregar
            if i < total:
                time.sleep(self.delay)

        return results

    def save_to_file(self, results: List[Dict[str, str]], filename: str, query: str):
        """
        Salva resultados em arquivo de texto formatado
        """
        with open(filename, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("=" * 80 + "\n")
            f.write(f"WEB SCRAPER - RESULTADOS DA BUSCA\n")
            f.write(f"Query: {query}\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de páginas coletadas: {len(results)}\n")
            f.write("=" * 80 + "\n\n")

            # Conteúdo de cada página
            for i, result in enumerate(results, 1):
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"PÁGINA {i}/{len(results)}\n")
                f.write("=" * 80 + "\n")
                f.write(f"Título: {result['title']}\n")
                f.write(f"URL: {result['url']}\n")
                f.write(f"Coletado em: {result['timestamp']}\n")
                f.write("-" * 80 + "\n\n")
                f.write(result['content'])
                f.write("\n\n")

        print(f"\n✅ Resultados salvos em: {filename}")

    def save_to_json(self, results: List[Dict[str, str]], filename: str):
        """
        Salva resultados em formato JSON
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"✅ Dados JSON salvos em: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Web Scraper - Busca e catalogação de conteúdo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python scraper.py "BBB26" --max 50
  python scraper.py "Pedro BBB26" --max 30 --output resultados.txt
  python scraper.py "Brothers" --max 100 --engine google
        """
    )

    parser.add_argument('query', help='Query de busca (ex: "BBB26", "Pedro BBB26")')
    parser.add_argument('--max', '-m', type=int, default=50,
                       help='Número máximo de resultados (padrão: 50)')
    parser.add_argument('--output', '-o', default=None,
                       help='Nome do arquivo de saída (padrão: busca_TIMESTAMP.txt)')
    parser.add_argument('--engine', '-e', choices=['duckduckgo', 'google'],
                       default='duckduckgo',
                       help='Motor de busca (padrão: duckduckgo)')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                       help='Delay entre requisições em segundos (padrão: 1.0)')
    parser.add_argument('--json', action='store_true',
                       help='Também salvar em formato JSON')

    args = parser.parse_args()

    # Inicializa scraper
    scraper = WebScraper(max_results=args.max, delay=args.delay)

    # Busca URLs
    if args.engine == 'google':
        urls = scraper.search_google_alternative(args.query)
    else:
        urls = scraper.search_duckduckgo(args.query)

    if not urls:
        print("❌ Nenhum resultado encontrado!")
        sys.exit(1)

    # Faz scraping
    print(f"\n📦 Iniciando coleta de {len(urls)} páginas...")
    results = scraper.scrape_multiple(urls)

    if not results:
        print("❌ Nenhum conteúdo extraído!")
        sys.exit(1)

    # Define nome do arquivo
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        query_clean = ''.join(c for c in args.query if c.isalnum() or c.isspace())[:30]
        query_clean = query_clean.replace(' ', '_')
        output_file = f"busca_{query_clean}_{timestamp}.txt"

    # Salva resultados
    scraper.save_to_file(results, output_file, args.query)

    if args.json:
        json_file = output_file.replace('.txt', '.json')
        scraper.save_to_json(results, json_file)

    print(f"\n🎉 Concluído! {len(results)} páginas catalogadas.")


if __name__ == '__main__':
    main()
