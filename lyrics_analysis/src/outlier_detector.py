"""
Outlier Detection Module - Identifies innovative and statistically unique songs.

This module finds songs that deviate from genre norms in meaningful ways:
- Vocabulary uniqueness (rare word usage)
- Structural innovation (non-standard patterns)
- Thematic surprise (unexpected combinations)
- Genre-bending (cross-pollination)

The goal: identify what makes songs DISTINCTIVE, not just different.
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional
import logging
import json
from pathlib import Path
import math

logger = logging.getLogger(__name__)


class OutlierDetector:
    """Detects statistically unique and innovative songs."""

    def __init__(self, corpus_data: List[Dict]):
        """
        Initialize outlier detector.

        Args:
            corpus_data: List of song dictionaries from processed corpus
        """
        self.corpus = corpus_data
        self.analyzed = False

        # Analysis results
        self.outlier_scores = []  # List of (song, scores) tuples
        self.genre_baselines = {}  # Genre-specific baselines
        self.vocabulary_stats = {}  # Global vocabulary statistics

    def analyze_corpus(self):
        """
        Analyze corpus to identify outliers and innovators.
        Main analysis method - run once to build outlier database.
        """
        logger.info("Analyzing corpus for outliers and innovations...")

        # Step 1: Build genre baselines
        logger.info("  Building genre baselines...")
        self._build_genre_baselines()

        # Step 2: Build vocabulary statistics
        logger.info("  Analyzing vocabulary statistics...")
        self._build_vocabulary_stats()

        # Step 3: Score each song
        logger.info("  Scoring songs for uniqueness...")
        self._score_all_songs()

        self.analyzed = True
        logger.info(f"✓ Analyzed {len(self.corpus)} songs for innovation")

    def _build_genre_baselines(self):
        """Build statistical baselines for each genre."""
        genre_songs = defaultdict(list)

        for song in self.corpus:
            genre = song.get('genre', 'Unknown')
            genre_songs[genre].append(song)

        for genre, songs in genre_songs.items():
            # Calculate baseline statistics
            word_counts = []
            line_counts = []
            repetition_scores = []

            for song in songs:
                lyrics = song.get('lyrics', '')
                words = lyrics.split()
                lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

                word_counts.append(len(words))
                line_counts.append(len(lines))

                # Repetition
                if lines:
                    unique_lines = len(set(l.lower() for l in lines))
                    rep = 1 - (unique_lines / len(lines))
                    repetition_scores.append(rep)

            self.genre_baselines[genre] = {
                'avg_words': sum(word_counts) / len(word_counts) if word_counts else 0,
                'std_words': self._std_dev(word_counts),
                'avg_lines': sum(line_counts) / len(line_counts) if line_counts else 0,
                'std_lines': self._std_dev(line_counts),
                'avg_repetition': sum(repetition_scores) / len(repetition_scores) if repetition_scores else 0,
                'std_repetition': self._std_dev(repetition_scores),
                'song_count': len(songs)
            }

    def _build_vocabulary_stats(self):
        """Build global vocabulary statistics for rarity scoring."""
        # Collect all words and their frequencies
        word_freq = Counter()

        for song in self.corpus:
            lyrics = song.get('lyrics', '').lower()
            words = re.findall(r'\b\w+\b', lyrics)
            word_freq.update(words)

        total_words = sum(word_freq.values())

        self.vocabulary_stats = {
            'word_freq': word_freq,
            'total_words': total_words,
            'unique_words': len(word_freq)
        }

    def _score_all_songs(self):
        """Score each song for innovation/uniqueness."""
        for i, song in enumerate(self.corpus):
            if (i + 1) % 500 == 0:
                logger.info(f"    Scored {i+1}/{len(self.corpus)} songs")

            scores = self._score_song(song)
            self.outlier_scores.append((song, scores))

        # Sort by composite innovation score
        self.outlier_scores.sort(key=lambda x: x[1]['composite_innovation'], reverse=True)

    def _score_song(self, song: Dict) -> Dict:
        """
        Score a single song for innovation across multiple dimensions.

        Args:
            song: Song dictionary

        Returns:
            Dictionary with innovation scores
        """
        lyrics = song.get('lyrics', '')
        genre = song.get('genre', 'Unknown')

        # Get genre baseline
        baseline = self.genre_baselines.get(genre, {})

        # Calculate individual scores
        vocab_score = self._vocabulary_uniqueness_score(lyrics)
        struct_score = self._structural_deviation_score(song, baseline)
        length_score = self._length_deviation_score(song, baseline)
        repetition_score = self._repetition_deviation_score(song, baseline)

        # Composite innovation score (weighted average)
        composite = (
            vocab_score * 0.4 +      # Vocabulary is most important
            struct_score * 0.2 +     # Structure matters
            length_score * 0.2 +     # Length deviation
            repetition_score * 0.2   # Repetition pattern
        )

        return {
            'vocabulary_uniqueness': round(vocab_score, 2),
            'structural_deviation': round(struct_score, 2),
            'length_deviation': round(length_score, 2),
            'repetition_deviation': round(repetition_score, 2),
            'composite_innovation': round(composite, 2)
        }

    def _vocabulary_uniqueness_score(self, lyrics: str) -> float:
        """
        Score based on use of rare/unique words.
        Higher score = uses more rare words.

        Args:
            lyrics: Song lyrics

        Returns:
            Score 0-100
        """
        words = re.findall(r'\b\w+\b', lyrics.lower())
        if not words:
            return 0

        word_freq = self.vocabulary_stats['word_freq']
        total_corpus_words = self.vocabulary_stats['total_words']

        # Calculate average rarity of words used
        rarity_scores = []

        for word in set(words):  # Unique words only
            freq = word_freq.get(word, 0)

            if freq == 0:
                rarity = 100  # Not in corpus at all!
            else:
                # Rarity = inverse log frequency
                # Common word (freq=10000): low rarity
                # Rare word (freq=5): high rarity
                rarity = 100 * (1 / (1 + math.log(freq + 1)))

            rarity_scores.append(rarity)

        avg_rarity = sum(rarity_scores) / len(rarity_scores) if rarity_scores else 0

        return min(avg_rarity, 100)

    def _structural_deviation_score(self, song: Dict, baseline: Dict) -> float:
        """
        Score based on structural deviation from genre norm.

        Args:
            song: Song dictionary
            baseline: Genre baseline statistics

        Returns:
            Score 0-100
        """
        if not baseline:
            return 50  # No baseline, assume average

        lyrics = song.get('lyrics', '')
        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

        actual_lines = len(lines)
        expected_lines = baseline.get('avg_lines', actual_lines)
        std_lines = baseline.get('std_lines', 1)

        if std_lines == 0:
            return 0

        # Z-score: how many standard deviations from mean
        z_score = abs(actual_lines - expected_lines) / std_lines

        # Convert to 0-100 scale
        # z=0 → 0 (perfectly normal)
        # z=2 → 50 (2 std devs)
        # z=4+ → 100 (very unusual)
        score = min(z_score * 25, 100)

        return score

    def _length_deviation_score(self, song: Dict, baseline: Dict) -> float:
        """
        Score based on word count deviation from genre norm.

        Args:
            song: Song dictionary
            baseline: Genre baseline statistics

        Returns:
            Score 0-100
        """
        if not baseline:
            return 50

        lyrics = song.get('lyrics', '')
        actual_words = len(lyrics.split())
        expected_words = baseline.get('avg_words', actual_words)
        std_words = baseline.get('std_words', 1)

        if std_words == 0:
            return 0

        z_score = abs(actual_words - expected_words) / std_words
        score = min(z_score * 25, 100)

        return score

    def _repetition_deviation_score(self, song: Dict, baseline: Dict) -> float:
        """
        Score based on repetition pattern deviation.

        Args:
            song: Song dictionary
            baseline: Genre baseline statistics

        Returns:
            Score 0-100
        """
        if not baseline:
            return 50

        lyrics = song.get('lyrics', '')
        lines = [l.strip().lower() for l in lyrics.split('\n') if l.strip()]

        if not lines:
            return 0

        unique_lines = len(set(lines))
        actual_rep = 1 - (unique_lines / len(lines))

        expected_rep = baseline.get('avg_repetition', actual_rep)
        std_rep = baseline.get('std_repetition', 0.1)

        if std_rep == 0:
            return 0

        z_score = abs(actual_rep - expected_rep) / std_rep
        score = min(z_score * 25, 100)

        return score

    def _std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values:
            return 0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)

    def get_top_outliers(self, n: int = 100, min_composite: float = 30) -> List[Tuple[Dict, Dict]]:
        """
        Get top N most innovative songs.

        Args:
            n: Number of outliers to return
            min_composite: Minimum composite innovation score

        Returns:
            List of (song, scores) tuples
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        # Filter by minimum score and take top N
        filtered = [
            (song, scores)
            for song, scores in self.outlier_scores
            if scores['composite_innovation'] >= min_composite
        ]

        return filtered[:n]

    def get_genre_outliers(self, genre: str, n: int = 20) -> List[Tuple[Dict, Dict]]:
        """
        Get top outliers for a specific genre.

        Args:
            genre: Genre name
            n: Number to return

        Returns:
            List of (song, scores) tuples
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        # Filter by genre
        genre_outliers = [
            (song, scores)
            for song, scores in self.outlier_scores
            if song.get('genre') == genre
        ]

        return genre_outliers[:n]

    def analyze_outlier_patterns(self) -> Dict:
        """
        Analyze what makes outliers distinctive.

        Returns:
            Dictionary with pattern analysis
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        top_100 = self.get_top_outliers(100)

        # Analyze patterns in top outliers
        artists = Counter(song['artist'] for song, _ in top_100)
        genres = Counter(song['genre'] for song, _ in top_100)

        # Average scores
        avg_scores = defaultdict(list)
        for _, scores in top_100:
            for key, value in scores.items():
                avg_scores[key].append(value)

        avg_scores_summary = {
            key: round(sum(values) / len(values), 2)
            for key, values in avg_scores.items()
        }

        return {
            'top_artists': dict(artists.most_common(10)),
            'genre_distribution': dict(genres.most_common()),
            'average_scores': avg_scores_summary,
            'innovation_drivers': self._identify_innovation_drivers(top_100)
        }

    def _identify_innovation_drivers(self, outliers: List[Tuple[Dict, Dict]]) -> Dict:
        """
        Identify what drives innovation in outliers.

        Args:
            outliers: List of (song, scores) tuples

        Returns:
            Dictionary with innovation drivers
        """
        # Count how many times each dimension is the primary driver
        primary_drivers = Counter()

        for _, scores in outliers:
            # Find which dimension has highest score
            dimension_scores = {
                'vocabulary': scores['vocabulary_uniqueness'],
                'structure': scores['structural_deviation'],
                'length': scores['length_deviation'],
                'repetition': scores['repetition_deviation']
            }

            primary = max(dimension_scores.items(), key=lambda x: x[1])[0]
            primary_drivers[primary] += 1

        return {
            'primary_innovation_drivers': dict(primary_drivers),
            'interpretation': {
                'vocabulary': 'Uses rare/unique words',
                'structure': 'Non-standard song structure',
                'length': 'Unusual length (very long or short)',
                'repetition': 'Unexpected repetition pattern'
            }
        }

    def generate_report(self) -> Dict:
        """Generate comprehensive outlier analysis report."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        top_100 = self.get_top_outliers(100)
        patterns = self.analyze_outlier_patterns()

        report = {
            'overview': {
                'total_songs_analyzed': len(self.corpus),
                'top_outliers_count': len(top_100),
                'genres_analyzed': len(self.genre_baselines)
            },
            'top_100_outliers': [
                {
                    'rank': i + 1,
                    'title': song['title'],
                    'artist': song['artist'],
                    'genre': song['genre'],
                    'scores': scores
                }
                for i, (song, scores) in enumerate(top_100)
            ],
            'patterns': patterns,
            'genre_baselines': self.genre_baselines
        }

        return report

    def save_report(self, output_path: Path):
        """Save outlier report to JSON file."""
        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved outlier report to {output_path}")

    def print_summary(self, top_n: int = 30):
        """Print formatted summary of top outliers."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        print("\n" + "="*80)
        print(" INNOVATION DETECTION - TOP OUTLIERS ".center(80, "="))
        print("="*80 + "\n")

        top_outliers = self.get_top_outliers(top_n)

        print(f"🚀 TOP {top_n} MOST INNOVATIVE SONGS")
        print("-" * 80)
        print(f"{'#':>3} {'Score':>5} {'Title':40s} {'Artist':25s} {'Genre':10s}")
        print("-" * 80)

        for i, (song, scores) in enumerate(top_outliers, 1):
            composite = scores['composite_innovation']

            # Innovation level indicator
            if composite >= 70:
                icon = "🔥"
            elif composite >= 60:
                icon = "⚡"
            elif composite >= 50:
                icon = "✨"
            else:
                icon = "💡"

            title = song['title'][:38]
            artist = song['artist'][:23]
            genre = song['genre'][:8]

            print(f"{i:3d} {icon} {composite:4.1f} {title:40s} {artist:25s} {genre:10s}")

        # Show patterns
        patterns = self.analyze_outlier_patterns()

        print(f"\n📊 INNOVATION PATTERNS")
        print("-" * 80)

        print(f"\nTop Innovative Artists:")
        for artist, count in list(patterns['top_artists'].items())[:5]:
            print(f"  • {artist:30s} - {count} songs in top 100")

        print(f"\nGenre Distribution in Top 100:")
        for genre, count in patterns['genre_distribution'].items():
            pct = count / len(top_outliers) * 100
            print(f"  • {genre:15s} - {count:2d} songs ({pct:5.1f}%)")

        print(f"\nAverage Innovation Scores (Top 100):")
        for key, value in patterns['average_scores'].items():
            if key != 'composite_innovation':
                print(f"  • {key:25s}: {value:.1f}/100")

        print(f"\nPrimary Innovation Drivers:")
        for driver, count in patterns['innovation_drivers']['primary_innovation_drivers'].items():
            interpretation = patterns['innovation_drivers']['interpretation'][driver]
            pct = count / len(top_outliers) * 100
            print(f"  • {driver:15s}: {count:2d} songs ({pct:5.1f}%) - {interpretation}")

        print("\n" + "="*80 + "\n")
