"""
Quality Scorer - Evaluates generated lyrics quality.

This module wraps Phase 2B analyzers to score generated lyrics:
- Uses EffectivenessAnalyzer for quality scoring
- Uses InnovationMetrics for 4D scoring
- Provides simple API for evaluating candidates
- Compares generated lyrics to corpus norms

This is the key module that makes generation QUALITY-AWARE.
"""

import sys
from pathlib import Path
from typing import Dict, Optional, List
import logging

# Import Phase 2B analyzers
from effectiveness_analyzer import EffectivenessAnalyzer
from innovation_metrics import InnovationMetrics

logger = logging.getLogger(__name__)


class QualityScorer:
    """Scores generated lyrics for quality and innovation."""

    def __init__(self, corpus_data: Optional[List[Dict]] = None):
        """
        Initialize quality scorer.

        Args:
            corpus_data: Optional corpus data for scoring context
        """
        # Initialize Phase 2B analyzers
        self.effectiveness_analyzer = EffectivenessAnalyzer(corpus_data or [])
        self.innovation_metrics = InnovationMetrics(corpus_data or [])

        # Track if analyzers are initialized
        self.has_corpus = corpus_data is not None and len(corpus_data) > 0

        if self.has_corpus:
            logger.info(f"✓ Quality scorer initialized with {len(corpus_data)} reference songs")
        else:
            logger.warning("Quality scorer initialized without corpus (limited functionality)")

    def score_effectiveness(self, lyrics: str) -> Dict:
        """
        Score lyrics effectiveness.

        Args:
            lyrics: Lyrics text to score

        Returns:
            Effectiveness scores dictionary
        """
        # EffectivenessAnalyzer expects a song dict
        song_dict = {'lyrics': lyrics}
        result = self.effectiveness_analyzer.analyze_song_effectiveness(song_dict)

        # Convert to our expected format
        return {
            'overall_score': result['composite_effectiveness'],
            'dimensions': {
                'coherence': result['structural_coherence'],
                'consistency': result['thematic_consistency'],
                'resonance': result['emotional_resonance'],
                'memorability': result['memorability']
            }
        }

    def score_4d(
        self,
        lyrics: str,
        genre: str = "MPB",
        innovation_score: Optional[Dict] = None,
        effectiveness_score: Optional[Dict] = None
    ) -> Dict:
        """
        Calculate 4D scores (Innovation, Authenticity, Risk, Effectiveness).

        Args:
            lyrics: Lyrics text
            genre: Genre for context
            innovation_score: Pre-calculated innovation score dict (optional)
            effectiveness_score: Pre-calculated effectiveness score dict (optional)

        Returns:
            4D scores dictionary
        """
        # Get effectiveness scores if not provided
        if effectiveness_score is None:
            effectiveness_result = self.score_effectiveness(lyrics)
            # Convert to expected format
            effectiveness_score = {
                'composite_effectiveness': effectiveness_result['overall_score']
            }

        # For innovation, pass None and let InnovationMetrics compute defaults
        # (since we don't have outlier detection in generation context)

        # Use InnovationMetrics to calculate 4D scores
        scores_4d = self.innovation_metrics.score_song_4d(
            song_or_lyrics=lyrics,
            innovation_score=None,  # Let it compute defaults
            effectiveness_score=effectiveness_score
        )

        return scores_4d

    def _estimate_innovation(self, lyrics: str) -> float:
        """
        Estimate innovation score for lyrics (simplified without full outlier analysis).

        Args:
            lyrics: Lyrics text

        Returns:
            Estimated innovation score (0-100)
        """
        words = lyrics.split()
        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

        # Simple heuristics for innovation
        unique_ratio = len(set(words)) / len(words) if words else 0
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        line_variety = len(set(lines)) / len(lines) if lines else 0

        # Combine heuristics
        innovation = (
            unique_ratio * 40 +  # Vocabulary diversity
            min(avg_word_length / 8, 1) * 30 +  # Word complexity
            line_variety * 30  # Structural variety
        )

        return min(100, innovation)

    def score_candidate(
        self,
        lyrics: str,
        genre: str = "MPB",
        target_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Score a generated lyrics candidate.

        Args:
            lyrics: Generated lyrics
            genre: Target genre
            target_profile: Optional target 4D profile to compare against

        Returns:
            Complete scoring report
        """
        # Get effectiveness scores
        effectiveness = self.score_effectiveness(lyrics)

        # Get 4D scores (pass the full effectiveness dict for proper formatting)
        effectiveness_dict = {
            'composite_effectiveness': effectiveness['overall_score']
        }

        scores_4d = self.score_4d(
            lyrics=lyrics,
            genre=genre,
            effectiveness_score=effectiveness_dict
        )

        # Calculate match to target if provided
        match_score = None
        if target_profile:
            match_score = self._calculate_profile_match(scores_4d, target_profile)

        report = {
            'effectiveness': effectiveness,
            'scores_4d': scores_4d,
            'match_to_target': match_score,
            'summary': {
                'innovation': scores_4d['innovation'],
                'authenticity': scores_4d['authenticity'],
                'risk': scores_4d['risk'],
                'effectiveness': scores_4d['effectiveness'],
                'quality': scores_4d['quality']
            }
        }

        return report

    def _calculate_profile_match(
        self,
        actual_scores: Dict,
        target_profile: Dict
    ) -> Dict:
        """
        Calculate how well actual scores match target profile.

        Args:
            actual_scores: Actual 4D scores
            target_profile: Target 4D scores

        Returns:
            Match analysis
        """
        dimensions = ['innovation', 'authenticity', 'risk', 'effectiveness']

        deviations = {}
        total_deviation = 0

        for dim in dimensions:
            if dim in target_profile and dim in actual_scores:
                target = target_profile[dim]
                actual = actual_scores[dim]
                deviation = abs(target - actual)

                deviations[dim] = {
                    'target': target,
                    'actual': actual,
                    'deviation': deviation
                }

                total_deviation += deviation

        # Calculate match score (0-100, where 100 is perfect match)
        avg_deviation = total_deviation / len(dimensions) if dimensions else 0
        match_score = max(0, 100 - avg_deviation)

        return {
            'match_score': match_score,
            'deviations': deviations,
            'assessment': self._assess_match(match_score)
        }

    def _assess_match(self, match_score: float) -> str:
        """Assess quality of match to target."""
        if match_score >= 90:
            return "Excellent match"
        elif match_score >= 75:
            return "Good match"
        elif match_score >= 60:
            return "Acceptable match"
        elif match_score >= 40:
            return "Poor match"
        else:
            return "Very poor match"

    def compare_candidates(
        self,
        candidates: List[str],
        genre: str = "MPB",
        target_profile: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Score multiple candidates and rank them.

        Args:
            candidates: List of generated lyrics
            genre: Target genre
            target_profile: Optional target profile

        Returns:
            List of scored candidates, sorted by quality
        """
        scored = []

        for i, lyrics in enumerate(candidates):
            try:
                score = self.score_candidate(
                    lyrics=lyrics,
                    genre=genre,
                    target_profile=target_profile
                )

                score['candidate_id'] = i
                score['lyrics'] = lyrics

                scored.append(score)

            except Exception as e:
                logger.warning(f"Failed to score candidate {i}: {e}")

        # Sort by match score if target provided, else by quality
        if target_profile:
            scored.sort(
                key=lambda x: x['match_to_target']['match_score'] if x['match_to_target'] else 0,
                reverse=True
            )
        else:
            scored.sort(
                key=lambda x: x['summary']['quality'],
                reverse=True
            )

        return scored

    def get_best_candidate(
        self,
        candidates: List[str],
        genre: str = "MPB",
        target_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Get the best candidate from a list.

        Args:
            candidates: List of generated lyrics
            genre: Target genre
            target_profile: Optional target profile

        Returns:
            Best candidate with scores
        """
        if not candidates:
            return None

        scored = self.compare_candidates(
            candidates=candidates,
            genre=genre,
            target_profile=target_profile
        )

        return scored[0] if scored else None

    def print_score_report(self, score: Dict):
        """
        Print formatted score report.

        Args:
            score: Score dictionary from score_candidate()
        """
        print("\n" + "="*60)
        print(" QUALITY SCORE REPORT ".center(60, "="))
        print("="*60 + "\n")

        summary = score['summary']
        print(f"📊 4D SCORES:")
        print(f"  Innovation:    {summary['innovation']:6.1f} / 100")
        print(f"  Authenticity:  {summary['authenticity']:6.1f} / 100")
        print(f"  Risk:          {summary['risk']:6.1f} / 100")
        print(f"  Effectiveness: {summary['effectiveness']:6.1f} / 100")
        print(f"  Quality:       {summary['quality']:6.1f} / 100")

        if score.get('match_to_target'):
            match = score['match_to_target']
            print(f"\n🎯 TARGET MATCH:")
            print(f"  Match Score: {match['match_score']:.1f} / 100")
            print(f"  Assessment:  {match['assessment']}")

            print(f"\n  Deviations:")
            for dim, dev in match['deviations'].items():
                print(f"    {dim:15s}: target={dev['target']:5.1f}, "
                      f"actual={dev['actual']:5.1f}, "
                      f"deviation={dev['deviation']:5.1f}")

        effectiveness = score['effectiveness']
        print(f"\n✅ EFFECTIVENESS BREAKDOWN:")
        print(f"  Coherence:     {effectiveness['dimensions']['coherence']:6.1f} / 100")
        print(f"  Consistency:   {effectiveness['dimensions']['consistency']:6.1f} / 100")
        print(f"  Resonance:     {effectiveness['dimensions']['resonance']:6.1f} / 100")
        print(f"  Memorability:  {effectiveness['dimensions']['memorability']:6.1f} / 100")

        print("\n" + "="*60 + "\n")
