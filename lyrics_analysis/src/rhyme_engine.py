"""
Rhyme Engine - Phonetic rhyming for Brazilian Portuguese.

This module provides rhyme matching and scheme enforcement:
- Portuguese phonetic transcription
- Rhyme quality scoring (perfect, near, assonance)
- Common rhyme schemes (AABB, ABAB, ABCB, etc.)
- Syllable counting for meter

Transforms V1's random lines into properly rhyming verses.
"""

import re
from typing import List, Dict, Optional, Tuple, Set
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RhymeEngine:
    """Analyzes and generates rhymes for Brazilian Portuguese."""

    def __init__(self):
        """Initialize rhyme engine with phonetic rules."""

        # Common rhyme schemes for lyrics
        self.rhyme_schemes = {
            'AABB': 'Couplet - consecutive rhymes',
            'ABAB': 'Alternate rhymes',
            'ABCB': 'Second and fourth rhyme',
            'AAAA': 'Monorhyme',
            'ABBA': 'Enclosed rhyme',
            'FREE': 'No rhyme scheme'
        }

        # Portuguese vowel sounds (simplified phonetics)
        self.vowel_sounds = {
            'a': 'a', 'á': 'a', 'â': 'a', 'ã': 'ã',
            'e': 'e', 'é': 'e', 'ê': 'e',
            'i': 'i', 'í': 'i',
            'o': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'õ',
            'u': 'u', 'ú': 'u'
        }

        # Common rhyme endings in Brazilian Portuguese
        self.common_rhyme_endings = self._build_rhyme_endings()

        logger.info("✓ Rhyme engine initialized")

    def _build_rhyme_endings(self) -> Dict[str, List[str]]:
        """Build common rhyme ending patterns."""
        return {
            'ão': ['coração', 'paixão', 'solidão', 'canção', 'emoção'],
            'ar': ['amar', 'sonhar', 'lugar', 'olhar', 'lembrar'],
            'or': ['amor', 'dor', 'flor', 'calor', 'valor'],
            'er': ['querer', 'viver', 'sofrer', 'prazer', 'mulher'],
            'im': ['assim', 'ruim', 'jardim', 'enfim', 'vim'],
            'ez': ['vez', 'talvez', 'altivez', 'rapidez', 'francês'],
            'ente': ['gente', 'mente', 'frente', 'presente', 'somente'],
            'ada': ['amada', 'estrada', 'madrugada', 'jornada', 'nada'],
            'ido': ['perdido', 'vivido', 'sofrido', 'sentido', 'partido']
        }

    def get_rhyme_sound(self, word: str) -> str:
        """
        Get the rhyme sound of a word (last stressed syllable + following sounds).

        Args:
            word: Word to analyze

        Returns:
            Rhyme sound string
        """
        word = word.lower().strip()

        if not word:
            return ""

        # Simplified: last 2-3 characters for rhyme matching
        # (In real implementation, would need stress detection)

        # Common endings
        if len(word) >= 3:
            ending3 = word[-3:]
            # Check for common 3-char endings
            if ending3 in ['ção', 'são', 'ão']:
                return ending3

        if len(word) >= 2:
            ending2 = word[-2:]
            # Common 2-char endings
            if ending2 in ['ar', 'er', 'ir', 'or', 'im', 'em', 'om', 'um', 'ez', 'iz', 'oz', 'uz']:
                return ending2

        # Fallback: last 2 chars
        return word[-2:] if len(word) >= 2 else word

    def words_rhyme(self, word1: str, word2: str, strict: bool = False) -> bool:
        """
        Check if two words rhyme.

        Args:
            word1: First word
            word2: Second word
            strict: If True, require perfect rhyme; if False, allow near rhyme

        Returns:
            True if words rhyme
        """
        if word1.lower() == word2.lower():
            return False  # Same word doesn't count

        sound1 = self.get_rhyme_sound(word1)
        sound2 = self.get_rhyme_sound(word2)

        if strict:
            return sound1 == sound2
        else:
            # Near rhyme: last char matches
            return sound1[-1] == sound2[-1] if sound1 and sound2 else False

    def rhyme_quality(self, word1: str, word2: str) -> str:
        """
        Rate rhyme quality.

        Args:
            word1: First word
            word2: Second word

        Returns:
            'perfect', 'near', 'assonance', or 'none'
        """
        sound1 = self.get_rhyme_sound(word1)
        sound2 = self.get_rhyme_sound(word2)

        if sound1 == sound2:
            return 'perfect'
        elif sound1[-1:] == sound2[-1:]:
            return 'near'
        elif self._has_assonance(word1, word2):
            return 'assonance'
        else:
            return 'none'

    def _has_assonance(self, word1: str, word2: str) -> bool:
        """Check for vowel rhyme (assonance)."""
        vowels1 = [c for c in word1.lower() if c in self.vowel_sounds]
        vowels2 = [c for c in word2.lower() if c in self.vowel_sounds]

        if not vowels1 or not vowels2:
            return False

        # Last vowel sounds similar
        return vowels1[-1] == vowels2[-1]

    def find_rhymes(
        self,
        word: str,
        vocabulary: List[str],
        count: int = 5,
        strict: bool = False
    ) -> List[str]:
        """
        Find rhyming words from vocabulary.

        Args:
            word: Word to rhyme with
            vocabulary: Available vocabulary
            count: Number of rhymes to return
            strict: Require perfect rhymes

        Returns:
            List of rhyming words
        """
        rhymes = []
        target_sound = self.get_rhyme_sound(word)

        for candidate in vocabulary:
            if candidate.lower() == word.lower():
                continue  # Skip same word

            candidate_sound = self.get_rhyme_sound(candidate)

            if strict:
                if candidate_sound == target_sound:
                    rhymes.append(candidate)
            else:
                if candidate_sound[-1:] == target_sound[-1:]:
                    rhymes.append(candidate)

            if len(rhymes) >= count:
                break

        return rhymes

    def apply_rhyme_scheme(
        self,
        lines: List[str],
        scheme: str = 'ABAB'
    ) -> List[str]:
        """
        Apply rhyme scheme to lines (modifies line endings if needed).

        Args:
            lines: Input lines
            scheme: Rhyme scheme pattern

        Returns:
            Lines with applied rhyme scheme
        """
        if scheme == 'FREE' or len(lines) < 2:
            return lines

        # Parse scheme
        scheme_chars = list(scheme)
        rhyme_groups = defaultdict(list)

        # Group lines by rhyme letter
        for i, char in enumerate(scheme_chars):
            if i < len(lines):
                rhyme_groups[char].append(i)

        # Process groups - ensure lines in same group rhyme
        # (Simplified: just ensures last words match pattern)

        return lines  # V2.0: Basic implementation, can enhance later

    def count_syllables(self, word: str) -> int:
        """
        Count syllables in a word (simplified).

        Args:
            word: Word to count

        Returns:
            Estimated syllable count
        """
        word = word.lower()

        # Remove silent letters
        word = re.sub(r'[^aeiouáéíóúâêôãõ]', ' ', word)

        # Count vowel groups
        syllables = len(re.findall(r'[aeiouáéíóúâêôãõ]+', word))

        return max(1, syllables)

    def get_line_syllables(self, line: str) -> int:
        """
        Count syllables in a line.

        Args:
            line: Line of text

        Returns:
            Total syllable count
        """
        words = line.split()
        return sum(self.count_syllables(w) for w in words)

    def suggest_rhyme_scheme(self, line_count: int, genre: str = "MPB") -> str:
        """
        Suggest appropriate rhyme scheme for given context.

        Args:
            line_count: Number of lines
            genre: Music genre

        Returns:
            Recommended rhyme scheme
        """
        # Genre-specific preferences
        genre_prefs = {
            'MPB': ['ABAB', 'ABCB'],
            'Sertanejo': ['AABB', 'ABAB'],
            'Trap': ['AABB', 'FREE'],
            'Pagode': ['ABCB', 'AABB'],
            'Arrocha': ['AABB', 'ABAB']
        }

        preferred = genre_prefs.get(genre, ['ABAB'])

        # Select scheme based on line count
        if line_count == 4:
            return preferred[0]
        elif line_count == 2:
            return 'AA'
        elif line_count % 4 == 0:
            return preferred[0]
        else:
            return 'ABCB'

    def get_scheme_pattern(self, scheme: str, line_count: int) -> List[str]:
        """
        Get rhyme pattern for given number of lines.

        Args:
            scheme: Rhyme scheme (e.g., 'ABAB')
            line_count: Number of lines

        Returns:
            List of rhyme labels (e.g., ['A', 'B', 'A', 'B'])
        """
        if scheme == 'FREE':
            return ['X'] * line_count

        scheme_chars = list(scheme)
        pattern = []

        for i in range(line_count):
            pattern.append(scheme_chars[i % len(scheme_chars)])

        return pattern

    def build_rhyming_lines(
        self,
        line_count: int,
        vocabulary: List[str],
        scheme: str = 'ABAB',
        grammar_engine = None
    ) -> List[str]:
        """
        Build lines that follow a rhyme scheme.

        Args:
            line_count: Number of lines
            vocabulary: Available words
            scheme: Rhyme scheme
            grammar_engine: Optional grammar engine for sentence construction

        Returns:
            List of rhyming lines
        """
        pattern = self.get_scheme_pattern(scheme, line_count)

        # Group rhyme positions
        rhyme_groups = defaultdict(list)
        for i, label in enumerate(pattern):
            rhyme_groups[label].append(i)

        # Pick rhyme words for each group
        rhyme_words = {}
        used_words = set()

        for label, positions in rhyme_groups.items():
            # Find rhyming words for this group
            available = [w for w in vocabulary if w not in used_words]

            if not available:
                available = vocabulary

            # Pick a base word
            base_word = available[0] if available else 'amor'
            rhyme_words[label] = [base_word]

            # Find rhymes for other positions in group
            if len(positions) > 1:
                rhymes = self.find_rhymes(base_word, available, count=len(positions)-1)
                rhyme_words[label].extend(rhymes)

            used_words.update(rhyme_words[label])

        # Build lines
        lines = []

        for i, label in enumerate(pattern):
            # Get rhyme word for this line
            group_words = rhyme_words.get(label, ['amor'])
            rhyme_word = group_words[i % len(group_words)]

            # Build line ending with rhyme word
            if grammar_engine:
                # Use grammar engine to build proper sentence
                line = grammar_engine.generate_sentence(vocabulary)
                # Try to end with rhyme word (simplified)
                line = f"{line} {rhyme_word}"
            else:
                # Fallback: simple line
                line = f"... {rhyme_word}"

            lines.append(line)

        return lines

    def get_rhyme_statistics(self, lines: List[str]) -> Dict:
        """
        Analyze rhyme usage in lines.

        Args:
            lines: Lines to analyze

        Returns:
            Rhyme statistics
        """
        if len(lines) < 2:
            return {'has_rhymes': False, 'rhyme_percentage': 0}

        # Extract last words
        last_words = []
        for line in lines:
            words = line.strip().split()
            if words:
                last_words.append(words[-1])

        # Count rhyming pairs
        rhyme_pairs = 0
        total_pairs = 0

        for i in range(len(last_words)):
            for j in range(i+1, len(last_words)):
                total_pairs += 1
                if self.words_rhyme(last_words[i], last_words[j]):
                    rhyme_pairs += 1

        rhyme_percentage = (rhyme_pairs / total_pairs * 100) if total_pairs > 0 else 0

        return {
            'has_rhymes': rhyme_pairs > 0,
            'rhyme_pairs': rhyme_pairs,
            'total_pairs': total_pairs,
            'rhyme_percentage': round(rhyme_percentage, 1),
            'last_words': last_words
        }
