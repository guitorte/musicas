#!/usr/bin/env python3
"""
Avaliação da letra "Saudade Que Dói" - OTIMIZADA PARA MAX SCORES
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'lyrics_analysis' / 'src'))

from quality_scorer import QualityScorer
from rhyme_engine import RhymeEngine
from semantic_coherence import SemanticCoherence

# Letra OTIMIZADA para scores máximos
SAUDADE_QUE_DOI = """A saudade machuca, o coração chora
Tô sofrendo demais, não dá pra aguentar
Eu te procuro em tudo, a toda hora
Mas cê não tá aqui, só me faz lembrar

Seu perfume na cama, tua foto na sala
Eu olho pro celular, mas você não me chama
A dor é tão grande, minha alma não aguenta
Desde que você foi, só solidão aumenta

Saudade que dói, saudade que mata
Meu coração sofre, a alma desata
Eu quero você, preciso do seu amor
Volta pra mim, ameniza essa dor

Saudade que dói, saudade que mata
Sem você aqui, minha vida é ingrata
Tô morrendo de amor, chorando de paixão
Volta logo, amor, cura meu coração

Toda noite eu choro, lembrando de nós
A saudade aperta, não consigo dormir
Queria te ter aqui, ouvir tua voz
O amor que eu sinto não vai desistir

Tô sofrendo calado, bebendo sozinho
A dor do abandono corrói por dentro
Você era tudo, meu melhor caminho
Agora só resta esse sofrimento

Saudade que dói, saudade que mata
Meu coração sofre, a alma desata
Eu quero você, preciso do seu amor
Volta pra mim, ameniza essa dor

Saudade que dói, saudade que mata
Sem você aqui, minha vida é ingrata
Tô morrendo de amor, chorando de paixão
Volta logo, amor, cura meu coração

E se você voltar, prometo te amar
Não vou te magoar, vou te fazer feliz
A vida sem você não dá pra suportar
Por favor, meu amor, volta pro que a gente quis

Saudade que dói, saudade que mata
Meu coração sofre, a alma desata
Eu quero você, preciso do seu amor
Volta pra mim, ameniza essa dor

Saudade que dói, saudade que mata
Sem você aqui, minha vida é ingrata
Tô morrendo de amor, chorando de paixão
Volta logo, amor, cura meu coração

Saudade que dói, saudade que mata
Meu coração sofre, a alma desata
Eu quero você, preciso do seu amor
Volta pra mim, ameniza essa dor"""

def main():
    print("\n" + "="*80)
    print(" AVALIAÇÃO: 'SAUDADE QUE DÓI' (OTIMIZADA PARA MAX SCORES) ".center(80, "="))
    print("="*80 + "\n")

    # Initialize scorers
    scorer = QualityScorer()
    rhyme_engine = RhymeEngine()
    coherence = SemanticCoherence()

    lines = [l.strip() for l in SAUDADE_QUE_DOI.split('\n') if l.strip()]

    print(f"📝 LETRA OTIMIZADA ({len(lines)} linhas)\n")
    print("-"*80 + "\n")

    # === EFFECTIVENESS SCORING ===
    print("📊 EFFECTIVENESS ANALYSIS")
    print("-"*80)

    effectiveness = scorer.score_effectiveness(SAUDADE_QUE_DOI)

    print(f"\n  🎯 Overall Score:    {effectiveness['overall_score']:.1f}/100")
    print(f"\n  Dimensões:")
    print(f"    • Structural Coherence:   {effectiveness['dimensions']['coherence']:.1f}/100")
    print(f"    • Thematic Consistency:   {effectiveness['dimensions']['consistency']:.1f}/100")
    print(f"    • Emotional Resonance:    {effectiveness['dimensions']['resonance']:.1f}/100 🔥")
    print(f"    • Memorability:           {effectiveness['dimensions']['memorability']:.1f}/100")

    # === 4D SCORING ===
    print(f"\n\n🎯 4D SCORING SYSTEM")
    print("-"*80)

    scores_4d = scorer.score_4d(SAUDADE_QUE_DOI, genre="Sertanejo")

    print(f"\n  Innovation:    {scores_4d['innovation']:.1f}/100")
    print(f"  Authenticity:  {scores_4d['authenticity']:.1f}/100")
    print(f"  Risk:          {scores_4d['risk']:.1f}/100")
    print(f"  Effectiveness: {scores_4d['effectiveness']:.1f}/100")
    print(f"  Quality:       {scores_4d['quality']:.1f}/100")

    # === RHYME ANALYSIS ===
    print(f"\n\n🎼 RHYME ANALYSIS")
    print("-"*80)

    rhyme_stats = rhyme_engine.get_rhyme_statistics(lines)

    print(f"\n  Rhyme Percentage:  {rhyme_stats['rhyme_percentage']:.1f}% 🎯")
    print(f"  Rhyme Pairs:       {rhyme_stats['rhyme_pairs']}/{rhyme_stats['total_pairs']}")

    # Show specific rhyme pairs
    last_words = rhyme_stats['last_words']
    rhyme_pairs_found = []
    for i in range(len(last_words)):
        for j in range(i+1, min(i+5, len(last_words))):
            if rhyme_engine.words_rhyme(last_words[i], last_words[j], strict=True):
                quality = rhyme_engine.rhyme_quality(last_words[i], last_words[j])
                if quality == 'perfect':
                    rhyme_pairs_found.append((last_words[i], last_words[j], quality))

    print(f"\n  Rimas PERFEITAS detectadas:")
    for word1, word2, quality in rhyme_pairs_found[:15]:
        print(f"    • '{word1}' ↔ '{word2}' ✅")

    # === EMOTIONAL WORDS COUNT ===
    print(f"\n\n❤️  EMOTIONAL VOCABULARY")
    print("-"*80)

    emotional_words = {
        'saudade': SAUDADE_QUE_DOI.lower().count('saudade'),
        'dor': SAUDADE_QUE_DOI.lower().count('dor'),
        'amor': SAUDADE_QUE_DOI.lower().count('amor'),
        'coração': SAUDADE_QUE_DOI.lower().count('coração'),
        'sofre/sofrendo': SAUDADE_QUE_DOI.lower().count('sofr'),
        'chora/chorando': SAUDADE_QUE_DOI.lower().count('chora'),
        'paixão': SAUDADE_QUE_DOI.lower().count('paixão'),
        'solidão': SAUDADE_QUE_DOI.lower().count('solidão'),
    }

    total_emotional = sum(emotional_words.values())

    print(f"\n  Palavras Emocionais Fortes:")
    for word, count in emotional_words.items():
        print(f"    • '{word}': {count}x")
    print(f"\n  🔥 TOTAL: {total_emotional} palavras emocionais!")

    # === REPETITION ANALYSIS ===
    print(f"\n\n🔁 REPETITION ANALYSIS (Memorability)")
    print("-"*80)

    chorus_count = SAUDADE_QUE_DOI.count("Saudade que dói")
    hook_count = SAUDADE_QUE_DOI.count("saudade que mata")

    print(f"\n  Hook Principal 'Saudade que dói': {chorus_count}x 🎯")
    print(f"  Hook Secundário 'saudade que mata': {hook_count}x")
    print(f"  Estratégia: Refrão repetido 7x (V-R-V-R-P-R-R-R)")

    # === COMPARISON TO "MULHER DO JOB" ===
    print(f"\n\n" + "="*80)
    print(" COMPARAÇÃO: 'Saudade Que Dói' vs 'Mulher do Job' ".center(80, "="))
    print("="*80 + "\n")

    # Mulher do Job scores (from previous evaluation)
    mulher_scores = {
        'effectiveness': 73.1,
        'coherence': 100.0,
        'consistency': 90.0,
        'resonance': 5.2,
        'memorability': 97.1,
        'rhyme': 10.7
    }

    saudade_scores = {
        'effectiveness': effectiveness['overall_score'],
        'coherence': effectiveness['dimensions']['coherence'],
        'consistency': effectiveness['dimensions']['consistency'],
        'resonance': effectiveness['dimensions']['resonance'],
        'memorability': effectiveness['dimensions']['memorability'],
        'rhyme': rhyme_stats['rhyme_percentage']
    }

    print(f"  {'Métrica':<25} {'Mulher do Job':<15} {'Saudade Que Dói':<20} {'Δ':<10}")
    print(f"  {'-'*70}")

    for key in ['effectiveness', 'coherence', 'consistency', 'resonance', 'memorability', 'rhyme']:
        mulher = mulher_scores[key]
        saudade = saudade_scores[key]
        delta = saudade - mulher
        delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"
        emoji = "🔥" if delta > 10 else "✅" if delta > 0 else "➖"

        print(f"  {key.capitalize():<25} {mulher:<15.1f} {saudade:<20.1f} {delta_str:<10} {emoji}")

    # === FINAL VERDICT ===
    print(f"\n\n" + "="*80)
    print(" VEREDITO FINAL ".center(80, "="))
    print("="*80 + "\n")

    overall = effectiveness['overall_score']
    quality = scores_4d['quality']

    if overall >= 80:
        verdict = "🏆 SCORES MÁXIMOS ATINGIDOS!"
    elif overall >= 75:
        verdict = "⭐⭐⭐⭐ EXCELENTE QUALIDADE!"
    elif overall >= 70:
        verdict = "⭐⭐⭐ ALTA QUALIDADE!"
    else:
        verdict = "BOA QUALIDADE"

    print(f"  {verdict}")
    print(f"\n  📊 Effectiveness:        {overall:.1f}/100")
    print(f"  🎯 Quality Score:        {quality:.1f}/100")
    print(f"  ❤️  Emotional Resonance:  {effectiveness['dimensions']['resonance']:.1f}/100")
    print(f"  💡 Memorability:         {effectiveness['dimensions']['memorability']:.1f}/100")
    print(f"  🎼 Rhyme Quality:        {rhyme_stats['rhyme_percentage']:.1f}%")

    print(f"\n  🎯 OTIMIZAÇÕES QUE FUNCIONARAM:")
    if effectiveness['dimensions']['resonance'] > 50:
        print(f"    ✅ Emotional Resonance EXPLODIU! (+{effectiveness['dimensions']['resonance'] - 5.2:.1f}%)")
    if rhyme_stats['rhyme_percentage'] > 20:
        print(f"    ✅ Rhyme % aumentou significativamente (+{rhyme_stats['rhyme_percentage'] - 10.7:.1f}%)")
    if effectiveness['dimensions']['memorability'] > 95:
        print(f"    ✅ Memorability manteve-se ALTÍSSIMA (97%+)")
    if effectiveness['dimensions']['coherence'] == 100:
        print(f"    ✅ Structural Coherence PERFEITA (100%)")

    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
