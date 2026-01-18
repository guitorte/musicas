"""
Pattern Detection Module - Identifies genre-specific formulas and conventions.

This module maps what makes each genre distinctive: vocabulary, themes,
structures that define MPB vs Sertanejo vs Trap, etc.

Understanding conventions is the foundation for strategic innovation.
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Set, Tuple
import logging
import json
from pathlib import Path
import math

logger = logging.getLogger(__name__)


class PatternDetector:
    """Detects genre-specific patterns and formulas in lyrics."""

    def __init__(self, corpus_data: List[Dict]):
        """
        Initialize pattern detector.

        Args:
            corpus_data: List of song dictionaries from processed corpus
        """
        self.corpus = corpus_data
        self.analyzed = False

        # Analysis results
        self.genre_profiles = {}  # {genre: profile_dict}
        self.vocabulary_maps = {}  # {genre: word_frequency}
        self.theme_signatures = {}  # {genre: theme_distribution}
        self.structural_patterns = {}  # {genre: structure_stats}

    def analyze_corpus(self):
        """
        Analyze corpus to extract genre-specific patterns.
        Main analysis method - run once to build pattern database.
        """
        logger.info("Analyzing corpus for genre patterns...")

        # Group songs by genre
        genre_songs = defaultdict(list)
        for song in self.corpus:
            genre = song.get('genre', 'Unknown')
            genre_songs[genre].append(song)

        # Analyze each genre
        for genre, songs in genre_songs.items():
            logger.info(f"  Analyzing {genre} ({len(songs)} songs)")
            self.genre_profiles[genre] = self._analyze_genre(songs, genre)

        self.analyzed = True
        logger.info(f"✓ Analyzed {len(genre_songs)} genres")

    def _analyze_genre(self, songs: List[Dict], genre: str) -> Dict:
        """
        Deep analysis of a single genre.

        Args:
            songs: List of songs in this genre
            genre: Genre name

        Returns:
            Genre profile dictionary
        """
        # Collect all lyrics for this genre
        all_lyrics = ' '.join(s.get('lyrics', '') for s in songs)
        all_words = self._tokenize(all_lyrics)

        profile = {
            'song_count': len(songs),
            'vocabulary': self._analyze_vocabulary(all_words, songs),
            'themes': self._analyze_themes(songs),
            'structure': self._analyze_structure(songs),
            'distinctive_features': self._find_distinctive_features(songs, genre),
            'common_patterns': self._find_common_patterns(songs)
        }

        return profile

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.split()

    def _analyze_vocabulary(self, words: List[str], songs: List[Dict]) -> Dict:
        """
        Analyze vocabulary characteristics.

        Args:
            words: All words in genre
            songs: Song list for additional stats

        Returns:
            Vocabulary analysis dict
        """
        word_freq = Counter(words)
        total_words = len(words)
        unique_words = len(word_freq)

        # Get top words
        top_words = word_freq.most_common(100)

        # Calculate vocabulary richness (Type-Token Ratio)
        ttr = unique_words / total_words if total_words > 0 else 0

        # Word length distribution
        word_lengths = [len(w) for w in words]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'vocabulary_richness': round(ttr, 4),
            'avg_word_length': round(avg_word_length, 2),
            'top_100_words': [
                {'word': word, 'count': count, 'frequency': round(count/total_words, 4)}
                for word, count in top_words
            ]
        }

    def _analyze_themes(self, songs: List[Dict]) -> Dict:
        """
        Analyze thematic content using keyword matching.

        Args:
            songs: List of songs

        Returns:
            Theme distribution dictionary
        """
        # Expanded theme keywords for Brazilian music
        theme_keywords = {
            'amor_romantico': ['amor', 'amar', 'te amo', 'paixão', 'coração', 'beijar', 'abraço', 'casal', 'namoro'],
            'sofrimento': ['solidão', 'sofrer', 'sofrendo', 'dor', 'doer', 'chorar', 'choro', 'tristeza', 'triste', 'saudade'],
            'festa': ['festa', 'dançar', 'dança', 'balada', 'cerveja', 'bebida', 'beber', 'alegria', 'alegre'],
            'traicao': ['traição', 'trair', 'traiu', 'mentira', 'mentir', 'infiel', 'outro', 'outra'],
            'saudade': ['saudade', 'saudades', 'falta', 'lembrar', 'lembrança', 'recordar', 'memória'],
            'sexualidade': ['corpo', 'beijo', 'cama', 'tesão', 'desejo', 'quente', 'sedução'],
            'natureza': ['sol', 'lua', 'mar', 'céu', 'estrela', 'vento', 'chuva', 'rio'],
            'urbano': ['cidade', 'rua', 'favela', 'quebrada', 'bairro', 'carro', 'moto'],
            'ostentacao': ['dinheiro', 'grana', 'ouro', 'diamante', 'carro', 'luxo', 'sucesso'],
            'social': ['vida', 'mundo', 'gente', 'povo', 'brasil', 'país', 'social'],
            'religioso': ['deus', 'senhor', 'fé', 'rezar', 'oração', 'anjo', 'céu'],
            'familia': ['mãe', 'pai', 'filho', 'família', 'casa', 'lar']
        }

        theme_scores = defaultdict(int)
        total_songs = len(songs)

        for song in songs:
            lyrics_lower = song.get('lyrics', '').lower()

            for theme, keywords in theme_keywords.items():
                for keyword in keywords:
                    if keyword in lyrics_lower:
                        theme_scores[theme] += 1
                        break  # Count once per song per theme

        # Normalize to percentages
        theme_distribution = {
            theme: {
                'song_count': count,
                'percentage': round((count / total_songs * 100), 2)
            }
            for theme, count in theme_scores.items()
        }

        # Sort by prevalence
        sorted_themes = sorted(theme_distribution.items(), key=lambda x: x[1]['percentage'], reverse=True)

        return dict(sorted_themes)

    def _analyze_structure(self, songs: List[Dict]) -> Dict:
        """
        Analyze structural characteristics.

        Args:
            songs: List of songs

        Returns:
            Structure statistics
        """
        line_counts = []
        word_counts = []
        paragraph_counts = []
        repetition_scores = []

        for song in songs:
            lyrics = song.get('lyrics', '')

            lines = lyrics.split('\n')
            non_empty_lines = [l for l in lines if l.strip()]
            words = lyrics.split()
            paragraphs = lyrics.split('\n\n')
            non_empty_paragraphs = [p for p in paragraphs if p.strip()]

            line_counts.append(len(non_empty_lines))
            word_counts.append(len(words))
            paragraph_counts.append(len(non_empty_paragraphs))

            # Measure repetition (unique lines / total lines)
            if non_empty_lines:
                unique_lines = len(set(l.lower().strip() for l in non_empty_lines))
                repetition = 1 - (unique_lines / len(non_empty_lines))
                repetition_scores.append(repetition)

        return {
            'avg_lines': round(sum(line_counts) / len(line_counts), 1) if line_counts else 0,
            'avg_words': round(sum(word_counts) / len(word_counts), 1) if word_counts else 0,
            'avg_paragraphs': round(sum(paragraph_counts) / len(paragraph_counts), 1) if paragraph_counts else 0,
            'avg_repetition': round(sum(repetition_scores) / len(repetition_scores), 3) if repetition_scores else 0,
            'line_range': [min(line_counts), max(line_counts)] if line_counts else [0, 0],
            'word_range': [min(word_counts), max(word_counts)] if word_counts else [0, 0]
        }

    def _find_distinctive_features(self, songs: List[Dict], genre: str) -> Dict:
        """
        Find what makes this genre distinctive vs other genres.

        Args:
            songs: Songs in this genre
            genre: Genre name

        Returns:
            Distinctive features dictionary
        """
        # Calculate TF-IDF like scoring for words
        # Words that appear frequently in THIS genre but not in others = distinctive

        genre_words = Counter()
        for song in songs:
            words = self._tokenize(song.get('lyrics', ''))
            genre_words.update(words)

        # Get words from other genres
        other_genres_words = Counter()
        for song in self.corpus:
            if song.get('genre') != genre:
                words = self._tokenize(song.get('lyrics', ''))
                other_genres_words.update(words)

        # Calculate distinctiveness score
        distinctive_words = []
        for word, count in genre_words.most_common(500):
            # Skip very common words
            if len(word) < 3:
                continue

            genre_freq = count / sum(genre_words.values())
            other_freq = other_genres_words.get(word, 0) / sum(other_genres_words.values()) if other_genres_words else 0

            # Distinctive = high in this genre, low in others
            if other_freq > 0:
                distinctiveness = genre_freq / other_freq
            else:
                distinctiveness = genre_freq * 100  # Very distinctive

            if distinctiveness > 2:  # At least 2x more common in this genre
                distinctive_words.append({
                    'word': word,
                    'genre_frequency': round(genre_freq, 5),
                    'other_frequency': round(other_freq, 5),
                    'distinctiveness': round(distinctiveness, 2)
                })

        # Sort by distinctiveness
        distinctive_words.sort(key=lambda x: x['distinctiveness'], reverse=True)

        return {
            'top_distinctive_words': distinctive_words[:50]
        }

    def _find_common_patterns(self, songs: List[Dict]) -> Dict:
        """
        Find common structural patterns (intro/verse/chorus markers).

        Args:
            songs: List of songs

        Returns:
            Common patterns dictionary
        """
        # Look for common markers
        markers = {
            'refrão': 0,
            'chorus': 0,
            'verso': 0,
            'verse': 0,
            'intro': 0,
            'ponte': 0,
            'bridge': 0
        }

        for song in songs:
            lyrics_lower = song.get('lyrics', '').lower()
            for marker in markers:
                if marker in lyrics_lower:
                    markers[marker] += 1

        total = len(songs)

        return {
            'structure_markers': {
                marker: {
                    'count': count,
                    'percentage': round((count / total * 100), 2)
                }
                for marker, count in markers.items()
                if count > 0
            }
        }

    def get_genre_formula(self, genre: str) -> Dict:
        """
        Get the "formula" for a specific genre.

        Args:
            genre: Genre name

        Returns:
            Genre formula dictionary
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        if genre not in self.genre_profiles:
            raise ValueError(f"Genre '{genre}' not found in corpus")

        return self.genre_profiles[genre]

    def compare_genres(self, genre1: str, genre2: str) -> Dict:
        """
        Compare two genres to find similarities and differences.

        Args:
            genre1: First genre
            genre2: Second genre

        Returns:
            Comparison dictionary
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        profile1 = self.genre_profiles.get(genre1)
        profile2 = self.genre_profiles.get(genre2)

        if not profile1 or not profile2:
            raise ValueError(f"One or both genres not found")

        # Compare vocabularies
        words1 = set(w['word'] for w in profile1['vocabulary']['top_100_words'])
        words2 = set(w['word'] for w in profile2['vocabulary']['top_100_words'])

        common_words = words1 & words2
        unique_to_1 = words1 - words2
        unique_to_2 = words2 - words1

        # Compare themes
        themes1 = set(profile1['themes'].keys())
        themes2 = set(profile2['themes'].keys())

        common_themes = themes1 & themes2

        return {
            'vocabulary_overlap': {
                'common_words_count': len(common_words),
                'unique_to_' + genre1: len(unique_to_1),
                'unique_to_' + genre2: len(unique_to_2),
                'overlap_percentage': round(len(common_words) / min(len(words1), len(words2)) * 100, 2)
            },
            'structural_comparison': {
                genre1: profile1['structure'],
                genre2: profile2['structure']
            },
            'theme_comparison': {
                'common_themes': list(common_themes),
                genre1 + '_unique': list(themes1 - themes2),
                genre2 + '_unique': list(themes2 - themes1)
            }
        }

    def generate_report(self) -> Dict:
        """
        Generate comprehensive pattern analysis report.

        Returns:
            Report dictionary
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        report = {
            'overview': {
                'total_genres': len(self.genre_profiles),
                'genres_analyzed': list(self.genre_profiles.keys())
            },
            'genre_profiles': self.genre_profiles
        }

        return report

    def save_report(self, output_path: Path):
        """Save pattern report to JSON file."""
        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved pattern report to {output_path}")

    def print_summary(self):
        """Print formatted summary of genre patterns."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        print("\n" + "="*80)
        print(" GENRE PATTERN ANALYSIS ".center(80, "="))
        print("="*80 + "\n")

        for genre, profile in sorted(self.genre_profiles.items()):
            print(f"🎵 {genre.upper()}")
            print("-" * 80)

            # Basic stats
            print(f"Songs: {profile['song_count']:,}")
            vocab = profile['vocabulary']
            print(f"Vocabulary: {vocab['unique_words']:,} unique words | Richness: {vocab['vocabulary_richness']}")

            # Structure
            struct = profile['structure']
            print(f"Structure: {struct['avg_lines']:.0f} lines | {struct['avg_words']:.0f} words | "
                  f"{struct['avg_repetition']:.1%} repetition")

            # Top themes
            print(f"\nTop Themes:")
            for i, (theme, data) in enumerate(list(profile['themes'].items())[:5], 1):
                print(f"  {i}. {theme:20s} - {data['percentage']:5.1f}% of songs")

            # Distinctive words
            print(f"\nMost Distinctive Words (vs other genres):")
            distinctive = profile['distinctive_features']['top_distinctive_words'][:10]
            for i, word_data in enumerate(distinctive, 1):
                print(f"  {i:2d}. {word_data['word']:15s} - {word_data['distinctiveness']:.1f}x more common")

            # Top vocabulary
            print(f"\nTop 10 Most Common Words:")
            for i, word_data in enumerate(vocab['top_100_words'][:10], 1):
                print(f"  {i:2d}. {word_data['word']:15s} - {word_data['count']:6,} uses")

            print()

        print("="*80 + "\n")
