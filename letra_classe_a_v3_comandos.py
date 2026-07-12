"""
CLASSE A V3 - Versão com Comandos e Duplo Sentido
Critérios adicionais:
- Linguagem imperativa (comandos)
- Duplo sentido sexual implícito
- Boa deniability (pode ser interpretado inocentemente)
- Mantém sofisticação
"""

CLASSE_A_V3_COMANDOS = """
[Intro - Naldo falando]
Ô, ô, ô!
Isso é Naldo!
Vem, vem, vem!
Fatal!

[Verso 1]
Chega devagar, mostra teu padrão
Deixa eu sentir a energia da tua mão
Solta essa vibe, não esconde não
Entra no clima, que hoje tem conexão

Vem com calma, deixa acontecer
Mostra teu jogo, quero conhecer
Segura esse lance com classe, vê
Aguenta a pressão, que é outro nível, cê

[Pré-Refrão]
Sente a química quando ela passa, ô, ô
Olha nos olhos, deixa a vibe tomar conta
Para tudo, presta atenção
Essa dose certa vai explodir na mão

[Refrão - 2x]
Classe A, classe A
Vem devagar que eu quero aproveitar
Classe A, classe A
Mostra teu padrão, deixa eu admirar

[Verso 2]
Toma teu tempo, não precisa acelerar
Deixa fluir, que eu quero saborear
Segura esse desejo, controla o ar
Sente o momento, tá pronta pra arrasar

Vem sem pressa, mostra quem tu é
Solta esse charme, deixa eu te ver
Entra no ritmo, balança com fé
Aguenta o tranco, que é prazer de A a Z

[Pré-Refrão]
Sente a química quando ela passa, ô, ô
Olha nos olhos, deixa a vibe tomar conta
Para tudo, presta atenção
Essa dose certa vai explodir na mão

[Refrão - 3x]
Classe A, classe A
Vem devagar que eu quero aproveitar
Classe A, classe A
Mostra teu padrão, deixa eu admirar

[Ponte]
Olha só (olha só!)
Vem assim que tá bom demais (vem!)
Deixa rolar (deixa!)
Que essa noite não volta mais

Sente o poder, sente o comando
Mostra tua força, vai soltando
Aguenta firme, segura na mão
Essa composição fatal tá pegando fogo, irmão!

[Refrão Final - 4x com ad-libs]
Classe A, classe A (Vem, vem!)
Vem devagar que eu quero aproveitar (Assim!)
Classe A, classe A (Ô, ô! Fatal!)
Mostra teu padrão, deixa eu admirar (Naldo!)

[Outro - Naldo falando]
Vem com classe, entendeu?
Mostra teu padrão!
Fatal! Naldo!
"""

print("="*80)
print(" CLASSE A V3 - COMANDOS + DUPLO SENTIDO ".center(80, "="))
print("="*80 + "\n")

print("🎯 NOVOS CRITÉRIOS APLICADOS:")
print("-" * 80 + "\n")

print("1️⃣  COMANDOS NO IMPERATIVO (Linguagem de Controle):")
print("-" * 80)

comandos = {
    "Vem": "Vem devagar, Vem com calma, Vem sem pressa, Vem assim",
    "Mostra": "Mostra teu padrão, Mostra teu jogo, Mostra quem tu é, Mostra tua força",
    "Deixa": "Deixa eu sentir, Deixa acontecer, Deixa fluir, Deixa rolar, Deixa a vibe tomar",
    "Solta": "Solta essa vibe, Solta esse charme, Vai soltando",
    "Sente": "Sente a química, Sente o momento, Sente o poder, Sente o comando",
    "Entra": "Entra no clima, Entra no ritmo",
    "Segura": "Segura esse lance, Segura esse desejo, Segura na mão, Aguenta firme",
    "Olha": "Olha nos olhos, Olha só, Para tudo",
    "Toma": "Toma teu tempo",
    "Aguenta": "Aguenta a pressão, Aguenta o tranco"
}

total_comandos = sum(CLASSE_A_V3_COMANDOS.count(v.split(",")[0]) for v in comandos.values())

for cmd, usos in comandos.items():
    print(f"  • {cmd:<10} → {usos}")

print(f"\n  TOTAL: ~{total_comandos}+ comandos na letra!")

print("\n" + "="*80)
print("2️⃣  DUPLO SENTIDO SEXUAL (com Deniability):")
print("-" * 80 + "\n")

duplo_sentido = [
    {
        "frase": "Chega devagar, mostra teu padrão",
        "inocente": "Chegue com calma e mostre sua qualidade/classe",
        "sexual": "Aproximação física gradual e sedutora",
        "deniability": "⭐⭐⭐⭐⭐"
    },
    {
        "frase": "Deixa eu sentir a energia da tua mão",
        "inocente": "Deixe eu perceber sua presença/aura",
        "sexual": "Toque físico, contato íntimo",
        "deniability": "⭐⭐⭐⭐"
    },
    {
        "frase": "Entra no clima, que hoje tem conexão",
        "inocente": "Entre no ambiente, há sintonia",
        "sexual": "Clima de sedução, química sexual",
        "deniability": "⭐⭐⭐⭐⭐"
    },
    {
        "frase": "Vem com calma, deixa acontecer",
        "inocente": "Venha tranquilamente, deixe fluir naturalmente",
        "sexual": "Preliminares, deixar o sexo acontecer",
        "deniability": "⭐⭐⭐⭐⭐"
    },
    {
        "frase": "Mostra teu jogo, quero conhecer",
        "inocente": "Mostre sua estratégia/personalidade",
        "sexual": "Mostre suas habilidades de sedução",
        "deniability": "⭐⭐⭐⭐⭐"
    },
    {
        "frase": "Segura esse lance com classe",
        "inocente": "Lide com a situação com elegância",
        "sexual": "Controle do desejo/excitação",
        "deniability": "⭐⭐⭐⭐"
    },
    {
        "frase": "Aguenta a pressão",
        "inocente": "Suporte o desafio/responsabilidade",
        "sexual": "Aguente a intensidade sexual",
        "deniability": "⭐⭐⭐⭐"
    },
    {
        "frase": "Essa dose certa vai explodir na mão",
        "inocente": "A medida perfeita vai dar resultado",
        "sexual": "Clímax, orgasmo",
        "deniability": "⭐⭐⭐"
    },
    {
        "frase": "Toma teu tempo, não precisa acelerar",
        "inocente": "Vá no seu ritmo, sem pressa",
        "sexual": "Prolongar preliminares, não se apressar",
        "deniability": "⭐⭐⭐⭐⭐"
    },
    {
        "frase": "Deixa fluir, que eu quero saborear",
        "inocente": "Deixe acontecer naturalmente, quero aproveitar",
        "sexual": "Deixe o prazer fluir, quero prolongar",
        "deniability": "⭐⭐⭐⭐"
    },
    {
        "frase": "Segura esse desejo, controla o ar",
        "inocente": "Controle sua vontade, mantenha a calma",
        "sexual": "Controle a excitação, respiração ofegante",
        "deniability": "⭐⭐⭐⭐"
    },
    {
        "frase": "Entra no ritmo, balança com fé",
        "inocente": "Entre na dança, balance com confiança",
        "sexual": "Movimento sexual, ritmo do ato",
        "deniability": "⭐⭐⭐⭐"
    },
    {
        "frase": "Aguenta o tranco, que é prazer de A a Z",
        "inocente": "Aguente o desafio, é satisfação completa",
        "sexual": "Aguente a intensidade, prazer total",
        "deniability": "⭐⭐⭐"
    },
    {
        "frase": "Vem devagar que eu quero aproveitar",
        "inocente": "Venha com calma que quero desfrutar",
        "sexual": "Vem devagar no ato, prolongar prazer",
        "deniability": "⭐⭐⭐⭐"
    },
    {
        "frase": "Essa composição fatal tá pegando fogo",
        "inocente": "Essa combinação incrível está bombando",
        "sexual": "A química sexual está intensa",
        "deniability": "⭐⭐⭐⭐⭐"
    },
]

for i, ds in enumerate(duplo_sentido, 1):
    print(f"{i:>2}. \"{ds['frase']}\"")
    print(f"    Inocente: {ds['inocente']}")
    print(f"    Sexual:   {ds['sexual']}")
    print(f"    Deniability: {ds['deniability']}\n")

print("="*80)
print("3️⃣  ANÁLISE DE SOPHISTICAÇÃO:")
print("-" * 80 + "\n")

print("✅ MANTÉM SOFISTICAÇÃO:")
print("  • Nenhuma linguagem vulgar direta")
print("  • Todo duplo sentido é implícito")
print("  • Pode ser cantada em rádio sem censura")
print("  • Contexto de acompanhante sofisticada mantido")
print("  • Zero menção a valores/preço\n")

print("✅ EMPODERAMENTO FEMININO:")
print("  • 'Ela que passa' - protagonismo feminino")
print("  • 'Mostra teu padrão' - ela define o padrão")
print("  • 'Sente o poder, sente o comando' - poder feminino")
print("  • Comandos PARA ela mostrar/sentir, não submissão\n")

print("✅ DENIABILITY ALTA:")
print("  • Média de ⭐⭐⭐⭐ (4/5 estrelas)")
print("  • Pode ser interpretado como dança, sedução leve")
print("  • Palavras-chave: clima, energia, vibe, ritmo, jogo")
print("  • Sem palavras explicitamente sexuais\n")

print("="*80)
print("4️⃣  ESTRUTURA MUSICAL:")
print("-" * 80 + "\n")

print("🎵 COMANDOS COMO HOOK:")
print("  • Refrão: 'Vem devagar que eu quero aproveitar' (imperativo)")
print("  • Repetição de comandos cria chamado-resposta")
print("  • Intro/Outro: 'Vem, vem, vem!' (explosivo)")
print("  • Ponte: 'Olha só', 'Vem assim', 'Deixa rolar' (interativo)\n")

print("🎤 ESTILO NALDO:")
print("  • Comandos diretos (característico do funk)")
print("  • Coloquialismos: 'cê', 'tá', 'ô', 'irmão'")
print("  • Energia crescente (calma → explosão)")
print("  • Ad-libs: 'Vem!', 'Assim!', 'Ô, ô!'\n")

print("="*80)
print(" COMPARAÇÃO V2 vs V3 ".center(80, "="))
print("="*80 + "\n")

print("V2 (Empoderamento Puro):")
print("  • Foco: Independência feminina, sofisticação")
print("  • Tom: Respeitoso, elegante")
print("  • Sexual: Apenas 'desejo' implícito")
print("  • Comandos: Poucos (narrativa descritiva)\n")

print("V3 (Comandos + Duplo Sentido):")
print("  • Foco: Sedução sofisticada, interação")
print("  • Tom: Sensual mas elegante")
print("  • Sexual: Múltiplos duplo sentidos (15+)")
print("  • Comandos: Muitos (linguagem imperativa)\n")

print("="*80)
print(" LETRA COMPLETA V3 ".center(80, "="))
print("="*80 + "\n")
print(CLASSE_A_V3_COMANDOS)

print("\n" + "="*80)
print(" RECOMENDAÇÃO ".center(80, "="))
print("="*80 + "\n")

print("V3 É MAIS OUSADA que V2, mas mantém:")
print("  ✅ Sofisticação (sem vulgaridade)")
print("  ✅ Deniability alta (pode tocar em rádio)")
print("  ✅ Duplo sentido Fatal Model ('composição fatal')")
print("  ✅ Estilo Naldo Benny (comandos, energia)")
print("  ✅ Zero menção a preço\n")

print("NOVA: Conotação sexual implícita torna mais envolvente!")
print("NOVA: Comandos criam interação direta com público!")
print("NOVA: Múltiplos layers de interpretação!\n")

print("="*80)

# Count stats
lyrics = CLASSE_A_V3_COMANDOS
print("\n📊 ESTATÍSTICAS V3:")
print("-" * 80)
print(f"  Comandos (imperativo): ~25+ ocorrências")
print(f"  Duplo sentido sexual: 15+ frases")
print(f"  Deniability média: ⭐⭐⭐⭐ (4/5)")
print(f"  Coloquialismos: {lyrics.count('ô') + lyrics.count('cê') + lyrics.count('tá')}+ ocorrências")
print(f"  'Classe A' (hook): {lyrics.count('Classe A')}x")
print(f"  'Fatal' (marca): {lyrics.count('Fatal')}x")
print("\n" + "="*80 + "\n")
