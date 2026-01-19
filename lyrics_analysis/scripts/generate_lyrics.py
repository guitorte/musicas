#!/usr/bin/env python3
"""
Generate Lyrics - Quality-aware Brazilian lyrics generation CLI.

This script provides a command-line interface for generating lyrics
using the Phase 4 intelligent generation system.

Usage:
    # Generate with default settings (balanced profile, MPB)
    python generate_lyrics.py

    # Generate with specific genre and profile
    python generate_lyrics.py --genre Trap --profile experimental

    # Generate with custom 4D targets
    python generate_lyrics.py --innovation 70 --effectiveness 80

    # Generate batch
    python generate_lyrics.py --count 5 --genre Sertanejo

    # List available options
    python generate_lyrics.py --list-genres
    python generate_lyrics.py --list-profiles
    python generate_lyrics.py --list-themes
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from lyrics_generator import LyricsGenerator
from innovation_controller import InnovationController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate Brazilian lyrics with quality-aware AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Generation parameters
    parser.add_argument(
        '--genre',
        type=str,
        default='MPB',
        help='Target genre (default: MPB)'
    )

    parser.add_argument(
        '--theme',
        type=str,
        default=None,
        help='Optional theme (amor_romantico, festa, sofrimento, etc.)'
    )

    parser.add_argument(
        '--profile',
        type=str,
        default='balanced',
        help='Generation profile (balanced, safe, experimental, sweet_spot, etc.)'
    )

    # Custom 4D targets (override profile)
    parser.add_argument(
        '--innovation',
        type=float,
        default=None,
        help='Innovation level (0-100)'
    )

    parser.add_argument(
        '--authenticity',
        type=float,
        default=None,
        help='Authenticity level (0-100)'
    )

    parser.add_argument(
        '--risk',
        type=float,
        default=None,
        help='Risk level (0-100)'
    )

    parser.add_argument(
        '--effectiveness',
        type=float,
        default=None,
        help='Effectiveness level (0-100)'
    )

    # Batch generation
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of lyrics to generate (default: 1)'
    )

    # Output
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file (JSON format)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode (less output)'
    )

    # List options
    parser.add_argument(
        '--list-genres',
        action='store_true',
        help='List available genres'
    )

    parser.add_argument(
        '--list-profiles',
        action='store_true',
        help='List available profiles'
    )

    parser.add_argument(
        '--list-themes',
        action='store_true',
        help='List available themes'
    )

    # Paths
    parser.add_argument(
        '--analysis-dir',
        type=str,
        default=None,
        help='Path to analysis directory'
    )

    parser.add_argument(
        '--corpus',
        type=str,
        default=None,
        help='Path to processed corpus file (for quality scoring)'
    )

    return parser.parse_args()


def load_corpus(corpus_path: str) -> list:
    """Load corpus data for quality scoring."""
    path = Path(corpus_path)

    if not path.exists():
        logger.warning(f"Corpus file not found: {corpus_path}")
        return []

    logger.info(f"Loading corpus from {corpus_path}...")

    if path.suffix == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif path.suffix == '.jsonl':
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
        return data
    else:
        logger.warning(f"Unknown corpus format: {path.suffix}")
        return []


def list_genres(generator: LyricsGenerator):
    """List available genres."""
    print("\n📚 AVAILABLE GENRES:")
    print("="*50)

    genres = generator.list_available_genres()

    for genre in genres:
        norms = generator.structure_gen.get_genre_norms(genre)
        print(f"\n  {genre}")
        print(f"    Avg lines:  {norms.get('avg_lines', 'N/A')}")
        print(f"    Avg words:  {norms.get('avg_words', 'N/A')}")
        print(f"    Chorus:     {norms.get('chorus_percentage', 'N/A')}%")

    print("\n" + "="*50 + "\n")


def list_profiles(generator: LyricsGenerator):
    """List available profiles."""
    print("\n🎛️  AVAILABLE PROFILES:")
    print("="*70)

    profiles = generator.list_available_profiles()

    for name, info in profiles.items():
        print(f"\n  {name.upper()}: {info['name']}")
        print(f"    {info['description']}")

        profile = info['profile']
        print(f"    Innovation:    {profile['innovation']:5.0f}")
        print(f"    Authenticity:  {profile['authenticity']:5.0f}")
        print(f"    Risk:          {profile['risk']:5.0f}")
        print(f"    Effectiveness: {profile['effectiveness']:5.0f}")

    print("\n" + "="*70 + "\n")


def list_themes(generator: LyricsGenerator):
    """List available themes."""
    print("\n🎨 AVAILABLE THEMES:")
    print("="*50)

    themes = generator.list_available_themes()

    for theme in themes:
        print(f"  • {theme}")

    print("\n" + "="*50 + "\n")


def save_results(results: list, output_path: str):
    """Save generation results to file."""
    path = Path(output_path)

    # Convert results to serializable format
    serializable = []

    for result in results:
        serializable.append({
            'lyrics': result['lyrics'],
            'genre': result['genre'],
            'theme': result.get('theme'),
            'target_profile': result['target_profile'],
            'final_score': {
                'summary': result['final_score']['summary'],
                'match_to_target': result['final_score'].get('match_to_target')
            },
            'structure': {
                'total_lines': result['structure']['total_lines'],
                'total_paragraphs': result['structure']['total_paragraphs'],
                'has_chorus': result['structure']['has_chorus']
            }
        })

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

    logger.info(f"✓ Results saved to {output_path}")


def main():
    """Main entry point."""
    args = parse_args()

    # Determine paths
    if args.analysis_dir:
        analysis_dir = Path(args.analysis_dir)
    else:
        # Default: ../analysis relative to script
        analysis_dir = Path(__file__).parent.parent / 'analysis'

    if not analysis_dir.exists():
        logger.error(f"Analysis directory not found: {analysis_dir}")
        sys.exit(1)

    # Load corpus if provided
    corpus_data = []
    if args.corpus:
        corpus_data = load_corpus(args.corpus)
        if corpus_data:
            logger.info(f"✓ Loaded {len(corpus_data)} songs for quality scoring")

    # Initialize generator
    try:
        generator = LyricsGenerator(
            analysis_dir=analysis_dir,
            corpus_data=corpus_data
        )
    except Exception as e:
        logger.error(f"Failed to initialize generator: {e}")
        sys.exit(1)

    # Handle list commands
    if args.list_genres:
        list_genres(generator)
        return

    if args.list_profiles:
        list_profiles(generator)
        return

    if args.list_themes:
        list_themes(generator)
        return

    # Build target profile
    controller = InnovationController()

    if any([args.innovation, args.authenticity, args.risk, args.effectiveness]):
        # Custom profile from command-line args
        target_profile = controller.create_profile(
            innovation=args.innovation if args.innovation is not None else 50,
            authenticity=args.authenticity if args.authenticity is not None else 80,
            risk=args.risk if args.risk is not None else 50,
            effectiveness=args.effectiveness if args.effectiveness is not None else 70
        )

        if not args.quiet:
            print("\n🎯 Using custom profile:")
            controller.print_profile(target_profile)
    else:
        # Use named profile
        profiles = controller.suggest_profiles()

        if args.profile not in profiles:
            logger.warning(f"Unknown profile '{args.profile}', using 'balanced'")
            args.profile = 'balanced'

        profile_info = profiles[args.profile]
        target_profile = profile_info['profile']

        if not args.quiet:
            print(f"\n🎯 Using profile: {profile_info['name']}")
            print(f"   {profile_info['description']}")
            controller.print_profile(target_profile)

    # Generate lyrics
    verbose = not args.quiet

    if args.count == 1:
        # Single generation
        result = generator.generate(
            genre=args.genre,
            target_profile=target_profile,
            theme=args.theme,
            verbose=verbose
        )

        results = [result]

    else:
        # Batch generation
        results = generator.generate_batch(
            count=args.count,
            genre=args.genre,
            target_profile=target_profile,
            theme=args.theme,
            verbose=verbose
        )

    # Save output if requested
    if args.output:
        save_results(results, args.output)

    # Print summary
    if not args.quiet:
        if args.count > 1:
            print(f"\n✅ Generated {len(results)} lyrics")

            # Show average scores
            avg_innovation = sum(r['final_score']['summary']['innovation'] for r in results) / len(results)
            avg_effectiveness = sum(r['final_score']['summary']['effectiveness'] for r in results) / len(results)
            avg_quality = sum(r['final_score']['summary']['quality'] for r in results) / len(results)

            print(f"\n📊 Average Scores:")
            print(f"  Innovation:    {avg_innovation:.1f}")
            print(f"  Effectiveness: {avg_effectiveness:.1f}")
            print(f"  Quality:       {avg_quality:.1f}")


if __name__ == '__main__':
    main()
