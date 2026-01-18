"""
Storage module for saving processed lyrics data.
Supports JSON and SQLite formats.
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class LyricsStorage:
    """Handles saving and loading lyrics data in various formats."""

    def __init__(self, output_dir: str):
        """
        Initialize storage handler.

        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_to_json(self, songs: List['Song'], filename: str = 'lyrics_corpus.json') -> Path:
        """
        Save songs to JSON file.

        Args:
            songs: List of Song objects
            filename: Output filename

        Returns:
            Path to created file
        """
        output_path = self.output_dir / filename

        # Convert songs to dictionaries
        data = {
            'metadata': {
                'total_songs': len(songs),
                'created_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'songs': [song.to_dict() for song in songs]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved {len(songs)} songs to {output_path}")
        return output_path

    def save_to_jsonl(self, songs: List['Song'], filename: str = 'lyrics_corpus.jsonl') -> Path:
        """
        Save songs to JSON Lines format (one JSON object per line).
        More efficient for large datasets and streaming.

        Args:
            songs: List of Song objects
            filename: Output filename

        Returns:
            Path to created file
        """
        output_path = self.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            for song in songs:
                json.dump(song.to_dict(), f, ensure_ascii=False)
                f.write('\n')

        logger.info(f"Saved {len(songs)} songs to {output_path} (JSONL format)")
        return output_path

    def save_to_sqlite(self, songs: List['Song'], filename: str = 'lyrics_corpus.db') -> Path:
        """
        Save songs to SQLite database.

        Args:
            songs: List of Song objects
            filename: Output filename

        Returns:
            Path to created database
        """
        output_path = self.output_dir / filename

        # Create connection
        conn = sqlite3.connect(output_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                lyrics TEXT NOT NULL,
                source_file TEXT,
                genre TEXT,
                year INTEGER,
                featuring TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert songs
        for song in songs:
            cursor.execute('''
                INSERT INTO songs (title, artist, lyrics, source_file, genre, year, featuring)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                song.title,
                song.artist,
                song.lyrics,
                song.source_file,
                song.genre,
                song.year,
                song.featuring
            ))

        # Insert metadata
        cursor.execute('''
            INSERT OR REPLACE INTO metadata (key, value)
            VALUES (?, ?)
        ''', ('total_songs', str(len(songs))))

        cursor.execute('''
            INSERT OR REPLACE INTO metadata (key, value)
            VALUES (?, ?)
        ''', ('created_at', datetime.now().isoformat()))

        conn.commit()
        conn.close()

        logger.info(f"Saved {len(songs)} songs to SQLite database: {output_path}")
        return output_path

    def load_from_json(self, filename: str = 'lyrics_corpus.json') -> List[Dict]:
        """
        Load songs from JSON file.

        Args:
            filename: Input filename

        Returns:
            List of song dictionaries
        """
        input_path = self.output_dir / filename

        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        songs = data.get('songs', [])
        logger.info(f"Loaded {len(songs)} songs from {input_path}")
        return songs

    def load_from_jsonl(self, filename: str = 'lyrics_corpus.jsonl') -> List[Dict]:
        """
        Load songs from JSON Lines file.

        Args:
            filename: Input filename

        Returns:
            List of song dictionaries
        """
        input_path = self.output_dir / filename
        songs = []

        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    songs.append(json.loads(line))

        logger.info(f"Loaded {len(songs)} songs from {input_path}")
        return songs

    def export_for_training(self, songs: List['Song'], filename: str = 'training_corpus.txt') -> Path:
        """
        Export lyrics in plain text format suitable for language model training.

        Args:
            songs: List of Song objects
            filename: Output filename

        Returns:
            Path to created file
        """
        output_path = self.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            for song in songs:
                # Write with metadata header
                f.write(f"### {song.title} - {song.artist}")
                if song.genre:
                    f.write(f" [{song.genre}]")
                f.write("\n\n")

                # Write lyrics
                f.write(song.lyrics)
                f.write("\n\n" + "="*80 + "\n\n")

        logger.info(f"Exported {len(songs)} songs for training: {output_path}")
        return output_path
