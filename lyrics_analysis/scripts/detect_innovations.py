#!/usr/bin/env python3
"""
Innovation Detection Script - Identifies what makes songs distinctive AND effective.

This script runs all Phase 2B innovation detection modules:
- Outlier detection (statistical uniqueness)
- Effectiveness analysis (what works)
- Innovation metrics (4D scoring)
- Temporal evolution (how patterns changed)

Output: Innovation Atlas with the "sweet spot" songs that are both
innovative AND effective.
"""

import sys
from pathlib import Path
import logging
import argparse
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from storage import LyricsStorage
from outlier_detector import OutlierDetector
from effectiveness_analyzer import EffectivenessAnalyzer
from innovation_metrics import InnovationMetrics
from temporal_analyzer import TemporalAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main innovation detection function."""
    parser = argparse.ArgumentParser(
        description='Detect innovations and identify sweet spot songs'
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
        default='../analysis/innovations',
        help='Output directory for innovation reports'
    )

    args = parser.parse_args()

    # Setup paths
    data_file = Path(args.data_file).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("="*80)
    logger.info(" INNOVATION DETECTION - PHASE 2B ".center(80, "="))
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
    logger.info("🔍 ANALYSIS 1/4: Outlier Detection (Statistical Uniqueness)")
    logger.info("-" * 80)

    outlier_detector = OutlierDetector(corpus)
    outlier_detector.analyze_corpus()
    outlier_detector.print_summary(top_n=20)

    outlier_output = output_dir / 'outlier_report.json'
    outlier_detector.save_report(outlier_output)
    logger.info(f"✓ Outlier report saved to {outlier_output}\n")

    # Get top outliers for further analysis
    top_outliers = outlier_detector.get_top_outliers(100)

    logger.info("📊 ANALYSIS 2/4: Effectiveness Analysis (What Works)")
    logger.info("-" * 80)

    effectiveness_analyzer = EffectivenessAnalyzer(corpus)
    effectiveness_analyzer.analyze_corpus()
    effectiveness_analyzer.print_summary()

    effectiveness_output = output_dir / 'effectiveness_report.json'
    effectiveness_analyzer.save_report(effectiveness_output)
    logger.info(f"✓ Effectiveness report saved to {effectiveness_output}\n")

    logger.info("✨ ANALYSIS 3/4: Innovation Metrics (4D Scoring)")
    logger.info("-" * 80)

    innovation_metrics = InnovationMetrics(corpus)

    # Combine outlier + effectiveness scores for 4D analysis
    logger.info("  Computing 4D scores for all songs...")
    all_4d_scores = []

    for song, outlier_scores in top_outliers:
        song_id = f"{song['artist']}_{song['title']}"
        effectiveness_scores = effectiveness_analyzer.effectiveness_scores.get(song_id, {})

        full_scores = innovation_metrics.score_song_4d(
            song,
            innovation_score=outlier_scores,
            effectiveness_score=effectiveness_scores
        )

        all_4d_scores.append((song, full_scores))

    innovation_metrics.print_summary(all_4d_scores, top_n=20)

    # Generate and save 4D report
    metrics_report = innovation_metrics.generate_report(all_4d_scores)
    metrics_output = output_dir / 'innovation_metrics.json'
    innovation_metrics.save_report(metrics_report, metrics_output)
    logger.info(f"✓ Innovation metrics saved to {metrics_output}\n")

    # Identify sweet spot songs
    sweet_spots = innovation_metrics.identify_sweet_spots(
        all_4d_scores,
        min_innovation=60,
        min_effectiveness=60
    )

    logger.info(f"🎯 Found {len(sweet_spots)} songs in THE SWEET SPOT")
    logger.info(f"   (Innovation ≥ 60 AND Effectiveness ≥ 60)\n")

    # Save sweet spot songs separately
    sweet_spot_summary = {
        'description': 'Songs that are BOTH innovative AND effective - learn from these!',
        'criteria': {
            'min_innovation': 60,
            'min_effectiveness': 60
        },
        'count': len(sweet_spots),
        'songs': [
            {
                'title': song['title'],
                'artist': song['artist'],
                'genre': song['genre'],
                'scores': scores
            }
            for song, scores in sweet_spots[:100]
        ]
    }

    sweet_spot_file = output_dir / 'SWEET_SPOT_SONGS.json'
    with open(sweet_spot_file, 'w', encoding='utf-8') as f:
        json.dump(sweet_spot_summary, f, ensure_ascii=False, indent=2)

    logger.info(f"✓ Sweet spot songs saved to {sweet_spot_file}\n")

    logger.info("📅 ANALYSIS 4/4: Temporal Evolution")
    logger.info("-" * 80)

    temporal_analyzer = TemporalAnalyzer(corpus)
    temporal_analyzer.analyze_corpus()
    temporal_analyzer.print_summary()

    temporal_output = output_dir / 'temporal_evolution.json'
    temporal_analyzer.save_report(temporal_output)
    logger.info(f"✓ Temporal report saved to {temporal_output}\n")

    # Generate master index
    logger.info("📋 Generating Innovation Atlas index...")

    atlas_index = {
        'title': 'Brazilian Lyrics Innovation Atlas',
        'description': 'Comprehensive analysis of innovations and what makes lyrics effective',
        'corpus_stats': {
            'total_songs': len(corpus),
            'top_outliers_analyzed': len(top_outliers),
            'sweet_spot_songs': len(sweet_spots)
        },
        'key_findings': {
            'innovation_patterns': outlier_detector.analyze_outlier_patterns(),
            'sweet_spot_characteristics': innovation_metrics.analyze_sweet_spots(sweet_spots) if sweet_spots else {},
            'temporal_trends': temporal_analyzer.identify_innovation_trends()
        },
        'key_files': {
            'sweet_spot_songs': {
                'file': 'SWEET_SPOT_SONGS.json',
                'description': 'Top songs that are BOTH innovative AND effective - study these!'
            },
            'outlier_report': {
                'file': 'outlier_report.json',
                'description': 'Statistical outliers and what makes them unique'
            },
            'innovation_metrics': {
                'file': 'innovation_metrics.json',
                'description': '4D scoring (Innovation, Authenticity, Risk, Effectiveness)'
            },
            'effectiveness_report': {
                'file': 'effectiveness_report.json',
                'description': 'What makes lyrics effective vs ineffective'
            },
            'temporal_evolution': {
                'file': 'temporal_evolution.json',
                'description': 'How Brazilian lyrics evolved over time'
            }
        },
        'usage': {
            'for_writers': 'Study SWEET_SPOT_SONGS.json to see what innovations work',
            'for_analysis': 'Use innovation_metrics.json to understand 4D scoring',
            'for_generation': 'Apply insights to balance innovation with effectiveness'
        }
    }

    index_file = output_dir / 'INNOVATION_ATLAS_INDEX.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(atlas_index, f, ensure_ascii=False, indent=2)

    # Final summary
    logger.info("="*80)
    logger.info(" INNOVATION DETECTION COMPLETE ".center(80, "="))
    logger.info("="*80)
    logger.info(f"Total songs analyzed: {len(corpus):,}")
    logger.info(f"Top outliers identified: {len(top_outliers)}")
    logger.info(f"Sweet spot songs found: {len(sweet_spots)}")
    logger.info(f"Output location: {output_dir}")
    logger.info("")
    logger.info("📁 Key Files Generated:")
    logger.info(f"  📌 {index_file.name} - Start here!")
    logger.info(f"  🎯 SWEET_SPOT_SONGS.json - Learn from these!")
    logger.info(f"  📊 innovation_metrics.json - 4D scoring system")
    logger.info(f"  🚀 outlier_report.json - Most innovative songs")
    logger.info(f"  ✅ effectiveness_report.json - What makes lyrics work")
    logger.info(f"  📅 temporal_evolution.json - How lyrics evolved")
    logger.info("")
    logger.info("💡 Next Steps:")
    logger.info("  1. Review SWEET_SPOT_SONGS.json to see what works")
    logger.info("  2. Study innovation_metrics.json to understand 4D scoring")
    logger.info("  3. Use these insights to build intelligent generator (Phase 4)")
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
