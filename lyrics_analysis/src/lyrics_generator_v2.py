"""
Lyrics Generator V2 - Enhanced with grammar, rhyme, and semantic coherence.

This version adds:
- Brazilian Portuguese grammar (proper sentence construction)
- Rhyme schemes (AABB, ABAB, etc.)
- Phrase patterns from corpus (natural-sounding lyrics)
- Semantic coherence (thematic consistency)

Transforms V1's word combinations into proper, rhyming, coherent Portuguese lyrics.
"""

import random
import logging
from pathlib import Path
from typing import List, Dict, Optional

from lyrics_generator import LyricsGenerator
from grammar_engine import GrammarEngine
from rhyme_engine import RhymeEngine
from phrase_patterns import PhrasePatternLearner
from semantic_coherence import SemanticCoherence

logger = logging.getLogger(__name__)


class LyricsGeneratorV2(LyricsGenerator):
    """V2 generator with grammar, rhyme, and coherence."""

    def __init__(
        self,
        analysis_dir: Path,
        corpus_data: Optional[List[Dict]] = None,
        enable_grammar: bool = True,
        enable_rhyme: bool = True,
        enable_patterns: bool = True,
        enable_coherence: bool = True
    ):
        """
        Initialize V2 lyrics generator.

        Args:
            analysis_dir: Path to analysis directory
            corpus_data: Optional corpus data
            enable_grammar: Enable grammar engine
            enable_rhyme: Enable rhyme engine
            enable_patterns: Enable phrase patterns
            enable_coherence: Enable semantic coherence
        """
        # Initialize base V1 generator
        super().__init__(analysis_dir, corpus_data)

        # Initialize V2 modules
        logger.info("Initializing V2 enhancement modules...")

        self.grammar_engine = GrammarEngine() if enable_grammar else None
        self.rhyme_engine = RhymeEngine() if enable_rhyme else None
        self.phrase_learner = PhrasePatternLearner(corpus_data) if enable_patterns else None
        self.semantic_coherence = SemanticCoherence() if enable_coherence else None

        self.v2_enabled = {
            'grammar': enable_grammar,
            'rhyme': enable_rhyme,
            'patterns': enable_patterns,
            'coherence': enable_coherence
        }

        logger.info(f"✓ V2 enhancements: {', '.join(k for k, v in self.v2_enabled.items() if v)}")

    def _generate_section_candidate(
        self,
        section: Dict,
        genre: str,
        theme: Optional[str],
        params: Dict
    ) -> Optional[str]:
        """
        Generate a single section candidate (V2 enhanced).

        Args:
            section: Section specification
            genre: Target genre
            theme: Optional theme
            params: Generation parameters

        Returns:
            Generated lyrics text
        """
        num_lines = section['lines']
        section_type = section['type']

        # Get thematic vocabulary
        if self.semantic_coherence and theme:
            vocabulary = self.semantic_coherence.get_thematic_vocabulary(theme, count=30)
        else:
            # Fallback to V1 vocabulary selection
            vocabulary = self.vocab_selector.select_words(
                genre=genre,
                theme=theme,
                innovation_level=params['vocabulary']['innovation_level'],
                count=30,
                avoid_cliches=params['vocabulary']['avoid_cliches']
            )

        if not vocabulary:
            return None

        # Generate lines based on V2 capabilities
        if self.v2_enabled['rhyme'] and section_type in ['verse', 'chorus']:
            # Generate rhyming lines
            lines = self._generate_rhyming_lines(
                line_count=num_lines,
                vocabulary=vocabulary,
                section_type=section_type,
                theme=theme
            )
        elif self.v2_enabled['grammar']:
            # Generate grammatically correct lines
            lines = self.grammar_engine.generate_lines(
                count=num_lines,
                vocabulary=vocabulary,
                theme=theme
            )
        elif self.v2_enabled['patterns'] and self.phrase_learner:
            # Generate using phrase patterns
            lines = [
                self.phrase_learner.generate_natural_line(vocabulary)
                for _ in range(num_lines)
            ]
        else:
            # Fallback to V1 generation
            lines = self.vocab_selector.generate_lines(
                count=num_lines,
                genre=genre,
                theme=theme,
                innovation_level=params['vocabulary']['innovation_level'],
                words_per_line=section['words_per_line'],
                avoid_cliches=params['vocabulary']['avoid_cliches']
            )

        # Apply semantic coherence
        if self.v2_enabled['coherence'] and theme:
            lines = self.semantic_coherence.ensure_verse_coherence(lines, theme)
            lines = self.semantic_coherence.add_transitions(lines, transition_density=0.2)

        # Handle chorus repetition
        if section_type == 'chorus' and params['repetition']['force_chorus']:
            # Keep lines coherent for repetition
            if len(lines) >= 4:
                # Repeat first 2 lines
                repeated = lines[:2] + lines[:2] + lines[2:]
                lines = repeated[:num_lines]

        return '\n'.join(lines)

    def _generate_rhyming_lines(
        self,
        line_count: int,
        vocabulary: List[str],
        section_type: str,
        theme: Optional[str]
    ) -> List[str]:
        """
        Generate lines with rhyme scheme.

        Args:
            line_count: Number of lines
            vocabulary: Available vocabulary
            section_type: Section type (verse, chorus, etc.)
            theme: Optional theme

        Returns:
            List of rhyming lines
        """
        # Select rhyme scheme based on section type
        if section_type == 'chorus':
            # Choruses often have tight rhymes
            scheme = 'AABB' if line_count == 4 else 'ABAB'
        else:
            # Verses can vary
            scheme = self.rhyme_engine.suggest_rhyme_scheme(line_count)

        # Build rhyming lines using grammar engine
        lines = self.rhyme_engine.build_rhyming_lines(
            line_count=line_count,
            vocabulary=vocabulary,
            scheme=scheme,
            grammar_engine=self.grammar_engine
        )

        return lines

    def generate(
        self,
        genre: str = "MPB",
        target_profile: Optional[Dict] = None,
        theme: Optional[str] = None,
        rhyme_scheme: Optional[str] = None,
        verbose: bool = False
    ) -> Dict:
        """
        Generate lyrics with V2 enhancements.

        Args:
            genre: Target genre
            target_profile: Optional 4D target profile
            theme: Optional theme
            rhyme_scheme: Optional rhyme scheme override
            verbose: Print generation progress

        Returns:
            Generation result with best lyrics and scores
        """
        if verbose:
            v2_features = ', '.join(k for k, v in self.v2_enabled.items() if v)
            print(f"\n🎵 V2 Generation (Features: {v2_features})")

        # Call parent generate method
        result = super().generate(
            genre=genre,
            target_profile=target_profile,
            theme=theme,
            verbose=verbose
        )

        # Add V2 metadata
        result['v2_enhancements'] = self.v2_enabled

        if self.rhyme_engine and result.get('lyrics'):
            # Analyze rhyme usage
            lines = result['lyrics'].split('\n')
            rhyme_stats = self.rhyme_engine.get_rhyme_statistics(lines)
            result['rhyme_statistics'] = rhyme_stats

            if verbose and rhyme_stats.get('has_rhymes'):
                print(f"\n🎼 Rhyme Analysis:")
                print(f"   Rhyme percentage: {rhyme_stats['rhyme_percentage']}%")

        if self.semantic_coherence and theme and result.get('lyrics'):
            # Measure coherence
            lines = result['lyrics'].split('\n')
            coherence = self.semantic_coherence.measure_coherence(lines, theme)
            result['semantic_coherence'] = coherence

            if verbose:
                print(f"   Semantic coherence: {coherence:.1f}%")

        return result

    def compare_v1_v2(
        self,
        genre: str = "MPB",
        target_profile: Optional[Dict] = None,
        theme: Optional[str] = None
    ) -> Dict:
        """
        Generate with both V1 and V2 for comparison.

        Args:
            genre: Target genre
            target_profile: Optional 4D target profile
            theme: Optional theme

        Returns:
            Comparison results
        """
        print("\n" + "="*70)
        print(" V1 vs V2 COMPARISON ".center(70, "="))
        print("="*70 + "\n")

        # Generate V1 (disable all V2 features temporarily)
        print("Generating V1 (baseline)...")
        v2_backup = self.v2_enabled.copy()

        # Temporarily disable V2
        for key in self.v2_enabled:
            self.v2_enabled[key] = False

        v1_result = super().generate(
            genre=genre,
            target_profile=target_profile,
            theme=theme,
            verbose=False
        )

        # Restore V2 settings
        self.v2_enabled = v2_backup

        # Generate V2
        print("Generating V2 (enhanced)...")
        v2_result = self.generate(
            genre=genre,
            target_profile=target_profile,
            theme=theme,
            verbose=False
        )

        # Compare
        comparison = {
            'v1': {
                'lyrics': v1_result['lyrics'],
                'quality': v1_result['final_score']['summary']['quality'],
                'effectiveness': v1_result['final_score']['summary']['effectiveness']
            },
            'v2': {
                'lyrics': v2_result['lyrics'],
                'quality': v2_result['final_score']['summary']['quality'],
                'effectiveness': v2_result['final_score']['summary']['effectiveness'],
                'rhyme_percentage': v2_result.get('rhyme_statistics', {}).get('rhyme_percentage', 0),
                'semantic_coherence': v2_result.get('semantic_coherence', 0)
            }
        }

        # Print comparison
        self._print_comparison(comparison)

        return comparison

    def _print_comparison(self, comparison: Dict):
        """Print V1 vs V2 comparison."""
        print("\n" + "="*70)
        print(" V1 BASELINE ".center(70, "="))
        print("="*70 + "\n")
        print(comparison['v1']['lyrics'][:500] + "...\n")
        print(f"Quality: {comparison['v1']['quality']:.1f}")
        print(f"Effectiveness: {comparison['v1']['effectiveness']:.1f}")

        print("\n" + "="*70)
        print(" V2 ENHANCED ".center(70, "="))
        print("="*70 + "\n")
        print(comparison['v2']['lyrics'][:500] + "...\n")
        print(f"Quality: {comparison['v2']['quality']:.1f}")
        print(f"Effectiveness: {comparison['v2']['effectiveness']:.1f}")
        print(f"Rhyme: {comparison['v2']['rhyme_percentage']:.1f}%")
        print(f"Coherence: {comparison['v2']['semantic_coherence']:.1f}%")

        print("\n" + "="*70)
        print(" IMPROVEMENT ".center(70, "="))
        print("="*70 + "\n")

        quality_delta = comparison['v2']['quality'] - comparison['v1']['quality']
        effectiveness_delta = comparison['v2']['effectiveness'] - comparison['v1']['effectiveness']

        print(f"Quality: {'+' if quality_delta >= 0 else ''}{quality_delta:.1f}")
        print(f"Effectiveness: {'+' if effectiveness_delta >= 0 else ''}{effectiveness_delta:.1f}")
        print(f"Rhyme added: {comparison['v2']['rhyme_percentage']:.1f}%")
        print(f"Coherence added: {comparison['v2']['semantic_coherence']:.1f}%")

        print("\n" + "="*70 + "\n")
