"""
Temporal Analyzer - Tracks how Brazilian lyrics evolved over time.

Infers era from artist/genre and tracks:
- Vocabulary evolution (words that emerged/declined)
- Structural changes (song length trends)
- Theme shifts (what topics rose/fell)
- Innovation diffusion (patterns that spread)

Note: Since we don't have explicit year data, we infer eras based on:
- Artist (Chico Buarque = 1970s-80s, Trap artists = 2020s)
- Genre (MPB = older, Trap = newer)
"""

from collections import Counter, defaultdict
from typing import List, Dict, Set
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class TemporalAnalyzer:
    """Analyzes evolution of lyrics patterns over time."""

    def __init__(self, corpus_data: List[Dict]):
        """
        Initialize temporal analyzer.

        Args:
            corpus_data: List of song dictionaries
        """
        self.corpus = corpus_data

        # Era classification (heuristic-based)
        self.era_markers = {
            'classic_mpb': {  # 1970s-1980s
                'artists': ['Chico Buarque', 'Caetano Veloso', 'Gilberto Gil', 'Djavan'],
                'estimated_period': '1970s-1980s'
            },
            'modern_traditional': {  # 2000s-2010s
                'genres': ['Sertanejo', 'Pagode', 'Arrocha'],
                'estimated_period': '2000s-2010s'
            },
            'contemporary': {  # 2015-2025
                'genres': ['Trap'],
                'artists': ['Orochi', 'Veigh', 'Matuê'],
                'estimated_period': '2015-2025'
            }
        }

        self.era_songs = defaultdict(list)
        self.analyzed = False

    def analyze_corpus(self):
        """Analyze temporal evolution in corpus."""
        logger.info("Analyzing temporal evolution...")

        # Classify songs by era
        self._classify_by_era()

        # Analyze evolution patterns
        self.evolution_patterns = self._analyze_evolution()

        self.analyzed = True
        logger.info(f"✓ Classified {len(self.corpus)} songs into eras")

    def _classify_by_era(self):
        """Classify songs into eras based on artist/genre."""
        for song in self.corpus:
            artist = song.get('artist', '')
            genre = song.get('genre', 'Unknown')

            era = 'unknown'

            # Check classic MPB
            if artist in self.era_markers['classic_mpb']['artists']:
                era = 'classic_mpb'
            # Check contemporary
            elif genre in self.era_markers['contemporary']['genres']:
                era = 'contemporary'
            elif artist in self.era_markers['contemporary'].get('artists', []):
                era = 'contemporary'
            # Check modern traditional
            elif genre in self.era_markers['modern_traditional']['genres']:
                era = 'modern_traditional'
            # Default to modern traditional for MPB not in classic list
            elif genre == 'MPB':
                era = 'modern_traditional'

            self.era_songs[era].append(song)

    def _analyze_evolution(self) -> Dict:
        """Analyze how patterns evolved across eras."""
        evolution = {}

        # 1. Vocabulary evolution
        evolution['vocabulary'] = self._vocabulary_evolution()

        # 2. Structural evolution
        evolution['structure'] = self._structural_evolution()

        # 3. Thematic evolution
        evolution['themes'] = self._thematic_evolution()

        return evolution

    def _vocabulary_evolution(self) -> Dict:
        """Track vocabulary changes across eras."""
        era_vocab = {}

        for era, songs in self.era_songs.items():
            if not songs:
                continue

            # Collect all words for this era
            all_words = []
            for song in songs:
                lyrics = song.get('lyrics', '').lower()
                words = lyrics.split()
                all_words.extend(words)

            word_freq = Counter(all_words)
            total_words = len(all_words)
            unique_words = len(word_freq)

            era_vocab[era] = {
                'total_words': total_words,
                'unique_words': unique_words,
                'richness': unique_words / total_words if total_words > 0 else 0,
                'top_50_words': [word for word, count in word_freq.most_common(50)],
                'word_frequencies': dict(word_freq.most_common(100))
            }

        # Find words that emerged or declined
        if 'classic_mpb' in era_vocab and 'contemporary' in era_vocab:
            classic_words = set(era_vocab['classic_mpb']['top_50_words'])
            contemporary_words = set(era_vocab['contemporary']['top_50_words'])

            emerged = contemporary_words - classic_words
            declined = classic_words - contemporary_words

            era_vocab['evolution'] = {
                'words_that_emerged': list(emerged)[:20],
                'words_that_declined': list(declined)[:20],
                'interpretation': 'Comparing 1970s-80s MPB to 2020s Trap shows vocabulary shift'
            }

        return era_vocab

    def _structural_evolution(self) -> Dict:
        """Track structural changes across eras."""
        era_structure = {}

        for era, songs in self.era_songs.items():
            if not songs:
                continue

            lengths = []
            line_counts = []
            repetitions = []

            for song in songs:
                lyrics = song.get('lyrics', '')
                words = lyrics.split()
                lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

                lengths.append(len(words))
                line_counts.append(len(lines))

                # Repetition
                if lines:
                    unique_lines = len(set(l.lower() for l in lines))
                    rep = 1 - (unique_lines / len(lines))
                    repetitions.append(rep)

            era_structure[era] = {
                'avg_length': round(sum(lengths) / len(lengths), 1) if lengths else 0,
                'avg_lines': round(sum(line_counts) / len(line_counts), 1) if line_counts else 0,
                'avg_repetition': round(sum(repetitions) / len(repetitions), 3) if repetitions else 0,
                'song_count': len(songs)
            }

        return era_structure

    def _thematic_evolution(self) -> Dict:
        """Track thematic shifts across eras."""
        theme_keywords = {
            'romantic_love': ['amor', 'coração', 'paixão', 'beijar'],
            'suffering': ['dor', 'chorar', 'tristeza', 'saudade'],
            'party': ['festa', 'dançar', 'alegria', 'cerveja'],
            'social_political': ['vida', 'mundo', 'povo', 'brasil', 'país'],
            'urban': ['cidade', 'rua', 'favela', 'quebrada'],
            'ostentation': ['dinheiro', 'ouro', 'carro', 'luxo']
        }

        era_themes = {}

        for era, songs in self.era_songs.items():
            if not songs:
                continue

            theme_counts = Counter()

            for song in songs:
                lyrics_lower = song.get('lyrics', '').lower()

                for theme, keywords in theme_keywords.items():
                    if any(keyword in lyrics_lower for keyword in keywords):
                        theme_counts[theme] += 1

            total = len(songs)

            era_themes[era] = {
                theme: {
                    'count': count,
                    'percentage': round((count / total * 100), 1)
                }
                for theme, count in theme_counts.items()
            }

        return era_themes

    def identify_innovation_trends(self) -> Dict:
        """
        Identify which innovations spread vs died.

        Returns:
            Dictionary with trend analysis
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        trends = {}

        # Compare structural trends
        if 'classic_mpb' in self.era_songs and 'contemporary' in self.era_songs:
            classic_struct = self.evolution_patterns['structure']['classic_mpb']
            contemporary_struct = self.evolution_patterns['structure']['contemporary']

            trends['structural_trends'] = {
                'length_change': {
                    'classic': classic_struct['avg_length'],
                    'contemporary': contemporary_struct['avg_length'],
                    'change': round(contemporary_struct['avg_length'] - classic_struct['avg_length'], 1),
                    'interpretation': 'Songs got longer' if contemporary_struct['avg_length'] > classic_struct['avg_length'] else 'Songs got shorter'
                },
                'repetition_change': {
                    'classic': classic_struct['avg_repetition'],
                    'contemporary': contemporary_struct['avg_repetition'],
                    'change': round(contemporary_struct['avg_repetition'] - classic_struct['avg_repetition'], 3),
                    'interpretation': 'More repetitive' if contemporary_struct['avg_repetition'] > classic_struct['avg_repetition'] else 'Less repetitive'
                }
            }

        # Compare thematic trends
        if 'classic_mpb' in self.evolution_patterns['themes'] and 'contemporary' in self.evolution_patterns['themes']:
            classic_themes = self.evolution_patterns['themes']['classic_mpb']
            contemporary_themes = self.evolution_patterns['themes']['contemporary']

            theme_changes = {}
            for theme in classic_themes:
                if theme in contemporary_themes:
                    classic_pct = classic_themes[theme]['percentage']
                    contemporary_pct = contemporary_themes[theme]['percentage']
                    change = contemporary_pct - classic_pct

                    theme_changes[theme] = {
                        'classic': classic_pct,
                        'contemporary': contemporary_pct,
                        'change': round(change, 1),
                        'trend': 'rising' if change > 5 else ('declining' if change < -5 else 'stable')
                    }

            trends['thematic_trends'] = theme_changes

        return trends

    def generate_report(self) -> Dict:
        """Generate temporal evolution report."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        innovation_trends = self.identify_innovation_trends()

        return {
            'overview': {
                'eras_identified': list(self.era_songs.keys()),
                'era_definitions': self.era_markers,
                'song_distribution': {
                    era: len(songs)
                    for era, songs in self.era_songs.items()
                }
            },
            'evolution_patterns': self.evolution_patterns,
            'innovation_trends': innovation_trends,
            'methodology': {
                'note': 'Era classification is heuristic-based (artist/genre)',
                'classic_mpb': 'Estimated 1970s-1980s based on classic artists',
                'modern_traditional': 'Estimated 2000s-2010s based on traditional genres',
                'contemporary': 'Estimated 2015-2025 based on Trap and modern artists'
            }
        }

    def save_report(self, output_path: Path):
        """Save temporal analysis report to JSON file."""
        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved temporal report to {output_path}")

    def print_summary(self):
        """Print formatted summary of temporal evolution."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        print("\n" + "="*80)
        print(" TEMPORAL EVOLUTION ANALYSIS ".center(80, "="))
        print("="*80 + "\n")

        print("📅 ERA DISTRIBUTION")
        print("-" * 80)
        for era, songs in sorted(self.era_songs.items(), key=lambda x: len(x[1]), reverse=True):
            if era == 'unknown':
                continue
            period = self.era_markers.get(era, {}).get('estimated_period', 'Unknown')
            print(f"{era:20s} ({period:15s}): {len(songs):4d} songs")

        print(f"\n📊 STRUCTURAL EVOLUTION")
        print("-" * 80)
        print(f"{'Era':20s} {'Avg Words':>10s} {'Avg Lines':>10s} {'Repetition':>12s}")
        print("-" * 80)

        for era in ['classic_mpb', 'modern_traditional', 'contemporary']:
            if era in self.evolution_patterns['structure']:
                struct = self.evolution_patterns['structure'][era]
                print(f"{era:20s} {struct['avg_length']:10.1f} {struct['avg_lines']:10.1f} {struct['avg_repetition']:11.1%}")

        if 'evolution' in self.evolution_patterns['vocabulary']:
            print(f"\n🔄 VOCABULARY EVOLUTION (Classic MPB → Contemporary Trap)")
            print("-" * 80)

            vocab_evo = self.evolution_patterns['vocabulary']['evolution']

            print(f"\nWords that EMERGED in Contemporary:")
            emerged = vocab_evo.get('words_that_emerged', [])[:15]
            for i, word in enumerate(emerged, 1):
                print(f"  {i:2d}. {word}")

            print(f"\nWords that DECLINED from Classic:")
            declined = vocab_evo.get('words_that_declined', [])[:15]
            for i, word in enumerate(declined, 1):
                print(f"  {i:2d}. {word}")

        print("\n" + "="*80 + "\n")
