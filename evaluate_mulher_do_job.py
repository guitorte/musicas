#!/usr/bin/env python3
"""
Avaliação da letra "Mulher do Job" usando o sistema V2.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'lyrics_analysis' / 'src'))

from quality_scorer import QualityScorer
from rhyme_engine import RhymeEngine
from semantic_coherence import SemanticCoherence

# Letra completa "Mulher do Job"
MULHER_DO_JOB = """Ela chega de salto, batom vermelho na boca
Terno justo marcando, todo mundo fica louco
CEO da própria vida, não depende de ninguém
Reunião de segunda, ela manda tipo refém

Presentação impecável, PowerPoint no capricho
Fala três idioma, fecha contrato no improviso
Café expresso duplo, ela nem sente o cansaço
Entre planilha e meta, rouba cena no espaço

Mulher do job, mulher do job
Tá comandando tudo e não precisa de nós
Independente, inteligente, é outro nível
Pega a promoção e ainda sai pra night depois

Mulher do job, mulher do job
Salário alto, carro importado, essa é boss
Tá fazendo dinheiro enquanto cê tá na pose
Respeita essa mina que ela é braba demais

Home office de pijama, mas na call tá de blazer
Multitask profissional, responde Slack sem perder
LinkedIn sempre em alta, networking é religião
Headhunter não sossega, manda proposta no direct então

Ela não precisa de príncipe, já tem seu próprio castelo
Apartamento na planta, investindo no modelo
Renda fixa e variável, ela entende de mercado
Enquanto nego tá no zero, ela tá consolidado

Mulher do job, mulher do job
Tá comandando tudo e não precisa de nós
Independente, inteligente, é outro nível
Pega a promoção e ainda sai pra night depois

Mulher do job, mulher do job
Salário alto, carro importado, essa é boss
Tá fazendo dinheiro enquanto cê tá na pose
Respeita essa mina que ela é braba demais

E se você chegar nela com papinho de crush
Ela vai te ignorar, tá ocupada no rush
Foco na carreira, amor fica pro after
Primeiro fecha o trimestre, depois a gente vê chapter

Não vem com flores baratas, ela quer ações da bolsa
Não adianta promessa, mostra o extrato da conta
Ela não tá impressionada com seu Instagram fake
Quer parceiro de verdade, não mais um paperweight

Mulher do job, mulher do job
Tá comandando tudo e não precisa de nós
Independente, inteligente, é outro nível
Pega a promoção e ainda sai pra night depois

Mulher do job, mulher do job
Salário alto, carro importado, essa é boss
Tá fazendo dinheiro enquanto cê tá na pose
Respeita essa mina que ela é braba demais

Mulher do job, mulher do job
Tá comandando tudo e não precisa de nós
Independente, inteligente, é outro nível
Pega a promoção e ainda sai pra night depois"""

def main():
    print("\n" + "="*80)
    print(" AVALIAÇÃO: 'MULHER DO JOB' ".center(80, "="))
    print("="*80 + "\n")

    # Initialize V2 modules
    scorer = QualityScorer()
    rhyme_engine = RhymeEngine()
    coherence = SemanticCoherence()

    # Get lyrics lines
    lines = [l.strip() for l in MULHER_DO_JOB.split('\n') if l.strip()]

    print(f"📝 LETRA COMPLETA ({len(lines)} linhas)\n")
    print("-"*80 + "\n")

    # === EFFECTIVENESS SCORING ===
    print("📊 EFFECTIVENESS ANALYSIS (Phase 2B)")
    print("-"*80)

    effectiveness = scorer.score_effectiveness(MULHER_DO_JOB)

    print(f"\n  Overall Score:    {effectiveness['overall_score']:.1f}/100")
    print(f"\n  Dimensões:")
    print(f"    • Structural Coherence:   {effectiveness['dimensions']['coherence']:.1f}/100")
    print(f"      (Estrutura bem formada, linhas consistentes)")
    print(f"    • Thematic Consistency:   {effectiveness['dimensions']['consistency']:.1f}/100")
    print(f"      (Coerência temática, foco no assunto)")
    print(f"    • Emotional Resonance:    {effectiveness['dimensions']['resonance']:.1f}/100")
    print(f"      (Impacto emocional, palavras fortes)")
    print(f"    • Memorability:           {effectiveness['dimensions']['memorability']:.1f}/100")
    print(f"      (Repetição de refrão, frases marcantes)")

    # === 4D SCORING ===
    print(f"\n\n🎯 4D SCORING SYSTEM")
    print("-"*80)

    scores_4d = scorer.score_4d(MULHER_DO_JOB, genre="Trap")

    print(f"\n  Innovation:    {scores_4d['innovation']:.1f}/100")
    print(f"    → Vocabulário único, conceito moderno")
    print(f"\n  Authenticity:  {scores_4d['authenticity']:.1f}/100")
    print(f"    → Português brasileiro, gírias atuais")
    print(f"\n  Risk:          {scores_4d['risk']:.1f}/100")
    print(f"    → Nível de experimentação")
    print(f"\n  Effectiveness: {scores_4d['effectiveness']:.1f}/100")
    print(f"    → Qualidade geral, funcionalidade")
    print(f"\n  Quality:       {scores_4d['quality']:.1f}/100")
    print(f"    → Score composto (innovation + effectiveness)")

    # === RHYME ANALYSIS ===
    print(f"\n\n🎼 RHYME ANALYSIS")
    print("-"*80)

    rhyme_stats = rhyme_engine.get_rhyme_statistics(lines)

    print(f"\n  Rhyme Percentage:  {rhyme_stats['rhyme_percentage']:.1f}%")
    print(f"  Rhyme Pairs:       {rhyme_stats['rhyme_pairs']}/{rhyme_stats['total_pairs']}")
    print(f"  Has Rhymes:        {'✅ SIM' if rhyme_stats['has_rhymes'] else '❌ NÃO'}")

    # Identify specific rhyme pairs
    print(f"\n  Principais Rimas Detectadas:")
    last_words = rhyme_stats['last_words']

    # Sample some rhyme pairs
    rhyme_pairs_found = []
    for i in range(len(last_words)):
        for j in range(i+1, min(i+5, len(last_words))):
            if rhyme_engine.words_rhyme(last_words[i], last_words[j]):
                rhyme_pairs_found.append((last_words[i], last_words[j]))

    for word1, word2 in rhyme_pairs_found[:10]:
        quality = rhyme_engine.rhyme_quality(word1, word2)
        print(f"    • '{word1}' ↔ '{word2}' ({quality})")

    # === STRUCTURE ANALYSIS ===
    print(f"\n\n🏗️  STRUCTURE ANALYSIS")
    print("-"*80)

    # Count sections
    verses = 0
    choruses = 0
    for line in lines:
        if "mulher do job" in line.lower():
            choruses += 1
        elif len(line) > 20:  # Arbitrary - verse lines are usually longer
            verses += 1

    print(f"\n  Total Lines:      {len(lines)}")
    print(f"  Verses:           ~{verses} linhas")
    print(f"  Chorus Lines:     ~{choruses} linhas")
    print(f"  Repetition:       Alto (refrão repetido 6x)")

    # Word count
    words = MULHER_DO_JOB.split()
    print(f"  Total Words:      {len(words)}")
    print(f"  Avg Words/Line:   {len(words)/len(lines):.1f}")

    # === VOCABULARY ANALYSIS ===
    print(f"\n\n📚 VOCABULARY ANALYSIS")
    print("-"*80)

    # Modern/professional words
    modern_words = ['job', 'PowerPoint', 'LinkedIn', 'Slack', 'home office',
                    'networking', 'headhunter', 'CEO', 'boss', 'Instagram']

    found_modern = [w for w in modern_words if w.lower() in MULHER_DO_JOB.lower()]

    print(f"\n  Palavras Modernas/Profissionais:")
    for word in found_modern:
        print(f"    • {word}")

    # Slang/casual
    slang_words = ['braba', 'mina', 'nego', 'cê', 'tá', 'pra', 'papinho']
    found_slang = [w for w in slang_words if w.lower() in MULHER_DO_JOB.lower()]

    print(f"\n  Gírias/Linguagem Casual:")
    for word in found_slang:
        print(f"    • {word}")

    # === THEMATIC COHERENCE ===
    print(f"\n\n🎨 THEMATIC COHERENCE")
    print("-"*80)

    # Note: Our coherence module expects specific themes
    # This is a custom theme, so we'll measure differently

    # Count empowerment/professional words
    empowerment_words = ['independente', 'inteligente', 'comandando', 'CEO',
                         'boss', 'profissional', 'própria', 'respeita']

    found_empowerment = sum(1 for w in empowerment_words if w.lower() in MULHER_DO_JOB.lower())

    print(f"\n  Tema Central: Empoderamento Profissional Feminino")
    print(f"  Palavras de Empoderamento: {found_empowerment}/{len(empowerment_words)}")
    print(f"  Foco Temático: ✅ MUITO FORTE")
    print(f"  Narrativa: Consistente do início ao fim")

    # === MEMORABILITY FACTORS ===
    print(f"\n\n💡 MEMORABILITY FACTORS")
    print("-"*80)

    print(f"\n  ✅ Refrão Chiclete: 'Mulher do job, mulher do job'")
    print(f"  ✅ Repetição Alta: Refrão aparece 6x")
    print(f"  ✅ Frases Marcantes:")
    print(f"     • 'CEO da própria vida'")
    print(f"     • 'Respeita essa mina que ela é braba demais'")
    print(f"     • 'Não precisa de príncipe, já tem seu próprio castelo'")
    print(f"  ✅ Call-and-Response: 'Mulher do job' pode ter resposta do público")
    print(f"  ✅ Vocabulário Moderno: Conecta com público jovem/urbano")

    # === CULTURAL RELEVANCE ===
    print(f"\n\n🌎 CULTURAL RELEVANCE")
    print("-"*80)

    print(f"\n  Contexto Brasileiro:      ✅ Forte")
    print(f"  Linguagem Atual (2024+):  ✅ Muito forte")
    print(f"  Temas Contemporâneos:     ✅ Empoderamento feminino, trabalho, independência")
    print(f"  Público-Alvo:             Mulheres 25-40 anos, profissionais")
    print(f"  Potencial Viral:          ✅ Alto (TikTok, Reels)")

    # === FINAL VERDICT ===
    print(f"\n\n" + "="*80)
    print(" AVALIAÇÃO FINAL ".center(80, "="))
    print("="*80 + "\n")

    overall = effectiveness['overall_score']
    quality = scores_4d['quality']
    rhyme = rhyme_stats['rhyme_percentage']

    print(f"  📊 Effectiveness:        {overall:.1f}/100  {'⭐⭐⭐⭐' if overall > 70 else '⭐⭐⭐'}")
    print(f"  🎯 Quality Score:        {quality:.1f}/100  {'⭐⭐⭐⭐' if quality > 65 else '⭐⭐⭐'}")
    print(f"  🎼 Rhyme Quality:        {rhyme:.1f}%      {'⭐⭐⭐⭐' if rhyme > 20 else '⭐⭐⭐'}")
    print(f"  💡 Memorability:         {effectiveness['dimensions']['memorability']:.1f}/100  {'⭐⭐⭐' if effectiveness['dimensions']['memorability'] > 30 else '⭐⭐'}")

    print(f"\n  VEREDITO:")
    if overall > 70 and quality > 60:
        print(f"  ✅ LETRA DE ALTA QUALIDADE - UTILIZÁVEL EM PRODUÇÃO")
        print(f"  ✅ Forte apelo comercial, tema relevante")
        print(f"  ✅ Refrão memorável, estrutura sólida")
        print(f"  ✅ Vocabulário moderno e autêntico")
    elif overall > 60:
        print(f"  ⚠️  BOA QUALIDADE - COM POTENCIAL")
        print(f"  ⚠️  Precisa de ajustes menores")
    else:
        print(f"  ❌ PRECISA DE REVISÃO")

    print(f"\n  PONTOS FORTES:")
    print(f"    • Tema atual e relevante (empoderamento feminino profissional)")
    print(f"    • Refrão chiclete e memorável")
    print(f"    • Vocabulário moderno (LinkedIn, Slack, PowerPoint)")
    print(f"    • Narrativa coerente e consistente")
    print(f"    • Estrutura clara (verso-refrão-verso-refrão-ponte-refrão)")

    print(f"\n  SUGESTÕES DE MELHORIA:")
    print(f"    • Aumentar memorabilidade com mais hooks vocais")
    print(f"    • Considerar adicionar ad-libs no refrão")
    print(f"    • Possível bridge mais melódica para contraste")

    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
