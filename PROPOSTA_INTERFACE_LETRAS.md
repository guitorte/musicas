# INTERFACE PARA EXPLORAÇÃO E BUSCA DE LETRAS

## SEUS USE CASES

### 1. EXPLORAÇÃO/INSPIRAÇÃO (Browsing)
**Necessidades:**
- Ler letras confortavelmente
- Descobrir músicas similares
- Navegar por mood/tema/gênero
- Serendipidade (achar coisas que não estava procurando)
- Ver análises técnicas junto com as letras

### 2. BUSCA ESPECÍFICA (Search)
**Necessidades:**
- Encontrar padrões técnicos específicos ("letras com anáfora em sertanejo")
- Buscar por conceito/tema ("ciúme destrutivo")
- Buscar por estrutura ("refrão paradoxal")
- Buscar por recursos sonoros ("rimas nasais")
- Filtros combinados (gênero + artista + tema)

---

## SOLUÇÃO PROPOSTA: WEB APP RAG + INTERFACE

Um sistema web local com 3 modos:

```
┌─────────────────────────────────────┐
│   🎵 LYRICS EXPLORER                │
├─────────────────────────────────────┤
│  [Explorar] [Buscar] [Gerar]        │
└─────────────────────────────────────┘
```

---

## MODO 1: EXPLORAR (Para Inspiração)

### Layout:

```
┌──────────────────────────────────────────────────────────┐
│  🎲 EXPLORAR LETRAS                                       │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  📂 Navegação:                                            │
│   ○ Por Gênero  ○ Por Artista  ○ Por Mood  ○ Aleatório  │
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Pagode    │  │   Sertanejo │  │     MPB     │      │
│  │  1,001      │  │    337      │  │   1,846     │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                           │
│  🎯 Filtros rápidos:                                      │
│   [Romântico] [Melancólico] [Confrontacional]            │
│   [Com anáfora] [Alto memorável] [Paradoxos]             │
│                                                           │
│  ═══════════════════════════════════════════════════════ │
│                                                           │
│  📝 ALEXANDRE PIRES - "Depois do Prazer" ⭐⭐⭐⭐⭐        │
│  Pagode • Confessional • Contradição                     │
│                                                           │
│  Tô fazendo amor                                          │
│  Com outra pessoa                                         │
│  Mas meu coração                                          │
│  Vai ser pra sempre teu                                   │
│  ...                                                      │
│                                                           │
│  💡 Recursos técnicos:                                    │
│  • Redondilha menor (5 sílabas)                          │
│  • Anáfora: "Vou falar... Vou jurar..."                  │
│  • Contradição: "A verdade é que eu minto"               │
│  • Rimas nasais: -ão, -em                                │
│                                                           │
│  🎵 Similares: [3 músicas com estrutura similar]         │
│                                                           │
│  [◄ Anterior]  [🎲 Aleatória]  [Próxima ►]              │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Features:

**1. Navegação Visual**
- Cards por gênero com contador
- Filtros visuais por mood/tema
- Tag cloud de recursos técnicos

**2. Leitura Confortável**
- Fonte grande, espaçamento adequado
- Destaque de recursos técnicos na própria letra
- Análise técnica colapsável (não atrapalha leitura)

**3. Descoberta**
- Botão "Aleatória" com filtros
- "Similares a esta" (via RAG)
- "Explore este artista"
- "Mais deste gênero"

**4. Bookmarks/Favoritos**
- Marcar letras como favoritas
- Criar coleções temáticas
- Exportar seleção

---

## MODO 2: BUSCAR (Para Específico)

### Layout:

```
┌──────────────────────────────────────────────────────────┐
│  🔍 BUSCA AVANÇADA                                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Busca Semântica:                                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │ "letras sobre ciúme destrutivo com tom confessional"│  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ⚙️ Filtros Técnicos:                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │ Gênero       │ │ Artista      │ │ Recursos     │     │
│  │ ☑ Pagode     │ │ ☐ Todos      │ │ ☑ Anáfora    │     │
│  │ ☑ Sertanejo  │ │ ☑ Filtrar    │ │ ☑ Paradoxo   │     │
│  │ ☐ MPB        │ └──────────────┘ │ ☐ Metáfora   │     │
│  │ ☐ Trap       │                  └──────────────┘     │
│  └──────────────┘                                        │
│                                                           │
│  📊 Estrutura:                    🎵 Métrica:            │
│  ☑ Redondilha menor (5 sílabas)  ☐ Presente indicativo  │
│  ☐ Octossílabo (8 sílabas)       ☑ Rimas nasais (-ão)   │
│  ☐ Sem enjambement               ☐ Alta memorabilidade  │
│                                                           │
│  [Buscar] [Limpar filtros]                               │
│                                                           │
│  ═══════════════════════════════════════════════════════ │
│                                                           │
│  📋 RESULTADOS (127 letras encontradas)                  │
│                                                           │
│  1. ⭐⭐⭐⭐⭐ ALEXANDRE PIRES - "Depois do Prazer"         │
│     Pagode • Redondilha • Anáfora + Contradição          │
│     Match: 98% - "Vou falar... Vou jurar... A verdade    │
│     é que eu minto"                                       │
│     [Ver letra completa]                                  │
│                                                           │
│  2. ⭐⭐⭐⭐ DILSINHO - "Péssimo Negócio"                  │
│     Sertanejo • Octossílabo • Contradição numérica       │
│     Match: 94% - "Mil frases certas... uma errada..."    │
│     [Ver letra completa]                                  │
│                                                           │
│  [Carregar mais resultados...]                           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Features:

**1. Busca Semântica (RAG)**
```
Query: "letras que falam de mentir para esconder sentimentos"

Retorna:
- "Depois do Prazer" (Alexandre Pires)
- "Vou Mentir" (conceitual)
- Letras similares semanticamente
```

**2. Busca por Padrões Técnicos**
```
Filtros:
✓ Gênero: Pagode
✓ Métrica: Redondilha menor
✓ Recursos: Anáfora
✓ Rimas: Nasais

Retorna: Todas as letras que combinam esses critérios
```

**3. Busca Combinada**
```
"amor impossível"
+ Sertanejo
+ Alta memorabilidade
+ Presente do indicativo

Retorna: Letras específicas que atendem TUDO
```

**4. Ranking de Relevância**
- Mostra % de match
- Destaca trechos que matcharam
- Ordena por relevância semântica

---

## MODO 3: GERAR (Bonus)

### Layout:

```
┌──────────────────────────────────────────────────────────┐
│  ✨ GERAR NOVA LETRA                                      │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  📝 Tema:                                                 │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Ciúme que machuca a relação                        │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  🎵 Gênero:          📊 Tom:           ⭐ Referências:   │
│  ○ Pagode            ○ Romântico       Buscar similar    │
│  ● Sertanejo         ● Confessional    automaticamente   │
│  ○ MPB               ○ Celebratório                      │
│  ○ Trap              ○ Melancólico     Ou escolher:      │
│                                         ☐ Alexandre Pires│
│  🔧 Recursos técnicos (baseado na análise):              │
│  ☑ Usar redondilha menor (5 sílabas)                     │
│  ☑ Anáfora obsessiva                                     │
│  ☑ Contradição clara                                     │
│  ☑ Rimas nasais perfeitas                                │
│  ☐ Sem enjambement                                       │
│                                                           │
│  [Gerar letra]                                            │
│                                                           │
│  ─────────────────────────────────────────────────────── │
│                                                           │
│  📄 LETRA GERADA:                                         │
│                                                           │
│  [Letra aparece aqui após gerar]                         │
│                                                           │
│  💡 Exemplos usados do corpus:                            │
│  • "Depois do Prazer" (Alexandre Pires)                  │
│  • "Me Apaixonei Pela Pessoa Errada" (Exaltasamba)       │
│  • "Refém" (Dilsinho)                                    │
│                                                           │
│  [Gerar novamente] [Editar] [Salvar]                     │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## STACK TÉCNICA RECOMENDADA

### Backend (Python):

```python
# FastAPI para API REST
from fastapi import FastAPI
import chromadb
from anthropic import Anthropic

app = FastAPI()

# RAG System
vector_db = chromadb.PersistentClient(path="./chroma_db")
claude = Anthropic(api_key="...")

# Endpoints
@app.get("/explore/random")
def get_random_song(genre=None, filters=None):
    """Retorna letra aleatória com filtros"""
    pass

@app.post("/search/semantic")
def semantic_search(query: str, filters: dict):
    """Busca semântica com RAG"""
    results = vector_db.query(query_texts=[query], n_results=20)
    return apply_filters(results, filters)

@app.post("/search/technical")
def technical_search(filters: dict):
    """Busca por padrões técnicos"""
    # Filtrar por metadados: métrica, recursos, etc.
    pass

@app.post("/generate")
def generate_lyrics(theme, genre, tone, references):
    """Gerar letra com RAG + Claude"""
    # Buscar exemplos similares
    # Construir prompt com análises
    # Gerar com Claude
    pass
```

### Frontend (Opções):

**Opção 1: Streamlit (Mais rápido - 1 dia)**
```python
import streamlit as st

st.title("🎵 Lyrics Explorer")

tab1, tab2, tab3 = st.tabs(["Explorar", "Buscar", "Gerar"])

with tab1:
    # Interface de exploração
    genre = st.selectbox("Gênero", ["Todos", "Pagode", "Sertanejo"])
    if st.button("🎲 Letra aleatória"):
        song = get_random_song(genre)
        st.markdown(f"### {song['artista']} - {song['titulo']}")
        st.text(song['letra'])
```

**Vantagens Streamlit:**
- ✅ Implementação em 1 dia
- ✅ Python puro (sem JS)
- ✅ Já tem componentes prontos
- ✅ Roda local facilmente

**Opção 2: React + FastAPI (Mais bonito - 1 semana)**
- Interface mais polida
- Mais customizável
- Melhor UX

---

## FEATURES AVANÇADAS

### 1. BUSCA POR EXEMPLO
```
"Encontre letras similares a esta"
[Cola uma letra]
→ RAG busca as mais similares semanticamente
```

### 2. ANÁLISE EM TEMPO REAL
```
[Cola uma letra sua]
→ Sistema analisa automaticamente:
  • Métrica detectada
  • Recursos identificados
  • Similaridade com corpus
  • Sugestões de melhoria
```

### 3. COLEÇÕES PERSONALIZADAS
```
Criar coleção: "Inspirações para pagode romântico"
Adicionar letras manualmente
Sistema sugere adições automáticas (similares)
```

### 4. EXPORTAÇÃO
```
Exportar busca como:
- PDF formatado
- Markdown
- JSON (com metadados)
```

### 5. ESTATÍSTICAS VISUAIS
```
Dashboard:
- Nuvem de palavras do corpus
- Distribuição de métricas
- Recursos mais usados por gênero
- Evolução temporal (se tiver datas)
```

---

## IMPLEMENTAÇÃO FASEADA

### FASE 1: MVP (1 semana)
**Objetivo:** Funcional básico para uso imediato

**Entregas:**
- [ ] Backend RAG básico (busca semântica)
- [ ] Interface Streamlit com 2 modos:
  - Explorar (navegação simples)
  - Buscar (semântica + filtros básicos)
- [ ] 5,159 letras indexadas no Chroma
- [ ] Deploy local (localhost)

**Stack:**
- Python + FastAPI
- Chroma (vector DB)
- Streamlit (frontend)
- OpenAI embeddings ou Sentence-Transformers

**Esforço:** 20-30 horas

---

### FASE 2: Refinamento (1 semana)
**Objetivo:** Melhorar UX e adicionar features

**Entregas:**
- [ ] Modo Gerar (integração Claude)
- [ ] Filtros técnicos avançados
- [ ] Sistema de favoritos/bookmarks
- [ ] Busca por padrões técnicos
- [ ] Análise em tempo real
- [ ] Export para PDF/MD

**Esforço:** 20-30 horas

---

### FASE 3: Polish (1 semana)
**Objetivo:** Experiência premium

**Entregas:**
- [ ] Interface React (opcional)
- [ ] Dashboard de estatísticas
- [ ] Coleções personalizadas
- [ ] Busca por exemplo
- [ ] Sugestões inteligentes
- [ ] Mobile-friendly

**Esforço:** 30-40 horas

---

## ALTERNATIVAS MAIS SIMPLES

### OPÇÃO A: CLI Tool (4 horas)
```bash
# Busca rápida
$ lyrics search "ciúme destrutivo" --genre=sertanejo

# Aleatória
$ lyrics random --genre=pagode

# Similar
$ lyrics similar "Depois do Prazer"

# Análise
$ lyrics analyze minha_letra.txt
```

**Vantagens:**
- ✅ Super rápido de implementar
- ✅ Eficiente para power users
- ✅ Integra com terminal/editor

**Desvantagens:**
- ❌ Não é visual/confortável para leitura
- ❌ Menos intuitivo para exploração

---

### OPÇÃO B: Obsidian Vault (2 horas setup)
```
Criar vault Obsidian com:
- 1 nota = 1 letra
- Tags: #pagode #anafora #5estrelas
- Links entre letras similares
- Dataview para queries
```

**Exemplo query Dataview:**
```
TABLE artista, titulo, memorabilidade
FROM #pagode
WHERE contains(recursos, "anáfora")
SORT memorabilidade DESC
```

**Vantagens:**
- ✅ Setup ultra-rápido
- ✅ Markdown nativo
- ✅ Gráfico de conexões
- ✅ Busca nativa boa

**Desvantagens:**
- ❌ Não tem busca semântica (só keywords)
- ❌ Precisa criar todas as notas manualmente

---

### OPÇÃO C: Notion Database (3 horas setup)
```
Database com campos:
- Título (texto)
- Artista (select)
- Gênero (multi-select)
- Letra (texto longo)
- Recursos (multi-select)
- Memorabilidade (número)
- Análise (texto)
```

**Vantagens:**
- ✅ Visual bonito
- ✅ Fácil de usar
- ✅ Colaborativo
- ✅ Mobile app

**Desvantagens:**
- ❌ Importação manual trabalhosa
- ❌ Não tem busca semântica
- ❌ Limitado a 5,159 blocos (pode ter custo)

---

## RECOMENDAÇÃO FINAL

Para seu caso específico:

### **Curto Prazo (esta semana):**
**Opção B: Obsidian Vault** (2 horas)
- Setup rápido
- Já dá pra usar hoje
- Bom para leitura e busca básica

### **Médio Prazo (próximas 2 semanas):**
**Web App Streamlit** (FASE 1)
- Busca semântica com RAG
- Interface confortável
- Exploração + Busca específica
- Base para crescer

### **Longo Prazo (1-2 meses):**
**Sistema completo** (FASE 1 + 2 + 3)
- Melhor UX
- Todas as features avançadas
- Geração integrada

---

## PRÓXIMOS PASSOS

1. **Decidir:** Qual opção faz mais sentido agora?
2. **Prototipar:** Começar pelo mais simples que funciona
3. **Iterar:** Adicionar features conforme necessidade

Quer que eu:
1. **Implemente o Obsidian Vault** (rápido, funcional hoje)?
2. **Comece o Web App Streamlit** (melhor solução completa)?
3. **Crie o CLI tool** (para uso no terminal)?
