#!/usr/bin/env python3
"""
Test: Claude-generated lyrics evaluated by our V2 system.

This demonstrates the correct architecture:
LLM generates → V2 scores/validates → Select best
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'lyrics_analysis' / 'src'))

from quality_scorer import QualityScorer
from rhyme_engine import RhymeEngine
from semantic_coherence import SemanticCoherence

# Claude-generated lyrics
claude_lyrics = {
    'mpb': """Quando você não está aqui
O tempo para de correr
Fico contando as horas
Esperando você voltar

Seus olhos têm o brilho
Das estrelas no céu do mar
E quando você sorri
Eu esqueço de respirar

Amor, me diz que é pra sempre
Que esse sonho não vai acabar
Amor, fica mais um momento
Deixa o mundo esperar""",

    'sertanejo': """De novo bebendo sozinha
Olhando seu nome no celular
A saudade machuca demais
Mas eu não vou te ligar

Todo mundo me avisou
Que você ia me fazer chorar
Mas eu teimosa, apaixonada
Não quis escutar

E agora tô aqui
Pagando o preço da ilusão
Você curtindo a vida
E eu sofrendo de paixão""",

    'trap': """Essa mina me chama de love
Mas eu tô no corre, não posso parar
Bolso cheio, corrente pesada
Inveja dos manos que tá pra brotar

Vim da quebrada, hoje tô voando
Dubai na DM, champagne estourando
Os falsos somando, os reais tão do lado
Sucesso chegou, nós tá preparado

Skrr skrr na Mercedes preta
Hater fala mal mas a vida éreta"""
}

def evaluate_lyrics(lyrics: str, genre: str, theme: str):
    """Evaluate Claude-generated lyrics with our V2 system."""
    print("\n" + "="*70)
    print(f" EVALUATING {genre.upper()} LYRICS ".center(70, "="))
    print("="*70 + "\n")

    print(lyrics)
    print("\n" + "-"*70 + "\n")

    # Initialize scorers
    scorer = QualityScorer()
    rhyme_engine = RhymeEngine()
    coherence = SemanticCoherence()

    # Score effectiveness
    effectiveness = scorer.score_effectiveness(lyrics)

    # Score 4D
    scores_4d = scorer.score_4d(lyrics, genre=genre)

    # Analyze rhymes
    lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
    rhyme_stats = rhyme_engine.get_rhyme_statistics(lines)

    # Measure coherence
    coherence_score = coherence.measure_coherence(lines, theme)

    # Print results
    print("📊 EFFECTIVENESS SCORES:")
    print(f"  Overall:      {effectiveness['overall_score']:.1f}/100")
    print(f"  Coherence:    {effectiveness['dimensions']['coherence']:.1f}/100")
    print(f"  Consistency:  {effectiveness['dimensions']['consistency']:.1f}/100")
    print(f"  Resonance:    {effectiveness['dimensions']['resonance']:.1f}/100")
    print(f"  Memorability: {effectiveness['dimensions']['memorability']:.1f}/100")

    print(f"\n🎯 4D SCORES:")
    print(f"  Innovation:    {scores_4d['innovation']:.1f}/100")
    print(f"  Authenticity:  {scores_4d['authenticity']:.1f}/100")
    print(f"  Risk:          {scores_4d['risk']:.1f}/100")
    print(f"  Effectiveness: {scores_4d['effectiveness']:.1f}/100")
    print(f"  Quality:       {scores_4d['quality']:.1f}/100")

    print(f"\n🎼 RHYME ANALYSIS:")
    print(f"  Rhyme percentage: {rhyme_stats['rhyme_percentage']:.1f}%")
    print(f"  Rhyme pairs: {rhyme_stats['rhyme_pairs']}/{rhyme_stats['total_pairs']}")

    print(f"\n🎨 SEMANTIC COHERENCE:")
    print(f"  Thematic consistency: {coherence_score:.1f}%")

    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" CLAUDE (LLM) vs V2 GENERATOR COMPARISON ".center(70, "="))
    print("="*70)
    print("\nClaude generates lyrics → V2 system evaluates them")
    print("This shows the correct architecture: LLM + Quality Scorer\n")

    # Evaluate each genre
    evaluate_lyrics(claude_lyrics['mpb'], 'MPB', 'amor_romantico')
    evaluate_lyrics(claude_lyrics['sertanejo'], 'Sertanejo', 'sofrimento')
    evaluate_lyrics(claude_lyrics['trap'], 'Trap', 'ostentacao')

    print("\n" + "="*70)
    print(" CONCLUSION ".center(70, "="))
    print("="*70)
    print("""
Claude (LLM) generates REAL lyrics with:
- Semantic meaning ✓
- Narrative coherence ✓
- Cultural context ✓
- Natural flow ✓

V2 system provides:
- Quality scoring ✓
- Rhyme analysis ✓
- Coherence measurement ✓
- Effectiveness rating ✓

CORRECT ARCHITECTURE: LLM generates → V2 validates/scores → Pick best
    """)
