"""
Structure Generator - Creates song structures from learned templates.

This module generates song structure blueprints based on Phase 2A analysis:
- Uses common structural templates
- Adjusts structure based on genre norms
- Controls repetition (chorus) based on innovation level
- Provides scaffolding for lyrics generation

The generator creates a template that the vocabulary selector fills.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class StructureGenerator:
    """Generates song structures from templates."""

    def __init__(self, analysis_dir: Path):
        """
        Initialize structure generator.

        Args:
            analysis_dir: Path to analysis directory containing Phase 2A results
        """
        self.analysis_dir = Path(analysis_dir)

        # Load Phase 2A structural data
        self.templates = self._load_templates()
        self.genre_norms = self._load_genre_norms()

        logger.info("✓ Structure generator initialized")

    def _load_templates(self) -> List[Dict]:
        """Load structural templates from Phase 2A analysis."""
        template_path = self.analysis_dir / "patterns" / "structure_templates.json"

        if not template_path.exists():
            logger.warning(f"Templates not found: {template_path}")
            return []

        with open(template_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        templates = data.get('templates', [])
        logger.info(f"  Loaded {len(templates)} structural templates")

        return templates

    def _load_genre_norms(self) -> Dict:
        """Load genre norms from Phase 2A analysis."""
        template_path = self.analysis_dir / "patterns" / "structure_templates.json"

        if not template_path.exists():
            return {}

        with open(template_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        norms = data.get('genre_norms', {})
        logger.info(f"  Loaded norms for {len(norms)} genres")

        return norms

    def select_template(
        self,
        genre: Optional[str] = None,
        innovation_level: float = 0.5,
        target_length: Optional[str] = None
    ) -> Dict:
        """
        Select a structural template based on parameters.

        Args:
            genre: Target genre (affects length/style)
            innovation_level: 0-1, higher = less common templates
            target_length: Optional line count bucket (e.g., "20-29")

        Returns:
            Selected template dictionary
        """
        if not self.templates:
            # Fallback default
            return {
                'template': {
                    'line_count_bucket': '20-29',
                    'paragraph_count': 4,
                    'has_repetition': True
                },
                'count': 0
            }

        # Filter by length if specified
        candidates = self.templates
        if target_length:
            candidates = [t for t in self.templates
                         if t['template']['line_count_bucket'] == target_length]
            if not candidates:
                candidates = self.templates

        # Select based on innovation level
        if innovation_level > 0.7:
            # High innovation: pick less common templates (bottom 30%)
            start_idx = int(len(candidates) * 0.7)
            pool = candidates[start_idx:]
        elif innovation_level > 0.4:
            # Medium innovation: middle templates
            start_idx = int(len(candidates) * 0.3)
            end_idx = int(len(candidates) * 0.7)
            pool = candidates[start_idx:end_idx]
        else:
            # Low innovation: most common templates (top 30%)
            end_idx = int(len(candidates) * 0.3)
            pool = candidates[:end_idx] if end_idx > 0 else candidates

        # Pick random from pool
        template = random.choice(pool) if pool else self.templates[0]

        return template

    def generate_structure(
        self,
        genre: str = "MPB",
        innovation_level: float = 0.5,
        effectiveness_target: float = 0.7
    ) -> Dict:
        """
        Generate a complete song structure.

        Args:
            genre: Target genre
            innovation_level: 0-1, higher = more innovative structure
            effectiveness_target: 0-1, target effectiveness score

        Returns:
            Structure specification dictionary
        """
        # Get genre norms
        norms = self.genre_norms.get(genre, {
            'avg_lines': 30,
            'avg_words': 200,
            'avg_paragraphs': 6,
            'chorus_percentage': 60
        })

        # Select template
        avg_lines = norms['avg_lines']
        line_bucket = self._get_line_bucket(avg_lines, innovation_level)
        template_data = self.select_template(
            genre=genre,
            innovation_level=innovation_level,
            target_length=line_bucket
        )

        template = template_data['template']

        # Determine structure type
        has_chorus = template['has_repetition']

        # If effectiveness target is high, favor structures with choruses
        if effectiveness_target > 0.7 and not has_chorus:
            if random.random() < 0.7:  # 70% chance to add chorus
                has_chorus = True

        # Build structure
        structure = self._build_structure_blueprint(
            template=template,
            genre=genre,
            has_chorus=has_chorus,
            norms=norms
        )

        return structure

    def _get_line_bucket(self, avg_lines: float, innovation_level: float) -> str:
        """
        Get line count bucket based on average and innovation level.

        Args:
            avg_lines: Average lines for genre
            innovation_level: 0-1, affects deviation from average

        Returns:
            Line bucket string (e.g., "20-29")
        """
        # Adjust target based on innovation
        if innovation_level > 0.7:
            # High innovation: deviate from average
            deviation = random.choice([-20, -10, 10, 20])
        elif innovation_level > 0.4:
            # Medium innovation: slight deviation
            deviation = random.choice([-10, 0, 10])
        else:
            # Low innovation: stick to average
            deviation = 0

        target_lines = int(avg_lines + deviation)

        # Convert to bucket
        bucket_start = (target_lines // 10) * 10
        return f"{bucket_start}-{bucket_start + 9}"

    def _build_structure_blueprint(
        self,
        template: Dict,
        genre: str,
        has_chorus: bool,
        norms: Dict
    ) -> Dict:
        """
        Build detailed structure blueprint.

        Args:
            template: Selected template
            genre: Target genre
            has_chorus: Whether to include chorus
            norms: Genre norms

        Returns:
            Detailed structure specification
        """
        # Parse line count bucket
        line_bucket = template['line_count_bucket']
        line_range = line_bucket.split('-')
        min_lines = int(line_range[0])
        max_lines = int(line_range[1])
        target_lines = random.randint(min_lines, max_lines)

        paragraph_count = template['paragraph_count']

        # Calculate words per line based on genre norms
        avg_words = norms.get('avg_words', 200)
        words_per_line = int(avg_words / target_lines)

        # Build section structure
        sections = []

        if has_chorus:
            # Structure with chorus: verse-chorus-verse-chorus-bridge-chorus
            chorus_lines = max(4, target_lines // 8)
            verse_lines = max(4, (target_lines - chorus_lines * 3) // 2)
            bridge_lines = max(2, target_lines - (verse_lines * 2 + chorus_lines * 3))

            sections = [
                {'type': 'verse', 'lines': verse_lines, 'words_per_line': words_per_line},
                {'type': 'chorus', 'lines': chorus_lines, 'words_per_line': words_per_line - 1},
                {'type': 'verse', 'lines': verse_lines, 'words_per_line': words_per_line},
                {'type': 'chorus', 'lines': chorus_lines, 'words_per_line': words_per_line - 1},
                {'type': 'bridge', 'lines': bridge_lines, 'words_per_line': words_per_line + 1},
                {'type': 'chorus', 'lines': chorus_lines, 'words_per_line': words_per_line - 1}
            ]
        else:
            # Structure without chorus: just verses
            lines_per_section = max(4, target_lines // paragraph_count)

            for i in range(paragraph_count):
                sections.append({
                    'type': 'verse',
                    'lines': lines_per_section,
                    'words_per_line': words_per_line
                })

        # Build final structure
        structure = {
            'genre': genre,
            'total_lines': target_lines,
            'total_paragraphs': paragraph_count,
            'has_chorus': has_chorus,
            'sections': sections,
            'template_info': template,
            'estimated_words': sum(s['lines'] * s['words_per_line'] for s in sections)
        }

        return structure

    def structure_to_text_template(self, structure: Dict) -> str:
        """
        Convert structure to text template with placeholders.

        Args:
            structure: Structure specification

        Returns:
            Text template with [SECTION] markers
        """
        lines = []

        for section in structure['sections']:
            section_type = section['type'].upper()
            section_lines = section['lines']

            lines.append(f"[{section_type}]")

            for i in range(section_lines):
                lines.append(f"___ {' ___ ' * (section['words_per_line'] - 1)}")

            lines.append("")  # Blank line between sections

        return '\n'.join(lines)

    def get_genre_norms(self, genre: str) -> Dict:
        """
        Get structural norms for a genre.

        Args:
            genre: Genre name

        Returns:
            Genre norms dictionary
        """
        return self.genre_norms.get(genre, {
            'avg_lines': 30,
            'avg_words': 200,
            'avg_paragraphs': 6,
            'chorus_percentage': 60
        })

    def list_available_genres(self) -> List[str]:
        """Get list of available genres with norms."""
        return list(self.genre_norms.keys())

    def analyze_structure(self, lyrics: str) -> Dict:
        """
        Analyze the structure of given lyrics.

        Args:
            lyrics: Lyrics text

        Returns:
            Structure analysis
        """
        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
        paragraphs = [p.strip() for p in lyrics.split('\n\n') if p.strip()]
        words = lyrics.split()

        # Check for repetition
        from collections import Counter
        line_counts = Counter(l.lower() for l in lines)
        has_chorus = any(count >= 2 for count in line_counts.values())

        return {
            'total_lines': len(lines),
            'total_paragraphs': len(paragraphs),
            'total_words': len(words),
            'words_per_line': len(words) / len(lines) if lines else 0,
            'lines_per_paragraph': len(lines) / len(paragraphs) if paragraphs else 0,
            'has_chorus': has_chorus
        }
