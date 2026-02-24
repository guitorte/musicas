#!/usr/bin/env python3
"""
Export all lyrics lines to a CSV file with deduplication, similarity filtering, and alphabetical sorting.

Strategy: normalize lines by stripping punctuation/accents, then deduplicate
on the normalized key. Among duplicates, keep the "cleanest" original form.
Then compare only immediate neighbors (window=5) for any remaining near-matches.
"""

import json
import csv
import re
import unicodedata
from pathlib import Path

def normalize(line):
    """
    Create a normalized key from a line:
    - lowercase
    - remove accents
    - strip all non-alphanumeric characters (punctuation, quotes, etc.)
    - collapse whitespace
    """
    s = line.lower()
    # Remove accents: decompose unicode, drop combining marks
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    # Keep only letters, digits, spaces
    s = re.sub(r'[^a-z0-9\s]', '', s)
    # Collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def export_lyrics_to_csv():
    """
    Process letras_search.json and export all unique lines (versos) to a CSV file.
    """
    json_file = Path('letras_search.json')

    if not json_file.exists():
        print(f"Error: {json_file} not found")
        return

    print(f"Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract all lines from lyrics
    all_lines = set()

    print(f"Processing {len(data)} songs...")
    for song in data:
        if 'l' in song and song['l']:
            for line in song['l'].split('\n'):
                line = line.strip()
                if line:
                    all_lines.add(line)

    print(f"Found {len(all_lines)} unique lines (exact duplicates removed)")

    # --- Phase 1: Deduplicate by normalized key ---
    # Group lines that normalize to the same string.
    # Among each group, keep the shortest (usually the "cleanest" version).
    print("Phase 1: Deduplicating by normalized form (strips punctuation/accents)...")
    groups = {}
    for line in all_lines:
        key = normalize(line)
        if not key:  # skip lines that become empty after normalization
            continue
        if key not in groups:
            groups[key] = line
        else:
            # Keep the shorter original (less punctuation clutter)
            if len(line) < len(groups[key]):
                groups[key] = line

    deduped = sorted(groups.values())
    print(f"  {len(all_lines)} -> {len(deduped)} lines after normalization dedup")

    # --- Phase 2: Remove near-neighbors (window=5) ---
    # After sorting, lines that are ~80%+ similar will be adjacent.
    # Compare each line against the previous 5 kept lines using a fast check.
    print("Phase 2: Removing near-neighbor duplicates (window=5)...")
    kept = []
    for line in deduped:
        norm = normalize(line)
        is_dup = False
        # Check only the last 5 kept lines
        for prev in kept[-5:]:
            prev_norm = normalize(prev)
            # Quick length check
            if abs(len(norm) - len(prev_norm)) > max(len(norm), len(prev_norm)) * 0.2:
                continue
            # Check if one is a substring of the other
            if norm in prev_norm or prev_norm in norm:
                is_dup = True
                break
            # Simple ratio: count matching characters in order
            matches = sum(1 for a, b in zip(norm, prev_norm) if a == b)
            max_len = max(len(norm), len(prev_norm))
            if max_len > 0 and matches / max_len >= 0.80:
                is_dup = True
                break
        if not is_dup:
            kept.append(line)

    print(f"  {len(deduped)} -> {len(kept)} lines after neighbor dedup")

    # Write to CSV
    output_file = Path('lyrics_lines.csv')
    print(f"Writing to {output_file}...")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['verso'])
        for line in kept:
            writer.writerow([line])

    print(f"Done! Exported {len(kept)} unique lines to {output_file}")

if __name__ == '__main__':
    export_lyrics_to_csv()
