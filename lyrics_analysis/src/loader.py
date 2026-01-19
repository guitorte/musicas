"""
Data loader module for handling different lyrics file formats.
Supports multiple formats found in the Brazilian lyrics corpus.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Song:
    """Represents a single song with its metadata and lyrics."""
    title: str
    artist: str
    lyrics: str
    source_file: str
    genre: Optional[str] = None
    year: Optional[int] = None
    featuring: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert Song to dictionary."""
        return {
            'title': self.title,
            'artist': self.artist,
            'lyrics': self.lyrics,
            'source_file': self.source_file,
            'genre': self.genre,
            'year': self.year,
            'featuring': self.featuring
        }


class LyricsLoader:
    """Handles loading and parsing lyrics from different file formats."""

    # Different separators used in the corpus
    SEPARATOR_ENDOFTEXT = "<|endoftext|>"
    SEPARATOR_EQUALS = "=" * 40

    def __init__(self, corpus_path: str):
        """
        Initialize the lyrics loader.

        Args:
            corpus_path: Path to the directory containing lyrics files
        """
        self.corpus_path = Path(corpus_path)
        if not self.corpus_path.exists():
            raise ValueError(f"Corpus path does not exist: {corpus_path}")

    def load_all_songs(self) -> List[Song]:
        """
        Load all songs from all text files in the corpus.

        Returns:
            List of Song objects
        """
        all_songs = []
        txt_files = list(self.corpus_path.glob("*.txt"))

        logger.info(f"Found {len(txt_files)} text files to process")

        for txt_file in txt_files:
            if txt_file.name == "001.txt":  # Skip test file
                continue

            logger.info(f"Processing: {txt_file.name}")
            songs = self._load_file(txt_file)
            all_songs.extend(songs)
            logger.info(f"  Loaded {len(songs)} songs")

        logger.info(f"Total songs loaded: {len(all_songs)}")
        return all_songs

    def _load_file(self, file_path: Path) -> List[Song]:
        """
        Load songs from a single file, auto-detecting format.

        Args:
            file_path: Path to the lyrics file

        Returns:
            List of Song objects from this file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try latin-1 encoding as fallback
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()

        # Infer genre from filename
        genre = self._infer_genre(file_path.name)

        # Detect format and parse accordingly
        if self.SEPARATOR_EQUALS in content:
            return self._parse_structured_format(content, file_path.name, genre)
        else:
            return self._parse_simple_format(content, file_path.name, genre)

    def _parse_simple_format(self, content: str, source_file: str, genre: Optional[str]) -> List[Song]:
        """
        Parse simple format: Title\nArtist\n\nLyrics\n<|endoftext|>

        Args:
            content: File content
            source_file: Name of source file
            genre: Inferred genre

        Returns:
            List of Song objects
        """
        songs = []
        entries = content.split(self.SEPARATOR_ENDOFTEXT)

        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            lines = entry.split('\n')
            if len(lines) < 3:
                continue

            # First line: title (may include featuring)
            title_line = lines[0].strip()
            title, featuring = self._extract_featuring(title_line)

            # Second line: artist
            artist = lines[1].strip()

            # Rest: lyrics (skip empty lines at start)
            lyrics_start = 2
            while lyrics_start < len(lines) and not lines[lyrics_start].strip():
                lyrics_start += 1

            lyrics = '\n'.join(lines[lyrics_start:]).strip()

            if title and artist and lyrics:
                songs.append(Song(
                    title=title,
                    artist=artist,
                    lyrics=lyrics,
                    source_file=source_file,
                    genre=genre,
                    featuring=featuring
                ))

        return songs

    def _parse_structured_format(self, content: str, source_file: str, genre: Optional[str]) -> List[Song]:
        """
        Parse structured format: TÍTULO: ...\nARTISTA: ...\n--- LETRA ---\n...\n====...

        Args:
            content: File content
            source_file: Name of source file
            genre: Inferred genre

        Returns:
            List of Song objects
        """
        songs = []
        entries = content.split(self.SEPARATOR_EQUALS)

        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            # Extract title
            title_match = re.search(r'TÍTULO:\s*(.+?)(?:\n|$)', entry, re.IGNORECASE)
            if not title_match:
                continue
            title_line = title_match.group(1).strip()
            title, featuring = self._extract_featuring(title_line)

            # Extract artist
            artist_match = re.search(r'ARTISTA:\s*(.+?)(?:\n|$)', entry, re.IGNORECASE)
            if not artist_match:
                continue
            artist = artist_match.group(1).strip()

            # Extract lyrics (after --- LETRA ---)
            letra_match = re.search(r'---\s*LETRA\s*---\s*\n(.+)', entry, re.IGNORECASE | re.DOTALL)
            if not letra_match:
                continue
            lyrics = letra_match.group(1).strip()

            if title and artist and lyrics:
                songs.append(Song(
                    title=title,
                    artist=artist,
                    lyrics=lyrics,
                    source_file=source_file,
                    genre=genre,
                    featuring=featuring
                ))

        return songs

    def _extract_featuring(self, title: str) -> tuple[str, Optional[str]]:
        """
        Extract featuring artists from title.

        Args:
            title: Song title possibly containing featuring info

        Returns:
            Tuple of (clean_title, featuring_artists)
        """
        # Match patterns like (part. Artist), (feat. Artist), (ft. Artist)
        patterns = [
            r'\((?:part\.|feat\.|ft\.)\s*(.+?)\)',
            r'\[(?:part\.|feat\.|ft\.)\s*(.+?)\]'
        ]

        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                featuring = match.group(1).strip()
                clean_title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()
                return clean_title, featuring

        return title, None

    def _infer_genre(self, filename: str) -> Optional[str]:
        """
        Infer genre from filename.

        Args:
            filename: Name of the lyrics file

        Returns:
            Genre string or None
        """
        filename_lower = filename.lower()

        genre_map = {
            'arrocha': 'Arrocha',
            'pagode': 'Pagode',
            'mpb': 'MPB',
            'trap': 'Trap',
            'sertanejo': 'Sertanejo',
            'funk': 'Funk',
            'samba': 'Samba',
            'bossa': 'Bossa Nova',
            'forro': 'Forró',
            'axe': 'Axé'
        }

        # Also check for artist names
        artist_map = {
            'marilia': 'Sertanejo',
            'chico': 'MPB',
            'djavan': 'MPB'
        }

        for key, genre in genre_map.items():
            if key in filename_lower:
                return genre

        for key, genre in artist_map.items():
            if key in filename_lower:
                return genre

        return None
