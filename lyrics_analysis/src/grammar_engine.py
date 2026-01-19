"""
Grammar Engine - Brazilian Portuguese sentence construction.

This module provides grammatically correct sentence generation:
- Subject-Verb-Object templates
- Proper verb conjugations
- Pronoun and article agreement
- Common lyrical sentence patterns

Transforms V1's random word sequences into proper Portuguese sentences.
"""

import random
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class GrammarEngine:
    """Constructs grammatically correct Brazilian Portuguese sentences."""

    def __init__(self):
        """Initialize grammar engine with Portuguese rules."""

        # Common pronouns
        self.pronouns = {
            'eu': {'conjugation': '1s', 'meaning': 'I'},
            'você': {'conjugation': '3s', 'meaning': 'you'},
            'ele': {'conjugation': '3s', 'meaning': 'he'},
            'ela': {'conjugation': '3s', 'meaning': 'she'},
            'nós': {'conjugation': '1p', 'meaning': 'we'},
            'eles': {'conjugation': '3p', 'meaning': 'they_m'},
            'elas': {'conjugation': '3p', 'meaning': 'they_f'}
        }

        # Common verb patterns (infinitive → conjugations)
        self.verbs = self._build_verb_templates()

        # Sentence templates (lyrical patterns)
        self.sentence_templates = self._build_sentence_templates()

        # Common prepositions and connectors
        self.prepositions = ['de', 'em', 'com', 'por', 'para', 'sem', 'sobre']
        self.connectors = ['e', 'mas', 'porque', 'quando', 'se', 'que']

        logger.info("✓ Grammar engine initialized")

    def _build_verb_templates(self) -> Dict:
        """Build common verb conjugation templates."""
        return {
            # Verb: {conjugation: form}
            'amar': {
                '1s': 'amo', '2s': 'amas', '3s': 'ama',
                '1p': 'amamos', '2p': 'amais', '3p': 'amam'
            },
            'ser': {
                '1s': 'sou', '2s': 'és', '3s': 'é',
                '1p': 'somos', '2p': 'sois', '3p': 'são'
            },
            'estar': {
                '1s': 'estou', '2s': 'estás', '3s': 'está',
                '1p': 'estamos', '2p': 'estais', '3p': 'estão'
            },
            'ter': {
                '1s': 'tenho', '2s': 'tens', '3s': 'tem',
                '1p': 'temos', '2p': 'tendes', '3p': 'têm'
            },
            'querer': {
                '1s': 'quero', '2s': 'queres', '3s': 'quer',
                '1p': 'queremos', '2p': 'quereis', '3p': 'querem'
            },
            'viver': {
                '1s': 'vivo', '2s': 'vives', '3s': 'vive',
                '1p': 'vivemos', '2p': 'viveis', '3p': 'vivem'
            },
            'sentir': {
                '1s': 'sinto', '2s': 'sentes', '3s': 'sente',
                '1p': 'sentimos', '2p': 'sentis', '3p': 'sentem'
            },
            'dançar': {
                '1s': 'danço', '2s': 'danças', '3s': 'dança',
                '1p': 'dançamos', '2p': 'dançais', '3p': 'dançam'
            },
            'cantar': {
                '1s': 'canto', '2s': 'cantas', '3s': 'canta',
                '1p': 'cantamos', '2p': 'cantais', '3p': 'cantam'
            },
            'sofrer': {
                '1s': 'sofro', '2s': 'sofres', '3s': 'sofre',
                '1p': 'sofremos', '2p': 'sofreis', '3p': 'sofrem'
            },
            'chorar': {
                '1s': 'choro', '2s': 'choras', '3s': 'chora',
                '1p': 'choramos', '2p': 'chorais', '3p': 'choram'
            },
            'sonhar': {
                '1s': 'sonho', '2s': 'sonhas', '3s': 'sonha',
                '1p': 'sonhamos', '2p': 'sonhais', '3p': 'sonham'
            }
        }

    def _build_sentence_templates(self) -> List[Dict]:
        """
        Build lyrical sentence templates.

        Templates use placeholders:
        - {pronoun} - subject pronoun
        - {verb} - conjugated verb
        - {noun} - noun/object
        - {adj} - adjective
        - {prep} - preposition
        - {connector} - connecting word
        """
        return [
            # Simple: "Eu amo você"
            {
                'pattern': '{pronoun} {verb} {noun}',
                'slots': ['pronoun', 'verb', 'noun'],
                'weight': 10
            },

            # With preposition: "Eu penso em você"
            {
                'pattern': '{pronoun} {verb} {prep} {noun}',
                'slots': ['pronoun', 'verb', 'prep', 'noun'],
                'weight': 8
            },

            # With adjective: "Você é linda"
            {
                'pattern': '{pronoun} {verb} {adj}',
                'slots': ['pronoun', 'verb', 'adj'],
                'weight': 7
            },

            # Compound: "Eu quero te amar"
            {
                'pattern': '{pronoun} {verb} te amar',
                'slots': ['pronoun', 'verb'],
                'weight': 6
            },

            # Negation: "Eu não quero sofrer"
            {
                'pattern': '{pronoun} não {verb}',
                'slots': ['pronoun', 'verb'],
                'weight': 5
            },

            # Question: "Onde você está?"
            {
                'pattern': 'Onde {pronoun} {verb}',
                'slots': ['pronoun', 'verb'],
                'weight': 4
            },

            # Existential: "Tem amor no ar"
            {
                'pattern': 'Tem {noun} no ar',
                'slots': ['noun'],
                'weight': 3
            },

            # Poetic: "A vida é bela"
            {
                'pattern': 'A {noun} é {adj}',
                'slots': ['noun', 'adj'],
                'weight': 5
            },

            # Connector: "Quando você sorri"
            {
                'pattern': 'Quando {pronoun} {verb}',
                'slots': ['pronoun', 'verb'],
                'weight': 4
            },

            # Complex: "Se você me ama, me diga"
            {
                'pattern': 'Se {pronoun} me {verb}',
                'slots': ['pronoun', 'verb'],
                'weight': 3
            }
        ]

    def generate_sentence(
        self,
        vocabulary: List[str],
        theme: Optional[str] = None,
        target_syllables: Optional[int] = None
    ) -> str:
        """
        Generate a grammatically correct sentence.

        Args:
            vocabulary: Available words to use
            theme: Optional theme for word selection
            target_syllables: Optional syllable count target

        Returns:
            Generated sentence
        """
        # Select template (weighted random)
        template = self._select_template()

        # Fill template slots
        sentence = self._fill_template(template, vocabulary)

        return sentence

    def _select_template(self) -> Dict:
        """Select sentence template with weighted probability."""
        total_weight = sum(t['weight'] for t in self.sentence_templates)
        rand = random.uniform(0, total_weight)

        current = 0
        for template in self.sentence_templates:
            current += template['weight']
            if rand <= current:
                return template

        return self.sentence_templates[0]

    def _fill_template(self, template: Dict, vocabulary: List[str]) -> str:
        """Fill template slots with appropriate words."""
        pattern = template['pattern']
        slots = template['slots']

        fills = {}

        for slot in slots:
            if slot == 'pronoun':
                fills[slot] = random.choice(list(self.pronouns.keys()))

            elif slot == 'verb':
                # Get conjugation for pronoun
                pronoun = fills.get('pronoun', 'ele')
                conjugation = self.pronouns[pronoun]['conjugation']

                # Pick random verb and conjugate
                verb_infinitive = random.choice(list(self.verbs.keys()))
                fills[slot] = self.verbs[verb_infinitive][conjugation]

            elif slot == 'prep':
                fills[slot] = random.choice(self.prepositions)

            elif slot == 'connector':
                fills[slot] = random.choice(self.connectors)

            elif slot in ['noun', 'adj']:
                # Use vocabulary words
                if vocabulary:
                    fills[slot] = random.choice(vocabulary)
                else:
                    fills[slot] = 'amor' if slot == 'noun' else 'belo'

        # Fill pattern
        try:
            sentence = pattern.format(**fills)
        except KeyError:
            # Fallback if template has unfilled slots
            sentence = pattern

        return sentence

    def generate_lines(
        self,
        count: int,
        vocabulary: List[str],
        theme: Optional[str] = None
    ) -> List[str]:
        """
        Generate multiple grammatically correct lines.

        Args:
            count: Number of lines
            vocabulary: Available vocabulary
            theme: Optional theme

        Returns:
            List of generated lines
        """
        lines = []

        for _ in range(count):
            sentence = self.generate_sentence(vocabulary, theme)
            lines.append(sentence)

        return lines

    def conjugate_verb(self, verb: str, pronoun: str) -> str:
        """
        Conjugate a verb for a pronoun.

        Args:
            verb: Verb infinitive
            pronoun: Subject pronoun

        Returns:
            Conjugated verb form
        """
        if verb not in self.verbs:
            return verb  # Return as-is if unknown

        conjugation = self.pronouns.get(pronoun, {}).get('conjugation', '3s')
        return self.verbs[verb].get(conjugation, verb)

    def add_verb(self, infinitive: str, conjugations: Dict):
        """
        Add a new verb to the engine.

        Args:
            infinitive: Verb infinitive form
            conjugations: Dict of conjugation → form
        """
        self.verbs[infinitive] = conjugations

    def add_template(self, pattern: str, slots: List[str], weight: int = 5):
        """
        Add a new sentence template.

        Args:
            pattern: Template pattern string
            slots: List of slot names
            weight: Selection weight
        """
        self.sentence_templates.append({
            'pattern': pattern,
            'slots': slots,
            'weight': weight
        })
