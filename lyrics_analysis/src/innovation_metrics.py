"""
Innovation Metrics - The 4D Scoring System.

This is the crown jewel that enables INTELLIGENT generation.

Combines outlier detection + effectiveness analysis into a unified
scoring system that can measure ANY song (corpus or generated) on:

1. Innovation (0-100): How novel/unique?
2. Authenticity (0-100): How genuinely Brazilian?
3. Risk (0-100): How experimental?
4. Effectiveness (0-100): Does it work?

The Sweet Spot: High innovation + High effectiveness
"""

import re
from collections import Counter
from typing import Dict, List, Tuple, Optional
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class InnovationMetrics:
    """4D scoring system for lyrics innovation and quality."""

    def __init__(self, corpus_data: List[Dict]):
        """
        Initialize innovation metrics system.

        Args:
            corpus_data: List of song dictionaries
        """
        self.corpus = corpus_data

        # Brazilian Portuguese markers for authenticity
        self.brazilian_markers = {
            'regional_words': [
                'saudade', 'caipira', 'sertão', 'cabaré', 'forró',
                'pagode', 'sambista', 'macumba', 'umbanda', 'cachaça'
            ],
            'colloquial_portuguese': [
                'tô', 'tá', 'cê', 'pra', 'né', 'oxe', 'uai',
                'bora', 'valeu', 'beleza', 'mano', 'vei'
            ],
            'brazilian_places': [
                'brasil', 'rio', 'são paulo', 'bahia', 'nordeste',
                'favela', 'morro', 'praia', 'amazônia'
            ],
            'cultural_references': [
                'carnaval', 'futebol', 'capoeira', 'churrasco',
                'feijoada', 'cafuné', 'muleque'
            ]
        }

    def score_song_4d(self,
                     song_or_lyrics: Dict | str,
                     innovation_score: Optional[Dict] = None,
                     effectiveness_score: Optional[Dict] = None) -> Dict:
        """
        Score a song on all 4 dimensions.

        Args:
            song_or_lyrics: Either song dict or lyrics string
            innovation_score: Pre-computed innovation scores (optional)
            effectiveness_score: Pre-computed effectiveness scores (optional)

        Returns:
            Dictionary with 4D scores
        """
        # Handle both dict and string inputs
        if isinstance(song_or_lyrics, dict):
            lyrics = song_or_lyrics.get('lyrics', '')
            genre = song_or_lyrics.get('genre', 'Unknown')
        else:
            lyrics = song_or_lyrics
            genre = 'Unknown'

        # Calculate each dimension
        innovation = innovation_score.get('composite_innovation', 50) if innovation_score else 50
        authenticity = self._authenticity_score(lyrics, genre)
        risk = self._risk_score(innovation_score) if innovation_score else 50
        effectiveness = effectiveness_score.get('composite_effectiveness', 50) if effectiveness_score else 50

        # Calculate composite "quality" score
        # Sweet spot = high innovation + high effectiveness
        quality = (innovation + effectiveness) / 2

        return {
            'innovation': round(innovation, 1),
            'authenticity': round(authenticity, 1),
            'risk': round(risk, 1),
            'effectiveness': round(effectiveness, 1),
            'quality': round(quality, 1),
            'assessment': self._assess_scores(innovation, authenticity, risk, effectiveness)
        }

    def _authenticity_score(self, lyrics: str, genre: str) -> float:
        """
        Score how authentically Brazilian the lyrics are.

        Args:
            lyrics: Song lyrics
            genre: Genre (affects expectations)

        Returns:
            Score 0-100
        """
        lyrics_lower = lyrics.lower()
        words = lyrics_lower.split()
        word_count = len(words)

        if word_count == 0:
            return 0

        score = 50  # Start neutral

        # 1. Brazilian Portuguese markers (max +30 points)
        marker_count = 0

        for category, markers in self.brazilian_markers.items():
            for marker in markers:
                if marker in lyrics_lower:
                    marker_count += 1

        # Each marker adds points, but diminishing returns
        marker_bonus = min(marker_count * 5, 30)
        score += marker_bonus

        # 2. Portuguese grammatical structures (max +20 points)
        portuguese_structures = [
            r'\bestou\b', r'\bestá\b', r'\bestamos\b',  # Estar conjugations
            r'\bvocê\b', r'\bvoce\b',  # Você (Brazilian, not tu)
            r'\ba gente\b',  # "A gente" instead of "nós"
            r'\bpra\b', r'\bpro\b'  # Contractions
        ]

        structure_count = sum(
            1 for pattern in portuguese_structures
            if re.search(pattern, lyrics_lower)
        )

        score += min(structure_count * 4, 20)

        # 3. NOT using English (penalty for too much English)
        english_words = ['the', 'and', 'yeah', 'baby', 'love', 'money', 'shit', 'fuck']
        english_count = sum(1 for word in english_words if word in words)

        if english_count > 10:
            score -= min((english_count - 10) * 2, 20)

        # 4. Genre-specific authenticity
        if genre == 'MPB':
            # MPB should be more literary/poetic
            literary_words = ['alma', 'sonho', 'lua', 'mar', 'terra', 'canta']
            if sum(1 for w in literary_words if w in lyrics_lower) >= 2:
                score += 10

        elif genre == 'Trap':
            # Trap can be bilingual (not a penalty)
            if 5 <= english_count <= 15:
                score += 5  # Appropriate bilingual mixing

        # Cap at 0-100
        return max(min(score, 100), 0)

    def _risk_score(self, innovation_score: Dict) -> float:
        """
        Calculate risk level based on innovation components.
        Higher deviation = higher risk.

        Args:
            innovation_score: Innovation scores dict

        Returns:
            Score 0-100
        """
        if not innovation_score:
            return 50

        # Risk is driven by the maximum deviation in any dimension
        dimensions = [
            innovation_score.get('vocabulary_uniqueness', 0),
            innovation_score.get('structural_deviation', 0),
            innovation_score.get('length_deviation', 0),
            innovation_score.get('repetition_deviation', 0)
        ]

        # Risk = average of top 2 highest dimensions
        # (If you deviate a lot in multiple ways, very risky)
        top_2 = sorted(dimensions, reverse=True)[:2]
        risk = sum(top_2) / 2

        return round(risk, 1)

    def _assess_scores(self, innovation: float, authenticity: float,
                      risk: float, effectiveness: float) -> str:
        """
        Provide human-readable assessment based on scores.

        Args:
            innovation: Innovation score
            authenticity: Authenticity score
            risk: Risk score
            effectiveness: Effectiveness score

        Returns:
            Assessment string
        """
        # The Sweet Spot: High innovation + High effectiveness
        if innovation >= 60 and effectiveness >= 60:
            if authenticity >= 70:
                return "SWEET SPOT: Innovative, effective, and authentic"
            else:
                return "Innovative and effective, but may lack Brazilian authenticity"

        # High innovation but low effectiveness = Experimental/Risky
        elif innovation >= 60 and effectiveness < 60:
            return "Experimental: Novel but may not work well"

        # High effectiveness but low innovation = Safe/Formulaic
        elif innovation < 40 and effectiveness >= 60:
            return "Safe and effective: Formulaic but works"

        # Low on both = Problems
        elif innovation < 40 and effectiveness < 40:
            return "Needs improvement: Neither innovative nor particularly effective"

        # Balanced
        else:
            return "Balanced: Moderate innovation and effectiveness"

    def identify_sweet_spots(self,
                           scored_songs: List[Tuple[Dict, Dict]],
                           min_innovation: float = 60,
                           min_effectiveness: float = 60) -> List[Tuple[Dict, Dict]]:
        """
        Identify songs in the "sweet spot" - innovative AND effective.

        Args:
            scored_songs: List of (song, full_4d_scores) tuples
            min_innovation: Minimum innovation threshold
            min_effectiveness: Minimum effectiveness threshold

        Returns:
            List of sweet spot songs
        """
        sweet_spots = []

        for song, scores in scored_songs:
            if (scores['innovation'] >= min_innovation and
                scores['effectiveness'] >= min_effectiveness):
                sweet_spots.append((song, scores))

        # Sort by quality (innovation + effectiveness)
        sweet_spots.sort(key=lambda x: x[1]['quality'], reverse=True)

        return sweet_spots

    def categorize_by_quadrant(self, scored_songs: List[Tuple[Dict, Dict]]) -> Dict:
        """
        Categorize songs into 4 quadrants based on innovation vs effectiveness.

        Quadrants:
        - High Innovation, High Effectiveness: THE SWEET SPOT
        - High Innovation, Low Effectiveness: EXPERIMENTAL
        - Low Innovation, High Effectiveness: SAFE/FORMULAIC
        - Low Innovation, Low Effectiveness: NEEDS IMPROVEMENT

        Args:
            scored_songs: List of (song, full_4d_scores) tuples

        Returns:
            Dictionary with songs categorized by quadrant
        """
        quadrants = {
            'sweet_spot': [],       # High/High
            'experimental': [],     # High/Low
            'safe_formulaic': [],   # Low/High
            'needs_improvement': []  # Low/Low
        }

        for song, scores in scored_songs:
            innovation = scores['innovation']
            effectiveness = scores['effectiveness']

            if innovation >= 50 and effectiveness >= 50:
                quadrants['sweet_spot'].append((song, scores))
            elif innovation >= 50 and effectiveness < 50:
                quadrants['experimental'].append((song, scores))
            elif innovation < 50 and effectiveness >= 50:
                quadrants['safe_formulaic'].append((song, scores))
            else:
                quadrants['needs_improvement'].append((song, scores))

        # Sort each quadrant
        for quadrant in quadrants.values():
            quadrant.sort(key=lambda x: x[1]['quality'], reverse=True)

        return quadrants

    def generate_report(self, scored_songs: List[Tuple[Dict, Dict]]) -> Dict:
        """
        Generate comprehensive 4D metrics report.

        Args:
            scored_songs: List of (song, full_4d_scores) tuples

        Returns:
            Report dictionary
        """
        # Calculate averages
        avg_innovation = sum(s[1]['innovation'] for s in scored_songs) / len(scored_songs)
        avg_authenticity = sum(s[1]['authenticity'] for s in scored_songs) / len(scored_songs)
        avg_risk = sum(s[1]['risk'] for s in scored_songs) / len(scored_songs)
        avg_effectiveness = sum(s[1]['effectiveness'] for s in scored_songs) / len(scored_songs)
        avg_quality = sum(s[1]['quality'] for s in scored_songs) / len(scored_songs)

        # Categorize by quadrant
        quadrants = self.categorize_by_quadrant(scored_songs)

        # Sweet spot analysis
        sweet_spots = quadrants['sweet_spot']

        return {
            'overview': {
                'total_songs': len(scored_songs),
                'average_scores': {
                    'innovation': round(avg_innovation, 2),
                    'authenticity': round(avg_authenticity, 2),
                    'risk': round(avg_risk, 2),
                    'effectiveness': round(avg_effectiveness, 2),
                    'quality': round(avg_quality, 2)
                }
            },
            'quadrant_distribution': {
                'sweet_spot': len(quadrants['sweet_spot']),
                'experimental': len(quadrants['experimental']),
                'safe_formulaic': len(quadrants['safe_formulaic']),
                'needs_improvement': len(quadrants['needs_improvement'])
            },
            'sweet_spot_songs': [
                {
                    'title': song['title'],
                    'artist': song['artist'],
                    'genre': song['genre'],
                    'scores': scores
                }
                for song, scores in sweet_spots[:50]
            ],
            'methodology': {
                'innovation': 'Vocabulary uniqueness + structural deviation + length + repetition patterns',
                'authenticity': 'Brazilian Portuguese markers + cultural references + language structures',
                'risk': 'Degree of experimental deviation from norms',
                'effectiveness': 'Coherence + consistency + resonance + memorability',
                'quality': 'Composite of innovation + effectiveness (the sweet spot measure)'
            }
        }

    def save_report(self, report: Dict, output_path: Path):
        """Save 4D metrics report to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved 4D metrics report to {output_path}")

    def print_summary(self, scored_songs: List[Tuple[Dict, Dict]], top_n: int = 20):
        """Print formatted summary of 4D scoring."""
        print("\n" + "="*80)
        print(" 4D INNOVATION METRICS - SWEET SPOT ANALYSIS ".center(80, "="))
        print("="*80 + "\n")

        quadrants = self.categorize_by_quadrant(scored_songs)

        print("📊 QUADRANT DISTRIBUTION")
        print("-" * 80)
        total = len(scored_songs)
        print(f"✨ Sweet Spot (High Inn. + High Eff.):  {len(quadrants['sweet_spot']):4d} ({len(quadrants['sweet_spot'])/total*100:5.1f}%)")
        print(f"🔬 Experimental (High Inn. + Low Eff.): {len(quadrants['experimental']):4d} ({len(quadrants['experimental'])/total*100:5.1f}%)")
        print(f"🛡️  Safe/Formulaic (Low Inn. + High Eff.):{len(quadrants['safe_formulaic']):4d} ({len(quadrants['safe_formulaic'])/total*100:5.1f}%)")
        print(f"⚠️  Needs Work (Low Inn. + Low Eff.):   {len(quadrants['needs_improvement']):4d} ({len(quadrants['needs_improvement'])/total*100:5.1f}%)")

        print(f"\n✨ TOP {top_n} SWEET SPOT SONGS (Innovative + Effective)")
        print("-" * 80)
        print(f"{'#':>3} {'Inn':>4} {'Eff':>4} {'Qlty':>4} {'Title':35s} {'Artist':20s}")
        print("-" * 80)

        for i, (song, scores) in enumerate(quadrants['sweet_spot'][:top_n], 1):
            inn = int(scores['innovation'])
            eff = int(scores['effectiveness'])
            qty = int(scores['quality'])

            title = song['title'][:33]
            artist = song['artist'][:18]

            print(f"{i:3d} {inn:4d} {eff:4d} {qty:4d} {title:35s} {artist:20s}")

        # Average scores
        print(f"\n📈 CORPUS AVERAGE SCORES")
        print("-" * 80)

        avg_scores = {
            'innovation': sum(s[1]['innovation'] for s in scored_songs) / len(scored_songs),
            'authenticity': sum(s[1]['authenticity'] for s in scored_songs) / len(scored_songs),
            'risk': sum(s[1]['risk'] for s in scored_songs) / len(scored_songs),
            'effectiveness': sum(s[1]['effectiveness'] for s in scored_songs) / len(scored_songs),
            'quality': sum(s[1]['quality'] for s in scored_songs) / len(scored_songs)
        }

        for metric, score in avg_scores.items():
            bar_length = int(score / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"{metric:15s}: {bar} {score:.1f}/100")

        print("\n" + "="*80 + "\n")
