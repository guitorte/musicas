#!/usr/bin/env python3
"""
Main script to process the Brazilian Portuguese lyrics corpus.

This script:
1. Loads all lyrics from the corpus
2. Cleans and normalizes the text
3. Extracts metadata
4. Saves to structured formats (JSON, JSONL, SQLite)
5. Generates and displays statistics
"""

import sys
from pathlib import Path
import logging
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from loader import LyricsLoader, Song
from cleaner import LyricsCleaner
from metadata import MetadataExtractor
from storage import LyricsStorage
from stats import CorpusStatistics

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main processing function."""
    parser = argparse.ArgumentParser(
        description='Process Brazilian Portuguese lyrics corpus'
    )
    parser.add_argument(
        '--corpus-path',
        type=str,
        default='../letras',
        help='Path to the lyrics corpus directory (default: ../letras)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='../lyrics_analysis/data/processed',
        help='Output directory for processed data (default: ../lyrics_analysis/data/processed)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'jsonl', 'sqlite', 'all'],
        default='all',
        help='Output format (default: all)'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Apply text cleaning (default: True)',
        default=True
    )
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='Only generate and display statistics, do not save data'
    )

    args = parser.parse_args()

    # Resolve paths
    corpus_path = Path(args.corpus_path).resolve()
    output_dir = Path(args.output_dir).resolve()

    logger.info("="*80)
    logger.info(" BRAZILIAN PORTUGUESE LYRICS PROCESSING PIPELINE ".center(80, "="))
    logger.info("="*80)
    logger.info(f"Corpus Path: {corpus_path}")
    logger.info(f"Output Directory: {output_dir}")
    logger.info(f"Output Format: {args.format}")
    logger.info("="*80 + "\n")

    # Step 1: Load corpus
    logger.info("📂 Step 1: Loading corpus...")
    loader = LyricsLoader(str(corpus_path))
    songs = loader.load_all_songs()
    logger.info(f"✓ Loaded {len(songs)} songs\n")

    if len(songs) == 0:
        logger.error("No songs found! Exiting.")
        sys.exit(1)

    # Step 2: Clean text
    if args.clean:
        logger.info("🧹 Step 2: Cleaning lyrics text...")
        cleaner = LyricsCleaner(remove_brackets=False, normalize_unicode=True)

        for song in songs:
            song.lyrics = cleaner.clean_text(song.lyrics)
            song.title = cleaner.clean_song_metadata(song.title)
            song.artist = cleaner.clean_song_metadata(song.artist)

        logger.info(f"✓ Cleaned {len(songs)} songs\n")
    else:
        logger.info("⏭️  Step 2: Skipping text cleaning\n")

    # Step 3: Extract metadata (optional enhancement)
    logger.info("🔍 Step 3: Extracting metadata...")
    extractor = MetadataExtractor()

    # Add a sample metadata extraction for first song
    if songs:
        sample_metadata = extractor.extract_metadata(songs[0])
        logger.info(f"✓ Metadata extraction ready (sample from '{songs[0].title}')")
        logger.info(f"  Detected themes: {list(sample_metadata['themes'].keys())[:5]}")
        logger.info(f"  Structure: {sample_metadata['structure']['total_lines']} lines, "
                   f"{sample_metadata['structure']['total_words']} words\n")

    # Step 4: Generate statistics
    logger.info("📊 Step 4: Generating statistics...")
    stats_generator = CorpusStatistics(songs)
    stats_generator.print_summary()

    # Save statistics
    stats_output = output_dir / 'corpus_statistics.json'
    output_dir.mkdir(parents=True, exist_ok=True)
    stats_generator.save_statistics(stats_output)
    logger.info(f"✓ Statistics saved to {stats_output}\n")

    # Step 5: Save processed data
    if not args.stats_only:
        logger.info("💾 Step 5: Saving processed data...")
        storage = LyricsStorage(str(output_dir))

        if args.format in ['json', 'all']:
            json_path = storage.save_to_json(songs)
            logger.info(f"✓ Saved to JSON: {json_path}")

        if args.format in ['jsonl', 'all']:
            jsonl_path = storage.save_to_jsonl(songs)
            logger.info(f"✓ Saved to JSONL: {jsonl_path}")

        if args.format in ['sqlite', 'all']:
            db_path = storage.save_to_sqlite(songs)
            logger.info(f"✓ Saved to SQLite: {db_path}")

        # Also export training format
        training_path = storage.export_for_training(songs)
        logger.info(f"✓ Exported for training: {training_path}\n")

    # Final summary
    logger.info("="*80)
    logger.info(" PROCESSING COMPLETE ".center(80, "="))
    logger.info("="*80)
    logger.info(f"Total songs processed: {len(songs):,}")
    if not args.stats_only:
        logger.info(f"Output location: {output_dir}")
        logger.info(f"Available formats: JSON, JSONL, SQLite, Training TXT")
    logger.info("="*80 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\nProcessing interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n\nError during processing: {e}", exc_info=True)
        sys.exit(1)
