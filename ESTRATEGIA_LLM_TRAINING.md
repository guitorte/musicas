# ESTRATÉGIA: TREINAR LLM NO CORPUS DE LETRAS

## CONTEXTO ATUAL

**Corpus disponível:**
- 478 letras brasileiras (swipe collection)
- 5,159 letras total no repositório
- Análises técnicas completas (métrica, sonoridade, ganchos, padrões)
- Padrões identificados e documentados

**Objetivo:**
Criar um sistema de LLM que entenda e gere letras no estilo do corpus.

---

## OPÇÕES DE IMPLEMENTAÇÃO

### OPÇÃO 1: RAG (Retrieval-Augmented Generation) ⭐ RECOMENDADO

**Como funciona:**
1. Criar embeddings de todas as letras do corpus
2. Armazenar em vector database
3. Quando usuário pede uma letra, buscar exemplos similares
4. Passar exemplos + análises como contexto para o LLM
5. LLM gera baseado nos exemplos

**Prós:**
- ✅ Não precisa treinar modelo (usa Claude/GPT/Llama existente)
- ✅ Mais barato (sem custos de fine-tuning)
- ✅ Mais rápido de implementar (1-2 dias)
- ✅ Flexível (pode adicionar/remover letras facilmente)
- ✅ Explícito (sabe quais exemplos usou)
- ✅ Funciona bem com corpus médio (478-5000 letras)

**Contras:**
- ❌ Limitado pelo tamanho do contexto do LLM
- ❌ Não "aprende" padrões implícitos profundos

**Stack sugerido:**
```
Embeddings: OpenAI text-embedding-3-large ou Sentence-Transformers
Vector DB: Chroma, FAISS, ou Pinecone
LLM: Claude 3.5 Sonnet (você), GPT-4, ou Llama 3
```

**Custo estimado:**
- Embeddings: ~$2-5 para 5000 letras (one-time)
- Queries: ~$0.01-0.10 por geração
- Total setup: < $50

---

### OPÇÃO 2: FINE-TUNING (LoRA/QLoRA)

**Como funciona:**
1. Preparar dataset de treino (letras formatadas)
2. Fine-tunar modelo base (Llama 3, Mistral, GPT-3.5-turbo)
3. Usar modelo fine-tunado para gerar letras

**Prós:**
- ✅ Modelo realmente "aprende" os padrões
- ✅ Não depende de retrieval
- ✅ Pode capturar padrões sutis
- ✅ Melhor para grande volume de gerações

**Contras:**
- ❌ Mais caro ($100-1000+ dependendo do modelo)
- ❌ Mais complexo tecnicamente
- ❌ Corpus pode ser pequeno demais (idealmente 10k+ exemplos)
- ❌ Menos flexível (re-treinar para atualizar)
- ❌ Pode overfitar com corpus pequeno

**Stack sugerido:**
```
Modelo base: Llama 3 8B, Mistral 7B, ou GPT-3.5-turbo
Framework: Hugging Face PEFT (LoRA), Axolotl, ou OpenAI fine-tuning API
Hardware: GPU (A100/H100) ou Google Colab Pro+
```

**Custo estimado:**
- Treino: $100-500 (depende de epochs e hardware)
- Inferência: $0.01-0.05 por geração
- Total setup: $200-1000

---

### OPÇÃO 3: PROMPT ENGINEERING AVANÇADO (atual otimizado)

**Como funciona:**
1. Usar análises existentes como "manual" do modelo
2. Passar análises técnicas + exemplos específicos no prompt
3. Usar Claude/GPT diretamente sem fine-tuning ou RAG

**Prós:**
- ✅ Mais simples (já estamos fazendo isso)
- ✅ Zero setup adicional
- ✅ Mais barato inicialmente
- ✅ Totalmente flexível

**Contras:**
- ❌ Limitado ao contexto (200k tokens no Claude)
- ❌ Precisa passar análises toda vez
- ❌ Não escala bem para produção
- ❌ Menos consistente

**Já temos:**
- Análises técnicas completas
- Padrões identificados
- Estratégias documentadas

---

## COMPARAÇÃO LADO A LADO

| Critério | RAG | Fine-tuning | Prompt Engineering |
|----------|-----|-------------|-------------------|
| Custo setup | $50 | $200-1000 | $0 |
| Custo por query | $0.01-0.10 | $0.01-0.05 | $0.10-0.50 |
| Tempo setup | 1-2 dias | 1-2 semanas | 0 (já feito) |
| Complexidade | Média | Alta | Baixa |
| Qualidade | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Escalabilidade | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Flexibilidade | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Corpus pequeno OK? | Sim | Não ideal | Sim |

---

## RECOMENDAÇÃO: RAG (Opção 1)

Para o seu caso específico, **RAG é a melhor escolha** porque:

1. **Corpus tamanho médio**: 478-5000 letras é perfeito para RAG, mas pode ser pouco para fine-tuning
2. **Análises já feitas**: Podemos incluir análises técnicas no contexto
3. **Custo-benefício**: Setup barato, resultados excelentes
4. **Flexibilidade**: Fácil adicionar novas letras ou ajustar
5. **Explicitabilidade**: Pode ver quais exemplos influenciaram cada geração

---

## IMPLEMENTAÇÃO RAG - PASSO A PASSO

### FASE 1: PREPARAÇÃO DO CORPUS (1 dia)

**1.1. Estruturar dados:**
```json
{
  "id": "001_alexandre_pires_depois_prazer",
  "artista": "Alexandre Pires",
  "titulo": "Depois do Prazer",
  "genero": "Pagode",
  "letra": "...",
  "analise_tecnica": {
    "metrica": "Redondilha menor (5 sílabas)",
    "rimas": "Nasais (-ão, -em)",
    "recursos": ["Anáfora", "Contradição"],
    "memorabilidade": 5,
    "tom": "Confessional"
  },
  "tags": ["contradição", "amor", "mentira", "pagode"]
}
```

**1.2. Criar chunks inteligentes:**
Cada chunk = 1 letra completa + metadados + análise resumida

**Script:**
```python
import json

def prepare_corpus_for_rag():
    # Carregar letras
    with open('letras_separadas.json') as f:
        letras = json.load(f)

    # Carregar análises
    analises = load_analyses()

    # Combinar
    corpus_rag = []
    for letra in letras:
        chunk = {
            'id': f"{letra['artista']}_{letra['titulo']}",
            'text': f"Artista: {letra['artista']}\nTítulo: {letra['titulo']}\nGênero: {letra['genero']}\n\nLetra:\n{letra['letra']}",
            'metadata': {
                'artista': letra['artista'],
                'genero': letra['genero'],
                'analise': get_analysis_for_song(letra, analises)
            }
        }
        corpus_rag.append(chunk)

    return corpus_rag
```

---

### FASE 2: CRIAR EMBEDDINGS (1 hora)

**2.1. Escolher modelo de embedding:**

**Opção A: OpenAI (melhor qualidade)**
```python
from openai import OpenAI

client = OpenAI(api_key='sua-key')

def create_embeddings(corpus):
    embeddings = []
    for item in corpus:
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=item['text']
        )
        embeddings.append({
            'id': item['id'],
            'embedding': response.data[0].embedding,
            'metadata': item['metadata'],
            'text': item['text']
        })
    return embeddings
```

**Custo**: ~$0.13 por 1M tokens → ~$2-5 para todo corpus

**Opção B: Sentence-Transformers (grátis, local)**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def create_embeddings_local(corpus):
    texts = [item['text'] for item in corpus]
    embeddings = model.encode(texts, show_progress_bar=True)

    return [{
        'id': item['id'],
        'embedding': emb.tolist(),
        'metadata': item['metadata'],
        'text': item['text']
    } for item, emb in zip(corpus, embeddings)]
```

**Custo**: Grátis (roda local)

---

### FASE 3: VECTOR DATABASE (2 horas)

**Opção A: Chroma (mais simples, local)**
```python
import chromadb

# Inicializar
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_collection(
    name="letras_brasileiras",
    metadata={"description": "Corpus de 5000 letras brasileiras"}
)

# Adicionar embeddings
def add_to_chroma(embeddings):
    collection.add(
        ids=[e['id'] for e in embeddings],
        embeddings=[e['embedding'] for e in embeddings],
        documents=[e['text'] for e in embeddings],
        metadatas=[e['metadata'] for e in embeddings]
    )

# Buscar similares
def search_similar(query, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results
```

**Opção B: FAISS (mais rápido, produção)**
```python
import faiss
import numpy as np

# Criar índice
def create_faiss_index(embeddings):
    dimension = len(embeddings[0]['embedding'])
    index = faiss.IndexFlatL2(dimension)

    vectors = np.array([e['embedding'] for e in embeddings]).astype('float32')
    index.add(vectors)

    # Salvar
    faiss.write_index(index, "letras.index")

    return index

# Buscar
def search_faiss(query_embedding, index, k=5):
    query_vec = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_vec, k)
    return indices[0], distances[0]
```

---

### FASE 4: SISTEMA DE GERAÇÃO (4 horas)

```python
import anthropic

class LetrasRAG:
    def __init__(self, vector_db, claude_api_key):
        self.vector_db = vector_db
        self.claude = anthropic.Anthropic(api_key=claude_api_key)
        self.analises_tecnicas = self.load_analyses()

    def load_analyses(self):
        """Carregar análises técnicas do markdown"""
        return {
            'metricas': open('ANALISE_POETICA_TECNICA_SWIPE.md').read(),
            'ganchos': open('analise_ganchos_swipe_71_100.md').read(),
            'padroes': open('ANALISE_TECNICA_SWIPE.md').read()
        }

    def gerar_letra(self, tema, genero, tom, referencias_especificas=None):
        # 1. Buscar exemplos similares
        query = f"letra de {genero} sobre {tema} com tom {tom}"
        exemplos = self.vector_db.search(query, n_results=5)

        # 2. Construir prompt com contexto
        prompt = self.build_prompt(
            tema=tema,
            genero=genero,
            tom=tom,
            exemplos=exemplos,
            referencias=referencias_especificas
        )

        # 3. Gerar com Claude
        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return response.content[0].text

    def build_prompt(self, tema, genero, exemplos, tom, referencias):
        # Análise técnica do gênero
        analise_genero = self.get_genre_analysis(genero)

        # Exemplos do corpus
        exemplos_text = "\n\n".join([
            f"EXEMPLO {i+1} - {ex['metadata']['artista']} - \"{ex['metadata']['titulo']}\":\n{ex['text']}"
            for i, ex in enumerate(exemplos[:3])
        ])

        prompt = f"""Você é um compositor especializado em letras brasileiras de {genero}.

## ANÁLISE TÉCNICA DO GÊNERO {genero.upper()}:

{analise_genero}

## EXEMPLOS DO CORPUS SIMILAR AO QUE PEDIMOS:

{exemplos_text}

## TAREFA:

Escrever uma letra de {genero} sobre o tema: "{tema}"
Tom emocional: {tom}

Requisitos técnicos baseados na análise do corpus:
- Seguir a métrica identificada para {genero}
- Usar os recursos sonoros típicos do gênero
- Criar gancho memorável seguindo os padrões identificados
- Manter autenticidade e especificidade dos detalhes

{'Referências específicas solicitadas: ' + referencias if referencias else ''}

Escreva a letra agora:"""

        return prompt

    def get_genre_analysis(self, genero):
        """Extrair análise específica do gênero dos markdowns"""
        # Simplificado - na prática, parsear os MDs
        analyses = {
            'Pagode': """
- Métrica: Redondilha menor (5 sílabas)
- Rimas: Nasais perfeitas (-ão, -em)
- Recursos: Anáfora, contradição, sem enjambement
- Tom: Confessional, direto
- BPM: 100-110
            """,
            'Sertanejo': """
- Métrica: Octossílabo (8 sílabas)
- Rimas: Oxítonas finais (suspensão melódica)
- Recursos: Paralelismo, narrativa, enjambement moderado
- Tom: Narrativo, emotivo
- BPM: 90-100
            """,
            # ... outros gêneros
        }
        return analyses.get(genero, "Análise geral do corpus")
```

---

### FASE 5: INTERFACE/USO (2 horas)

```python
# Inicializar sistema
rag = LetrasRAG(
    vector_db=chroma_collection,
    claude_api_key='sua-key'
)

# Exemplo 1: Gerar letra similar a uma existente
letra1 = rag.gerar_letra(
    tema="ciúme destrutivo que machuca a relação",
    genero="Sertanejo",
    tom="confessional arrependido"
)

# Exemplo 2: Gerar com referências específicas
letra2 = rag.gerar_letra(
    tema="apostaram contra o casal",
    genero="Pagode",
    tom="celebratório romântico",
    referencias_especificas="Inspirar em Alexandre Pires e Exaltasamba"
)

# Exemplo 3: Buscar letras similares primeiro
similar = rag.vector_db.search("amor impossível sofrência")
for s in similar[:3]:
    print(f"{s['metadata']['artista']} - {s['metadata']['titulo']}")
```

---

## ROADMAP DE IMPLEMENTAÇÃO

### SEMANA 1: Setup Básico
- [ ] Dia 1-2: Preparar corpus estruturado (JSON com metadados)
- [ ] Dia 3: Criar embeddings (OpenAI ou local)
- [ ] Dia 4: Setup vector database (Chroma)
- [ ] Dia 5: Testes de retrieval

### SEMANA 2: Sistema de Geração
- [ ] Dia 1-2: Implementar LetrasRAG class
- [ ] Dia 3: Integrar análises técnicas nos prompts
- [ ] Dia 4-5: Testes e refinamento

### SEMANA 3: Refinamento
- [ ] Avaliar qualidade das gerações
- [ ] Ajustar retrieval (número de exemplos, filtros)
- [ ] Otimizar prompts
- [ ] Documentar

---

## MELHORIAS FUTURAS

### Curto Prazo:
1. **Filtros avançados**: Por artista, época, memorabilidade
2. **Análise automática**: Avaliar letras geradas automaticamente
3. **Interface web**: Streamlit ou Gradio
4. **Cache**: Salvar gerações boas

### Médio Prazo:
1. **Hybrid search**: Combinar semantic + keyword
2. **Re-ranking**: Reordenar resultados por relevância
3. **Feedback loop**: Aprender com gerações aprovadas/rejeitadas
4. **Multi-query**: Buscar por múltiplos aspectos (tema + tom + estrutura)

### Longo Prazo:
1. **Fine-tuning**: Depois de ter muitas gerações boas, fine-tunar modelo
2. **Ensemble**: Combinar RAG + modelo fine-tunado
3. **Agentes**: Sistema multi-agente (um gera, outro critica, outro refina)

---

## CUSTO ESTIMADO TOTAL

### Setup inicial (one-time):
- Embeddings: $2-5 (OpenAI) ou $0 (local)
- Vector DB: $0 (Chroma local) ou $20/mês (Pinecone cloud)
- Desenvolvimento: Seu tempo (20-30 horas)

### Operacional (por mês):
- 100 gerações: $10-50 (Claude API)
- Vector DB: $0-20
- Total: $10-70/mês

**ROI**: Muito melhor que fine-tuning ($500-1000 setup)

---

## PRÓXIMOS PASSOS

1. **Decidir**: RAG, Fine-tuning, ou continuar com Prompt Engineering?
2. **Se RAG**: Local (grátis) ou Cloud (melhor qualidade)?
3. **Começar**: Preparar corpus estruturado

Quer que eu comece implementando o sistema RAG?
