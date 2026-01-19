"""
Lyrics Generator - Quality-aware Brazilian lyrics generation.

This is the main orchestrator that brings together all Phase 4 modules:
- Creates song structure from templates (StructureGenerator)
- Selects vocabulary with cliché avoidance (VocabularySelector)
- Scores candidates for quality (QualityScorer)
- Iteratively refines toward 4D targets (InnovationController)

The key innovation: Generate MULTIPLE candidates, score them, pick the best.
This is not blind generation - it's QUALITY-AWARE generation.
"""

import random
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from structure_generator import StructureGenerator
from vocabulary_selector import VocabularySelector
from quality_scorer import QualityScorer
from innovation_controller import InnovationController

logger = logging.getLogger(__name__)


class LyricsGenerator:
    """Quality-aware lyrics generator with 4D control."""

    def __init__(
        self,
        analysis_dir: Path,
        corpus_data: Optional[List[Dict]] = None
    ):
        """
        Initialize lyrics generator.

        Args:
            analysis_dir: Path to analysis directory (Phase 2A/2B results)
            corpus_data: Optional corpus data for quality scoring
        """
        self.analysis_dir = Path(analysis_dir)

        # Initialize all modules
        logger.info("Initializing lyrics generator modules...")

        self.structure_gen = StructureGenerator(analysis_dir)
        self.vocab_selector = VocabularySelector(analysis_dir)
        self.quality_scorer = QualityScorer(corpus_data)
        self.controller = InnovationController()

        logger.info("✓ Lyrics generator ready")

    def generate(
        self,
        genre: str = "MPB",
        target_profile: Optional[Dict] = None,
        theme: Optional[str] = None,
        verbose: bool = False
    ) -> Dict:
        """
        Generate lyrics with quality-aware iterative refinement.

        Args:
            genre: Target genre
            target_profile: Optional 4D target profile
            theme: Optional theme
            verbose: Print generation progress

        Returns:
            Generation result with best lyrics and scores
        """
        if verbose:
            print("\n🎵 Starting quality-aware lyrics generation...")

        # Use default profile if not provided
        if target_profile is None:
            target_profile = self.controller.default_profile

        if verbose:
            print(f"\n📊 Target Profile:")
            self.controller.print_profile(target_profile)

        # Convert profile to generation parameters
        params = self.controller.profile_to_generation_params(target_profile, genre)

        if verbose:
            print(f"\n🏗️  Generating structure for {genre}...")

        # Generate song structure
        structure = self.structure_gen.generate_structure(
            genre=genre,
            innovation_level=params['structure']['innovation_level'],
            effectiveness_target=params['structure']['effectiveness_target']
        )

        if verbose:
            print(f"   Structure: {structure['total_lines']} lines, "
                  f"{structure['total_paragraphs']} sections, "
                  f"{'with' if structure['has_chorus'] else 'without'} chorus")

        # Generate lyrics section by section
        if verbose:
            print(f"\n✍️  Generating lyrics sections...")

        sections_lyrics = []
        section_scores = []

        for i, section in enumerate(structure['sections']):
            if verbose:
                print(f"   Section {i+1}/{len(structure['sections'])}: "
                      f"{section['type']} ({section['lines']} lines)")

            # Generate this section
            section_lyrics, score = self._generate_section(
                section=section,
                genre=genre,
                theme=theme,
                params=params,
                target_profile=target_profile,
                verbose=verbose
            )

            sections_lyrics.append({
                'type': section['type'],
                'lyrics': section_lyrics,
                'score': score
            })

            section_scores.append(score)

        # Assemble full lyrics
        full_lyrics = self._assemble_lyrics(sections_lyrics, structure)

        # Final quality check
        if verbose:
            print(f"\n📈 Final quality scoring...")

        final_score = self.quality_scorer.score_candidate(
            lyrics=full_lyrics,
            genre=genre,
            target_profile=target_profile
        )

        result = {
            'lyrics': full_lyrics,
            'structure': structure,
            'sections': sections_lyrics,
            'final_score': final_score,
            'target_profile': target_profile,
            'genre': genre,
            'theme': theme
        }

        if verbose:
            print(f"\n✅ Generation complete!")
            self._print_result_summary(result)

        return result

    def _generate_section(
        self,
        section: Dict,
        genre: str,
        theme: Optional[str],
        params: Dict,
        target_profile: Dict,
        verbose: bool = False
    ) -> Tuple[str, Dict]:
        """
        Generate a single section (verse/chorus/bridge).

        Args:
            section: Section specification
            genre: Target genre
            theme: Optional theme
            params: Generation parameters
            target_profile: 4D target profile
            verbose: Print progress

        Returns:
            (section_lyrics, score)
        """
        num_candidates = params['strategy']['candidates_per_section']

        # Generate multiple candidates
        candidates = []

        for _ in range(num_candidates):
            candidate = self._generate_section_candidate(
                section=section,
                genre=genre,
                theme=theme,
                params=params
            )

            if candidate:
                candidates.append(candidate)

        if not candidates:
            # Fallback: generate simple placeholder
            lines = [f"Line {i+1}" for i in range(section['lines'])]
            return '\n'.join(lines), {}

        # Score all candidates
        if verbose:
            print(f"      Generated {len(candidates)} candidates, scoring...")

        scored_candidates = []

        for candidate in candidates:
            try:
                score = self.quality_scorer.score_candidate(
                    lyrics=candidate,
                    genre=genre,
                    target_profile=target_profile
                )

                scored_candidates.append({
                    'lyrics': candidate,
                    'score': score
                })

            except Exception as e:
                logger.debug(f"Failed to score candidate: {e}")

        if not scored_candidates:
            # No scoreable candidates, return first
            return candidates[0], {}

        # Pick best candidate (highest match to target)
        if target_profile:
            best = max(
                scored_candidates,
                key=lambda x: x['score'].get('match_to_target', {}).get('match_score', 0)
            )
        else:
            best = max(
                scored_candidates,
                key=lambda x: x['score']['summary']['quality']
            )

        if verbose:
            quality = best['score']['summary']['quality']
            print(f"      Selected best (quality: {quality:.1f})")

        return best['lyrics'], best['score']

    def _generate_section_candidate(
        self,
        section: Dict,
        genre: str,
        theme: Optional[str],
        params: Dict
    ) -> Optional[str]:
        """
        Generate a single section candidate.

        Args:
            section: Section specification
            genre: Target genre
            theme: Optional theme
            params: Generation parameters

        Returns:
            Generated lyrics text
        """
        num_lines = section['lines']
        words_per_line = section['words_per_line']

        # Generate lines
        lines = self.vocab_selector.generate_lines(
            count=num_lines,
            genre=genre,
            theme=theme,
            innovation_level=params['vocabulary']['innovation_level'],
            words_per_line=words_per_line,
            avoid_cliches=params['vocabulary']['avoid_cliches']
        )

        if not lines:
            return None

        # Handle chorus repetition
        if section['type'] == 'chorus' and params['repetition']['force_chorus']:
            # Repeat some lines for chorus effect
            if len(lines) >= 4:
                # Repeat middle lines
                repeated = lines[:2] + lines[:2] + lines[2:]
                lines = repeated[:num_lines]

        return '\n'.join(lines)

    def _assemble_lyrics(
        self,
        sections_lyrics: List[Dict],
        structure: Dict
    ) -> str:
        """
        Assemble full lyrics from sections.

        Args:
            sections_lyrics: List of section dictionaries
            structure: Song structure

        Returns:
            Complete lyrics text
        """
        assembled = []

        # Track chorus for reuse
        chorus_lyrics = None

        for section_data in sections_lyrics:
            section_type = section_data['type']
            lyrics = section_data['lyrics']

            # Add section marker (optional, can be removed for cleaner output)
            # assembled.append(f"[{section_type.upper()}]")

            # Reuse chorus if we've seen it before
            if section_type == 'chorus':
                if chorus_lyrics is None:
                    chorus_lyrics = lyrics
                    assembled.append(lyrics)
                else:
                    # Reuse first chorus
                    assembled.append(chorus_lyrics)
            else:
                assembled.append(lyrics)

            # Blank line between sections
            assembled.append("")

        return '\n'.join(assembled).strip()

    def _print_result_summary(self, result: Dict):
        """Print formatted result summary."""
        print("\n" + "="*70)
        print(" GENERATED LYRICS ".center(70, "="))
        print("="*70 + "\n")

        print(result['lyrics'])

        print("\n" + "="*70)

        score = result['final_score']
        summary = score['summary']

        print(f"\n📊 QUALITY SCORES:")
        print(f"  Innovation:    {summary['innovation']:6.1f} / 100")
        print(f"  Authenticity:  {summary['authenticity']:6.1f} / 100")
        print(f"  Risk:          {summary['risk']:6.1f} / 100")
        print(f"  Effectiveness: {summary['effectiveness']:6.1f} / 100")
        print(f"  Overall:       {summary['quality']:6.1f} / 100")

        if score.get('match_to_target'):
            match = score['match_to_target']
            print(f"\n🎯 TARGET MATCH: {match['match_score']:.1f} / 100 ({match['assessment']})")

        print(f"\n🏗️  STRUCTURE:")
        struct = result['structure']
        print(f"  Genre:      {struct['genre']}")
        print(f"  Lines:      {struct['total_lines']}")
        print(f"  Sections:   {struct['total_paragraphs']}")
        print(f"  Has Chorus: {'Yes' if struct['has_chorus'] else 'No'}")

        print("\n" + "="*70 + "\n")

    def generate_batch(
        self,
        count: int,
        genre: str = "MPB",
        target_profile: Optional[Dict] = None,
        theme: Optional[str] = None,
        verbose: bool = False
    ) -> List[Dict]:
        """
        Generate multiple lyrics.

        Args:
            count: Number of lyrics to generate
            genre: Target genre
            target_profile: Optional 4D target profile
            theme: Optional theme
            verbose: Print progress

        Returns:
            List of generation results
        """
        results = []

        for i in range(count):
            if verbose:
                print(f"\n{'='*70}")
                print(f" GENERATING LYRICS {i+1}/{count} ".center(70, "="))
                print(f"{'='*70}\n")

            result = self.generate(
                genre=genre,
                target_profile=target_profile,
                theme=theme,
                verbose=verbose
            )

            results.append(result)

        return results

    def generate_with_profile_name(
        self,
        profile_name: str,
        genre: str = "MPB",
        theme: Optional[str] = None,
        verbose: bool = False
    ) -> Dict:
        """
        Generate lyrics using a named profile.

        Args:
            profile_name: Profile name (balanced, safe, experimental, etc.)
            genre: Target genre
            theme: Optional theme
            verbose: Print progress

        Returns:
            Generation result
        """
        profiles = self.controller.suggest_profiles()

        if profile_name not in profiles:
            logger.warning(f"Unknown profile '{profile_name}', using 'balanced'")
            profile_name = 'balanced'

        profile_info = profiles[profile_name]
        target_profile = profile_info['profile']

        if verbose:
            print(f"\nUsing profile: {profile_info['name']}")
            print(f"Description: {profile_info['description']}")

        return self.generate(
            genre=genre,
            target_profile=target_profile,
            theme=theme,
            verbose=verbose
        )

    def list_available_genres(self) -> List[str]:
        """Get list of available genres."""
        return self.structure_gen.list_available_genres()

    def list_available_themes(self) -> List[str]:
        """Get list of available themes."""
        return self.vocab_selector.list_available_themes()

    def list_available_profiles(self) -> Dict[str, Dict]:
        """Get available generation profiles."""
        return self.controller.suggest_profiles()
