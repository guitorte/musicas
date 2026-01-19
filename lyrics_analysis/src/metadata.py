"""
Metadata extraction and enrichment module.
Extracts additional information from lyrics and metadata fields.
"""

import re
from typing import Optional, List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MetadataExtractor:
    """Extracts and enriches metadata from songs."""

    # Common themes in Brazilian music
    THEMES = {
        'amor': ['amor', 'amar', 'coração', 'paixão', 'beijar', 'abraço'],
        'sofrimento': ['solidão', 'sofr', 'dor', 'chorar', 'tristeza', 'saudade'],
        'festa': ['festa', 'dançar', 'balada', 'cerveja', 'bebida', 'alegria'],
        'relacionamento': ['você', 'nós', 'juntos', 'casal', 'namoro', 'relacionamento'],
        'traição': ['traição', 'trair', 'outro', 'outra', 'mentira', 'infiel'],
        'natureza': ['sol', 'lua', 'mar', 'céu', 'estrela', 'vento'],
        'social': ['vida', 'mundo', 'gente', 'povo', 'brasil', 'país'],
    }

    def extract_metadata(self, song: 'Song') -> Dict:
        """
        Extract enhanced metadata from a song.

        Args:
            song: Song object

        Returns:
            Dictionary with extracted metadata
        """
        lyrics_lower = song.lyrics.lower()

        metadata = {
            'basic': {
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'featuring': song.featuring,
                'source_file': song.source_file
            },
            'structure': self._analyze_structure(song.lyrics),
            'themes': self._detect_themes(lyrics_lower),
            'language': self._analyze_language(lyrics_lower),
            'entities': self._extract_entities(song.lyrics),
        }

        return metadata

    def _analyze_structure(self, lyrics: str) -> Dict:
        """
        Analyze structural elements of lyrics.

        Args:
            lyrics: Lyrics text

        Returns:
            Dictionary with structure information
        """
        lines = lyrics.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        paragraphs = lyrics.split('\n\n')
        non_empty_paragraphs = [p for p in paragraphs if p.strip()]

        # Count words
        words = lyrics.split()

        # Detect repeated lines (chorus)
        line_counts = {}
        for line in non_empty_lines:
            line_clean = line.strip().lower()
            if len(line_clean) > 10:  # Minimum length
                line_counts[line_clean] = line_counts.get(line_clean, 0) + 1

        max_repetitions = max(line_counts.values()) if line_counts else 0

        return {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'paragraphs': len(non_empty_paragraphs),
            'total_words': len(words),
            'unique_words': len(set(w.lower() for w in words)),
            'avg_words_per_line': len(words) / len(non_empty_lines) if non_empty_lines else 0,
            'has_repetition': max_repetitions >= 2,
            'max_line_repetitions': max_repetitions
        }

    def _detect_themes(self, lyrics_lower: str) -> Dict[str, float]:
        """
        Detect themes present in lyrics based on keyword matching.

        Args:
            lyrics_lower: Lowercase lyrics text

        Returns:
            Dictionary mapping theme to score (0-1)
        """
        theme_scores = {}

        for theme, keywords in self.THEMES.items():
            matches = 0
            for keyword in keywords:
                # Count occurrences
                matches += lyrics_lower.count(keyword)

            # Normalize by lyrics length (per 100 words)
            word_count = len(lyrics_lower.split())
            score = (matches / word_count * 100) if word_count > 0 else 0

            # Cap at 1.0
            theme_scores[theme] = min(score, 1.0)

        return theme_scores

    def _analyze_language(self, lyrics_lower: str) -> Dict:
        """
        Analyze language characteristics.

        Args:
            lyrics_lower: Lowercase lyrics text

        Returns:
            Dictionary with language statistics
        """
        # Count pronouns (informal vs formal)
        voce_count = lyrics_lower.count('você') + lyrics_lower.count('voce')
        tu_count = lyrics_lower.count('tu ')

        # Count common Portuguese words
        common_words = {
            'que': lyrics_lower.count(' que '),
            'de': lyrics_lower.count(' de '),
            'e': lyrics_lower.count(' e '),
            'o': lyrics_lower.count(' o '),
            'a': lyrics_lower.count(' a ')
        }

        # Detect potential Spanish (some trap songs)
        spanish_indicators = ['yo ', 'mi ', 'tu ', 'el ', 'la ', 'cuando', 'mucho']
        spanish_count = sum(lyrics_lower.count(word) for word in spanish_indicators)

        words = lyrics_lower.split()

        return {
            'informal_pronouns': voce_count + tu_count,
            'possible_spanish': spanish_count > 5,
            'common_word_density': sum(common_words.values()) / len(words) if words else 0,
        }

    def _extract_entities(self, lyrics: str) -> Dict:
        """
        Extract named entities (simplified - proper nouns).

        Args:
            lyrics: Original lyrics text

        Returns:
            Dictionary with extracted entities
        """
        # Simple heuristic: words that start with capital letter
        # and are not at start of line
        words = lyrics.split()

        potential_names = []
        for i, word in enumerate(words):
            # Remove punctuation
            clean_word = re.sub(r'[^\w]', '', word)

            # Check if capitalized and not first word of sentence
            if clean_word and clean_word[0].isupper() and len(clean_word) > 2:
                # Not right after period (simplified check)
                if i == 0 or not words[i-1].endswith('.'):
                    potential_names.append(clean_word)

        # Count frequency
        name_counts = {}
        for name in potential_names:
            name_counts[name] = name_counts.get(name, 0) + 1

        # Return top 10 most frequent
        sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            'potential_names': [name for name, count in sorted_names],
            'name_frequencies': dict(sorted_names)
        }

    def enrich_with_external_data(self, song: 'Song', external_data: Dict) -> Dict:
        """
        Enrich song with external data sources (placeholder for future expansion).

        Args:
            song: Song object
            external_data: External data dictionary

        Returns:
            Enriched metadata
        """
        # Placeholder for future integration with:
        # - Spotify API for popularity, audio features
        # - MusicBrainz for release dates
        # - Lyrics APIs for verified data

        return {
            'artist_popularity': external_data.get('artist_popularity'),
            'release_year': external_data.get('release_year'),
            'verified': external_data.get('verified', False)
        }
