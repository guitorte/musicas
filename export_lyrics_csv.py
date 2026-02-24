#!/usr/bin/env python3
"""
Export all lyrics lines to a CSV file with deduplication and alphabetical sorting.
"""

import json
import csv
from pathlib import Path

def export_lyrics_to_csv():
    """
    Process letras_search.json and export all unique lines (versos) to a CSV file.
    """
    # Load the JSON file
    json_file = Path('letras_search.json')

    if not json_file.exists():
        print(f"Error: {json_file} not found")
        return

    print(f"Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract all lines from lyrics
    all_lines = set()  # Use set to automatically remove duplicates

    print(f"Processing {len(data)} songs...")
    for song in data:
        if 'l' in song and song['l']:  # Check if lyrics exist
            # Split by newline to get individual lines/verses
            lines = song['l'].split('\n')
            for line in lines:
                # Remove leading/trailing whitespace
                line = line.strip()
                # Only add non-empty lines
                if line:
                    all_lines.add(line)

    # Convert to sorted list
    sorted_lines = sorted(all_lines)

    print(f"Found {len(sorted_lines)} unique lines")

    # Write to CSV
    output_file = Path('lyrics_lines.csv')
    print(f"Writing to {output_file}...")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['verso'])
        # Write each line
        for line in sorted_lines:
            writer.writerow([line])

    print(f"Done! Exported {len(sorted_lines)} unique lines to {output_file}")

if __name__ == '__main__':
    export_lyrics_to_csv()
