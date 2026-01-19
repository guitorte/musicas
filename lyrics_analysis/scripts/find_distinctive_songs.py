#!/usr/bin/env python3
"""
Find Distinctive Songs - Identify most distinctive songs in corpus.

Analyzes corpus for distinctiveness features:
- Slant rhymes (imperfect rhymes)
- Authentic colloquialisms/gírias
- Dialogue markers
- Unique vocabulary (TF-IDF)
- Narrative complexity (irony, twists)
"""

import sys
import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from rhyme_engine import RhymeEngine


class DistinctivenessDetector:
    """Detects distinctive features in lyrics."""

    def __init__(self):
        self.rhyme_engine = RhymeEngine()

        # Colloquial markers (Brazilian Portuguese)
        self.colloquialisms = {
            # Contrações informais
            'cê', 'tá', 'pra', 'tô', 'vô', 'pô', 'né', 'ó',
            # Gírias gerais
            'hein', 'heim', 'cara', 'mano', 'véi', 'velho', 'bixo',
            # Diminutivos afetivos
            'casalzinho', 'amorzinho', 'benzinho', 'mozão',
            # Interjeições coloquiais
            'ô', 'eita', 'oxe', 'uai', 'sô', 'tchê',
            # Expressões populares
            'sacanagem', 'cachaça', 'farra', 'galera', 'rapaziada'
        }

        # Dialogue markers
        self.dialogue_markers = [
            r'\?',  # Questions
            r'!',   # Exclamations
            r'hein\b',
            r'né\b',
            r'ó\b',
            r'olha\b',
            r'escuta\b',
            r'você\b.*disse',
            r'eu disse',
            r'falei\b',
            r'fala\b',
        ]

        # Irony/sarcasm markers
        self.irony_markers = [
            r'bonito',
            r'lindo',
            r'maravilha',
            r'que beleza',
            r'parabéns',
            r'brincadeira',
            r'sério',
            r'claro',
        ]

    def detect_slant_rhymes(self, lines: List[str]) -> Dict:
        """Detect slant/imperfect rhymes."""
        if not lines:
            return {'count': 0, 'ratio': 0.0, 'examples': []}

        last_words = []
        for line in lines:
            words = line.strip().split()
            if words:
                # Clean last word
                last_word = re.sub(r'[^\w]', '', words[-1].lower())
                if last_word:
                    last_words.append(last_word)

        perfect_rhymes = 0
        slant_rhymes = 0
        examples = []

        # Check adjacent lines (common rhyme pattern)
        for i in range(len(last_words) - 1):
            w1, w2 = last_words[i], last_words[i + 1]

            if w1 == w2:
                continue  # Skip identical words

            if self.rhyme_engine.words_rhyme(w1, w2, strict=True):
                quality = self.rhyme_engine.rhyme_quality(w1, w2)

                if quality == 'perfect':
                    perfect_rhymes += 1
                else:
                    slant_rhymes += 1
                    if len(examples) < 5:
                        examples.append((w1, w2, quality))

        total_rhymes = perfect_rhymes + slant_rhymes
        slant_ratio = slant_rhymes / total_rhymes if total_rhymes > 0 else 0.0

        return {
            'count': slant_rhymes,
            'ratio': slant_ratio,
            'examples': examples
        }

    def detect_colloquialisms(self, lyrics: str) -> Dict:
        """Detect colloquial/informal language."""
        lyrics_lower = lyrics.lower()

        found = []
        for word in self.colloquialisms:
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, lyrics_lower)
            if matches:
                found.append((word, len(matches)))

        return {
            'count': sum(c for _, c in found),
            'unique': len(found),
            'examples': found[:10]
        }

    def detect_dialogue(self, lyrics: str) -> Dict:
        """Detect dialogue markers."""
        dialogue_score = 0
        examples = []

        for pattern in self.dialogue_markers:
            matches = re.findall(pattern, lyrics, re.IGNORECASE)
            dialogue_score += len(matches)

            if matches and len(examples) < 3:
                # Find line with this pattern
                for line in lyrics.split('\n'):
                    if re.search(pattern, line, re.IGNORECASE):
                        examples.append(line.strip()[:60])
                        break

        return {
            'score': dialogue_score,
            'examples': examples
        }

    def detect_irony(self, lyrics: str) -> Dict:
        """Detect potential irony/sarcasm."""
        irony_score = 0
        examples = []

        for pattern in self.irony_markers:
            matches = re.findall(pattern, lyrics, re.IGNORECASE)
            if matches:
                irony_score += len(matches)

                # Context matters - check for negation or contrast nearby
                for line in lyrics.split('\n'):
                    if re.search(pattern, line, re.IGNORECASE):
                        # Check for contrast words
                        if re.search(r'\b(mas|porém|entretanto|contudo|só que)\b', line, re.IGNORECASE):
                            irony_score += 2
                            if len(examples) < 3:
                                examples.append(line.strip()[:60])

        return {
            'score': irony_score,
            'examples': examples
        }

    def compute_vocabulary_uniqueness(self, lyrics: str, corpus_words: Counter) -> float:
        """Compute vocabulary uniqueness using simple frequency analysis."""
        words = re.findall(r'\b\w+\b', lyrics.lower())

        if not words:
            return 0.0

        # Score based on word rarity in corpus
        uniqueness_scores = []
        total_corpus_words = sum(corpus_words.values())

        for word in set(words):
            freq = corpus_words.get(word, 0)

            # Lower frequency = higher uniqueness
            if freq == 0:
                score = 100  # Very unique (not in corpus)
            else:
                # Normalize: words appearing in <1% of corpus are distinctive
                percentage = (freq / total_corpus_words) * 100
                score = max(0, 100 - (percentage * 10))

            uniqueness_scores.append(score)

        return sum(uniqueness_scores) / len(uniqueness_scores) if uniqueness_scores else 0.0

    def score_distinctiveness(
        self,
        lyrics: str,
        lines: List[str],
        corpus_words: Counter
    ) -> Dict:
        """Compute overall distinctiveness score."""

        # Detect features
        slant = self.detect_slant_rhymes(lines)
        colloquial = self.detect_colloquialisms(lyrics)
        dialogue = self.detect_dialogue(lyrics)
        irony = self.detect_irony(lyrics)
        vocab_unique = self.compute_vocabulary_uniqueness(lyrics, corpus_words)

        # Compute weighted score
        scores = {
            'slant_rhymes': min(100, slant['ratio'] * 200),  # 20% weight
            'colloquialisms': min(100, colloquial['count'] * 5),  # 25% weight
            'dialogue': min(100, dialogue['score'] * 10),  # 25% weight
            'irony': min(100, irony['score'] * 10),  # 15% weight
            'vocabulary_uniqueness': vocab_unique  # 15% weight
        }

        overall = (
            scores['slant_rhymes'] * 0.20 +
            scores['colloquialisms'] * 0.25 +
            scores['dialogue'] * 0.25 +
            scores['irony'] * 0.15 +
            scores['vocabulary_uniqueness'] * 0.15
        )

        return {
            'overall': overall,
            'breakdown': scores,
            'features': {
                'slant_rhymes': slant,
                'colloquialisms': colloquial,
                'dialogue': dialogue,
                'irony': irony
            }
        }


def build_corpus_vocabulary(songs: List[Dict]) -> Counter:
    """Build corpus-wide word frequency counter."""
    corpus_words = Counter()

    for song in songs:
        lyrics = song.get('lyrics', '')
        words = re.findall(r'\b\w+\b', lyrics.lower())
        corpus_words.update(words)

    return corpus_words


def analyze_corpus(corpus_path: Path, top_n: int = 20) -> List[Dict]:
    """Analyze corpus and find most distinctive songs."""

    print(f"Loading corpus from {corpus_path}...")
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    songs = corpus['songs']
    print(f"✓ Loaded {len(songs)} songs\n")

    print("Building corpus vocabulary...")
    corpus_words = build_corpus_vocabulary(songs)
    print(f"✓ Found {len(corpus_words)} unique words\n")

    print("Analyzing distinctiveness...")
    detector = DistinctivenessDetector()

    results = []

    for i, song in enumerate(songs):
        if (i + 1) % 500 == 0:
            print(f"  Processed {i + 1}/{len(songs)} songs...")

        lyrics = song.get('lyrics', '')
        if not lyrics:
            continue

        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

        score_result = detector.score_distinctiveness(lyrics, lines, corpus_words)

        results.append({
            'title': song['title'],
            'artist': song['artist'],
            'genre': song.get('genre', 'Unknown'),
            'distinctiveness': score_result['overall'],
            'breakdown': score_result['breakdown'],
            'features': score_result['features']
        })

    print(f"\n✓ Analyzed {len(results)} songs\n")

    # Sort by distinctiveness
    results.sort(key=lambda x: x['distinctiveness'], reverse=True)

    return results[:top_n]


def print_report(distinctive_songs: List[Dict]):
    """Print distinctiveness report."""

    print("=" * 80)
    print(" TOP 20 MOST DISTINCTIVE SONGS IN CORPUS ".center(80, "="))
    print("=" * 80 + "\n")

    for i, song in enumerate(distinctive_songs, 1):
        print(f"{i}. {song['title']} - {song['artist']}")
        print(f"   Genre: {song['genre']}")
        print(f"   Distinctiveness: {song['distinctiveness']:.1f}/100\n")

        print(f"   Breakdown:")
        for feature, score in song['breakdown'].items():
            print(f"     • {feature.replace('_', ' ').title()}: {score:.1f}/100")

        print(f"\n   Distinctive Features:")

        # Slant rhymes
        slant = song['features']['slant_rhymes']
        if slant['count'] > 0:
            print(f"     • Slant rhymes: {slant['count']} ({slant['ratio']*100:.0f}% of rhymes)")
            if slant['examples']:
                examples = ', '.join([f"'{w1}'↔'{w2}'" for w1, w2, _ in slant['examples'][:3]])
                print(f"       Examples: {examples}")

        # Colloquialisms
        colloq = song['features']['colloquialisms']
        if colloq['count'] > 0:
            print(f"     • Colloquialisms: {colloq['count']} occurrences ({colloq['unique']} unique)")
            if colloq['examples']:
                examples = ', '.join([f"'{w}' ({c}x)" for w, c in colloq['examples'][:5]])
                print(f"       Examples: {examples}")

        # Dialogue
        dialogue = song['features']['dialogue']
        if dialogue['score'] > 0:
            print(f"     • Dialogue markers: {dialogue['score']}")
            if dialogue['examples']:
                print(f"       Examples:")
                for ex in dialogue['examples'][:2]:
                    print(f"         - \"{ex}...\"")

        # Irony
        irony = song['features']['irony']
        if irony['score'] > 0:
            print(f"     • Irony/sarcasm markers: {irony['score']}")
            if irony['examples']:
                print(f"       Examples:")
                for ex in irony['examples'][:2]:
                    print(f"         - \"{ex}...\"")

        print("\n" + "-" * 80 + "\n")


def save_results(distinctive_songs: List[Dict], output_path: Path):
    """Save results to JSON."""

    output = {
        'description': 'Top 20 most distinctive songs in corpus',
        'methodology': {
            'slant_rhymes': 'Detects imperfect rhymes (20% weight)',
            'colloquialisms': 'Counts Brazilian colloquial expressions (25% weight)',
            'dialogue': 'Identifies direct dialogue markers (25% weight)',
            'irony': 'Detects potential irony/sarcasm (15% weight)',
            'vocabulary_uniqueness': 'Measures word rarity in corpus (15% weight)'
        },
        'count': len(distinctive_songs),
        'songs': distinctive_songs
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Results saved to: {output_path}")


if __name__ == '__main__':
    # Paths
    project_root = Path(__file__).parent.parent.parent
    corpus_path = project_root / 'lyrics_analysis' / 'data' / 'processed' / 'lyrics_corpus.json'
    output_path = project_root / 'lyrics_analysis' / 'analysis' / 'innovations' / 'DISTINCTIVE_SONGS.json'

    # Analyze
    distinctive_songs = analyze_corpus(corpus_path, top_n=20)

    # Print report
    print_report(distinctive_songs)

    # Save results
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_results(distinctive_songs, output_path)
