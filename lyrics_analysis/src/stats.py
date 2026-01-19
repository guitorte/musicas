"""
Statistics and analysis module for lyrics corpus.
Generates comprehensive statistics about the corpus.
"""

from typing import List, Dict, Counter as CounterType
from collections import Counter, defaultdict
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class CorpusStatistics:
    """Generates statistics about the lyrics corpus."""

    def __init__(self, songs: List['Song']):
        """
        Initialize statistics generator.

        Args:
            songs: List of Song objects
        """
        self.songs = songs

    def generate_all_statistics(self) -> Dict:
        """
        Generate comprehensive statistics about the corpus.

        Returns:
            Dictionary with all statistics
        """
        stats = {
            'overview': self._overview_stats(),
            'by_genre': self._genre_stats(),
            'by_artist': self._artist_stats(),
            'text_analysis': self._text_stats(),
            'vocabulary': self._vocabulary_stats(),
        }

        return stats

    def _overview_stats(self) -> Dict:
        """Generate overview statistics."""
        total_songs = len(self.songs)

        # Count by source file
        source_counts = Counter(song.source_file for song in self.songs)

        # Count with/without metadata
        with_genre = sum(1 for song in self.songs if song.genre)
        with_featuring = sum(1 for song in self.songs if song.featuring)

        return {
            'total_songs': total_songs,
            'songs_by_file': dict(source_counts),
            'songs_with_genre': with_genre,
            'songs_with_featuring': with_featuring,
            'unique_artists': len(set(song.artist for song in self.songs)),
            'unique_genres': len(set(song.genre for song in self.songs if song.genre))
        }

    def _genre_stats(self) -> Dict:
        """Generate statistics by genre."""
        genre_stats = defaultdict(lambda: {
            'count': 0,
            'artists': set(),
            'total_words': 0,
            'total_chars': 0
        })

        for song in self.songs:
            genre = song.genre or 'Unknown'
            genre_stats[genre]['count'] += 1
            genre_stats[genre]['artists'].add(song.artist)
            genre_stats[genre]['total_words'] += len(song.lyrics.split())
            genre_stats[genre]['total_chars'] += len(song.lyrics)

        # Convert sets to counts and calculate averages
        result = {}
        for genre, data in genre_stats.items():
            result[genre] = {
                'song_count': data['count'],
                'unique_artists': len(data['artists']),
                'avg_words_per_song': data['total_words'] / data['count'] if data['count'] > 0 else 0,
                'avg_chars_per_song': data['total_chars'] / data['count'] if data['count'] > 0 else 0
            }

        return result

    def _artist_stats(self) -> Dict:
        """Generate statistics by artist."""
        artist_counts = Counter(song.artist for song in self.songs)

        # Get top artists
        top_artists = artist_counts.most_common(20)

        # Get detailed stats for top artists
        artist_details = {}
        for artist, count in top_artists[:10]:
            artist_songs = [s for s in self.songs if s.artist == artist]
            genres = set(s.genre for s in artist_songs if s.genre)

            total_words = sum(len(s.lyrics.split()) for s in artist_songs)

            artist_details[artist] = {
                'song_count': count,
                'genres': list(genres),
                'avg_words_per_song': total_words / count if count > 0 else 0
            }

        return {
            'total_unique_artists': len(artist_counts),
            'top_artists': dict(top_artists),
            'artist_details': artist_details
        }

    def _text_stats(self) -> Dict:
        """Generate text-based statistics."""
        total_words = 0
        total_chars = 0
        total_lines = 0

        word_counts = []
        char_counts = []
        line_counts = []

        for song in self.songs:
            words = len(song.lyrics.split())
            chars = len(song.lyrics)
            lines = len(song.lyrics.split('\n'))

            total_words += words
            total_chars += chars
            total_lines += lines

            word_counts.append(words)
            char_counts.append(chars)
            line_counts.append(lines)

        # Sort to get percentiles
        word_counts.sort()
        char_counts.sort()
        line_counts.sort()

        n = len(self.songs)

        return {
            'total_words': total_words,
            'total_chars': total_chars,
            'total_lines': total_lines,
            'avg_words_per_song': total_words / n if n > 0 else 0,
            'avg_chars_per_song': total_chars / n if n > 0 else 0,
            'avg_lines_per_song': total_lines / n if n > 0 else 0,
            'median_words_per_song': word_counts[n // 2] if n > 0 else 0,
            'min_words_per_song': min(word_counts) if word_counts else 0,
            'max_words_per_song': max(word_counts) if word_counts else 0,
            'percentile_25_words': word_counts[n // 4] if n > 0 else 0,
            'percentile_75_words': word_counts[3 * n // 4] if n > 0 else 0,
        }

    def _vocabulary_stats(self) -> Dict:
        """Generate vocabulary statistics."""
        # Collect all words
        all_words = []
        for song in self.songs:
            words = song.lyrics.lower().split()
            all_words.extend(words)

        # Count frequencies
        word_freq = Counter(all_words)

        # Get top words
        top_words = word_freq.most_common(50)

        return {
            'total_words': len(all_words),
            'unique_words': len(word_freq),
            'vocabulary_richness': len(word_freq) / len(all_words) if all_words else 0,
            'top_50_words': dict(top_words),
            'singleton_words': sum(1 for count in word_freq.values() if count == 1),
        }

    def print_summary(self):
        """Print a formatted summary of statistics."""
        stats = self.generate_all_statistics()

        print("\n" + "="*80)
        print(" CORPUS STATISTICS SUMMARY ".center(80, "="))
        print("="*80 + "\n")

        # Overview
        print("📊 OVERVIEW")
        print("-" * 80)
        overview = stats['overview']
        print(f"Total Songs: {overview['total_songs']:,}")
        print(f"Unique Artists: {overview['unique_artists']:,}")
        print(f"Unique Genres: {overview['unique_genres']}")
        print(f"Songs with Genre: {overview['songs_with_genre']:,} ({overview['songs_with_genre']/overview['total_songs']*100:.1f}%)")
        print(f"Songs with Featuring: {overview['songs_with_featuring']:,}")

        # Text stats
        print("\n📝 TEXT STATISTICS")
        print("-" * 80)
        text = stats['text_analysis']
        print(f"Total Words: {text['total_words']:,}")
        print(f"Total Characters: {text['total_chars']:,}")
        print(f"Average Words per Song: {text['avg_words_per_song']:.1f}")
        print(f"Median Words per Song: {text['median_words_per_song']}")
        print(f"Range: {text['min_words_per_song']} - {text['max_words_per_song']} words")

        # Vocabulary
        print("\n📚 VOCABULARY")
        print("-" * 80)
        vocab = stats['vocabulary']
        print(f"Total Word Tokens: {vocab['total_words']:,}")
        print(f"Unique Words: {vocab['unique_words']:,}")
        print(f"Vocabulary Richness: {vocab['vocabulary_richness']:.4f}")
        print(f"\nTop 10 Most Common Words:")
        for i, (word, count) in enumerate(list(vocab['top_50_words'].items())[:10], 1):
            print(f"  {i:2d}. {word:15s} - {count:6,} occurrences")

        # Genres
        print("\n🎵 BY GENRE")
        print("-" * 80)
        for genre, data in sorted(stats['by_genre'].items(), key=lambda x: x[1]['song_count'], reverse=True):
            print(f"{genre:20s}: {data['song_count']:4,} songs | "
                  f"{data['unique_artists']:3} artists | "
                  f"Avg {data['avg_words_per_song']:.0f} words/song")

        # Top artists
        print("\n🎤 TOP 10 ARTISTS")
        print("-" * 80)
        for i, (artist, count) in enumerate(list(stats['by_artist']['top_artists'].items())[:10], 1):
            genres = stats['by_artist']['artist_details'].get(artist, {}).get('genres', [])
            genre_str = ', '.join(genres[:2]) if genres else 'Unknown'
            print(f"  {i:2d}. {artist:30s} - {count:3} songs [{genre_str}]")

        print("\n" + "="*80 + "\n")

    def save_statistics(self, output_path: Path):
        """
        Save statistics to JSON file.

        Args:
            output_path: Path to output file
        """
        stats = self.generate_all_statistics()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved statistics to {output_path}")
