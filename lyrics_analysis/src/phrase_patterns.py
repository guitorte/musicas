"""
Phrase Patterns - Learn natural phrase structures from corpus.

This module extracts and applies common phrase patterns:
- N-gram patterns (2-5 word sequences)
- Phrase templates with wildcards
- Word collocation patterns
- Transitional phrases

Uses corpus analysis to generate more natural-sounding lyrics.
"""

import json
import random
import re
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from collections import Counter, defaultdict
import logging

logger = logging.getLogger(__name__)


class PhrasePatternLearner:
    """Learns and applies phrase patterns from corpus."""

    def __init__(self, corpus_data: Optional[List[Dict]] = None):
        """
        Initialize phrase pattern learner.

        Args:
            corpus_data: Optional corpus data to learn from
        """
        self.corpus = corpus_data or []

        # Learned patterns
        self.bigrams = Counter()  # 2-word sequences
        self.trigrams = Counter()  # 3-word sequences
        self.phrase_templates = []  # Common templates
        self.collocations = defaultdict(list)  # Word → common next words

        if self.corpus:
            self._learn_patterns()
            logger.info(f"✓ Learned patterns from {len(self.corpus)} songs")
        else:
            logger.info("✓ Phrase pattern learner initialized (no corpus)")

    def _learn_patterns(self):
        """Extract patterns from corpus."""
        logger.info("Learning phrase patterns from corpus...")

        for song in self.corpus:
            lyrics = song.get('lyrics', '')
            self._extract_ngrams(lyrics)

        logger.info(f"  Learned {len(self.bigrams)} bigrams, {len(self.trigrams)} trigrams")

    def _extract_ngrams(self, text: str):
        """Extract n-grams from text."""
        # Clean and tokenize
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)

        # Extract bigrams
        for i in range(len(words) - 1):
            bigram = (words[i], words[i+1])
            self.bigrams[bigram] += 1

            # Track collocations
            self.collocations[words[i]].append(words[i+1])

        # Extract trigrams
        for i in range(len(words) - 2):
            trigram = (words[i], words[i+1], words[i+2])
            self.trigrams[trigram] += 1

    def get_common_bigrams(self, min_count: int = 5, top_k: int = 100) -> List[Tuple]:
        """
        Get most common bigrams.

        Args:
            min_count: Minimum occurrences
            top_k: Number to return

        Returns:
            List of (bigram, count) tuples
        """
        filtered = [(bg, cnt) for bg, cnt in self.bigrams.items() if cnt >= min_count]
        filtered.sort(key=lambda x: x[1], reverse=True)
        return filtered[:top_k]

    def get_common_trigrams(self, min_count: int = 3, top_k: int = 100) -> List[Tuple]:
        """
        Get most common trigrams.

        Args:
            min_count: Minimum occurrences
            top_k: Number to return

        Returns:
            List of (trigram, count) tuples
        """
        filtered = [(tg, cnt) for tg, cnt in self.trigrams.items() if cnt >= min_count]
        filtered.sort(key=lambda x: x[1], reverse=True)
        return filtered[:top_k]

    def suggest_next_word(self, previous_word: str, vocabulary: Optional[List[str]] = None) -> Optional[str]:
        """
        Suggest next word based on collocations.

        Args:
            previous_word: Previous word in sequence
            vocabulary: Optional vocabulary to choose from

        Returns:
            Suggested next word
        """
        previous_lower = previous_word.lower()

        candidates = self.collocations.get(previous_lower, [])

        if not candidates:
            return None

        # Filter by vocabulary if provided
        if vocabulary:
            vocab_lower = [w.lower() for w in vocabulary]
            candidates = [c for c in candidates if c in vocab_lower]

        if not candidates:
            return None

        # Return most common
        counter = Counter(candidates)
        return counter.most_common(1)[0][0]

    def generate_phrase_from_pattern(
        self,
        pattern_type: str = 'bigram',
        vocabulary: Optional[List[str]] = None
    ) -> str:
        """
        Generate phrase using learned patterns.

        Args:
            pattern_type: 'bigram' or 'trigram'
            vocabulary: Optional vocabulary constraint

        Returns:
            Generated phrase
        """
        if pattern_type == 'trigram' and self.trigrams:
            # Pick random common trigram
            common_trigrams = self.get_common_trigrams(min_count=2, top_k=50)
            if common_trigrams:
                trigram, _ = random.choice(common_trigrams)
                return ' '.join(trigram)

        elif pattern_type == 'bigram' and self.bigrams:
            # Pick random common bigram
            common_bigrams = self.get_common_bigrams(min_count=3, top_k=50)
            if common_bigrams:
                bigram, _ = random.choice(common_bigrams)
                return ' '.join(bigram)

        return ""

    def build_phrase_chain(
        self,
        start_word: str,
        max_length: int = 8,
        vocabulary: Optional[List[str]] = None
    ) -> str:
        """
        Build phrase using word chain (Markov-like).

        Args:
            start_word: Starting word
            max_length: Maximum words
            vocabulary: Optional vocabulary constraint

        Returns:
            Generated phrase
        """
        phrase = [start_word.lower()]

        for _ in range(max_length - 1):
            next_word = self.suggest_next_word(phrase[-1], vocabulary)

            if not next_word:
                break

            phrase.append(next_word)

        return ' '.join(phrase)

    def get_phrase_templates(self, genre: Optional[str] = None) -> List[str]:
        """
        Get common phrase templates.

        Args:
            genre: Optional genre filter

        Returns:
            List of template strings
        """
        # Hardcoded templates for V2 (can be learned from corpus in future)
        templates = [
            "eu {verb} {noun}",
            "você é {adj}",
            "{noun} do meu {noun}",
            "quando você {verb}",
            "se eu pudesse {verb}",
            "todo {noun} que eu {verb}",
            "não quero {verb}",
            "preciso {verb}",
            "sonho com {noun}",
            "sinto {noun}"
        ]

        return templates

    def fill_template(self, template: str, vocabulary: List[str]) -> str:
        """
        Fill a phrase template with vocabulary.

        Args:
            template: Template string with {placeholders}
            vocabulary: Words to use

        Returns:
            Filled phrase
        """
        # Simple placeholder filling
        filled = template

        placeholders = re.findall(r'\{(\w+)\}', template)

        for placeholder in placeholders:
            # Pick random word from vocabulary
            if vocabulary:
                word = random.choice(vocabulary)
                filled = filled.replace(f'{{{placeholder}}}', word, 1)

        return filled

    def generate_natural_line(
        self,
        vocabulary: List[str],
        strategy: str = 'mixed'
    ) -> str:
        """
        Generate a natural-sounding line.

        Args:
            vocabulary: Available vocabulary
            strategy: 'chain', 'template', or 'mixed'

        Returns:
            Generated line
        """
        if strategy == 'chain' or (strategy == 'mixed' and random.random() < 0.3):
            # Use word chain
            if vocabulary:
                start_word = random.choice(vocabulary)
                return self.build_phrase_chain(start_word, max_length=8, vocabulary=vocabulary)

        elif strategy == 'template' or strategy == 'mixed':
            # Use template
            templates = self.get_phrase_templates()
            if templates:
                template = random.choice(templates)
                return self.fill_template(template, vocabulary)

        # Fallback
        return ' '.join(random.sample(vocabulary, min(5, len(vocabulary))))

    def save_patterns(self, output_path: Path):
        """Save learned patterns to file."""
        data = {
            'bigrams': [(list(bg), cnt) for bg, cnt in self.get_common_bigrams(top_k=200)],
            'trigrams': [(list(tg), cnt) for tg, cnt in self.get_common_trigrams(top_k=200)],
            'collocation_counts': {
                word: dict(Counter(words)) for word, words in list(self.collocations.items())[:500]
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved patterns to {output_path}")

    def load_patterns(self, input_path: Path):
        """Load pre-computed patterns from file."""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load bigrams
        for bigram_list, count in data.get('bigrams', []):
            bigram = tuple(bigram_list)
            self.bigrams[bigram] = count

        # Load trigrams
        for trigram_list, count in data.get('trigrams', []):
            trigram = tuple(trigram_list)
            self.trigrams[trigram] = count

        # Load collocations
        for word, word_counts in data.get('collocation_counts', {}).items():
            self.collocations[word] = [w for w, count in word_counts.items() for _ in range(count)]

        logger.info(f"Loaded patterns from {input_path}")
