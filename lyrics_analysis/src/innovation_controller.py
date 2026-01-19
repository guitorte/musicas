"""
Innovation Controller - Maps 4D targets to generation parameters.

This module translates user-specified 4D targets into concrete generation parameters:
- Innovation → vocabulary rarity, structure uniqueness
- Authenticity → genre-specific vocabulary, Portuguese markers
- Risk → experimentation level, cliché tolerance
- Effectiveness → chorus presence, memorability features

The controller is the "brain" that interprets user intent.
"""

from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class InnovationController:
    """Controls generation parameters based on 4D targets."""

    def __init__(self):
        """Initialize innovation controller."""
        # Default target profile (balanced)
        self.default_profile = {
            'innovation': 50.0,
            'authenticity': 80.0,
            'risk': 50.0,
            'effectiveness': 70.0
        }

        logger.info("✓ Innovation controller initialized")

    def create_profile(
        self,
        innovation: float = 50.0,
        authenticity: float = 80.0,
        risk: float = 50.0,
        effectiveness: float = 70.0
    ) -> Dict:
        """
        Create a 4D target profile.

        Args:
            innovation: 0-100, how innovative/distinctive (50=balanced)
            authenticity: 0-100, Brazilian Portuguese authenticity (80=recommended)
            risk: 0-100, experimental risk level (50=moderate)
            effectiveness: 0-100, quality/memorability target (70=good)

        Returns:
            Profile dictionary
        """
        profile = {
            'innovation': self._clamp(innovation, 0, 100),
            'authenticity': self._clamp(authenticity, 0, 100),
            'risk': self._clamp(risk, 0, 100),
            'effectiveness': self._clamp(effectiveness, 0, 100)
        }

        return profile

    def profile_to_generation_params(self, profile: Dict, genre: str = "MPB") -> Dict:
        """
        Convert 4D profile to concrete generation parameters.

        Args:
            profile: 4D target profile
            genre: Target genre

        Returns:
            Generation parameters dictionary
        """
        innovation = profile.get('innovation', 50)
        authenticity = profile.get('authenticity', 80)
        risk = profile.get('risk', 50)
        effectiveness = profile.get('effectiveness', 70)

        # Map to generation parameters
        params = {
            # Structure parameters
            'structure': {
                'innovation_level': innovation / 100.0,  # 0-1
                'effectiveness_target': effectiveness / 100.0,  # 0-1
                'genre': genre
            },

            # Vocabulary parameters
            'vocabulary': {
                'genre': genre,
                'innovation_level': innovation / 100.0,
                'avoid_cliches': risk < 70,  # High risk = allow clichés
                'use_distinctive_words': innovation > 50,
                'authenticity_weight': authenticity / 100.0
            },

            # Generation strategy
            'strategy': {
                'candidates_per_section': self._map_candidates_count(risk),
                'max_iterations': self._map_max_iterations(effectiveness),
                'quality_threshold': self._map_quality_threshold(effectiveness),
                'exploration_factor': risk / 100.0  # 0-1
            },

            # Thematic parameters
            'themes': self._select_themes(genre, innovation, authenticity),

            # Repetition/chorus parameters
            'repetition': {
                'force_chorus': effectiveness > 60,
                'repetition_strength': self._map_repetition_strength(effectiveness),
                'variation_allowed': innovation / 100.0
            }
        }

        return params

    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp value to range."""
        return max(min_val, min(max_val, value))

    def _map_candidates_count(self, risk: float) -> int:
        """
        Map risk level to number of candidates to generate per section.

        Higher risk = more candidates to explore.
        """
        if risk > 70:
            return 15  # High risk: generate many candidates
        elif risk > 40:
            return 10  # Moderate risk
        else:
            return 5  # Low risk: fewer candidates

    def _map_max_iterations(self, effectiveness: float) -> int:
        """
        Map effectiveness target to max refinement iterations.

        Higher effectiveness target = more iterations to get it right.
        """
        if effectiveness > 80:
            return 5  # High effectiveness: iterate more
        elif effectiveness > 60:
            return 3  # Moderate effectiveness
        else:
            return 1  # Low effectiveness: quick generation

    def _map_quality_threshold(self, effectiveness: float) -> float:
        """
        Map effectiveness target to minimum quality threshold.

        Higher effectiveness = higher threshold.
        """
        return effectiveness / 100.0  # Direct mapping

    def _map_repetition_strength(self, effectiveness: float) -> float:
        """
        Map effectiveness to repetition strength.

        Higher effectiveness = stronger repetition (more memorable).
        """
        if effectiveness > 70:
            return 0.8  # Strong repetition
        elif effectiveness > 50:
            return 0.6  # Moderate repetition
        else:
            return 0.4  # Weak repetition

    def _select_themes(
        self,
        genre: str,
        innovation: float,
        authenticity: float
    ) -> list:
        """
        Select appropriate themes based on genre and targets.

        Args:
            genre: Target genre
            innovation: Innovation level
            authenticity: Authenticity level

        Returns:
            List of theme names
        """
        # Genre-typical themes
        genre_themes = {
            'MPB': ['amor_romantico', 'natureza', 'social'],
            'Sertanejo': ['amor_romantico', 'sofrimento', 'natureza'],
            'Pagode': ['amor_romantico', 'festa', 'social'],
            'Trap': ['ostentacao', 'social', 'amor_romantico'],
            'Arrocha': ['amor_romantico', 'sofrimento', 'festa']
        }

        typical_themes = genre_themes.get(genre, ['amor_romantico', 'social'])

        # If high innovation, consider mixing themes
        if innovation > 70:
            # Add unexpected theme
            all_themes = set()
            for themes in genre_themes.values():
                all_themes.update(themes)

            # Find themes NOT typical for this genre
            unexpected = list(all_themes - set(typical_themes))
            if unexpected:
                import random
                typical_themes.append(random.choice(unexpected))

        return typical_themes

    def suggest_profiles(self) -> Dict[str, Dict]:
        """
        Get pre-defined profile suggestions.

        Returns:
            Dictionary of profile name → profile
        """
        profiles = {
            'balanced': {
                'name': 'Balanced',
                'description': 'Good mix of innovation and effectiveness',
                'profile': {
                    'innovation': 50,
                    'authenticity': 80,
                    'risk': 50,
                    'effectiveness': 70
                }
            },

            'safe': {
                'name': 'Safe & Effective',
                'description': 'Focus on proven formulas',
                'profile': {
                    'innovation': 30,
                    'authenticity': 85,
                    'risk': 30,
                    'effectiveness': 80
                }
            },

            'experimental': {
                'name': 'Experimental',
                'description': 'Push boundaries, take risks',
                'profile': {
                    'innovation': 80,
                    'authenticity': 70,
                    'risk': 80,
                    'effectiveness': 50
                }
            },

            'sweet_spot': {
                'name': 'Sweet Spot',
                'description': 'High innovation + high effectiveness',
                'profile': {
                    'innovation': 70,
                    'authenticity': 80,
                    'risk': 60,
                    'effectiveness': 75
                }
            },

            'traditional': {
                'name': 'Traditional',
                'description': 'Classic Brazilian style',
                'profile': {
                    'innovation': 20,
                    'authenticity': 95,
                    'risk': 20,
                    'effectiveness': 75
                }
            },

            'contemporary': {
                'name': 'Contemporary',
                'description': 'Modern, trendy style',
                'profile': {
                    'innovation': 60,
                    'authenticity': 65,
                    'risk': 70,
                    'effectiveness': 70
                }
            }
        }

        return profiles

    def validate_profile(self, profile: Dict) -> Tuple[bool, str]:
        """
        Validate a 4D profile.

        Args:
            profile: Profile dictionary

        Returns:
            (is_valid, message)
        """
        required_keys = ['innovation', 'authenticity', 'risk', 'effectiveness']

        for key in required_keys:
            if key not in profile:
                return False, f"Missing required key: {key}"

            value = profile[key]
            if not isinstance(value, (int, float)):
                return False, f"{key} must be numeric"

            if not (0 <= value <= 100):
                return False, f"{key} must be between 0 and 100"

        return True, "Profile is valid"

    def explain_profile(self, profile: Dict) -> str:
        """
        Generate human-readable explanation of a profile.

        Args:
            profile: 4D profile

        Returns:
            Explanation string
        """
        innovation = profile.get('innovation', 50)
        authenticity = profile.get('authenticity', 80)
        risk = profile.get('risk', 50)
        effectiveness = profile.get('effectiveness', 70)

        # Interpret scores
        innovation_desc = self._interpret_score(
            innovation,
            {(0, 30): "very traditional", (30, 50): "somewhat conventional",
             (50, 70): "moderately innovative", (70, 100): "highly innovative"}
        )

        authenticity_desc = self._interpret_score(
            authenticity,
            {(0, 50): "experimental mix", (50, 70): "modern Brazilian",
             (70, 85): "authentic Brazilian", (85, 100): "very traditional Brazilian"}
        )

        risk_desc = self._interpret_score(
            risk,
            {(0, 30): "safe and proven", (30, 50): "moderate risk",
             (50, 70): "adventurous", (70, 100): "highly experimental"}
        )

        effectiveness_desc = self._interpret_score(
            effectiveness,
            {(0, 40): "experimental (quality not prioritized)",
             (40, 60): "acceptable quality",
             (60, 75): "good quality", (75, 100): "high quality"}
        )

        explanation = f"""
Profile Interpretation:
  Innovation:    {innovation:.0f}/100 - {innovation_desc}
  Authenticity:  {authenticity:.0f}/100 - {authenticity_desc}
  Risk:          {risk:.0f}/100 - {risk_desc}
  Effectiveness: {effectiveness:.0f}/100 - {effectiveness_desc}

This will generate lyrics that are {innovation_desc}, with {authenticity_desc} language,
taking {risk_desc} approach, targeting {effectiveness_desc}.
        """.strip()

        return explanation

    def _interpret_score(self, score: float, ranges: Dict) -> str:
        """Interpret score into description based on ranges."""
        for (min_val, max_val), description in ranges.items():
            if min_val <= score < max_val:
                return description

        return "undefined"

    def print_profile(self, profile: Dict):
        """Print formatted profile."""
        print("\n" + "="*60)
        print(" 4D GENERATION PROFILE ".center(60, "="))
        print("="*60 + "\n")

        print(self.explain_profile(profile))

        print("\n" + "="*60 + "\n")
