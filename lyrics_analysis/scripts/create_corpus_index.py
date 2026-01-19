#!/usr/bin/env python3
"""
Create Corpus Index - Generate an index of all songs with title and artist only.
"""

import json
from pathlib import Path


def create_corpus_index(corpus_path: Path, output_path: Path):
    """Create index with title, artist, and metadata only (no lyrics)."""

    print(f"Loading corpus from {corpus_path}...")
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    songs = corpus['songs']
    print(f"✓ Loaded {len(songs)} songs\n")

    # Create index
    index = []

    for i, song in enumerate(songs, 1):
        index.append({
            'id': i,
            'title': song.get('title', 'Unknown'),
            'artist': song.get('artist', 'Unknown'),
            'genre': song.get('genre', 'Unknown'),
            'year': song.get('year', None),
            'featuring': song.get('featuring', None)
        })

    # Create output
    output = {
        'metadata': {
            'total_songs': len(index),
            'created_at': corpus['metadata'].get('created_at', ''),
            'corpus_version': corpus['metadata'].get('version', '1.0')
        },
        'songs': index
    }

    # Save
    print(f"Saving index to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓ Created index with {len(index)} songs\n")

    # Print summary
    print("=" * 80)
    print(" CORPUS INDEX SUMMARY ".center(80, "="))
    print("=" * 80 + "\n")

    # Genre distribution
    genre_counts = {}
    for song in index:
        genre = song['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    print("Genre Distribution:")
    for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {genre}: {count}")

    print(f"\nTotal: {len(index)} songs")
    print(f"Output: {output_path}")
    print("\n" + "=" * 80 + "\n")


if __name__ == '__main__':
    # Paths
    project_root = Path(__file__).parent.parent.parent
    corpus_path = project_root / 'lyrics_analysis' / 'data' / 'processed' / 'lyrics_corpus.json'
    output_path = project_root / 'lyrics_analysis' / 'data' / 'processed' / 'corpus_index.json'

    # Create index
    create_corpus_index(corpus_path, output_path)
