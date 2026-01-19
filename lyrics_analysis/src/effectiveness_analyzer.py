"""
Effectiveness Analyzer - Measures what makes lyrics WORK.

This is the critical module that distinguishes good innovation from bad.
Being different is easy. Being different AND effective is the challenge.

Effectiveness dimensions:
1. Structural coherence (well-formed?)
2. Thematic consistency (makes sense?)
3. Emotional resonance (has impact?)
4. Memorability (sticks with you?)
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Optional, Tuple
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class EffectivenessAnalyzer:
    """Analyzes what makes lyrics effective vs ineffective."""

    def __init__(self, corpus_data: List[Dict]):
        """
        Initialize effectiveness analyzer.

        Args:
            corpus_data: List of song dictionaries
        """
        self.corpus = corpus_data
        self.analyzed = False

        # Theme keywords (from pattern_detector expanded)
        self.theme_keywords = {
            'amor_romantico': ['amor', 'amar', 'te amo', 'paixão', 'coração', 'beijar', 'abraço', 'casal'],
            'sofrimento': ['solidão', 'sofrer', 'dor', 'chorar', 'tristeza', 'saudade'],
            'festa': ['festa', 'dançar', 'balada', 'cerveja', 'bebida', 'alegria'],
            'traicao': ['traição', 'trair', 'mentira', 'infiel'],
            'natureza': ['sol', 'lua', 'mar', 'céu', 'estrela'],
            'urbano': ['cidade', 'rua', 'favela', 'quebrada'],
            'religioso': ['deus', 'fé', 'rezar', 'anjo'],
        }

        # Effectiveness scores for each song
        self.effectiveness_scores = {}

    def analyze_corpus(self):
        """Analyze corpus for effectiveness patterns."""
        logger.info("Analyzing corpus for effectiveness...")

        for i, song in enumerate(self.corpus):
            if (i + 1) % 500 == 0:
                logger.info(f"  Analyzed {i+1}/{len(self.corpus)} songs")

            song_id = f"{song['artist']}_{song['title']}"
            scores = self.analyze_song_effectiveness(song)
            self.effectiveness_scores[song_id] = scores

        self.analyzed = True
        logger.info(f"✓ Analyzed effectiveness for {len(self.corpus)} songs")

    def analyze_song_effectiveness(self, song: Dict) -> Dict:
        """
        Analyze effectiveness of a single song.

        Args:
            song: Song dictionary

        Returns:
            Dictionary with effectiveness scores
        """
        lyrics = song.get('lyrics', '')

        # Calculate individual effectiveness dimensions
        coherence = self._structural_coherence(lyrics)
        consistency = self._thematic_consistency(lyrics)
        resonance = self._emotional_resonance(lyrics)
        memorability = self._memorability_score(lyrics)

        # Composite effectiveness (weighted average)
        composite = (
            coherence * 0.25 +
            consistency * 0.25 +
            resonance * 0.25 +
            memorability * 0.25
        )

        return {
            'structural_coherence': round(coherence, 2),
            'thematic_consistency': round(consistency, 2),
            'emotional_resonance': round(resonance, 2),
            'memorability': round(memorability, 2),
            'composite_effectiveness': round(composite, 2)
        }

    def _structural_coherence(self, lyrics: str) -> float:
        """
        Measure structural coherence.
        Well-formed lyrics have:
        - Consistent line lengths
        - Clear paragraph breaks
        - Proper punctuation/formatting
        - Reasonable length

        Args:
            lyrics: Song lyrics

        Returns:
            Score 0-100
        """
        score = 100.0

        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

        if not lines:
            return 0

        # 1. Line length consistency (variance shouldn't be too high)
        line_lengths = [len(line.split()) for line in lines]
        if line_lengths:
            avg_len = sum(line_lengths) / len(line_lengths)
            variance = sum((l - avg_len) ** 2 for l in line_lengths) / len(line_lengths)

            # High variance = inconsistent structure
            # Penalize if variance > 50 (very inconsistent)
            if variance > 50:
                score -= min((variance - 50) / 10, 20)

        # 2. Paragraph structure (should have some, but not too many)
        paragraphs = lyrics.split('\n\n')
        non_empty_paras = [p for p in paragraphs if p.strip()]

        if len(lines) > 10:  # Only check for longer songs
            if len(non_empty_paras) < 2:
                score -= 15  # No paragraph breaks = wall of text
            elif len(non_empty_paras) > len(lines) / 2:
                score -= 10  # Too fragmented

        # 3. Reasonable length (not too short, not absurdly long)
        word_count = len(lyrics.split())

        if word_count < 20:
            score -= 30  # Too short to be substantial
        elif word_count > 1500:
            score -= 20  # Extremely long, may lose focus

        # 4. Not mostly gibberish (check for reasonable word lengths)
        words = lyrics.split()
        if words:
            avg_word_len = sum(len(w) for w in words) / len(words)

            if avg_word_len < 2:  # Mostly single characters
                score -= 40
            elif avg_word_len > 15:  # Abnormally long words
                score -= 20

        return max(score, 0)

    def _thematic_consistency(self, lyrics: str) -> float:
        """
        Measure thematic consistency.
        Good lyrics focus on 1-3 main themes, not random everything.

        Args:
            lyrics: Song lyrics

        Returns:
            Score 0-100
        """
        lyrics_lower = lyrics.lower()

        # Count theme presence
        theme_matches = {}
        for theme, keywords in self.theme_keywords.items():
            count = sum(1 for keyword in keywords if keyword in lyrics_lower)
            if count > 0:
                theme_matches[theme] = count

        num_themes = len(theme_matches)

        # Scoring logic:
        # 1-2 themes: very focused (100)
        # 3 themes: focused (90)
        # 4 themes: acceptable (70)
        # 5+ themes: scattered (50-)

        if num_themes == 0:
            return 50  # No clear theme (neutral)
        elif num_themes <= 2:
            return 100  # Very focused
        elif num_themes == 3:
            return 90  # Focused
        elif num_themes == 4:
            return 70  # Acceptable
        else:
            return max(50 - (num_themes - 5) * 10, 10)  # Too scattered

    def _emotional_resonance(self, lyrics: str) -> float:
        """
        Measure emotional resonance.
        Strong lyrics have emotional depth, not just neutral description.

        Uses keyword presence for emotional indicators.

        Args:
            lyrics: Song lyrics

        Returns:
            Score 0-100
        """
        lyrics_lower = lyrics.lower()

        # Emotional intensity markers
        strong_emotions = [
            'amor', 'ódio', 'paixão', 'dor', 'alegria', 'tristeza',
            'saudade', 'solidão', 'feliz', 'sofrer', 'chorar',
            'coração', 'alma', 'sentir', 'emoção'
        ]

        # Sensory/vivid language
        vivid_language = [
            'olhos', 'beijo', 'abraço', 'toque', 'voz', 'corpo',
            'brilha', 'queima', 'corre', 'voa', 'explode'
        ]

        # Count emotional words
        emotion_count = sum(1 for word in strong_emotions if word in lyrics_lower)
        vivid_count = sum(1 for word in vivid_language if word in lyrics_lower)

        word_count = len(lyrics_lower.split())

        # Emotional density (per 100 words)
        if word_count > 0:
            emotion_density = (emotion_count / word_count) * 100
            vivid_density = (vivid_count / word_count) * 100
        else:
            return 0

        # Scoring
        score = 0

        # Base from emotional words (max 60 points)
        score += min(emotion_density * 20, 60)

        # Bonus from vivid language (max 40 points)
        score += min(vivid_density * 15, 40)

        return min(score, 100)

    def _memorability_score(self, lyrics: str) -> float:
        """
        Measure memorability potential.
        Memorable lyrics have:
        - Some repetition (chorus)
        - Catchy phrases (short repeated lines)
        - Rhythm/pattern (consistent line structure)

        Args:
            lyrics: Song lyrics

        Returns:
            Score 0-100
        """
        score = 0

        lines = [l.strip().lower() for l in lyrics.split('\n') if l.strip()]

        if not lines:
            return 0

        # 1. Repetition (chorus effect) - max 40 points
        line_counts = Counter(lines)
        most_common_count = line_counts.most_common(1)[0][1] if line_counts else 0

        if most_common_count >= 4:
            score += 40  # Strong chorus
        elif most_common_count == 3:
            score += 30  # Moderate repetition
        elif most_common_count == 2:
            score += 15  # Some repetition
        # else: 0 (no repetition, less memorable)

        # 2. Short catchy phrases (3-7 word lines repeated) - max 30 points
        short_lines = [l for l in lines if 3 <= len(l.split()) <= 7]
        short_repeated = sum(1 for l in set(short_lines) if lines.count(l) >= 2)

        score += min(short_repeated * 10, 30)

        # 3. Rhythmic consistency (similar line lengths) - max 30 points
        line_word_counts = [len(l.split()) for l in lines]
        if line_word_counts:
            # Count how many lines are within 2 words of most common length
            count_freq = Counter(line_word_counts)
            most_common_length = count_freq.most_common(1)[0][0]

            consistent_lines = sum(
                1 for count in line_word_counts
                if abs(count - most_common_length) <= 2
            )

            consistency_ratio = consistent_lines / len(line_word_counts)
            score += consistency_ratio * 30

        return min(score, 100)

    def identify_effective_innovations(self,
                                      outlier_scores: List[Tuple[Dict, Dict]],
                                      min_effectiveness: float = 60) -> List[Tuple[Dict, Dict, Dict]]:
        """
        Identify songs that are BOTH innovative AND effective.
        This is the sweet spot: fresh but it works.

        Args:
            outlier_scores: List of (song, innovation_scores) from OutlierDetector
            min_effectiveness: Minimum effectiveness threshold

        Returns:
            List of (song, innovation_scores, effectiveness_scores) tuples
        """
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        effective_innovations = []

        for song, innov_scores in outlier_scores:
            song_id = f"{song['artist']}_{song['title']}"
            effect_scores = self.effectiveness_scores.get(song_id, {})

            composite_effect = effect_scores.get('composite_effectiveness', 0)

            if composite_effect >= min_effectiveness:
                effective_innovations.append((song, innov_scores, effect_scores))

        # Sort by balance of innovation + effectiveness
        effective_innovations.sort(
            key=lambda x: x[1]['composite_innovation'] + x[2]['composite_effectiveness'],
            reverse=True
        )

        return effective_innovations

    def analyze_sweet_spots(self, effective_innovations: List[Tuple]) -> Dict:
        """
        Analyze the "sweet spot" songs - innovative AND effective.

        Args:
            effective_innovations: List from identify_effective_innovations

        Returns:
            Dictionary with sweet spot analysis
        """
        if not effective_innovations:
            return {}

        # Analyze patterns
        artists = Counter(song['artist'] for song, _, _ in effective_innovations)
        genres = Counter(song['genre'] for song, _, _ in effective_innovations)

        # Average scores
        avg_innovation = sum(
            innov['composite_innovation']
            for _, innov, _ in effective_innovations
        ) / len(effective_innovations)

        avg_effectiveness = sum(
            effect['composite_effectiveness']
            for _, _, effect in effective_innovations
        ) / len(effective_innovations)

        return {
            'sweet_spot_count': len(effective_innovations),
            'avg_innovation_score': round(avg_innovation, 2),
            'avg_effectiveness_score': round(avg_effectiveness, 2),
            'top_artists': dict(artists.most_common(10)),
            'genre_distribution': dict(genres.most_common()),
            'interpretation': 'These songs successfully balance innovation with effectiveness'
        }

    def generate_report(self) -> Dict:
        """Generate effectiveness analysis report."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        # Calculate aggregate statistics
        all_scores = list(self.effectiveness_scores.values())

        avg_coherence = sum(s['structural_coherence'] for s in all_scores) / len(all_scores)
        avg_consistency = sum(s['thematic_consistency'] for s in all_scores) / len(all_scores)
        avg_resonance = sum(s['emotional_resonance'] for s in all_scores) / len(all_scores)
        avg_memorability = sum(s['memorability'] for s in all_scores) / len(all_scores)
        avg_composite = sum(s['composite_effectiveness'] for s in all_scores) / len(all_scores)

        return {
            'overview': {
                'songs_analyzed': len(self.effectiveness_scores),
                'average_scores': {
                    'structural_coherence': round(avg_coherence, 2),
                    'thematic_consistency': round(avg_consistency, 2),
                    'emotional_resonance': round(avg_resonance, 2),
                    'memorability': round(avg_memorability, 2),
                    'composite_effectiveness': round(avg_composite, 2)
                }
            },
            'methodology': {
                'structural_coherence': 'Measures line consistency, paragraph structure, reasonable length',
                'thematic_consistency': 'Checks focus on 1-3 themes vs scattered',
                'emotional_resonance': 'Counts emotional and vivid language density',
                'memorability': 'Evaluates repetition, catchy phrases, rhythmic consistency'
            }
        }

    def save_report(self, output_path: Path):
        """Save effectiveness report to JSON file."""
        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved effectiveness report to {output_path}")

    def print_summary(self):
        """Print formatted summary of effectiveness analysis."""
        if not self.analyzed:
            raise RuntimeError("Must call analyze_corpus() first")

        print("\n" + "="*80)
        print(" EFFECTIVENESS ANALYSIS ".center(80, "="))
        print("="*80 + "\n")

        report = self.generate_report()

        print("📊 CORPUS-WIDE EFFECTIVENESS AVERAGES")
        print("-" * 80)

        avg_scores = report['overview']['average_scores']
        for dimension, score in avg_scores.items():
            bar_length = int(score / 2)  # Scale to 50 chars max
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"{dimension:30s}: {bar} {score:.1f}/100")

        print(f"\n💡 INTERPRETATION")
        print("-" * 80)
        print("Structural Coherence:  How well-formed and organized the lyrics are")
        print("Thematic Consistency:  Focus on coherent themes vs scattered topics")
        print("Emotional Resonance:   Depth of emotional and vivid language")
        print("Memorability:          Repetition, catchy phrases, rhythmic patterns")

        print("\n" + "="*80 + "\n")
