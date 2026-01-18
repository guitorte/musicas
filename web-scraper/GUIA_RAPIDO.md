# 🚀 Guia Rápido - Web Scraper

## Instalação (primeira vez)

```bash
cd web-scraper
pip install -r requirements.txt
```

## Uso Simples (Modo Interativo)

```bash
python buscar.py
```

Depois é só seguir o menu:
1. Digite seus queries (ex: BBB26, Pedro BBB26, Brothers)
2. Pressione Enter em uma linha vazia quando terminar
3. Escolha quantos links buscar (padrão: 50)
4. Escolha o motor de busca (DuckDuckGo é o padrão)
5. Confirme e aguarde

**Pronto!** Um arquivo `busca_multi_TIMESTAMP.txt` será criado com todo o conteúdo.

## Exemplos Rápidos de Linha de Comando

### Buscar 50 links sobre "BBB26"
```bash
python scraper.py "BBB26" --max 50
```

### Buscar 30 links e salvar com nome específico
```bash
python scraper.py "Pedro BBB26" --max 30 --output pedro_bbb.txt
```

### Buscar 100 links usando Google
```bash
python scraper.py "Brothers" --max 100 --engine google
```

### Salvar também em formato JSON
```bash
python scraper.py "BBB26" --max 50 --json
```

## Onde ficam os arquivos?

Os arquivos são salvos na mesma pasta onde você executou o comando:

- **Modo interativo**: `busca_multi_20260118_153045.txt`
- **Modo CLI**: `busca_BBB26_20260118_153045.txt`
- **JSON** (se solicitado): `busca_BBB26_20260118_153045.json`

## Dicas

✅ Use o modo interativo para múltiplos queries
✅ DuckDuckGo funciona melhor e é mais rápido
✅ Comece com poucos links (10-20) para testar
✅ Aumentando o `--delay` evita bloqueios (ex: `--delay 2.0`)

## Ajuda

```bash
python scraper.py --help
```

---

**É isso! Simples e direto.** 🎯
