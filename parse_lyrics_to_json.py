#!/usr/bin/env python3
"""
Universal Lyrics Parser for Google Colab
Parses various lyrics file formats into a single unified JSON structure
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any


class LyricsParser:
    """Intelligent parser that handles multiple lyrics file formats"""

    def __init__(self, input_folder: str):
        self.input_folder = Path(input_folder)
        self.songs = []

    def parse_all_files(self) -> List[Dict[str, Any]]:
        """Parse all files in the input folder"""
        print(f"🔍 Scanning folder: {self.input_folder}")

        # Get all files (recursively)
        files = list(self.input_folder.rglob('*'))
        file_list = [f for f in files if f.is_file()]

        print(f"📁 Found {len(file_list)} files")

        for file_path in file_list:
            print(f"\n📄 Processing: {file_path.name}")
            try:
                self._parse_file(file_path)
            except Exception as e:
                print(f"⚠️  Error parsing {file_path.name}: {str(e)}")

        print(f"\n✅ Successfully parsed {len(self.songs)} songs")
        return self.songs

    def _parse_file(self, file_path: Path):
        """Parse a single file based on its format"""

        # Skip non-text files
        if file_path.suffix.lower() == '.pdf':
            print("   ⏭️  Skipping PDF file")
            return

        # Handle JSON files
        if file_path.suffix.lower() == '.json':
            self._parse_json_file(file_path)
            return

        # Handle text files
        if file_path.suffix.lower() in ['.txt', '']:
            self._parse_text_file(file_path)
            return

        print(f"   ⏭️  Skipping unknown file type: {file_path.suffix}")

    def _parse_json_file(self, file_path: Path):
        """Parse JSON files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, list):
                count = len(data)
                self.songs.extend(data)
                print(f"   ✓ Loaded {count} songs from JSON")
            elif isinstance(data, dict):
                self.songs.append(data)
                print(f"   ✓ Loaded 1 song from JSON")
        except Exception as e:
            print(f"   ✗ Failed to parse JSON: {str(e)}")

    def _parse_text_file(self, file_path: Path):
        """Parse text files with various formats"""
        try:
            # Try UTF-8 first
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Fallback to latin-1
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()

            # Skip empty or very small files
            if len(content.strip()) < 10:
                print(f"   ⏭️  Skipping empty/minimal file")
                return

            # Detect format and parse
            songs_found = self._detect_and_parse_format(content, file_path.name)
            print(f"   ✓ Parsed {songs_found} songs")

        except Exception as e:
            print(f"   ✗ Failed to parse text file: {str(e)}")

    def _detect_and_parse_format(self, content: str, filename: str) -> int:
        """Detect the format and parse accordingly"""

        initial_count = len(self.songs)

        # Format 1: TÍTULO/ARTISTA with === separators
        if 'TÍTULO:' in content and 'ARTISTA:' in content:
            self._parse_titulo_artista_format(content, filename)

        # Format 2: Title\nArtist\n\nLyrics with <|endoftext|> separator
        elif '<|endoftext|>' in content:
            self._parse_endoftext_format(content, filename)

        # Format 3: Generic format (try to guess structure)
        else:
            self._parse_generic_format(content, filename)

        return len(self.songs) - initial_count

    def _parse_titulo_artista_format(self, content: str, filename: str):
        """Parse format: TÍTULO: ... ARTISTA: ... --- LETRA --- ... ==="""

        # Split by separator
        separators = ['=' * 40, '=' * 30, '=' * 20]

        # Find the separator that works
        songs_text = []
        for sep in separators:
            if sep in content:
                songs_text = content.split(sep)
                break

        if not songs_text:
            songs_text = [content]  # No separator, treat as single song

        for song_text in songs_text:
            song_text = song_text.strip()
            if len(song_text) < 20:
                continue

            # Extract TÍTULO
            title_match = re.search(r'TÍTULO:\s*(.+?)(?:\n|ARTISTA:)', song_text, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Unknown Title"

            # Extract ARTISTA
            artist_match = re.search(r'ARTISTA:\s*(.+?)(?:\n|---)', song_text, re.IGNORECASE)
            artist = artist_match.group(1).strip() if artist_match else "Unknown Artist"

            # Extract LETRA (everything after --- LETRA ---)
            letra_match = re.search(r'---\s*LETRA\s*---\s*(.+)', song_text, re.DOTALL | re.IGNORECASE)
            lyrics = letra_match.group(1).strip() if letra_match else song_text

            # Clean up lyrics
            lyrics = self._clean_lyrics(lyrics)

            if lyrics:
                self.songs.append({
                    "titulo": title,
                    "artista": artist,
                    "letra": lyrics,
                    "fonte": filename
                })

    def _parse_endoftext_format(self, content: str, filename: str):
        """Parse format: Title\nArtist\n\nLyrics<|endoftext|>"""

        # Split by <|endoftext|>
        songs_text = content.split('<|endoftext|>')

        for song_text in songs_text:
            song_text = song_text.strip()
            if len(song_text) < 20:
                continue

            # Split into lines
            lines = song_text.split('\n')

            # First non-empty line is usually the title
            # Second non-empty line is usually the artist
            non_empty_lines = [line.strip() for line in lines if line.strip()]

            if len(non_empty_lines) < 2:
                continue

            title = non_empty_lines[0]
            artist = non_empty_lines[1]

            # Everything after the second line (skipping empty lines) is lyrics
            # Find where lyrics start (after first blank line)
            lyrics_start = 0
            blank_found = False
            for i, line in enumerate(lines):
                if not line.strip():
                    blank_found = True
                elif blank_found:
                    lyrics_start = i
                    break

            if lyrics_start > 0:
                lyrics = '\n'.join(lines[lyrics_start:]).strip()
            else:
                # Fallback: everything except first 2 lines
                lyrics = '\n'.join(non_empty_lines[2:]).strip()

            lyrics = self._clean_lyrics(lyrics)

            if lyrics:
                self.songs.append({
                    "titulo": title,
                    "artista": artist,
                    "letra": lyrics,
                    "fonte": filename
                })

    def _parse_generic_format(self, content: str, filename: str):
        """Generic parser for unknown formats - best effort"""

        # Try to identify song boundaries using common patterns
        # Look for patterns like: Title followed by Artist on next line

        lines = content.split('\n')

        # Simple heuristic: if file is small, treat as single song
        if len(lines) < 50:
            # Assume first line is title, second is artist
            non_empty = [line.strip() for line in lines if line.strip()]
            if len(non_empty) >= 3:
                title = non_empty[0]
                artist = non_empty[1]
                lyrics = '\n'.join(non_empty[2:])

                self.songs.append({
                    "titulo": title,
                    "artista": artist,
                    "letra": self._clean_lyrics(lyrics),
                    "fonte": filename
                })
        else:
            # For larger files, try to split by empty lines + capital letter pattern
            # This is a best-effort approach
            print(f"   ⚠️  Using generic parser (may need manual review)")

            # Treat whole content as one song with unknown structure
            self.songs.append({
                "titulo": f"Collection from {filename}",
                "artista": "Various Artists",
                "letra": self._clean_lyrics(content),
                "fonte": filename,
                "note": "File format not recognized - may need manual parsing"
            })

    def _clean_lyrics(self, lyrics: str) -> str:
        """Clean up lyrics text"""

        # Remove common artifacts
        lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Remove [Sabe de quem é...] type text
        lyrics = re.sub(r'\(/contribuicoes/.*?\)', '', lyrics)  # Remove URLs

        # Remove excessive whitespace
        lyrics = re.sub(r'\n{3,}', '\n\n', lyrics)
        lyrics = lyrics.strip()

        return lyrics

    def save_to_json(self, output_path: str, indent: int = 2):
        """Save parsed songs to JSON file"""

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.songs, f, ensure_ascii=False, indent=indent)

        print(f"\n💾 Saved {len(self.songs)} songs to: {output_file}")
        print(f"📊 File size: {output_file.stat().st_size / 1024:.2f} KB")

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about parsed songs"""

        if not self.songs:
            return {"total_songs": 0}

        artists = [song.get('artista', 'Unknown') for song in self.songs]
        sources = [song.get('fonte', 'Unknown') for song in self.songs]

        from collections import Counter

        stats = {
            "total_songs": len(self.songs),
            "unique_artists": len(set(artists)),
            "top_artists": dict(Counter(artists).most_common(10)),
            "files_processed": len(set(sources)),
            "sources": dict(Counter(sources))
        }

        return stats


# ============================================================================
# MAIN EXECUTION FOR GOOGLE COLAB
# ============================================================================

def main():
    """Main function for Google Colab"""

    print("=" * 70)
    print("🎵 UNIVERSAL LYRICS PARSER 🎵")
    print("=" * 70)

    # Configuration
    INPUT_FOLDER = "/content/letras"  # Default Colab path
    OUTPUT_FILE = "/content/all_lyrics.json"

    # Check if running in Colab
    try:
        from google.colab import drive
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False

    # If in Colab, you can mount Google Drive
    if IN_COLAB:
        print("\n🔗 Running in Google Colab")

        # Uncomment the next 2 lines if you want to use Google Drive
        # print("Mounting Google Drive...")
        # drive.mount('/content/drive')
        # INPUT_FOLDER = "/content/drive/MyDrive/letras"  # Update path as needed

    # Check if folder exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"\n❌ Folder not found: {INPUT_FOLDER}")
        print(f"\n📋 Please upload your files to: {INPUT_FOLDER}")
        print(f"   Or update INPUT_FOLDER variable in the script")
        return

    # Parse all files
    parser = LyricsParser(INPUT_FOLDER)
    songs = parser.parse_all_files()

    if not songs:
        print("\n⚠️  No songs found!")
        return

    # Save to JSON
    parser.save_to_json(OUTPUT_FILE)

    # Show statistics
    print("\n" + "=" * 70)
    print("📊 STATISTICS")
    print("=" * 70)

    stats = parser.get_statistics()
    print(f"\n📚 Total songs: {stats['total_songs']}")
    print(f"🎤 Unique artists: {stats['unique_artists']}")
    print(f"\n🔝 Top 10 Artists:")
    for artist, count in stats['top_artists'].items():
        print(f"   • {artist}: {count} songs")

    print(f"\n📁 Files processed:")
    for source, count in stats['sources'].items():
        print(f"   • {source}: {count} songs")

    print("\n" + "=" * 70)
    print("✅ DONE! Your JSON file is ready!")
    print("=" * 70)

    # Download file in Colab
    if IN_COLAB:
        print(f"\n💾 To download the file, run:")
        print(f'   from google.colab import files')
        print(f'   files.download("{OUTPUT_FILE}")')


if __name__ == "__main__":
    main()
