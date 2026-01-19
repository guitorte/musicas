#!/usr/bin/env python3
"""
Pattern Analysis Script - Analyzes conventions in Brazilian lyrics corpus.

This script runs all Phase 2A pattern detection modules:
- Cliché detection (overused phrases)
- Pattern detection (genre formulas)
- Structure analysis (song templates)

Output: Convention Atlas with actionable insights for avoiding clichés
and understanding genre formulas.
"""

import sys
from pathlib import Path
import logging
import argparse
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from storage import LyricsStorage
from cliche_detector import ClicheDetector
from pattern_detector import PatternDetector
from structure_analyzer import StructureAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main analysis function."""
    parser = argparse.ArgumentParser(
        description='Analyze patterns and conventions in lyrics corpus'
    )
    parser.add_argument(
        '--data-file',
        type=str,
        default='../data/processed/lyrics_corpus.jsonl',
        help='Path to processed corpus (JSONL format)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='../analysis/patterns',
        help='Output directory for analysis reports'
    )
    parser.add_argument(
        '--skip-cliches',
        action='store_true',
        help='Skip cliché detection'
    )
    parser.add_argument(
        '--skip-patterns',
        action='store_true',
        help='Skip pattern detection'
    )
    parser.add_argument(
        '--skip-structure',
        action='store_true',
        help='Skip structure analysis'
    )

    args = parser.parse_args()

    # Setup paths
    data_file = Path(args.data_file).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("="*80)
    logger.info(" PATTERN ANALYSIS - PHASE 2A ".center(80, "="))
    logger.info("="*80)
    logger.info(f"Data File: {data_file}")
    logger.info(f"Output Directory: {output_dir}")
    logger.info("="*80 + "\n")

    # Load corpus
    logger.info("📂 Loading corpus...")
    storage = LyricsStorage(str(data_file.parent))

    try:
        corpus = storage.load_from_jsonl(data_file.name)
        logger.info(f"✓ Loaded {len(corpus):,} songs\n")
    except Exception as e:
        logger.error(f"Failed to load corpus: {e}")
        sys.exit(1)

    # Run analyses
    analyses_run = []

    # 1. Cliché Detection
    if not args.skip_cliches:
        logger.info("🔍 ANALYSIS 1/3: Cliché Detection")
        logger.info("-" * 80)

        cliche_detector = ClicheDetector(corpus, min_ngram=2, max_ngram=5)
        cliche_detector.analyze_corpus()

        # Print summary
        cliche_detector.print_summary(top_n=15)

        # Save report
        cliche_output = output_dir / 'cliche_report.json'
        cliche_detector.save_report(cliche_output)

        # Save top clichés for quick reference
        top_cliches_summary = {
            'WARNING': 'These are the most overused phrases in Brazilian lyrics - AVOID THEM!',
            'top_2word_cliches': [
                {'phrase': phrase, 'uses': count, 'in_percent_of_songs': round(pct, 2)}
                for phrase, count, pct in cliche_detector.get_top_cliches(n=2, top_k=100)
            ],
            'top_3word_cliches': [
                {'phrase': phrase, 'uses': count, 'in_percent_of_songs': round(pct, 2)}
                for phrase, count, pct in cliche_detector.get_top_cliches(n=3, top_k=50)
            ]
        }

        cliches_summary_file = output_dir / 'AVOID_THESE_CLICHES.json'
        with open(cliches_summary_file, 'w', encoding='utf-8') as f:
            json.dump(top_cliches_summary, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ Cliché reports saved to {output_dir}/")
        logger.info(f"  📌 Quick reference: {cliches_summary_file.name}\n")

        analyses_run.append('cliche_detection')

    # 2. Pattern Detection
    if not args.skip_patterns:
        logger.info("🎵 ANALYSIS 2/3: Genre Pattern Detection")
        logger.info("-" * 80)

        pattern_detector = PatternDetector(corpus)
        pattern_detector.analyze_corpus()

        # Print summary
        pattern_detector.print_summary()

        # Save report
        pattern_output = output_dir / 'pattern_report.json'
        pattern_detector.save_report(pattern_output)

        # Save genre formulas for quick reference
        formulas_summary = {
            'description': 'What makes each genre distinctive - the "formula" for each genre',
            'genres': {}
        }

        for genre in pattern_detector.genre_profiles.keys():
            formula = pattern_detector.get_genre_formula(genre)

            # Extract key insights
            formulas_summary['genres'][genre] = {
                'song_count': formula['song_count'],
                'vocabulary_richness': formula['vocabulary']['vocabulary_richness'],
                'avg_words_per_song': formula['structure']['avg_words'],
                'repetition_level': formula['structure']['avg_repetition'],
                'top_5_words': [w['word'] for w in formula['vocabulary']['top_100_words'][:5]],
                'top_5_themes': list(formula['themes'].keys())[:5],
                'top_10_distinctive_words': [
                    w['word'] for w in formula['distinctive_features']['top_distinctive_words'][:10]
                ]
            }

        formulas_file = output_dir / 'genre_formulas.json'
        with open(formulas_file, 'w', encoding='utf-8') as f:
            json.dump(formulas_summary, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ Pattern reports saved to {output_dir}/")
        logger.info(f"  📌 Quick reference: {formulas_file.name}\n")

        analyses_run.append('pattern_detection')

    # 3. Structure Analysis
    if not args.skip_structure:
        logger.info("📐 ANALYSIS 3/3: Structural Pattern Analysis")
        logger.info("-" * 80)

        structure_analyzer = StructureAnalyzer(corpus)
        structure_analyzer.analyze_corpus()

        # Print summary
        structure_analyzer.print_summary()

        # Save report
        structure_output = output_dir / 'structure_report.json'
        structure_analyzer.save_report(structure_output)

        # Save structure templates for quick reference
        templates_summary = {
            'description': 'Common structural templates found in Brazilian lyrics',
            'templates': structure_analyzer.templates[:20],
            'genre_norms': {}
        }

        for genre, profile in structure_analyzer.structure_profiles.items():
            templates_summary['genre_norms'][genre] = {
                'avg_lines': profile['line_patterns']['avg_lines_per_song'],
                'avg_words': profile['length_distribution']['avg_words'],
                'avg_paragraphs': profile['paragraph_patterns']['avg_paragraphs_per_song'],
                'chorus_percentage': profile['repetition_analysis']['chorus_percentage']
            }

        templates_file = output_dir / 'structure_templates.json'
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(templates_summary, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ Structure reports saved to {output_dir}/")
        logger.info(f"  📌 Quick reference: {templates_file.name}\n")

        analyses_run.append('structure_analysis')

    # Generate master index
    logger.info("📋 Generating Convention Atlas index...")

    atlas_index = {
        'title': 'Brazilian Lyrics Convention Atlas',
        'description': 'Comprehensive analysis of patterns and conventions in Brazilian music lyrics',
        'corpus_stats': {
            'total_songs': len(corpus),
            'genres': len(set(s.get('genre', 'Unknown') for s in corpus)),
            'artists': len(set(s.get('artist', 'Unknown') for s in corpus))
        },
        'analyses_included': analyses_run,
        'key_files': {
            'cliche_detection': {
                'full_report': 'cliche_report.json',
                'quick_reference': 'AVOID_THESE_CLICHES.json',
                'description': 'Overused phrases to AVOID in new lyrics'
            },
            'pattern_detection': {
                'full_report': 'pattern_report.json',
                'quick_reference': 'genre_formulas.json',
                'description': 'Genre-specific patterns and distinctive features'
            },
            'structure_analysis': {
                'full_report': 'structure_report.json',
                'quick_reference': 'structure_templates.json',
                'description': 'Common song structures and templates'
            }
        },
        'usage': {
            'for_writers': 'Use AVOID_THESE_CLICHES.json to check your lyrics for overused phrases',
            'for_analysis': 'Use genre_formulas.json to understand what makes each genre distinctive',
            'for_generation': 'Use structure_templates.json to model common song structures'
        }
    }

    index_file = output_dir / 'CONVENTION_ATLAS_INDEX.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(atlas_index, f, ensure_ascii=False, indent=2)

    # Final summary
    logger.info("="*80)
    logger.info(" PATTERN ANALYSIS COMPLETE ".center(80, "="))
    logger.info("="*80)
    logger.info(f"Analyses completed: {', '.join(analyses_run)}")
    logger.info(f"Output location: {output_dir}")
    logger.info("")
    logger.info("📁 Key Files Generated:")
    logger.info(f"  📌 {index_file.name} - Start here!")
    if 'cliche_detection' in analyses_run:
        logger.info(f"  🚫 AVOID_THESE_CLICHES.json - Top overused phrases")
    if 'pattern_detection' in analyses_run:
        logger.info(f"  🎵 genre_formulas.json - What makes each genre unique")
    if 'structure_analysis' in analyses_run:
        logger.info(f"  📐 structure_templates.json - Common song structures")
    logger.info("")
    logger.info("💡 Next Steps:")
    logger.info("  1. Review AVOID_THESE_CLICHES.json to see what phrases to avoid")
    logger.info("  2. Study genre_formulas.json to understand genre conventions")
    logger.info("  3. Use this knowledge to identify INNOVATIONS (Phase 2B)")
    logger.info("="*80 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\nAnalysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n\nError during analysis: {e}", exc_info=True)
        sys.exit(1)
