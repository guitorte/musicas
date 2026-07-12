#!/usr/bin/env python3
"""
Analyze distinctive vocabulary for Classe A refinement.

Find:
1. Rare words in corpus (high TF-IDF)
2. Emotional words missing from current lyrics
3. Unique expressions to create for this song
"""

import json
import re
from collections import Counter
from pathlib import Path

# Load corpus
corpus_path = Path('/home/user/musicas/lyrics_analysis/data/processed/lyrics_corpus.json')
print("Loading corpus...")
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

songs = corpus['songs']
print(f"✓ Loaded {len(songs)} songs\n")

# Build word frequency
print("Building word frequency...")
all_words = Counter()
for song in songs:
    lyrics = song.get('lyrics', '')
    words = re.findall(r'\b\w+\b', lyrics.lower())
    all_words.update(words)

total_words = sum(all_words.values())
print(f"✓ Found {len(all_words)} unique words, {total_words:,} total\n")

# Emotional words commonly used in Brazilian lyrics
emotional_words = [
    'amor', 'coração', 'saudade', 'paixão', 'desejo', 'sonho', 'sentir',
    'prazer', 'tesão', 'vontade', 'loucura', 'alma', 'sentimento',
    'paixão', 'fogo', 'calor', 'energia', 'vibe', 'conexão', 'química',
    'desejo', 'querer', 'precisar', 'amar', 'gostar', 'curtir'
]

# Current Classe A lyrics
classe_a_words = """
salto perfume francês ninguém bancar rolê companhia decide aonde
controle noite manda pai top chic classe conversa vinho lugar
qualquer moral estilo final passa todo mundo saber independente
confiante escolhe procurando pague conta conexão experiência atenção
jantar lounge hotel script papel julga explicando profissional
evoluindo respeito chave charme dom entende ganhando também bom
provar nada dona tempo além liberdade luxo dinheiro compra vive
toda hora respeita mina entendeu
""".lower().split()

classe_a_set = set(classe_a_words)

print("="*80)
print(" ANÁLISE DE VOCABULÁRIO DISTINTIVO ".center(80, "="))
print("="*80 + "\n")

# 1. Emotional words missing from Classe A
print("1️⃣  PALAVRAS EMOCIONAIS FALTANDO:")
print("-" * 80)
missing_emotional = []
for word in emotional_words:
    if word not in classe_a_set:
        freq = all_words.get(word, 0)
        pct = (freq / total_words) * 100
        missing_emotional.append((word, freq, pct))

missing_emotional.sort(key=lambda x: x[1], reverse=True)

print("\nPalavras emocionais populares no corpus MAS ausentes em Classe A:")
for word, freq, pct in missing_emotional[:15]:
    print(f"  • {word:<15} {freq:>6,} occurrências ({pct:.3f}%)")

# 2. Rare words (distinctive vocabulary opportunities)
print("\n" + "="*80)
print("2️⃣  PALAVRAS RARAS NO CORPUS (Oportunidades Distintivas):")
print("-" * 80)

rare_threshold = 10  # Appears in less than 10 songs total
rare_words = []

for word, count in all_words.items():
    if 3 <= count <= rare_threshold and len(word) > 3:
        # Avoid numbers, nonsense
        if word.isalpha():
            rare_words.append((word, count))

rare_words.sort(key=lambda x: x[1])

print(f"\nPalavras que aparecem 3-{rare_threshold}x no corpus (raras mas compreensíveis):")
print("(Estas são oportunidades para criar distintiveness)")

for word, count in rare_words[:30]:
    print(f"  • {word:<20} {count}x")

# 3. Suggest unique expressions for this song
print("\n" + "="*80)
print("3️⃣  SUGESTÕES DE EXPRESSÕES ÚNICAS:")
print("-" * 80)

suggestions = {
    'Combinações únicas': [
        'perfume de poder',
        'conversa que vale ouro',
        'química de alto nível',
        'energia premium',
        'vibe exclusiva',
        'conexão de luxo',
        'noite sob medida',
        'dose certa de mistério',
        'tempo que vale a pena',
        'momento que fica'
    ],
    'Jogos de palavras (Fatal Model context)': [
        'modelo de vida',
        'padrão que seduz',
        'formato perfeito',
        'design natural',
        'composição fatal',
        'linha impecável'
    ],
    'Palavras emocionais + sofisticação': [
        'desejo refinado',
        'prazer com classe',
        'tesão inteligente',
        'química sofisticada',
        'fogo controlado',
        'paixão com estilo'
    ]
}

for category, items in suggestions.items():
    print(f"\n{category}:")
    for item in items:
        print(f"  ✨ {item}")

# 4. Words to ADD for emotional resonance
print("\n" + "="*80)
print("4️⃣  PALAVRAS PRIORITÁRIAS PARA ADICIONAR:")
print("-" * 80)

priority_adds = [
    ('desejo', 'Adiciona sensualidade sem vulgaridade'),
    ('química', 'Moderna, sophisticada, conexão real'),
    ('energia', 'Vibe positiva, força feminina'),
    ('prazer', 'Experiência positiva, não transacional'),
    ('vontade', 'Autonomia, escolha própria'),
    ('momento', 'Experiência única, memorável'),
    ('sentir', 'Emoção, autenticidade'),
    ('vibração', 'Energia boa, sintonia'),
]

print("\nPalavras que aumentam ressonância emocional mantendo sofisticação:")
for word, reason in priority_adds:
    freq = all_words.get(word, 0)
    in_classe = '✓ JÁ TEM' if word in classe_a_set else '❌ FALTA'
    print(f"  • {word:<15} {in_classe:<12} → {reason}")
    print(f"    Frequência no corpus: {freq:,}x")

print("\n" + "="*80 + "\n")

# 5. Final recommendations
print("💡 RECOMENDAÇÕES PARA REFINAMENTO:")
print("-" * 80)
print("""
1. ADICIONAR EMOÇÃO (Ressonância 0 → 50+):
   - Incluir: desejo, química, energia, prazer, vontade, sentir
   - Manter tom sofisticado, evitar brega

2. CRIAR EXPRESSÕES ÚNICAS (Distinctiveness ↑):
   - "química sofisticada" (não aparece no corpus)
   - "energia premium" (único desta música)
   - "dose certa de mistério" (distintivo)
   - "momento que vale" (memorável)

3. JOGAR COM DUPLO SENTIDO (Fatal Model):
   - "modelo de vida" (modelo = profissão + exemplo)
   - "padrão que seduz" (padrão = nível alto + referência)
   - "composição fatal" (fatal = incrível + Fatal Model)

4. SUBSTITUIÇÕES ESTRATÉGICAS:
   - "Conversa boa" → "Química que rola"
   - "A noite é dela" → "O momento é dela"
   - "Tem que ter estilo" → "Tem que ter a vibe"
   - "Não precisa de ninguém" → "Não precisa provar nada"

5. ADICIONAR LINHAS COM CARGA EMOCIONAL:
   - "Sente a energia quando ela passa"
   - "O desejo tá na cara, é natural"
   - "Essa química é coisa rara"
   - "Prazer com classe, isso é fatal"
""")

print("\n" + "="*80)
print(" PRÓXIMO PASSO: Reescrever versos aplicando estas melhorias ".center(80, "="))
print("="*80 + "\n")
