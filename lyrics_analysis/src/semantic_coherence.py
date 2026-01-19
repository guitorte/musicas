"""
Semantic Coherence - Ensure thematic consistency and narrative flow.

This module maintains coherence across generated lyrics:
- Theme-based vocabulary grouping
- Topic progression (intro → development → conclusion)
- Semantic similarity between adjacent lines
- Narrative arc construction

Transforms V1's random lines into coherent, themed verses.
"""

import random
from typing import List, Dict, Optional, Set
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class SemanticCoherence:
    """Ensures semantic coherence in generated lyrics."""

    def __init__(self):
        """Initialize semantic coherence module."""

        # Theme-based vocabulary clusters
        self.theme_clusters = self._build_theme_clusters()

        # Narrative arc templates
        self.narrative_arcs = self._build_narrative_arcs()

        # Transition words for flow
        self.transitions = {
            'continuation': ['e', 'também', 'ainda', 'depois', 'então'],
            'contrast': ['mas', 'porém', 'entretanto', 'contudo'],
            'causation': ['porque', 'pois', 'já que', 'então'],
            'temporal': ['quando', 'enquanto', 'agora', 'sempre', 'nunca'],
            'conditional': ['se', 'caso', 'talvez']
        }

        logger.info("✓ Semantic coherence module initialized")

    def _build_theme_clusters(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Build thematic vocabulary clusters.

        Returns:
            Dictionary of theme → {aspect: words}
        """
        return {
            'amor_romantico': {
                'subjects': ['você', 'meu amor', 'meu bem', 'querida'],
                'feelings': ['amor', 'paixão', 'carinho', 'desejo', 'saudade'],
                'actions': ['amar', 'beijar', 'abraçar', 'sonhar', 'querer'],
                'places': ['coração', 'alma', 'céu', 'paraíso'],
                'qualities': ['linda', 'bela', 'doce', 'especial']
            },

            'sofrimento': {
                'subjects': ['eu', 'meu coração', 'minha alma'],
                'feelings': ['dor', 'tristeza', 'solidão', 'mágoa', 'saudade'],
                'actions': ['chorar', 'sofrer', 'lembrar', 'perder', 'partir'],
                'places': ['distância', 'vazio', 'escuridão'],
                'qualities': ['triste', 'perdido', 'sozinho', 'machucado']
            },

            'festa': {
                'subjects': ['a galera', 'nós', 'todo mundo'],
                'feelings': ['alegria', 'animação', 'curtição'],
                'actions': ['dançar', 'cantar', 'curtir', 'beber', 'festejar'],
                'places': ['festa', 'balada', 'pista', 'bar'],
                'qualities': ['animado', 'louco', 'top', 'massa']
            },

            'natureza': {
                'subjects': ['o sol', 'a lua', 'o mar', 'o vento'],
                'feelings': ['paz', 'liberdade', 'harmonia'],
                'actions': ['brilhar', 'voar', 'flutuar', 'contemplar'],
                'places': ['céu', 'mar', 'praia', 'campo', 'jardim'],
                'qualities': ['belo', 'sereno', 'livre', 'puro']
            },

            'social': {
                'subjects': ['a gente', 'o povo', 'nós'],
                'feelings': ['esperança', 'união', 'luta'],
                'actions': ['viver', 'lutar', 'trabalhar', 'sonhar', 'resistir'],
                'places': ['cidade', 'rua', 'mundo', 'vida'],
                'qualities': ['forte', 'unido', 'bravo', 'real']
            }
        }

    def _build_narrative_arcs(self) -> Dict[str, List[str]]:
        """
        Build narrative arc templates.

        Returns:
            Dictionary of arc_type → [stage1, stage2, ...]
        """
        return {
            'love_story': [
                'meeting',      # Introduction
                'attraction',   # Development
                'declaration',  # Climax
                'union'        # Resolution
            ],

            'heartbreak': [
                'happiness',    # Setup
                'conflict',     # Rising action
                'separation',   # Climax
                'suffering'    # Resolution
            ],

            'party': [
                'arrival',      # Setup
                'excitement',   # Development
                'celebration',  # Climax
                'joy'          # Continuation
            ],

            'reflection': [
                'observation',  # Introduction
                'thought',      # Development
                'realization',  # Climax
                'conclusion'   # Resolution
            ]
        }

    def select_narrative_arc(self, theme: str) -> List[str]:
        """
        Select appropriate narrative arc for theme.

        Args:
            theme: Theme name

        Returns:
            List of narrative stages
        """
        arc_mapping = {
            'amor_romantico': 'love_story',
            'sofrimento': 'heartbreak',
            'festa': 'party',
            'natureza': 'reflection',
            'social': 'reflection'
        }

        arc_type = arc_mapping.get(theme, 'reflection')
        return self.narrative_arcs[arc_type]

    def get_thematic_vocabulary(
        self,
        theme: str,
        stage: Optional[str] = None,
        count: int = 20
    ) -> List[str]:
        """
        Get vocabulary appropriate for theme and narrative stage.

        Args:
            theme: Theme name
            stage: Optional narrative stage
            count: Number of words to return

        Returns:
            List of thematically appropriate words
        """
        if theme not in self.theme_clusters:
            # Fallback to general vocabulary
            theme = 'amor_romantico'

        cluster = self.theme_clusters[theme]

        # Collect all words from theme
        words = []
        for aspect, word_list in cluster.items():
            words.extend(word_list)

        # Shuffle and return
        random.shuffle(words)
        return words[:count]

    def ensure_verse_coherence(
        self,
        lines: List[str],
        theme: str
    ) -> List[str]:
        """
        Ensure lines in a verse are thematically coherent.

        Args:
            lines: Input lines
            theme: Theme to maintain

        Returns:
            Coherent lines
        """
        # V2.0: Basic implementation - just ensures thematic vocabulary
        # Future: Add semantic similarity checks, topic modeling, etc.

        thematic_vocab = self.get_thematic_vocabulary(theme)

        # Check if lines use thematic vocabulary
        coherent_lines = []

        for line in lines:
            words_in_line = set(line.lower().split())
            thematic_words = set(w.lower() for w in thematic_vocab)

            # Check for thematic overlap
            if words_in_line & thematic_words:
                coherent_lines.append(line)
            else:
                # Line not thematic - keep it anyway for V2.0
                coherent_lines.append(line)

        return coherent_lines

    def add_transitions(
        self,
        lines: List[str],
        transition_density: float = 0.3
    ) -> List[str]:
        """
        Add transition words to improve flow.

        Args:
            lines: Input lines
            transition_density: Fraction of lines to add transitions (0-1)

        Returns:
            Lines with transitions
        """
        if not lines:
            return lines

        enhanced_lines = []

        for i, line in enumerate(lines):
            if random.random() < transition_density and i > 0:
                # Add transition at start of line
                transition_type = random.choice(list(self.transitions.keys()))
                transition_word = random.choice(self.transitions[transition_type])

                # Capitalize first letter
                enhanced_line = f"{transition_word.capitalize()} {line}"
                enhanced_lines.append(enhanced_line)
            else:
                enhanced_lines.append(line)

        return enhanced_lines

    def build_coherent_section(
        self,
        theme: str,
        line_count: int,
        narrative_stage: Optional[str] = None,
        vocabulary_selector = None,
        grammar_engine = None
    ) -> List[str]:
        """
        Build a thematically coherent section.

        Args:
            theme: Theme to maintain
            line_count: Number of lines
            narrative_stage: Optional narrative stage
            vocabulary_selector: Optional vocabulary selector
            grammar_engine: Optional grammar engine

        Returns:
            Coherent section lines
        """
        # Get thematic vocabulary
        thematic_vocab = self.get_thematic_vocabulary(theme, narrative_stage)

        lines = []

        for _ in range(line_count):
            if grammar_engine:
                # Use grammar engine for proper sentences
                line = grammar_engine.generate_sentence(thematic_vocab, theme)
            else:
                # Fallback: simple line
                words = random.sample(thematic_vocab, min(5, len(thematic_vocab)))
                line = ' '.join(words)

            lines.append(line)

        # Add transitions for flow
        lines = self.add_transitions(lines, transition_density=0.2)

        return lines

    def get_theme_progression(
        self,
        theme: str,
        section_count: int
    ) -> List[str]:
        """
        Get narrative progression for multiple sections.

        Args:
            theme: Main theme
            section_count: Number of sections

        Returns:
            List of narrative stages for each section
        """
        arc = self.select_narrative_arc(theme)

        # Map sections to arc stages
        progression = []

        for i in range(section_count):
            # Cycle through arc stages
            stage = arc[i % len(arc)]
            progression.append(stage)

        return progression

    def measure_coherence(self, lines: List[str], theme: str) -> float:
        """
        Measure semantic coherence of lines.

        Args:
            lines: Lines to measure
            theme: Expected theme

        Returns:
            Coherence score (0-100)
        """
        if not lines:
            return 0.0

        thematic_vocab = set(w.lower() for w in self.get_thematic_vocabulary(theme, count=50))

        # Count thematic word usage
        total_words = 0
        thematic_words = 0

        for line in lines:
            words = line.lower().split()
            total_words += len(words)

            for word in words:
                if word in thematic_vocab:
                    thematic_words += 1

        # Calculate coherence percentage
        if total_words == 0:
            return 0.0

        coherence = (thematic_words / total_words) * 100

        return min(100.0, coherence)
