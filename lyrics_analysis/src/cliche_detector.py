"""
Cliché Detection Module - Identifies overused phrases in Brazilian lyrics.

This module finds patterns that appear frequently in the corpus,
helping identify what to AVOID when generating distinctive lyrics.

Key insight: Clichés became clichés because they worked initially,
but overuse makes them tired. Innovation = knowing clichés + strategic deviation.
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set, Optional
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ClicheDetector:
    """Detects and analyzes overused phrases (clichés) in lyrics corpus."""

    def __init__(self, corpus_data: List[Dict], min_ngram: int = 2, max_ngram: int = 5):
        """
        Initialize cliché detector.

        Args:
            corpus_data: List of song dictionaries from processed corpus
            min_ngram: Minimum N-gram size (default: 2 words)
            max_ngram: Maximum N-gram size (default: 5 words)
        """
        self.corpus = corpus_data
        self.min_ngram = min_ngram
        self.max_ngram = max_ngram

        # Will store N-gram frequencies
        self.ngram_counts = defaultdict(Counter)  # {n: Counter({ngram: count})}
        self.genre_ngram_counts = defaultdict(lambda: defaultdict(Counter))  # {genre: {n: Counter}}

        # Analysis results
        self.cliches = {}  # Overall clichés
        self.genre_cliches = {}  # Genre-specific clichés
        self.analyzed = False

    def analyze_corpus(self):
        """
        Analyze entire corpus to identify clichés.
        This is the main analysis method - run once to build the cliché database.
        """
        logger.info("Analyzing corpus for clichés...")

        total_songs = len(self.corpus)

        for i, song in enumerate(self.corpus):
            if (i + 1) % 500 == 0:
                logger.info(f"  Processing song {i+1}/{total_songs}")

            lyrics = song.get('lyrics', '')
            genre = song.get('genre', 'Unknown')

            # Extract N-grams
            for n in range(self.min_ngram, self.max_ngram + 1):
                ngrams = self._extract_ngrams(lyrics, n)

                # Update overall counts
                self.ngram_counts[n].update(ngrams)

                # Update genre-specific counts
                self.genre_ngram_counts[genre][n].update(ngrams)

        self.analyzed = True
        logger.info(f"✓ Analyzed {total_songs} songs")
        logger.info(f"  Found {sum(len(c) for c in self.ngram_counts.values()):,} unique N-grams")

    def _extract_ngrams(self, text: str, n: int) -> List[str]:
        """
        Extract N-grams from text.

        Args:
            text: Lyrics text
            n: N-gram size

        Returns:
            List of N-grams as strings
        """
        # Clean and tokenize
        text = text.lower()

        # Remove punctuation but keep words
        text = re.sub(r'[^\w\s]', ' ', text)

        # Split into words
        words = text.split()

        # Generate N-grams
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)

        return ngrams

    def get_top_cliches(self, n: int = 2, top_k: int = 100, min_occurrences: int = 10) -> List[Tuple[str, int, float]]:
        """
        Get top clichés (most overused N-grams).

        Args:
            n: N-gram size to analyze
            top_k: Number of top clichés to return
            min_occurrences: Minimum times phrase must appear

        Returns:
            List of (ngram, count, percentage_of_songs) tuples
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        total_songs = len(self.corpus)
        cliches = []

        for ngram, count in self.ngram_counts[n].most_common():
            if count < min_occurrences:
                break

            # Calculate percentage of songs containing this phrase
            percentage = (count / total_songs) * 100

            cliches.append((ngram, count, percentage))

            if len(cliches) >= top_k:
                break

        return cliches

    def get_genre_cliches(self, genre: str, n: int = 2, top_k: int = 50, min_occurrences: int = 5) -> List[Tuple[str, int, float]]:
        """
        Get clichés specific to a genre.

        Args:
            genre: Genre name
            n: N-gram size
            top_k: Number to return
            min_occurrences: Minimum occurrences

        Returns:
            List of (ngram, count, percentage) tuples
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        genre_songs = [s for s in self.corpus if s.get('genre') == genre]
        total_genre_songs = len(genre_songs)

        if total_genre_songs == 0:
            return []

        cliches = []

        for ngram, count in self.genre_ngram_counts[genre][n].most_common():
            if count < min_occurrences:
                break

            percentage = (count / total_genre_songs) * 100
            cliches.append((ngram, count, percentage))

            if len(cliches) >= top_k:
                break

        return cliches

    def check_text_for_cliches(self, text: str, threshold_percentile: float = 90) -> List[Dict]:
        """
        Check if text contains clichés.

        Args:
            text: Text to check
            threshold_percentile: Only flag phrases in top X percentile

        Returns:
            List of detected cliché dictionaries
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        detected = []

        for n in range(self.min_ngram, self.max_ngram + 1):
            ngrams = self._extract_ngrams(text, n)

            # Calculate threshold
            counts = list(self.ngram_counts[n].values())
            if not counts:
                continue

            counts.sort()
            threshold_idx = int(len(counts) * (threshold_percentile / 100))
            threshold = counts[threshold_idx] if threshold_idx < len(counts) else counts[-1]

            for ngram in ngrams:
                count = self.ngram_counts[n].get(ngram, 0)

                if count >= threshold:
                    total_songs = len(self.corpus)
                    percentage = (count / total_songs) * 100

                    # Calculate percentile rank
                    rank = sum(1 for c in counts if c > count)
                    percentile = 100 - (rank / len(counts) * 100)

                    detected.append({
                        'phrase': ngram,
                        'count': count,
                        'percentage': percentage,
                        'percentile': percentile,
                        'severity': self._classify_severity(percentile)
                    })

        # Remove duplicates (keep longest match)
        detected = self._deduplicate_cliches(detected)

        # Sort by severity
        detected.sort(key=lambda x: x['percentile'], reverse=True)

        return detected

    def _classify_severity(self, percentile: float) -> str:
        """Classify cliché severity based on percentile."""
        if percentile >= 99:
            return 'EXTREME'
        elif percentile >= 95:
            return 'HIGH'
        elif percentile >= 90:
            return 'MODERATE'
        else:
            return 'LOW'

    def _deduplicate_cliches(self, cliches: List[Dict]) -> List[Dict]:
        """Remove overlapping clichés, keeping the longest ones."""
        if not cliches:
            return []

        # Sort by phrase length (longest first)
        sorted_cliches = sorted(cliches, key=lambda x: len(x['phrase']), reverse=True)

        result = []
        used_words = set()

        for cliche in sorted_cliches:
            words = set(cliche['phrase'].split())

            # Check if this phrase overlaps significantly with already used phrases
            overlap = len(words & used_words) / len(words) if words else 0

            if overlap < 0.5:  # Less than 50% overlap
                result.append(cliche)
                used_words.update(words)

        return result

    def get_alternative_phrases(self, cliche_phrase: str, genre: Optional[str] = None, count: int = 10) -> List[Tuple[str, int]]:
        """
        Suggest alternative phrases that are less common.

        Args:
            cliche_phrase: The cliché to replace
            genre: Optional genre to find alternatives from
            count: Number of alternatives to return

        Returns:
            List of (alternative_phrase, usage_count) tuples
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        # Determine N-gram size from cliché
        n = len(cliche_phrase.split())

        # Get all N-grams of same size
        if genre:
            all_ngrams = self.genre_ngram_counts.get(genre, {}).get(n, Counter())
        else:
            all_ngrams = self.ngram_counts.get(n, Counter())

        # Extract semantic keywords from cliché (nouns, meaningful words)
        cliche_words = set(cliche_phrase.lower().split())

        # Find N-grams that:
        # 1. Share some semantic similarity (at least one word in common)
        # 2. Are LESS common (innovation!)
        # 3. Have minimum quality threshold (appear at least 2-3 times)

        cliche_count = all_ngrams.get(cliche_phrase.lower(), 0)
        alternatives = []

        for ngram, ngram_count in all_ngrams.items():
            # Must be less common than cliché
            if ngram_count >= cliche_count * 0.5:
                continue

            # Must have some quality threshold
            if ngram_count < 2:
                continue

            # Check for semantic overlap
            ngram_words = set(ngram.split())
            common_words = cliche_words & ngram_words

            # Has at least one word in common (semantic similarity)
            if len(common_words) >= 1 and ngram != cliche_phrase.lower():
                alternatives.append((ngram, ngram_count))

        # Sort by rarity (less common = better alternative)
        alternatives.sort(key=lambda x: x[1])

        return alternatives[:count]

    def generate_report(self) -> Dict:
        """
        Generate comprehensive cliché report.

        Returns:
            Dictionary with analysis results
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        report = {
            'overview': {
                'total_songs': len(self.corpus),
                'ngram_sizes_analyzed': list(range(self.min_ngram, self.max_ngram + 1)),
                'unique_ngrams': {
                    n: len(self.ngram_counts[n])
                    for n in range(self.min_ngram, self.max_ngram + 1)
                }
            },
            'top_cliches_by_size': {},
            'genre_cliches': {}
        }

        # Top clichés by N-gram size
        for n in range(self.min_ngram, self.max_ngram + 1):
            top = self.get_top_cliches(n=n, top_k=50)
            report['top_cliches_by_size'][f'{n}-grams'] = [
                {
                    'phrase': phrase,
                    'count': count,
                    'percentage': round(pct, 2)
                }
                for phrase, count, pct in top
            ]

        # Genre-specific clichés
        genres = set(s.get('genre', 'Unknown') for s in self.corpus)
        for genre in genres:
            genre_top = {}
            for n in range(self.min_ngram, self.max_ngram + 1):
                top = self.get_genre_cliches(genre=genre, n=n, top_k=30)
                if top:
                    genre_top[f'{n}-grams'] = [
                        {
                            'phrase': phrase,
                            'count': count,
                            'percentage': round(pct, 2)
                        }
                        for phrase, count, pct in top[:20]
                    ]

            if genre_top:
                report['genre_cliches'][genre] = genre_top

        return report

    def save_report(self, output_path: Path):
        """Save cliché report to JSON file."""
        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved cliché report to {output_path}")

    def print_summary(self, top_n: int = 20):
        """Print a formatted summary of top clichés."""
        print("\n" + "="*80)
        print(" CLICHÉ ANALYSIS - TOP OVERUSED PHRASES ".center(80, "="))
        print("="*80 + "\n")

        for n in range(self.min_ngram, self.max_ngram + 1):
            print(f"📝 TOP {top_n} MOST OVERUSED {n}-WORD PHRASES")
            print("-" * 80)

            top_cliches = self.get_top_cliches(n=n, top_k=top_n)

            for i, (phrase, count, pct) in enumerate(top_cliches, 1):
                severity = self._classify_severity(pct * 10)  # Approximate percentile
                severity_icon = {
                    'EXTREME': '🔥',
                    'HIGH': '⚠️ ',
                    'MODERATE': '⚡',
                    'LOW': '💡'
                }.get(severity, '  ')

                print(f"{i:3d}. {severity_icon} {phrase:40s} - {count:5,} uses ({pct:5.2f}% of songs)")

            print()

        # Genre comparison
        print(f"\n🎵 GENRE-SPECIFIC CLICHÉS (2-word phrases)")
        print("-" * 80)

        genres = set(s.get('genre', 'Unknown') for s in self.corpus)
        for genre in sorted(genres):
            top_5 = self.get_genre_cliches(genre=genre, n=2, top_k=5)
            if top_5:
                print(f"\n{genre}:")
                for phrase, count, pct in top_5:
                    print(f"  • {phrase:30s} - {count:4,} uses ({pct:5.2f}%)")

        print("\n" + "="*80 + "\n")
