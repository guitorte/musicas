# WBS & LISTA DE ATIVIDADES - LYRICS EXPLORER WEB APP

## ESCOPO DO PROJETO

**Nome:** Lyrics Explorer - Sistema Web para Exploração e Busca de Letras Brasileiras

**Objetivo:** Criar aplicação web local com busca semântica (RAG) e interface para explorar 5,159 letras brasileiras, facilitando inspiração e buscas técnicas específicas.

**Stakeholder:** Compositor/Letrista brasileiro

**Premissas:**
- Corpus de 5,159 letras já processado e disponível
- Análises técnicas completas já existentes (markdown)
- Deploy local (não precisa produção cloud)
- Uso pessoal (single user)

**Restrições:**
- Budget limitado (~$100 para setup)
- Desenvolvimento solo
- Prazo desejado: 2-3 semanas

**Critérios de Sucesso:**
- Busca semântica funcional com RAG
- Interface confortável para leitura
- Filtros técnicos funcionando
- Tempo de resposta < 3 segundos
- 100% do corpus indexado

---

## WBS (WORK BREAKDOWN STRUCTURE)

```
1. LYRICS EXPLORER WEB APP
   │
   ├── 1.1 PREPARAÇÃO DO AMBIENTE
   │   ├── 1.1.1 Setup de desenvolvimento
   │   ├── 1.1.2 Instalação de dependências
   │   └── 1.1.3 Configuração de APIs
   │
   ├── 1.2 PROCESSAMENTO DO CORPUS
   │   ├── 1.2.1 Estruturação de dados
   │   ├── 1.2.2 Integração de análises técnicas
   │   ├── 1.2.3 Criação de metadados
   │   └── 1.2.4 Validação de dados
   │
   ├── 1.3 SISTEMA RAG (BACKEND)
   │   ├── 1.3.1 Criação de embeddings
   │   ├── 1.3.2 Setup vector database
   │   ├── 1.3.3 Sistema de busca semântica
   │   ├── 1.3.4 Sistema de filtros técnicos
   │   └── 1.3.5 API REST (FastAPI)
   │
   ├── 1.4 INTERFACE WEB (FRONTEND)
   │   ├── 1.4.1 Setup Streamlit
   │   ├── 1.4.2 Modo Explorar
   │   ├── 1.4.3 Modo Buscar
   │   ├── 1.4.4 Modo Gerar (opcional)
   │   └── 1.4.5 Sistema de favoritos
   │
   ├── 1.5 INTEGRAÇÃO & TESTES
   │   ├── 1.5.1 Integração Frontend-Backend
   │   ├── 1.5.2 Testes de funcionalidade
   │   ├── 1.5.3 Testes de performance
   │   └── 1.5.4 Ajustes de UX
   │
   └── 1.6 DOCUMENTAÇÃO & DEPLOY
       ├── 1.6.1 Documentação de uso
       ├── 1.6.2 Scripts de instalação
       └── 1.6.3 Deploy local
```

---

## LISTA DETALHADA DE ATIVIDADES

### **FASE 1: PREPARAÇÃO DO AMBIENTE**
**Duração total:** 4 horas

#### 1.1.1 Setup de desenvolvimento
**Duração:** 1h
**Responsável:** Dev
**Descrição:** Preparar ambiente de desenvolvimento
**Atividades:**
- [ ] Criar virtual environment Python 3.10+
- [ ] Configurar estrutura de diretórios do projeto
- [ ] Inicializar git repository (se novo)
- [ ] Configurar .gitignore

**Entregável:** Ambiente de desenvolvimento pronto

**Comandos:**
```bash
python -m venv venv
source venv/bin/activate
mkdir -p {data,backend,frontend,tests,docs}
```

---

#### 1.1.2 Instalação de dependências
**Duração:** 1h
**Dependências:** 1.1.1
**Descrição:** Instalar bibliotecas necessárias

**Atividades:**
- [ ] Criar requirements.txt
- [ ] Instalar dependências Python
- [ ] Verificar compatibilidade de versões
- [ ] Testar importações básicas

**Entregável:** `requirements.txt` + ambiente funcional

**requirements.txt:**
```txt
# Backend
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
anthropic==0.7.1

# RAG
chromadb==0.4.18
sentence-transformers==2.2.2
# OU
openai==1.3.7

# Utils
pydantic==2.5.0
python-multipart==0.0.6

# Frontend
streamlit==1.28.0
plotly==5.18.0
pandas==2.1.3

# Testing
pytest==7.4.3
```

---

#### 1.1.3 Configuração de APIs
**Duração:** 2h
**Dependências:** 1.1.2
**Descrição:** Configurar chaves de API necessárias

**Atividades:**
- [ ] Criar conta OpenAI (se usar embeddings OpenAI)
- [ ] Obter API key Anthropic (para geração)
- [ ] Criar arquivo .env com keys
- [ ] Configurar variáveis de ambiente
- [ ] Testar conexão com APIs

**Entregável:** `.env` configurado e funcional

**.env template:**
```bash
# APIs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...  # opcional

# Config
VECTOR_DB_PATH=./data/chroma_db
CORPUS_PATH=./data/lyrics_corpus.json
```

---

### **FASE 2: PROCESSAMENTO DO CORPUS**
**Duração total:** 8 horas

#### 1.2.1 Estruturação de dados
**Duração:** 3h
**Dependências:** 1.1.3
**Descrição:** Preparar corpus em formato adequado para RAG

**Atividades:**
- [ ] Carregar lyrics_corpus.json existente
- [ ] Criar schema padronizado
- [ ] Adicionar IDs únicos
- [ ] Normalizar campos
- [ ] Criar índice de artistas/gêneros

**Script:** `scripts/prepare_corpus.py`

**Entregável:** `data/processed_corpus.json`

**Schema:**
```python
{
    "id": "uuid-único",
    "artista": "Alexandre Pires",
    "titulo": "Depois do Prazer",
    "genero": "Pagode",
    "letra": "texto completo...",
    "metadata": {
        "num_palavras": 240,
        "num_linhas": 47,
        "arquivo_origem": "lyrics pagodes001.txt"
    }
}
```

---

#### 1.2.2 Integração de análises técnicas
**Duração:** 3h
**Dependências:** 1.2.1
**Descrição:** Adicionar análises técnicas aos metadados

**Atividades:**
- [ ] Parsear arquivos markdown de análise
- [ ] Extrair padrões por gênero
- [ ] Mapear análises para letras específicas
- [ ] Criar lookup table de recursos técnicos
- [ ] Adicionar tags automáticas

**Script:** `scripts/integrate_analysis.py`

**Entregável:** Corpus com análises integradas

**Exemplo:**
```python
{
    "id": "001",
    "artista": "Alexandre Pires",
    "titulo": "Depois do Prazer",
    "letra": "...",
    "analise": {
        "metrica": "Redondilha menor (5 sílabas)",
        "recursos": ["Anáfora", "Contradição"],
        "rimas": ["Nasais (-ão, -em)"],
        "enjambement": "0%",
        "memorabilidade": 5,
        "tom": "Confessional"
    },
    "tags": ["pagode", "contradição", "anáfora", "5estrelas"]
}
```

---

#### 1.2.3 Criação de metadados
**Duração:** 1h
**Dependências:** 1.2.2
**Descrição:** Gerar metadados adicionais para busca

**Atividades:**
- [ ] Calcular estatísticas por letra (palavras, linhas)
- [ ] Extrair palavras-chave (TF-IDF)
- [ ] Criar categorias de mood/tema
- [ ] Gerar resumos curtos
- [ ] Adicionar timestamps

**Entregável:** Corpus enriquecido com metadados completos

---

#### 1.2.4 Validação de dados
**Duração:** 1h
**Dependências:** 1.2.3
**Descrição:** Validar integridade do corpus processado

**Atividades:**
- [ ] Verificar campos obrigatórios
- [ ] Validar tipos de dados
- [ ] Checar duplicatas
- [ ] Verificar encoding UTF-8
- [ ] Gerar relatório de validação

**Script:** `scripts/validate_corpus.py`

**Entregável:** Relatório de validação + corpus corrigido

---

### **FASE 3: SISTEMA RAG (BACKEND)**
**Duração total:** 16 horas

#### 1.3.1 Criação de embeddings
**Duração:** 4h
**Dependências:** 1.2.4
**Descrição:** Gerar embeddings vetoriais de todas as letras

**Atividades:**
- [ ] Escolher modelo de embedding (OpenAI vs local)
- [ ] Criar função de geração de embeddings
- [ ] Processar corpus em batches
- [ ] Salvar embeddings
- [ ] Validar dimensionalidade

**Script:** `backend/embeddings.py`

**Código:**
```python
from sentence_transformers import SentenceTransformer
import json

# Opção 1: Local (grátis)
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def create_embeddings(corpus):
    texts = []
    for song in corpus:
        # Combinar campos relevantes
        text = f"{song['titulo']} {song['artista']} {song['letra']}"
        texts.append(text)

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True
    )

    return embeddings

# Opção 2: OpenAI (melhor qualidade)
from openai import OpenAI
client = OpenAI()

def create_embeddings_openai(corpus):
    embeddings = []
    for song in corpus:
        text = f"{song['titulo']} {song['artista']} {song['letra']}"
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
```

**Entregável:** `data/embeddings.pkl` ou integrado no vector DB

**Estimativa de custo:**
- Local: $0
- OpenAI: ~$5 para 5,159 letras

---

#### 1.3.2 Setup vector database
**Duração:** 3h
**Dependências:** 1.3.1
**Descrição:** Configurar Chroma DB e popular com dados

**Atividades:**
- [ ] Instalar e configurar Chroma
- [ ] Criar collection
- [ ] Popular com embeddings + metadados
- [ ] Configurar índices
- [ ] Testar queries básicas

**Script:** `backend/vector_db.py`

**Código:**
```python
import chromadb
from chromadb.config import Settings

# Inicializar
client = chromadb.PersistentClient(
    path="./data/chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

# Criar collection
collection = client.create_collection(
    name="letras_brasileiras",
    metadata={
        "description": "5159 letras brasileiras",
        "hnsw:space": "cosine"
    }
)

# Adicionar dados
def populate_db(corpus, embeddings):
    ids = [song['id'] for song in corpus]
    documents = [song['letra'] for song in corpus]
    metadatas = [{
        'artista': song['artista'],
        'titulo': song['titulo'],
        'genero': song['genero'],
        'tags': ','.join(song.get('tags', [])),
        'memorabilidade': song.get('analise', {}).get('memorabilidade', 0)
    } for song in corpus]

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=metadatas
    )
```

**Entregável:** ChromaDB populado e funcional

---

#### 1.3.3 Sistema de busca semântica
**Duração:** 4h
**Dependências:** 1.3.2
**Descrição:** Implementar funções de busca semântica

**Atividades:**
- [ ] Criar função de busca básica
- [ ] Implementar busca com filtros
- [ ] Adicionar re-ranking (opcional)
- [ ] Implementar busca híbrida (semântica + keywords)
- [ ] Testar relevância dos resultados

**Script:** `backend/search.py`

**Código:**
```python
class SemanticSearch:
    def __init__(self, collection):
        self.collection = collection

    def search(self, query, n_results=10, filters=None):
        """Busca semântica com filtros"""
        where_filter = self._build_filter(filters)

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )

        return self._format_results(results)

    def _build_filter(self, filters):
        """Constrói filtro Chroma a partir de dict"""
        if not filters:
            return None

        where = {}
        if filters.get('genero'):
            where['genero'] = {'$in': filters['genero']}
        if filters.get('min_memorabilidade'):
            where['memorabilidade'] = {'$gte': filters['min_memorabilidade']}

        return where if where else None

    def _format_results(self, results):
        """Formata resultados para frontend"""
        formatted = []
        for i, doc in enumerate(results['documents'][0]):
            formatted.append({
                'id': results['ids'][0][i],
                'letra': doc,
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'relevance_score': 1 - results['distances'][0][i]
            })
        return formatted
```

**Entregável:** Módulo de busca funcional

---

#### 1.3.4 Sistema de filtros técnicos
**Duração:** 3h
**Dependências:** 1.3.3
**Descrição:** Implementar filtros por padrões técnicos

**Atividades:**
- [ ] Criar filtros por métrica (redondilha, octossílabo)
- [ ] Filtros por recursos (anáfora, paradoxo, etc.)
- [ ] Filtros por rimas (nasais, perfeitas, etc.)
- [ ] Filtros combinados (AND/OR)
- [ ] Testar todas as combinações

**Script:** `backend/filters.py`

**Código:**
```python
class TechnicalFilters:
    def __init__(self, corpus):
        self.corpus = corpus
        self._build_index()

    def _build_index(self):
        """Cria índice invertido para filtros rápidos"""
        self.by_metric = {}
        self.by_resource = {}
        self.by_genre = {}

        for song in self.corpus:
            # Índice por métrica
            metric = song.get('analise', {}).get('metrica', 'unknown')
            self.by_metric.setdefault(metric, []).append(song['id'])

            # Índice por recursos
            for resource in song.get('analise', {}).get('recursos', []):
                self.by_resource.setdefault(resource, []).append(song['id'])

            # Índice por gênero
            self.by_genre.setdefault(song['genero'], []).append(song['id'])

    def filter(self, metric=None, resources=None, genre=None):
        """Aplica filtros e retorna IDs"""
        result_ids = set(song['id'] for song in self.corpus)

        if metric:
            result_ids &= set(self.by_metric.get(metric, []))

        if resources:
            for resource in resources:
                result_ids &= set(self.by_resource.get(resource, []))

        if genre:
            result_ids &= set(self.by_genre.get(genre, []))

        return list(result_ids)
```

**Entregável:** Sistema de filtros técnicos funcional

---

#### 1.3.5 API REST (FastAPI)
**Duração:** 2h
**Dependências:** 1.3.3, 1.3.4
**Descrição:** Criar API REST para frontend

**Atividades:**
- [ ] Setup FastAPI
- [ ] Criar endpoints
- [ ] Adicionar CORS
- [ ] Documentação automática (Swagger)
- [ ] Testar todos endpoints

**Script:** `backend/main.py`

**Código:**
```python
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="Lyrics Explorer API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SearchRequest(BaseModel):
    query: str
    n_results: int = 10
    filters: Optional[dict] = None

class Song(BaseModel):
    id: str
    artista: str
    titulo: str
    genero: str
    letra: str
    analise: dict
    relevance_score: Optional[float] = None

# Endpoints
@app.get("/")
def root():
    return {"message": "Lyrics Explorer API", "version": "1.0"}

@app.post("/search/semantic", response_model=List[Song])
def search_semantic(request: SearchRequest):
    """Busca semântica"""
    results = semantic_search.search(
        query=request.query,
        n_results=request.n_results,
        filters=request.filters
    )
    return results

@app.get("/songs/{song_id}", response_model=Song)
def get_song(song_id: str):
    """Retorna letra específica"""
    return corpus_manager.get_by_id(song_id)

@app.get("/songs/random")
def get_random_song(genre: Optional[str] = None):
    """Retorna letra aleatória"""
    return corpus_manager.get_random(genre)

@app.get("/genres")
def list_genres():
    """Lista gêneros disponíveis"""
    return corpus_manager.get_genres()

@app.get("/artists")
def list_artists(genre: Optional[str] = None):
    """Lista artistas"""
    return corpus_manager.get_artists(genre)

@app.post("/generate")
def generate_lyrics(theme: str, genre: str, tone: str):
    """Gera letra com RAG + Claude"""
    return lyrics_generator.generate(theme, genre, tone)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Entregável:** API REST funcional + documentação Swagger

**Testar:**
```bash
uvicorn backend.main:app --reload
# Acesse http://localhost:8000/docs
```

---

### **FASE 4: INTERFACE WEB (FRONTEND)**
**Duração total:** 20 horas

#### 1.4.1 Setup Streamlit
**Duração:** 2h
**Dependências:** 1.3.5
**Descrição:** Configurar estrutura básica Streamlit

**Atividades:**
- [ ] Criar app.py principal
- [ ] Configurar páginas/tabs
- [ ] Setup tema/estilo
- [ ] Criar componentes reutilizáveis
- [ ] Testar navegação básica

**Script:** `frontend/app.py`

**Código:**
```python
import streamlit as st
import requests

# Config
st.set_page_config(
    page_title="Lyrics Explorer",
    page_icon="🎵",
    layout="wide"
)

# API base URL
API_URL = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.title("🎵 Lyrics Explorer")
    st.markdown("---")
    mode = st.radio(
        "Modo",
        ["🎲 Explorar", "🔍 Buscar", "✨ Gerar"]
    )

# Main content
if mode == "🎲 Explorar":
    st.header("Explorar Letras")
    # Conteúdo do modo explorar

elif mode == "🔍 Buscar":
    st.header("Buscar Letras")
    # Conteúdo do modo buscar

elif mode == "✨ Gerar":
    st.header("Gerar Nova Letra")
    # Conteúdo do modo gerar
```

**Entregável:** Estrutura básica do app funcional

---

#### 1.4.2 Modo Explorar
**Duração:** 6h
**Dependências:** 1.4.1
**Descrição:** Implementar interface de exploração

**Atividades:**
- [ ] Navegação por gênero
- [ ] Botão "Aleatória"
- [ ] Display de letra formatado
- [ ] Seção de análise técnica
- [ ] Botão "Similares a esta"
- [ ] Sistema de navegação (anterior/próxima)

**Código:**
```python
def modo_explorar():
    st.header("🎲 Explorar Letras")

    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        genre = st.selectbox(
            "Gênero",
            ["Todos", "Pagode", "Sertanejo", "MPB", "Trap", "Arrocha"]
        )
    with col2:
        mood_filter = st.multiselect(
            "Mood/Recursos",
            ["Romântico", "Melancólico", "Anáfora", "Paradoxo"]
        )
    with col3:
        if st.button("🎲 Aleatória"):
            st.session_state.current_song = get_random_song(genre)

    # Display da letra
    if 'current_song' in st.session_state:
        song = st.session_state.current_song

        # Header
        st.markdown(f"## {song['artista']} - \"{song['titulo']}\"")
        st.caption(f"{song['genero']} • {' • '.join(song.get('tags', []))}")

        # Letra
        st.markdown("---")
        st.text(song['letra'])

        # Análise técnica (colapsável)
        with st.expander("💡 Análise Técnica"):
            analise = song.get('analise', {})
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Métrica:** {analise.get('metrica', 'N/A')}")
                st.markdown(f"**Recursos:** {', '.join(analise.get('recursos', []))}")
            with col2:
                st.markdown(f"**Rimas:** {', '.join(analise.get('rimas', []))}")
                st.markdown(f"**Memorabilidade:** {'⭐' * analise.get('memorabilidade', 0)}")

        # Similares
        st.markdown("---")
        st.subheader("🎵 Letras Similares")
        similar = get_similar_songs(song['id'], n=3)
        for sim in similar:
            st.markdown(f"- **{sim['artista']}** - \"{sim['titulo']}\" ({sim['genero']})")

def get_random_song(genre=None):
    params = {'genre': genre} if genre != "Todos" else {}
    response = requests.get(f"{API_URL}/songs/random", params=params)
    return response.json()

def get_similar_songs(song_id, n=3):
    # Implementar busca por similaridade
    pass
```

**Entregável:** Modo Explorar funcional

---

#### 1.4.3 Modo Buscar
**Duração:** 8h
**Dependências:** 1.4.1
**Descrição:** Implementar interface de busca avançada

**Atividades:**
- [ ] Campo de busca semântica
- [ ] Filtros técnicos (checkboxes)
- [ ] Display de resultados com relevância
- [ ] Paginação
- [ ] Destaque de trechos relevantes
- [ ] Exportação de resultados

**Código:**
```python
def modo_buscar():
    st.header("🔍 Buscar Letras")

    # Busca semântica
    query = st.text_input(
        "Busca semântica",
        placeholder="Ex: letras sobre ciúme com tom confessional"
    )

    # Filtros técnicos
    st.subheader("⚙️ Filtros Técnicos")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Gênero**")
        genre_filter = st.multiselect(
            "Selecione",
            ["Pagode", "Sertanejo", "MPB", "Trap", "Arrocha"],
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("**Recursos**")
        resources_filter = st.multiselect(
            "Selecione",
            ["Anáfora", "Paradoxo", "Metáfora", "Contradição"],
            label_visibility="collapsed"
        )

    with col3:
        st.markdown("**Métrica**")
        metric_filter = st.selectbox(
            "Selecione",
            ["Todas", "Redondilha menor (5)", "Octossílabo (8)"],
            label_visibility="collapsed"
        )

    # Botão de busca
    if st.button("Buscar", type="primary"):
        with st.spinner("Buscando..."):
            results = search_lyrics(
                query=query,
                genres=genre_filter,
                resources=resources_filter,
                metric=metric_filter
            )
            st.session_state.search_results = results

    # Resultados
    if 'search_results' in st.session_state:
        results = st.session_state.search_results
        st.markdown(f"### 📋 {len(results)} resultados encontrados")

        for i, result in enumerate(results[:20]):  # Paginação
            with st.expander(
                f"{i+1}. {'⭐' * result.get('memorabilidade', 0)} "
                f"{result['artista']} - \"{result['titulo']}\" "
                f"(Match: {result['relevance_score']*100:.0f}%)"
            ):
                st.caption(f"{result['genero']} • {', '.join(result.get('recursos', []))}")
                st.text(result['letra'][:500] + "...")
                if st.button(f"Ver completa", key=f"btn_{i}"):
                    st.session_state.current_song = result
                    # Mudar para modo explorar

def search_lyrics(query, genres, resources, metric):
    filters = {
        'genero': genres if genres else None,
        'recursos': resources if resources else None,
        'metrica': metric if metric != "Todas" else None
    }

    response = requests.post(
        f"{API_URL}/search/semantic",
        json={
            'query': query,
            'n_results': 50,
            'filters': filters
        }
    )
    return response.json()
```

**Entregável:** Modo Buscar funcional

---

#### 1.4.4 Modo Gerar (opcional)
**Duração:** 4h
**Dependências:** 1.4.1
**Descrição:** Implementar interface de geração de letras

**Atividades:**
- [ ] Formulário de inputs (tema, gênero, tom)
- [ ] Opção de escolher referências
- [ ] Checkboxes de recursos técnicos
- [ ] Display de letra gerada
- [ ] Mostrar exemplos usados
- [ ] Botão "Gerar novamente"

**Código:**
```python
def modo_gerar():
    st.header("✨ Gerar Nova Letra")

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        theme = st.text_input("Tema", placeholder="Ex: ciúme destrutivo")
        genre = st.selectbox("Gênero", ["Pagode", "Sertanejo", "MPB"])
    with col2:
        tone = st.selectbox("Tom", ["Romântico", "Confessional", "Celebratório"])
        references = st.text_input("Referências (opcional)", placeholder="Ex: Alexandre Pires")

    # Recursos técnicos
    st.markdown("**Recursos técnicos desejados:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        use_anafora = st.checkbox("Anáfora")
    with col2:
        use_paradoxo = st.checkbox("Paradoxo")
    with col3:
        use_rimas_nasais = st.checkbox("Rimas nasais")

    # Botão gerar
    if st.button("Gerar Letra", type="primary"):
        with st.spinner("Gerando letra... (pode levar 10-20 segundos)"):
            result = generate_lyrics(theme, genre, tone, references)
            st.session_state.generated_lyrics = result

    # Display
    if 'generated_lyrics' in st.session_state:
        result = st.session_state.generated_lyrics

        st.markdown("### 📄 Letra Gerada:")
        st.text(result['letra'])

        with st.expander("💡 Exemplos usados do corpus"):
            for ex in result['exemplos_usados']:
                st.markdown(f"- {ex['artista']} - \"{ex['titulo']}\"")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Gerar novamente"):
                st.rerun()
        with col2:
            st.download_button(
                "💾 Salvar",
                data=result['letra'],
                file_name=f"{theme.replace(' ', '_')}.txt"
            )

def generate_lyrics(theme, genre, tone, references):
    response = requests.post(
        f"{API_URL}/generate",
        json={
            'theme': theme,
            'genre': genre,
            'tone': tone,
            'references': references
        }
    )
    return response.json()
```

**Entregável:** Modo Gerar funcional

---

#### 1.4.5 Sistema de favoritos
**Duração:** 2h (opcional)
**Dependências:** 1.4.2, 1.4.3
**Descrição:** Adicionar sistema de bookmarks

**Atividades:**
- [ ] Botão "Favoritar"
- [ ] Armazenar favoritos (JSON local)
- [ ] Página "Meus Favoritos"
- [ ] Remover favoritos
- [ ] Exportar lista de favoritos

**Entregável:** Sistema de favoritos funcional

---

### **FASE 5: INTEGRAÇÃO & TESTES**
**Duração total:** 8 horas

#### 1.5.1 Integração Frontend-Backend
**Duração:** 3h
**Dependências:** 1.3.5, 1.4.4
**Descrição:** Integrar e testar comunicação completa

**Atividades:**
- [ ] Testar todos os endpoints
- [ ] Tratamento de erros
- [ ] Loading states
- [ ] Timeout handling
- [ ] Validação de inputs

**Entregável:** Sistema integrado funcionando end-to-end

---

#### 1.5.2 Testes de funcionalidade
**Duração:** 2h
**Dependências:** 1.5.1
**Descrição:** Testes funcionais de cada feature

**Atividades:**
- [ ] Testar busca semântica (10 queries)
- [ ] Testar filtros técnicos (todas combinações)
- [ ] Testar navegação explorar
- [ ] Testar geração de letras
- [ ] Testar edge cases

**Script:** `tests/test_functionality.py`

**Entregável:** Relatório de testes + fixes

---

#### 1.5.3 Testes de performance
**Duração:** 2h
**Dependências:** 1.5.2
**Descrição:** Testar performance e otimizar

**Atividades:**
- [ ] Medir tempo de busca semântica
- [ ] Medir tempo de aplicação de filtros
- [ ] Testar com 100 queries simultâneas
- [ ] Identificar gargalos
- [ ] Otimizar queries lentas

**Métricas alvo:**
- Busca semântica: < 2 segundos
- Filtros técnicos: < 1 segundo
- Letra aleatória: < 500ms
- Geração com Claude: < 20 segundos

**Entregável:** Relatório de performance + otimizações

---

#### 1.5.4 Ajustes de UX
**Duração:** 1h
**Dependências:** 1.5.3
**Descrição:** Melhorias de experiência do usuário

**Atividades:**
- [ ] Ajustar espaçamentos
- [ ] Melhorar mensagens de erro
- [ ] Adicionar tooltips
- [ ] Otimizar responsividade
- [ ] Testar usabilidade

**Entregável:** Interface polida e usável

---

### **FASE 6: DOCUMENTAÇÃO & DEPLOY**
**Duração total:** 4 horas

#### 1.6.1 Documentação de uso
**Duração:** 2h
**Dependências:** 1.5.4
**Descrição:** Criar documentação para usuário final

**Atividades:**
- [ ] Criar README.md
- [ ] Documentar features
- [ ] Criar guia de uso rápido
- [ ] Screenshots/GIFs
- [ ] FAQ

**Entregável:** `README.md` + `docs/USER_GUIDE.md`

**Template README:**
```markdown
# 🎵 Lyrics Explorer

Sistema web para explorar e buscar letras brasileiras com IA.

## Features
- 🎲 Exploração de 5,159 letras brasileiras
- 🔍 Busca semântica com RAG
- ⚙️ Filtros técnicos avançados
- ✨ Geração de letras com Claude

## Instalação
...

## Uso
...
```

---

#### 1.6.2 Scripts de instalação
**Duração:** 1h
**Dependências:** 1.6.1
**Descrição:** Criar scripts automatizados de setup

**Atividades:**
- [ ] Script de instalação (setup.sh)
- [ ] Script de inicialização (run.sh)
- [ ] Configuração de .env template
- [ ] Checklist de pré-requisitos

**Scripts:**

**setup.sh:**
```bash
#!/bin/bash
echo "🎵 Lyrics Explorer - Setup"

# Verificar Python
python3 --version || exit 1

# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar diretórios
mkdir -p data/chroma_db

# Processar corpus
python scripts/prepare_corpus.py
python scripts/integrate_analysis.py
python backend/embeddings.py
python backend/vector_db.py

echo "✅ Setup completo!"
```

**run.sh:**
```bash
#!/bin/bash
source venv/bin/activate

# Iniciar backend
uvicorn backend.main:app --reload &
BACKEND_PID=$!

# Aguardar backend
sleep 3

# Iniciar frontend
streamlit run frontend/app.py

# Cleanup
kill $BACKEND_PID
```

**Entregável:** Scripts de setup automatizado

---

#### 1.6.3 Deploy local
**Duração:** 1h
**Dependências:** 1.6.2
**Descrição:** Deploy e configuração final

**Atividades:**
- [ ] Executar setup.sh
- [ ] Validar instalação
- [ ] Testar startup
- [ ] Criar atalhos (opcional)
- [ ] Configurar auto-start (opcional)

**Entregável:** Sistema rodando localmente

---

## CRONOGRAMA

### **Semana 1: Backend + Dados**
| Dia | Fase | Duração | Atividades |
|-----|------|---------|------------|
| Segunda | 1.1 + 1.2 | 12h | Setup + Processamento corpus |
| Terça | 1.3.1-1.3.2 | 7h | Embeddings + Vector DB |
| Quarta | 1.3.3-1.3.4 | 7h | Busca semântica + Filtros |
| Quinta | 1.3.5 | 2h | API REST |

**Entregável Semana 1:** Backend completo e funcional

---

### **Semana 2: Frontend**
| Dia | Fase | Duração | Atividades |
|-----|------|---------|------------|
| Segunda | 1.4.1-1.4.2 | 8h | Setup + Modo Explorar |
| Terça | 1.4.3 | 8h | Modo Buscar |
| Quarta | 1.4.4 | 4h | Modo Gerar |
| Quinta | 1.5.1-1.5.2 | 5h | Integração + Testes |

**Entregável Semana 2:** Frontend completo integrado

---

### **Semana 3: Testes + Deploy**
| Dia | Fase | Duração | Atividades |
|-----|------|---------|------------|
| Segunda | 1.5.3-1.5.4 | 3h | Performance + UX |
| Terça | 1.6.1-1.6.2 | 3h | Documentação + Scripts |
| Quarta | 1.6.3 | 1h | Deploy final |

**Entregável Semana 3:** Sistema completo e documentado

---

## RECURSOS NECESSÁRIOS

### **Humanos:**
- 1 desenvolvedor full-stack (você)
- Horas totais: ~60 horas (3 semanas part-time)

### **Tecnológicos:**
- Computador com Python 3.10+
- 10 GB espaço em disco
- Conexão internet (para APIs)

### **Financeiros:**
| Item | Custo |
|------|-------|
| OpenAI embeddings (opcional) | $5 |
| Anthropic API (geração) | $10-20 |
| **Total** | **$15-25** |

Se usar embeddings locais: **$10-20 total**

---

## RISCOS & MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| API keys não funcionarem | Baixa | Alto | Testar em 1.1.3, ter plano B (embeddings locais) |
| Corpus muito grande para embeddings | Média | Médio | Processar em batches, usar modelo menor |
| Performance lenta | Média | Médio | Testar cedo (1.5.3), otimizar queries |
| Interface complexa demais | Baixa | Médio | Começar simples, iterar |
| Tempo insuficiente | Média | Alto | Priorizar MVP, features opcionais depois |

---

## CRITÉRIOS DE ACEITAÇÃO

### **Funcional:**
- [ ] Busca semântica retorna resultados relevantes
- [ ] Filtros técnicos funcionam corretamente
- [ ] Modo explorar permite navegação confortável
- [ ] Geração de letras produz resultados coerentes
- [ ] 100% do corpus acessível

### **Performance:**
- [ ] Busca < 3 segundos
- [ ] Interface responsiva
- [ ] Sem crashes em uso normal

### **Usabilidade:**
- [ ] Interface intuitiva
- [ ] Documentação clara
- [ ] Instalação simples (< 30 minutos)

---

## PRÓXIMOS PASSOS

1. **Revisar e aprovar WBS**
2. **Iniciar Fase 1.1** (Setup)
3. **Tracking diário de progresso**
4. **Ajustar cronograma conforme necessário**

**Data prevista de conclusão:** 3 semanas a partir do início
