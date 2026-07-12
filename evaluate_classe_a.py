#!/usr/bin/env python3
"""Evaluate 'Classe A' lyrics with the scoring system."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'lyrics_analysis' / 'src'))

from quality_scorer import QualityScorer
from rhyme_engine import RhymeEngine
from semantic_coherence import SemanticCoherence

# Letra completa (sem tags de estrutura)
CLASSE_A_LYRICS = """
Ô, ô, ô!
Isso é Naldo!
Pra mulher que sabe o que quer, hein!

Ela chega de salto, perfume francês
Não precisa de ninguém pra bancar o rolê
Escolhe a companhia, decide aonde vai
Tá no controle da noite, ninguém manda nela, pai

É top, é chic, é classe A
Conversa boa, vinho e um lugar
Não é qualquer um que ela dá moral
Tem que ter estilo pra chegar no final

E quando ela passa, ô, ô
Todo mundo quer saber quem é
Independente, confiante, vê
Ela que escolhe com quem vai ser

Classe A, classe A
Sofisticada, ninguém vai te parar
Classe A, classe A
Você que manda nesse jogo, pode acreditar

Ela não tá procurando quem pague a conta não
Quer é conexão, experiência, atenção
Do jantar pro lounge, do lounge pro hotel
A noite é dela, e o script é de papel

Não julga, não fica se explicando
Profissional, tá sempre evoluindo
Respeito é a chave, charme é o dom
E quem entende isso sai ganhando também, bom!

E quando ela passa, ô, ô
Todo mundo quer saber quem é
Independente, confiante, vê
Ela que escolhe com quem vai ser

Classe A, classe A
Sofisticada, ninguém vai te parar
Classe A, classe A
Você que manda nesse jogo, pode acreditar

Não precisa provar nada pra ninguém
Ela é dona do seu tempo e vai além
Liberdade é luxo que dinheiro não compra
E ela vive isso todo dia, toda hora

Classe A, classe A
Sofisticada, ninguém vai te parar
Classe A, classe A
Você que manda nesse jogo, pode acreditar

Respeita a mina, entendeu?
Classe A! Naldo!
"""


def evaluate_lyrics():
    """Evaluate the lyrics with quality scoring system."""

    print("="*80)
    print(" CLASSE A - AVALIAÇÃO COM SISTEMA DE SCORING ".center(80, "="))
    print("="*80 + "\n")

    # Initialize scorers
    scorer = QualityScorer()
    rhyme_engine = RhymeEngine()
    coherence = SemanticCoherence()

    # Get lines
    lines = [l.strip() for l in CLASSE_A_LYRICS.strip().split('\n') if l.strip()]

    # 1. Effectiveness Score
    print("📊 EFFECTIVENESS ANALYSIS")
    print("-" * 80)

    effectiveness = scorer.score_effectiveness(CLASSE_A_LYRICS)

    print(f"\n  Overall Effectiveness: {effectiveness['overall_score']:.1f}/100", end="")
    stars = "⭐" * int(effectiveness['overall_score'] / 20)
    print(f" {stars}\n")

    print("  Breakdown:")
    for dim, score in effectiveness['dimensions'].items():
        print(f"    • {dim.replace('_', ' ').title():<25} {score:.1f}/100")

    # 2. 4D Scores
    print("\n" + "="*80)
    print("🎯 4D QUALITY SCORES")
    print("-" * 80)

    scores_4d = scorer.score_4d(CLASSE_A_LYRICS, genre='Funk')

    for dimension, score in scores_4d.items():
        score_val = score if isinstance(score, (int, float)) else 0
        print(f"  • {dimension.title():<20} {score_val:.1f}/100")

    # 3. Rhyme Analysis
    print("\n" + "="*80)
    print("🎵 RHYME ANALYSIS")
    print("-" * 80)

    rhyme_stats = rhyme_engine.get_rhyme_statistics(lines)

    print(f"\n  Rhyme Quality: {rhyme_stats['quality_score']:.1f}%")
    print(f"  Total Rhyme Pairs: {rhyme_stats['total_rhymes']}")
    print(f"  Rhyme Density: {rhyme_stats['rhyme_density']:.1f}%")

    if rhyme_stats['quality_distribution']:
        print(f"\n  Quality Distribution:")
        for quality, count in rhyme_stats['quality_distribution'].items():
            print(f"    • {quality.title():<15} {count:>3}")

    # 4. Coherence Analysis
    print("\n" + "="*80)
    print("🧠 SEMANTIC COHERENCE")
    print("-" * 80)

    coherence_score = coherence.score_coherence(CLASSE_A_LYRICS)

    print(f"\n  Overall Coherence: {coherence_score['score']:.1f}/100")
    print(f"  Assessment: {coherence_score['assessment']}")

    if coherence_score.get('strengths'):
        print(f"\n  Strengths:")
        for strength in coherence_score['strengths'][:3]:
            print(f"    ✓ {strength}")

    # 5. Distinctiveness Features
    print("\n" + "="*80)
    print("✨ DISTINCTIVENESS FEATURES")
    print("-" * 80)

    # Count colloquialisms
    colloquialisms = ['ô', 'tá', 'pra', 'pai', 'mina', 'rolê', 'moral', 'hein']
    colloq_count = sum(CLASSE_A_LYRICS.lower().count(c) for c in colloquialisms)

    # Count hook repetition
    hook_count = CLASSE_A_LYRICS.count('Classe A')

    # Count dialogue markers
    question_marks = CLASSE_A_LYRICS.count('?')
    exclamations = CLASSE_A_LYRICS.count('!')

    print(f"\n  Colloquialisms: {colloq_count} occurrences")
    print(f"    Words: {', '.join(colloquialisms)}")

    print(f"\n  Hook Repetition: '{hook_count}x 'Classe A'")
    print(f"    Strategy: Refrão chiclete (memorability)")

    print(f"\n  Dialogue Markers:")
    print(f"    • Questions (?): {question_marks}")
    print(f"    • Exclamations (!): {exclamations}")

    # 6. Final Verdict
    print("\n" + "="*80)
    print(" VERDICT ".center(80, "="))
    print("="*80 + "\n")

    overall = effectiveness['overall_score']

    if overall >= 75:
        verdict = "🏆 PRODUCTION-READY - ALTA QUALIDADE"
        recommendation = "Letra pronta para gravação!"
    elif overall >= 65:
        verdict = "✅ MUITO BOM - Pequenos ajustes opcionais"
        recommendation = "Considere refinar rimas ou adicionar mais variedade."
    elif overall >= 50:
        verdict = "⚠️  BOM - Precisa melhorias"
        recommendation = "Trabalhe na coerência temática e memorabilidade."
    else:
        verdict = "❌ PRECISA REVISÃO - Muitas melhorias necessárias"
        recommendation = "Revisite estrutura, coerência e qualidade das rimas."

    print(f"  {verdict}")
    print(f"\n  Recomendação: {recommendation}")

    print(f"\n  Adequação ao Naldo Benny: {'ALTA ✓' if colloq_count > 8 and hook_count > 10 else 'MÉDIA'}")
    print(f"  Tema Acompanhantes (sofisticado): {'ADEQUADO ✓' if 'luxo' in CLASSE_A_LYRICS.lower() else 'REVISAR'}")

    print("\n" + "="*80 + "\n")

    # Return scores for comparison
    return {
        'effectiveness': effectiveness['overall_score'],
        'coherence': coherence_score['score'],
        'consistency': effectiveness['dimensions']['consistency'],
        'resonance': effectiveness['dimensions']['resonance'],
        'memorability': effectiveness['dimensions']['memorability'],
        'rhyme': rhyme_stats['quality_score'],
        'distinctiveness': min(100, (colloq_count * 3) + (hook_count * 2))
    }


if __name__ == '__main__':
    scores = evaluate_lyrics()

    print("📈 SCORE SUMMARY:")
    print("-" * 80)
    for metric, score in scores.items():
        print(f"  {metric.title():<20} {score:>6.1f}/100")
    print()
