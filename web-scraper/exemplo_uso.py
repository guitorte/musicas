#!/usr/bin/env python3
"""
Exemplo de uso programático do Web Scraper
Demonstra como usar a classe WebScraper em seus próprios scripts
"""

from scraper import WebScraper
from datetime import datetime


def exemplo_basico():
    """Exemplo básico de uso"""
    print("=== EXEMPLO BÁSICO ===\n")

    # Inicializa o scraper
    scraper = WebScraper(max_results=10, delay=1.0)

    # Faz uma busca
    query = "Python programming 2026"
    urls = scraper.search_duckduckgo(query)

    print(f"Encontrados {len(urls)} links para '{query}'")
    print("\nPrimeiros 5 links:")
    for i, url in enumerate(urls[:5], 1):
        print(f"  {i}. {url}")


def exemplo_multiplos_queries():
    """Exemplo com múltiplos queries"""
    print("\n\n=== EXEMPLO MÚLTIPLOS QUERIES ===\n")

    queries = ["Python tutorial", "JavaScript basics", "Web development"]
    scraper = WebScraper(max_results=5, delay=1.0)

    all_results = []

    for query in queries:
        print(f"\nProcessando: {query}")
        urls = scraper.search_duckduckgo(query)

        # Coleta apenas os 2 primeiros links para demonstração
        for url in urls[:2]:
            content = scraper.extract_content(url)
            if content:
                all_results.append(content)
                print(f"  ✓ {content['title'][:50]}...")

    print(f"\nTotal coletado: {len(all_results)} páginas")


def exemplo_salvar_arquivo():
    """Exemplo de salvar em arquivo"""
    print("\n\n=== EXEMPLO SALVAR ARQUIVO ===\n")

    scraper = WebScraper(max_results=5, delay=1.0)
    query = "Web scraping tutorial"

    # Busca e extrai
    urls = scraper.search_duckduckgo(query)
    results = scraper.scrape_multiple(urls[:3])  # Apenas 3 para exemplo

    # Salva
    filename = f"exemplo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    scraper.save_to_file(results, filename, query)

    print(f"Arquivo salvo: {filename}")


def exemplo_json():
    """Exemplo de exportação JSON"""
    print("\n\n=== EXEMPLO JSON ===\n")

    scraper = WebScraper(max_results=3, delay=1.0)

    # Busca
    urls = scraper.search_duckduckgo("Beautiful Soup tutorial")

    # Extrai apenas 2 páginas
    results = scraper.scrape_multiple(urls[:2])

    # Salva em JSON
    filename = f"exemplo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    scraper.save_to_json(results, filename)

    print(f"JSON salvo: {filename}")


def exemplo_customizado():
    """Exemplo com configurações customizadas"""
    print("\n\n=== EXEMPLO CUSTOMIZADO ===\n")

    # Scraper com mais delay e menos resultados
    scraper = WebScraper(max_results=8, delay=2.0)

    query = "Machine learning 2026"

    # Busca usando Google
    print(f"Buscando '{query}' no Google...")
    urls = scraper.search_google_alternative(query)

    print(f"Encontrados {len(urls)} links")

    # Extrai apenas 1 para demonstração
    if urls:
        content = scraper.extract_content(urls[0])
        if content:
            print(f"\nPrimeiro resultado:")
            print(f"  Título: {content['title']}")
            print(f"  URL: {content['url']}")
            print(f"  Tamanho: {len(content['content'])} caracteres")


def main():
    """Executa todos os exemplos"""
    print("\n" + "=" * 60)
    print("EXEMPLOS DE USO DO WEB SCRAPER")
    print("=" * 60)

    try:
        # Descomente os exemplos que quiser executar

        exemplo_basico()

        # exemplo_multiplos_queries()
        # exemplo_salvar_arquivo()
        # exemplo_json()
        # exemplo_customizado()

        print("\n" + "=" * 60)
        print("✅ Exemplos executados com sucesso!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Erro: {e}")


if __name__ == '__main__':
    main()
