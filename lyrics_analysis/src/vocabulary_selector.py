"""
Vocabulary Selector - Intelligent word selection with cliché avoidance.

This module provides smart vocabulary selection for lyrics generation:
- Avoids overused clichés (from Phase 2A analysis)
- Selects genre-appropriate vocabulary
- Tunes word rarity based on innovation target
- Provides thematic word sets

The selector uses frequency data to balance familiarity and freshness.
"""

import json
import random
import re
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)


class VocabularySelector:
    """Selects vocabulary intelligently for lyrics generation."""

    def __init__(self, analysis_dir: Path):
        """
        Initialize vocabulary selector.

        Args:
            analysis_dir: Path to analysis directory containing Phase 2A results
        """
        self.analysis_dir = Path(analysis_dir)

        # Initialize vocabulary pools
        self.word_frequencies = {}  # Word → frequency across corpus
        self.genre_vocabularies = {}  # Genre → distinctive words

        # Load Phase 2A data
        self.cliches = self._load_cliches()
        self.genre_formulas = self._load_genre_formulas()

        # Build thematic vocabulary
        self.thematic_words = self._build_thematic_vocabulary()

        logger.info("✓ Vocabulary selector initialized")

    def _load_cliches(self) -> Dict:
        """Load cliché data from Phase 2A analysis."""
        cliche_path = self.analysis_dir / "patterns" / "AVOID_THESE_CLICHES.json"

        if not cliche_path.exists():
            logger.warning(f"Cliché file not found: {cliche_path}")
            return {}

        with open(cliche_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Build set of phrases to avoid
        avoid_phrases = set()
        for key in data:
            if 'cliches' in key.lower():
                for item in data[key]:
                    phrase = item.get('phrase', '')
                    if phrase:
                        avoid_phrases.add(phrase.lower())

        logger.info(f"  Loaded {len(avoid_phrases)} cliché phrases to avoid")
        return {'avoid': avoid_phrases}

    def _load_genre_formulas(self) -> Dict:
        """Load genre formulas from Phase 2A analysis."""
        formula_path = self.analysis_dir / "patterns" / "genre_formulas.json"

        if not formula_path.exists():
            logger.warning(f"Genre formulas not found: {formula_path}")
            return {}

        with open(formula_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract genre-specific vocabularies
        for genre, info in data.get('genres', {}).items():
            self.genre_vocabularies[genre] = {
                'distinctive': info.get('top_10_distinctive_words', []),
                'common': info.get('top_5_words', []),
                'themes': info.get('top_5_themes', []),
                'repetition_level': info.get('repetition_level', 0.3)
            }

        logger.info(f"  Loaded formulas for {len(self.genre_vocabularies)} genres")
        return data.get('genres', {})

    def _build_thematic_vocabulary(self) -> Dict[str, List[str]]:
        """
        Build thematic word pools for different subjects.

        Returns:
            Dictionary mapping themes to word lists
        """
        # Brazilian Portuguese thematic vocabulary
        themes = {
            'amor_romantico': [
                'amor', 'coração', 'paixão', 'beijo', 'abraço', 'saudade',
                'carinho', 'desejo', 'ternura', 'afeto', 'sentimento',
                'amar', 'gostar', 'querer', 'adorar', 'sonhar'
            ],
            'sofrimento': [
                'dor', 'lágrima', 'chorar', 'tristeza', 'solidão', 'saudade',
                'sofrer', 'perdido', 'vazio', 'angústia', 'mágoa',
                'partir', 'distância', 'ausência', 'lembrar'
            ],
            'festa': [
                'festa', 'dançar', 'samba', 'pagode', 'alegria', 'curtir',
                'balada', 'noite', 'cerveja', 'diversão', 'galera',
                'pista', 'som', 'música', 'agito', 'zueira'
            ],
            'natureza': [
                'sol', 'lua', 'mar', 'céu', 'estrela', 'flor', 'vento',
                'chuva', 'terra', 'rio', 'praia', 'noite', 'dia',
                'campo', 'jardim', 'brisa', 'manhã', 'tarde'
            ],
            'social': [
                'vida', 'mundo', 'gente', 'tempo', 'cidade', 'rua',
                'casa', 'família', 'amigo', 'povo', 'lugar',
                'história', 'caminho', 'trabalho', 'luta'
            ],
            'ostentacao': [
                'dinheiro', 'ouro', 'carro', 'roupa', 'marca', 'luxo',
                'status', 'poder', 'fama', 'sucesso', 'conquista',
                'grife', 'estilo', 'classe', 'inveja', 'destaque'
            ],
            'religioso': [
                'deus', 'fé', 'oração', 'benção', 'graça', 'alma',
                'céu', 'anjo', 'milagre', 'perdão', 'paz',
                'rezar', 'crer', 'espírito', 'sagrado'
            ]
        }

        return themes

    def select_words(
        self,
        genre: str,
        theme: Optional[str] = None,
        innovation_level: float = 0.5,
        count: int = 10,
        avoid_cliches: bool = True
    ) -> List[str]:
        """
        Select vocabulary for lyrics generation.

        Args:
            genre: Target genre (Trap, MPB, Sertanejo, etc.)
            theme: Optional theme (amor_romantico, festa, etc.)
            innovation_level: 0-1, higher = more rare/distinctive words
            count: Number of words to return
            avoid_cliches: Whether to filter out cliché words

        Returns:
            List of selected words
        """
        words = []

        # Start with genre-distinctive vocabulary
        if genre in self.genre_vocabularies:
            vocab = self.genre_vocabularies[genre]

            # Weight toward distinctive vs common based on innovation
            if innovation_level > 0.6:
                # High innovation: use distinctive words
                words.extend(vocab['distinctive'])
            else:
                # Lower innovation: mix common and distinctive
                words.extend(vocab['common'])
                words.extend(vocab['distinctive'][:5])

        # Add thematic words if theme specified
        if theme and theme in self.thematic_words:
            thematic = self.thematic_words[theme]
            words.extend(thematic)

        # Filter clichés if requested
        if avoid_cliches:
            words = [w for w in words if w.lower() not in self.cliches.get('avoid', set())]

        # Shuffle and return requested count
        random.shuffle(words)
        return words[:count] if words else []

    def is_cliche(self, phrase: str) -> bool:
        """
        Check if a phrase is a known cliché.

        Args:
            phrase: Text to check

        Returns:
            True if phrase contains clichés
        """
        phrase_lower = phrase.lower()

        # Check against known cliché phrases
        for cliche in self.cliches.get('avoid', set()):
            if cliche in phrase_lower:
                return True

        return False

    def suggest_rhymes(self, word: str, count: int = 5) -> List[str]:
        """
        Suggest rhyming words (simplified - could be enhanced with phonetic library).

        Args:
            word: Word to rhyme with
            count: Number of suggestions

        Returns:
            List of rhyming words
        """
        # Simple suffix-based rhyming (could be improved with phonetic analysis)
        if len(word) < 3:
            return []

        suffix = word[-2:]  # Last 2 chars

        # Collect all vocabulary
        all_words = set()
        for genre_vocab in self.genre_vocabularies.values():
            all_words.update(genre_vocab.get('distinctive', []))
            all_words.update(genre_vocab.get('common', []))

        for theme_words in self.thematic_words.values():
            all_words.update(theme_words)

        # Find words ending with same suffix
        rhymes = [w for w in all_words if w.endswith(suffix) and w != word]

        return rhymes[:count]

    def generate_line(
        self,
        genre: str,
        theme: Optional[str] = None,
        innovation_level: float = 0.5,
        word_count: int = 8,
        avoid_cliches: bool = True
    ) -> str:
        """
        Generate a single line of lyrics.

        Args:
            genre: Target genre
            theme: Optional theme
            innovation_level: 0-1, higher = more innovative
            word_count: Target words per line
            avoid_cliches: Whether to avoid clichés

        Returns:
            Generated line
        """
        # Select words
        words = self.select_words(
            genre=genre,
            theme=theme,
            innovation_level=innovation_level,
            count=word_count * 2,  # Get more to choose from
            avoid_cliches=avoid_cliches
        )

        if not words:
            return ""

        # Build line (simplified - could add grammar rules)
        selected = random.sample(words, min(word_count, len(words)))
        line = ' '.join(selected)

        # Capitalize first letter
        if line:
            line = line[0].upper() + line[1:]

        return line

    def generate_lines(
        self,
        count: int,
        genre: str,
        theme: Optional[str] = None,
        innovation_level: float = 0.5,
        words_per_line: int = 8,
        avoid_cliches: bool = True
    ) -> List[str]:
        """
        Generate multiple lines of lyrics.

        Args:
            count: Number of lines to generate
            genre: Target genre
            theme: Optional theme
            innovation_level: 0-1, higher = more innovative
            words_per_line: Target words per line
            avoid_cliches: Whether to avoid clichés

        Returns:
            List of generated lines
        """
        lines = []

        for _ in range(count):
            line = self.generate_line(
                genre=genre,
                theme=theme,
                innovation_level=innovation_level,
                word_count=words_per_line,
                avoid_cliches=avoid_cliches
            )

            if line:
                lines.append(line)

        return lines

    def get_genre_info(self, genre: str) -> Dict:
        """
        Get information about a genre's vocabulary characteristics.

        Args:
            genre: Genre name

        Returns:
            Genre vocabulary info
        """
        if genre not in self.genre_vocabularies:
            return {}

        return self.genre_vocabularies[genre]

    def list_available_genres(self) -> List[str]:
        """Get list of available genres."""
        return list(self.genre_vocabularies.keys())

    def list_available_themes(self) -> List[str]:
        """Get list of available themes."""
        return list(self.thematic_words.keys())
