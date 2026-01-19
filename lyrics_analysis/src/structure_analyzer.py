"""
Structure Analyzer - Extracts and analyzes song structural patterns.

This module identifies common song templates: verse/chorus patterns,
repetition structures, line length patterns, etc.

Understanding structural conventions helps identify innovative deviations.
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class StructureAnalyzer:
    """Analyzes structural patterns in songs."""

    def __init__(self, corpus_data: List[Dict]):
        """
        Initialize structure analyzer.

        Args:
            corpus_data: List of song dictionaries
        """
        self.corpus = corpus_data
        self.analyzed = False

        # Analysis results
        self.structure_profiles = {}  # {genre: structure_data}
        self.templates = []  # Common structural templates
        self.repetition_patterns = {}  # Repetition analysis

    def analyze_corpus(self):
        """
        Analyze corpus for structural patterns.
        Main analysis method - run once to build structure database.
        """
        logger.info("Analyzing corpus structure...")

        # Group by genre
        genre_songs = defaultdict(list)
        for song in self.corpus:
            genre = song.get('genre', 'Unknown')
            genre_songs[genre].append(song)

        # Analyze each genre
        for genre, songs in genre_songs.items():
            logger.info(f"  Analyzing {genre} structure ({len(songs)} songs)")
            self.structure_profiles[genre] = self._analyze_genre_structure(songs)

        # Extract common templates across corpus
        self._extract_templates()

        self.analyzed = True
        logger.info(f"✓ Analyzed structure for {len(genre_songs)} genres")

    def _analyze_genre_structure(self, songs: List[Dict]) -> Dict:
        """
        Analyze structural characteristics of a genre.

        Args:
            songs: List of songs in genre

        Returns:
            Structure profile dictionary
        """
        profile = {
            'line_patterns': self._analyze_line_patterns(songs),
            'paragraph_patterns': self._analyze_paragraph_patterns(songs),
            'repetition_analysis': self._analyze_repetition(songs),
            'length_distribution': self._analyze_length_distribution(songs),
            'structure_markers': self._analyze_structure_markers(songs)
        }

        return profile

    def _analyze_line_patterns(self, songs: List[Dict]) -> Dict:
        """Analyze line-level patterns."""
        line_lengths = []  # in words
        line_counts = []

        for song in songs:
            lyrics = song.get('lyrics', '')
            lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

            line_counts.append(len(lines))

            for line in lines:
                words = len(line.split())
                line_lengths.append(words)

        # Calculate statistics
        if line_lengths:
            sorted_lengths = sorted(line_lengths)
            n = len(sorted_lengths)

            return {
                'avg_words_per_line': round(sum(line_lengths) / len(line_lengths), 2),
                'median_words_per_line': sorted_lengths[n // 2],
                'min_words_per_line': min(line_lengths),
                'max_words_per_line': max(line_lengths),
                'avg_lines_per_song': round(sum(line_counts) / len(line_counts), 1),
                'line_length_distribution': self._get_distribution(line_lengths)
            }

        return {}

    def _analyze_paragraph_patterns(self, songs: List[Dict]) -> Dict:
        """Analyze paragraph/stanza patterns."""
        paragraph_counts = []
        paragraph_lengths = []  # in lines

        for song in songs:
            lyrics = song.get('lyrics', '')
            paragraphs = [p.strip() for p in lyrics.split('\n\n') if p.strip()]

            paragraph_counts.append(len(paragraphs))

            for para in paragraphs:
                lines = [l for l in para.split('\n') if l.strip()]
                paragraph_lengths.append(len(lines))

        if paragraph_lengths:
            return {
                'avg_paragraphs_per_song': round(sum(paragraph_counts) / len(paragraph_counts), 1),
                'avg_lines_per_paragraph': round(sum(paragraph_lengths) / len(paragraph_lengths), 1),
                'paragraph_count_distribution': self._get_distribution(paragraph_counts)
            }

        return {}

    def _analyze_repetition(self, songs: List[Dict]) -> Dict:
        """
        Analyze repetition patterns (chorus, repeated lines).

        Returns:
            Repetition analysis dictionary
        """
        repetition_scores = []
        chorus_detected = 0

        for song in songs:
            lyrics = song.get('lyrics', '')
            lines = [l.strip().lower() for l in lyrics.split('\n') if l.strip()]

            if not lines:
                continue

            # Count line repetitions
            line_counts = Counter(lines)

            # Find most repeated line
            most_common = line_counts.most_common(1)
            if most_common:
                max_repetition = most_common[0][1]

                # If a line repeats 3+ times, likely a chorus
                if max_repetition >= 3:
                    chorus_detected += 1

            # Calculate repetition ratio
            unique_lines = len(set(lines))
            total_lines = len(lines)
            repetition_ratio = 1 - (unique_lines / total_lines) if total_lines > 0 else 0

            repetition_scores.append(repetition_ratio)

        total_songs = len(songs)

        return {
            'avg_repetition_ratio': round(sum(repetition_scores) / len(repetition_scores), 3) if repetition_scores else 0,
            'songs_with_chorus': chorus_detected,
            'chorus_percentage': round((chorus_detected / total_songs * 100), 1) if total_songs > 0 else 0
        }

    def _analyze_length_distribution(self, songs: List[Dict]) -> Dict:
        """Analyze overall song length distributions."""
        word_counts = []
        char_counts = []

        for song in songs:
            lyrics = song.get('lyrics', '')
            words = lyrics.split()

            word_counts.append(len(words))
            char_counts.append(len(lyrics))

        if word_counts:
            sorted_words = sorted(word_counts)
            n = len(sorted_words)

            return {
                'avg_words': round(sum(word_counts) / n, 1),
                'median_words': sorted_words[n // 2],
                'percentile_25': sorted_words[n // 4],
                'percentile_75': sorted_words[3 * n // 4],
                'min_words': min(word_counts),
                'max_words': max(word_counts),
                'avg_chars': round(sum(char_counts) / len(char_counts), 0)
            }

        return {}

    def _analyze_structure_markers(self, songs: List[Dict]) -> Dict:
        """
        Detect structural markers and explicit structure indicators.

        Returns:
            Structure marker analysis
        """
        markers_found = defaultdict(int)

        # Common structure markers in Brazilian lyrics
        marker_patterns = {
            'refrão': [r'\[?refr[ãa]o\]?', r'\(refr[ãa]o\)'],
            'verso': [r'\[?verso\]?', r'\(verso\)'],
            'intro': [r'\[?intro\]?', r'\(intro\)'],
            'ponte': [r'\[?ponte\]?', r'\(ponte\)', r'\[?bridge\]?'],
            'final': [r'\[?final\]?', r'\(final\)', r'\[?outro\]?'],
            'instrumental': [r'\[?instrumental\]?', r'\(instrumental\)']
        }

        for song in songs:
            lyrics = song.get('lyrics', '').lower()

            for marker_type, patterns in marker_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, lyrics):
                        markers_found[marker_type] += 1
                        break  # Count once per song

        total = len(songs)

        return {
            marker: {
                'count': count,
                'percentage': round((count / total * 100), 1)
            }
            for marker, count in markers_found.items()
        }

    def _get_distribution(self, values: List[int]) -> Dict:
        """
        Get distribution summary for a list of values.

        Args:
            values: List of numeric values

        Returns:
            Distribution summary
        """
        if not values:
            return {}

        counter = Counter(values)
        most_common = counter.most_common(5)

        return {
            'most_common_values': [
                {'value': val, 'count': count}
                for val, count in most_common
            ]
        }

    def _extract_templates(self):
        """
        Extract common structural templates across corpus.
        A template is a common pattern of structure.
        """
        logger.info("  Extracting common structural templates")

        # For each song, create a structural fingerprint
        templates = []

        for song in self.corpus:
            template = self._extract_song_template(song)
            if template:
                templates.append(template)

        # Find most common templates
        template_counts = Counter(tuple(t.items()) for t in templates)

        self.templates = [
            {'template': dict(template), 'count': count}
            for template, count in template_counts.most_common(20)
        ]

    def _extract_song_template(self, song: Dict) -> Optional[Dict]:
        """
        Extract structural template from a single song.

        Args:
            song: Song dictionary

        Returns:
            Template dictionary or None
        """
        lyrics = song.get('lyrics', '')

        if not lyrics:
            return None

        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
        paragraphs = [p.strip() for p in lyrics.split('\n\n') if p.strip()]

        # Create template fingerprint
        template = {
            'line_count_bucket': self._bucket_value(len(lines), 10),  # Bucket by 10s
            'paragraph_count': len(paragraphs),
            'has_repetition': self._has_significant_repetition(lines)
        }

        return template

    def _bucket_value(self, value: int, bucket_size: int) -> str:
        """Bucket a value into ranges."""
        bucket = (value // bucket_size) * bucket_size
        return f"{bucket}-{bucket + bucket_size - 1}"

    def _has_significant_repetition(self, lines: List[str]) -> bool:
        """Check if song has significant line repetition (likely chorus)."""
        if not lines:
            return False

        line_counts = Counter(l.lower().strip() for l in lines)
        most_common = line_counts.most_common(1)

        return most_common[0][1] >= 3 if most_common else False

    def detect_song_structure(self, lyrics: str) -> Dict:
        """
        Detect structure of a specific song.

        Args:
            lyrics: Song lyrics text

        Returns:
            Detected structure dictionary
        """
        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
        paragraphs = [p.strip() for p in lyrics.split('\n\n') if p.strip()]

        # Find repeated sections (potential chorus)
        line_counts = Counter(l.lower().strip() for l in lines)
        repeated_lines = [(line, count) for line, count in line_counts.items() if count >= 2]
        repeated_lines.sort(key=lambda x: x[1], reverse=True)

        structure = {
            'total_lines': len(lines),
            'total_paragraphs': len(paragraphs),
            'repeated_sections': [
                {'line': line, 'repetitions': count}
                for line, count in repeated_lines[:5]
            ],
            'has_chorus': any(count >= 3 for _, count in repeated_lines),
            'repetition_ratio': 1 - (len(set(l.lower() for l in lines)) / len(lines)) if lines else 0
        }

        return structure

    def compare_to_genre_norm(self, lyrics: str, genre: str) -> Dict:
        """
        Compare a song's structure to genre norms.

        Args:
            lyrics: Song lyrics
            genre: Genre to compare against

        Returns:
            Comparison dictionary
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        if genre not in self.structure_profiles:
            raise ValueError(f"Genre '{genre}' not found")

        # Analyze this song
        song_structure = self.detect_song_structure(lyrics)

        # Get genre norms
        genre_profile = self.structure_profiles[genre]

        # Compare
        words = len(lyrics.split())
        genre_avg_words = genre_profile['length_distribution']['avg_words']

        lines = song_structure['total_lines']
        genre_avg_lines = genre_profile['line_patterns']['avg_lines_per_song']

        comparison = {
            'song_words': words,
            'genre_avg_words': genre_avg_words,
            'word_deviation': round(((words - genre_avg_words) / genre_avg_words * 100), 1),
            'song_lines': lines,
            'genre_avg_lines': genre_avg_lines,
            'line_deviation': round(((lines - genre_avg_lines) / genre_avg_lines * 100), 1),
            'has_chorus': song_structure['has_chorus'],
            'genre_chorus_percentage': genre_profile['repetition_analysis']['chorus_percentage'],
            'assessment': self._assess_deviation(words, genre_avg_words, lines, genre_avg_lines)
        }

        return comparison

    def _assess_deviation(self, words: int, avg_words: float, lines: int, avg_lines: float) -> str:
        """Assess if structure deviates from norm."""
        word_deviation = abs((words - avg_words) / avg_words)
        line_deviation = abs((lines - avg_lines) / avg_lines)

        avg_deviation = (word_deviation + line_deviation) / 2

        if avg_deviation < 0.2:
            return "Standard (within 20% of genre norm)"
        elif avg_deviation < 0.5:
            return "Moderate deviation (20-50% from norm)"
        else:
            return "Significant deviation (>50% from norm)"

    def generate_report(self) -> Dict:
        """Generate comprehensive structure analysis report."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        return {
            'overview': {
                'genres_analyzed': len(self.structure_profiles),
                'common_templates_found': len(self.templates)
            },
            'genre_structures': self.structure_profiles,
            'common_templates': self.templates
        }

    def save_report(self, output_path: Path):
        """Save structure report to JSON file."""
        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved structure report to {output_path}")

    def print_summary(self):
        """Print formatted summary of structural patterns."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        print("\n" + "="*80)
        print(" STRUCTURAL PATTERN ANALYSIS ".center(80, "="))
        print("="*80 + "\n")

        for genre, profile in sorted(self.structure_profiles.items()):
            print(f"📐 {genre.upper()}")
            print("-" * 80)

            # Line patterns
            line_p = profile['line_patterns']
            print(f"Lines: {line_p['avg_lines_per_song']:.1f} avg | "
                  f"{line_p['avg_words_per_line']:.1f} words/line | "
                  f"Range: {line_p['min_words_per_line']}-{line_p['max_words_per_line']} words")

            # Paragraph patterns
            para_p = profile['paragraph_patterns']
            print(f"Paragraphs: {para_p['avg_paragraphs_per_song']:.1f} avg | "
                  f"{para_p['avg_lines_per_paragraph']:.1f} lines/paragraph")

            # Length
            length = profile['length_distribution']
            print(f"Length: {length['avg_words']:.0f} words avg | "
                  f"Median: {length['median_words']} | "
                  f"Range: {length['min_words']}-{length['max_words']}")

            # Repetition
            rep = profile['repetition_analysis']
            print(f"Repetition: {rep['avg_repetition_ratio']:.1%} avg ratio | "
                  f"{rep['chorus_percentage']:.1f}% have detected chorus")

            # Structure markers
            markers = profile['structure_markers']
            if markers:
                print(f"Structure Markers:")
                for marker, data in sorted(markers.items(), key=lambda x: x[1]['percentage'], reverse=True):
                    print(f"  • {marker}: {data['percentage']}% of songs")

            print()

        # Common templates
        if self.templates:
            print("📋 MOST COMMON STRUCTURAL TEMPLATES")
            print("-" * 80)
            for i, template_data in enumerate(self.templates[:10], 1):
                template = template_data['template']
                count = template_data['count']
                print(f"{i:2d}. Lines: {template['line_count_bucket']:10s} | "
                      f"Paragraphs: {template['paragraph_count']:2d} | "
                      f"Has chorus: {template['has_repetition']:5} | "
                      f"Count: {count:4,}")
            print()

        print("="*80 + "\n")
