# 🔍 Web Scraper - Busca e Catalogação de Conteúdo

Ferramenta para buscar, coletar e catalogar conteúdo web a partir de queries personalizados.

## 📋 Características

- **Busca flexível**: Use DuckDuckGo ou Google como motor de busca
- **Múltiplos queries**: Busque por vários termos de uma vez
- **Extração inteligente**: Coleta título e conteúdo principal de cada página
- **Catalogação organizada**: Salva tudo em um único arquivo texto formatado
- **Exportação JSON**: Opção de salvar dados em formato JSON
- **Interface interativa**: Modo interativo fácil de usar
- **Linha de comando**: Modo CLI para automação

## 🚀 Instalação

### 1. Instalar dependências

```bash
cd web-scraper
pip install -r requirements.txt
```

### 2. Tornar scripts executáveis (opcional)

```bash
chmod +x scraper.py buscar.py
```

## 💡 Uso

### Modo 1: Interface Interativa (Recomendado)

A forma mais fácil de usar:

```bash
python buscar.py
```

O programa irá guiá-lo através de um menu interativo onde você pode:
1. Digitar múltiplos queries (ex: "BBB26", "Pedro BBB26", "Brothers")
2. Escolher quantos links buscar por query
3. Selecionar o motor de busca

**Exemplo de sessão:**

```
🔍 WEB SCRAPER - BUSCA E CATALOGAÇÃO DE CONTEÚDO

Digite suas queries de busca (uma por linha)
Quando terminar, digite uma linha vazia:

Query 1: BBB26
Query 2: Pedro BBB26
Query 3: Brothers
Query 4:

Quantos links por query? [padrão: 50]: 30

Motor de busca:
  1. DuckDuckGo (recomendado)
  2. Google
Escolha [1]: 1

Iniciar busca? [S/n]: S
```

### Modo 2: Linha de Comando (Avançado)

Para queries individuais com mais controle:

```bash
python scraper.py "BBB26" --max 50
```

**Exemplos:**

```bash
# Busca simples por "BBB26" com 50 resultados
python scraper.py "BBB26" --max 50

# Busca com nome de arquivo personalizado
python scraper.py "Pedro BBB26" --max 30 --output resultados_pedro.txt

# Usando Google como motor de busca
python scraper.py "Brothers" --engine google --max 100

# Salvando também em JSON
python scraper.py "BBB26" --max 50 --json

# Ajustando delay entre requisições (em segundos)
python scraper.py "BBB26" --max 50 --delay 2.0
```

## 📁 Arquivos de Saída

### Formato TXT

Arquivo principal com todo o conteúdo catalogado:

```
================================================================================
WEB SCRAPER - RESULTADOS DA BUSCA
Query: BBB26
Data: 18/01/2026 15:30:45
Total de páginas coletadas: 50
================================================================================

================================================================================
PÁGINA 1/50
================================================================================
Título: BBB26: Tudo sobre o Big Brother Brasil 2026
URL: https://exemplo.com/bbb26
Coletado em: 2026-01-18T15:30:45.123456
--------------------------------------------------------------------------------

[Conteúdo completo da página aqui...]
```

### Formato JSON (opcional)

Array com objetos contendo:

```json
[
  {
    "url": "https://exemplo.com/bbb26",
    "title": "BBB26: Tudo sobre...",
    "content": "Conteúdo completo...",
    "timestamp": "2026-01-18T15:30:45.123456"
  }
]
```

## ⚙️ Opções da Linha de Comando

```
scraper.py [-h] [--max MAX] [--output OUTPUT]
           [--engine {duckduckgo,google}] [--delay DELAY] [--json]
           query

Argumentos:
  query                 Query de busca (ex: "BBB26")

Opções:
  -h, --help           Mostra ajuda
  --max, -m MAX        Número máximo de resultados (padrão: 50)
  --output, -o FILE    Nome do arquivo de saída
  --engine, -e ENGINE  Motor de busca: duckduckgo ou google (padrão: duckduckgo)
  --delay, -d DELAY    Delay entre requisições em segundos (padrão: 1.0)
  --json               Também salvar em formato JSON
```

## 🎯 Casos de Uso

### Pesquisa sobre Reality Show

```bash
python buscar.py
# Digite: BBB26, Pedro BBB26, Brothers BBB26
```

### Monitoramento de Notícias

```bash
python scraper.py "eleições 2026" --max 100 --json
```

### Pesquisa Acadêmica

```bash
python scraper.py "inteligência artificial 2026" --max 200 --engine google
```

### Coleta de Múltiplos Tópicos

```bash
python buscar.py
# Digite vários queries relacionados ao seu tema de interesse
```

## 🔧 Customização

### Ajustar Delay entre Requisições

Para evitar sobrecarga nos servidores, há um delay padrão de 1 segundo entre cada requisição. Você pode ajustar:

```bash
python scraper.py "BBB26" --delay 2.0  # 2 segundos
```

### Limitar Conteúdo por Página

Edite `scraper.py` e ajuste a linha:

```python
content = content[:50000]  # Limita a 50k caracteres
```

### Adicionar Novos Seletores CSS

Para melhorar a extração de conteúdo de sites específicos, edite a lista `main_selectors` em `scraper.py`:

```python
main_selectors = [
    soup.find('article'),
    soup.find('main'),
    soup.find('div', class_='seu-seletor'),
    # Adicione mais aqui
]
```

## ⚠️ Considerações Importantes

### Uso Responsável

- **Respeite robots.txt**: Verifique se o site permite scraping
- **Delay adequado**: Mantenha delay entre requisições para não sobrecarregar servidores
- **Termos de uso**: Respeite os termos de serviço dos sites
- **Dados pessoais**: Tenha cuidado com dados pessoais coletados (LGPD/GDPR)

### Limitações

- **Anti-bot**: Alguns sites podem bloquear scraping automatizado
- **JavaScript**: Sites que dependem de JS podem ter conteúdo limitado
- **Rate limiting**: Motores de busca podem limitar número de requisições
- **Estrutura variável**: Sites diferentes têm estruturas diferentes

### Dicas para Melhores Resultados

1. **Use queries específicos**: Quanto mais específico, melhores os resultados
2. **Combine termos**: Use múltiplos queries para cobrir diferentes ângulos
3. **Ajuste max_results**: Comece com números menores para testar
4. **Prefira DuckDuckGo**: Menos restrições que Google

## 🐛 Solução de Problemas

### "Nenhum resultado encontrado"

- Tente outro motor de busca (`--engine google`)
- Verifique sua conexão com a internet
- Use queries mais genéricos

### "Erro ao extrair conteúdo"

- O site pode estar bloqueando scraping
- Tente aumentar o timeout editando `TIMEOUT` em `scraper.py`
- Alguns sites podem exigir autenticação

### Conteúdo extraído está incompleto

- Edite `main_selectors` em `scraper.py` para incluir seletores específicos do site
- Alguns sites carregam conteúdo via JavaScript (limitação atual)

## 📊 Estrutura do Projeto

```
web-scraper/
├── scraper.py          # Módulo principal com classe WebScraper
├── buscar.py           # Interface interativa
├── requirements.txt    # Dependências Python
└── README.md          # Este arquivo
```

## 🔄 Fluxo de Funcionamento

1. **Busca**: Query → Motor de busca → Lista de URLs
2. **Extração**: Para cada URL:
   - Download da página HTML
   - Parsing com BeautifulSoup
   - Extração de título e conteúdo
   - Limpeza e formatação
3. **Catalogação**: Todos os resultados → Arquivo único organizado

## 📝 Exemplos de Saída

### Nome de Arquivos Gerados

**Modo interativo (múltiplos queries):**
```
busca_multi_20260118_153045.txt
```

**Modo CLI (query único):**
```
busca_BBB26_20260118_153045.txt
busca_Pedro_BBB26_20260118_153045.txt
```

## 🚀 Próximos Passos

Sugestões para expandir a ferramenta:

- [ ] Suporte a Selenium para sites JavaScript
- [ ] Exportação para PDF ou DOCX
- [ ] Interface web com Flask
- [ ] Análise de sentimento do conteúdo
- [ ] Detecção automática de idioma
- [ ] Cache de resultados
- [ ] Suporte a proxies
- [ ] Agendamento de buscas recorrentes

## 📄 Licença

Este projeto é fornecido como está, para uso pessoal e educacional.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

---

**Desenvolvido para facilitar pesquisa e catalogação de conteúdo web** 🚀
