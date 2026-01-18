#!/usr/bin/env python3
"""
Interface interativa para o Web Scraper
Permite fazer buscas de forma mais amigável
"""

import sys
from scraper import WebScraper
from datetime import datetime


def print_banner():
    """Exibe banner do programa"""
    print("\n" + "=" * 60)
    print("🔍 WEB SCRAPER - BUSCA E CATALOGAÇÃO DE CONTEÚDO")
    print("=" * 60 + "\n")


def get_user_input():
    """Coleta informações do usuário de forma interativa"""
    print("Digite suas queries de busca (uma por linha)")
    print("Quando terminar, digite uma linha vazia:\n")

    queries = []
    while True:
        query = input(f"Query {len(queries) + 1}: ").strip()
        if not query:
            break
        queries.append(query)

    if not queries:
        print("❌ Nenhuma query fornecida!")
        sys.exit(1)

    print("\n" + "-" * 60)
    max_results = input("Quantos links por query? [padrão: 50]: ").strip()
    max_results = int(max_results) if max_results.isdigit() else 50

    print("\n" + "-" * 60)
    print("Motor de busca:")
    print("  1. DuckDuckGo (recomendado)")
    print("  2. Google")
    engine_choice = input("Escolha [1]: ").strip()
    engine = 'google' if engine_choice == '2' else 'duckduckgo'

    return queries, max_results, engine


def process_queries(queries, max_results, engine):
    """Processa todas as queries"""
    all_results = []
    scraper = WebScraper(max_results=max_results, delay=1.0)

    for i, query in enumerate(queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Processando query {i}/{len(queries)}: '{query}'")
        print("=" * 60)

        # Busca URLs
        if engine == 'google':
            urls = scraper.search_google_alternative(query)
        else:
            urls = scraper.search_duckduckgo(query)

        if not urls:
            print(f"⚠️  Nenhum resultado para '{query}'")
            continue

        # Faz scraping
        print(f"\n📦 Coletando conteúdo de {len(urls)} páginas...")
        results = scraper.scrape_multiple(urls)

        # Adiciona query ao resultado
        for result in results:
            result['query'] = query

        all_results.extend(results)
        print(f"\n✅ {len(results)} páginas coletadas para '{query}'")

    return all_results


def save_results(results, queries):
    """Salva todos os resultados em arquivo"""
    if not results:
        print("\n❌ Nenhum conteúdo foi coletado!")
        return

    # Gera nome do arquivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"busca_multi_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        # Cabeçalho
        f.write("=" * 80 + "\n")
        f.write("WEB SCRAPER - RESULTADOS DE MÚLTIPLAS BUSCAS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Queries pesquisadas: {len(queries)}\n")
        for q in queries:
            f.write(f"  • {q}\n")
        f.write(f"Total de páginas coletadas: {len(results)}\n")
        f.write("=" * 80 + "\n\n")

        # Agrupa por query
        queries_set = list(dict.fromkeys([r['query'] for r in results]))

        for query in queries_set:
            query_results = [r for r in results if r['query'] == query]

            f.write("\n" + "#" * 80 + "\n")
            f.write(f"QUERY: {query}\n")
            f.write(f"Páginas encontradas: {len(query_results)}\n")
            f.write("#" * 80 + "\n")

            for i, result in enumerate(query_results, 1):
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"PÁGINA {i}/{len(query_results)}\n")
                f.write("=" * 80 + "\n")
                f.write(f"Título: {result['title']}\n")
                f.write(f"URL: {result['url']}\n")
                f.write(f"Coletado em: {result['timestamp']}\n")
                f.write("-" * 80 + "\n\n")
                f.write(result['content'])
                f.write("\n\n")

    print(f"\n✅ Todos os resultados salvos em: {filename}")
    return filename


def main():
    """Função principal"""
    try:
        print_banner()

        # Coleta informações
        queries, max_results, engine = get_user_input()

        print("\n" + "=" * 60)
        print("📋 RESUMO:")
        print(f"  • Queries: {len(queries)}")
        print(f"  • Links por query: {max_results}")
        print(f"  • Motor: {engine}")
        print("=" * 60)

        confirm = input("\nIniciar busca? [S/n]: ").strip().lower()
        if confirm == 'n':
            print("Operação cancelada.")
            sys.exit(0)

        # Processa queries
        results = process_queries(queries, max_results, engine)

        # Salva resultados
        filename = save_results(results, queries)

        print("\n" + "=" * 60)
        print("🎉 CONCLUÍDO!")
        print(f"📊 Total de páginas catalogadas: {len(results)}")
        print(f"📁 Arquivo: {filename}")
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
