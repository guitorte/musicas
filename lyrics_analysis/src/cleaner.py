"""
Text cleaning and preprocessing module for Brazilian Portuguese lyrics.
Handles normalization, noise removal, and text standardization.
"""

import re
from typing import Optional
import unicodedata
import logging

logger = logging.getLogger(__name__)


class LyricsCleaner:
    """Cleans and normalizes lyrics text."""

    # Common noise patterns in scraped lyrics
    NOISE_PATTERNS = [
        r'\[.*?Envie pra gente.*?\]',  # Contribution prompts
        r'\(/contribuicoes/.*?\)',      # URLs
        r'Sabe de quem é a composição\?',  # Questions
        r'\[.*?composição.*?\]',        # Composition credits
        r'https?://\S+',                # URLs
        r'\[.*?Tradução.*?\]',         # Translation notes
        r'\[.*?Legendado.*?\]',        # Subtitle notes
    ]

    def __init__(self, remove_brackets: bool = False, normalize_unicode: bool = True):
        """
        Initialize the cleaner.

        Args:
            remove_brackets: If True, remove all bracketed content [...]
            normalize_unicode: If True, normalize unicode characters
        """
        self.remove_brackets = remove_brackets
        self.normalize_unicode = normalize_unicode

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.

        Args:
            text: Raw lyrics text

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Normalize unicode if requested
        if self.normalize_unicode:
            text = self._normalize_unicode(text)

        # Remove common noise patterns
        for pattern in self.NOISE_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Optionally remove all bracketed content
        if self.remove_brackets:
            text = re.sub(r'\[.*?\]', '', text)

        # Clean up excessive whitespace
        text = self._clean_whitespace(text)

        # Remove empty lines at start and end
        text = text.strip()

        return text

    def clean_song_metadata(self, text: str) -> str:
        """
        Clean metadata fields (artist, title, etc.).

        Args:
            text: Metadata text

        Returns:
            Cleaned metadata
        """
        if not text:
            return ""

        # Normalize unicode
        if self.normalize_unicode:
            text = self._normalize_unicode(text)

        # Remove common suffixes/prefixes
        text = text.strip()

        # Remove leading/trailing special characters
        text = text.strip('.,;:!?-—–')

        return text

    def _normalize_unicode(self, text: str) -> str:
        """
        Normalize unicode characters to standard forms.
        Preserves Portuguese diacritics (á, ã, ç, etc.).

        Args:
            text: Text to normalize

        Returns:
            Normalized text
        """
        # Use NFC normalization to preserve Portuguese characters
        return unicodedata.normalize('NFC', text)

    def _clean_whitespace(self, text: str) -> str:
        """
        Clean excessive whitespace while preserving structure.

        Args:
            text: Text to clean

        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)

        # Replace multiple newlines with max 2 (preserve paragraph breaks)
        text = re.sub(r'\n\n\n+', '\n\n', text)

        # Remove trailing whitespace from each line
        lines = [line.rstrip() for line in text.split('\n')]
        text = '\n'.join(lines)

        return text

    def extract_chorus(self, lyrics: str) -> Optional[str]:
        """
        Attempt to extract chorus/refrão from lyrics.
        Looks for repeated sections or marked sections.

        Args:
            lyrics: Full lyrics text

        Returns:
            Chorus text if found, None otherwise
        """
        # Look for explicit chorus markers
        chorus_patterns = [
            r'(?:Refrão|Chorus):\s*\n(.+?)(?:\n\n|\Z)',
            r'\[(?:Refrão|Chorus)\]\s*\n(.+?)(?:\n\n|\Z)',
        ]

        for pattern in chorus_patterns:
            match = re.search(pattern, lyrics, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()

        # Look for repeated sections (simple heuristic)
        paragraphs = lyrics.split('\n\n')
        if len(paragraphs) >= 3:
            # Check if any paragraph appears multiple times
            for para in paragraphs:
                para_clean = para.strip()
                if para_clean and len(para_clean) > 20:  # Min length
                    count = lyrics.count(para_clean)
                    if count >= 2:  # Repeated at least twice
                        return para_clean

        return None

    def get_text_stats(self, text: str) -> dict:
        """
        Get basic statistics about text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with statistics
        """
        lines = text.split('\n')
        words = text.split()

        return {
            'char_count': len(text),
            'word_count': len(words),
            'line_count': len(lines),
            'avg_line_length': len(text) / len(lines) if lines else 0,
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
        }
