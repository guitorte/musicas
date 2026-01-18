# 🎵 Brazilian Portuguese Lyrics Analysis Pipeline

A modular, extensible pipeline for analyzing Brazilian Portuguese song lyrics and generating new lyrics based on learned patterns.

## 📋 Project Overview

This project processes a corpus of Brazilian song lyrics across multiple genres (MPB, Sertanejo, Pagode, Trap, Arrocha, etc.) to:

1. **Phase 1 (Current)**: Data processing and analysis
   - Load and parse lyrics from various text formats
   - Clean and normalize Brazilian Portuguese text
   - Extract metadata and structural information
   - Generate comprehensive corpus statistics
   - Export to structured formats (JSON, JSONL, SQLite)

2. **Phase 2 (Future)**: Advanced NLP analysis
   - POS tagging and dependency parsing
   - Named entity recognition
   - Sentiment analysis
   - Rhyme and meter detection
   - Topic modeling

3. **Phase 3 (Future)**: Lyrics generation
   - Fine-tune language models on Brazilian Portuguese lyrics
   - Genre-specific text generation
   - Conditional generation (by artist, genre, theme)

## 🏗️ Project Structure

```
lyrics_analysis/
├── data/
│   ├── raw/              # Original corpus (not tracked in git)
│   ├── processed/        # Processed data (JSON, SQLite, etc.)
│   └── cache/            # Temporary processing files
├── src/
│   ├── __init__.py
│   ├── loader.py         # Multi-format lyrics loader
│   ├── cleaner.py        # Text cleaning and normalization
│   ├── metadata.py       # Metadata extraction
│   ├── storage.py        # Save to JSON/SQLite/training format
│   └── stats.py          # Corpus statistics
├── scripts/
│   └── process_corpus.py # Main processing script
├── tests/
│   └── __init__.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- The lyrics corpus in `../letras/` directory

### Installation

1. Clone the repository:
```bash
cd lyrics_analysis
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: Phase 1 uses only Python standard library, so no external dependencies are strictly required yet.

### Running the Pipeline

Process the entire corpus with default settings:

```bash
cd scripts
python process_corpus.py
```

The script will:
1. Load all lyrics from `../letras/`
2. Clean and normalize the text
3. Extract metadata
4. Generate and display statistics
5. Save processed data to `../lyrics_analysis/data/processed/`

### Command Line Options

```bash
python process_corpus.py --help

Options:
  --corpus-path PATH    Path to lyrics directory (default: ../letras)
  --output-dir PATH     Output directory (default: ../lyrics_analysis/data/processed)
  --format FORMAT       Output format: json, jsonl, sqlite, all (default: all)
  --clean               Apply text cleaning (default: True)
  --stats-only          Only generate statistics, don't save data
```

Examples:

```bash
# Only generate statistics
python process_corpus.py --stats-only

# Save only to JSON format
python process_corpus.py --format json

# Use custom paths
python process_corpus.py --corpus-path /path/to/lyrics --output-dir /path/to/output
```

## 📊 Output Formats

The pipeline generates multiple output formats:

### 1. JSON (lyrics_corpus.json)
Complete corpus with metadata in a single JSON file:
```json
{
  "metadata": {
    "total_songs": 4185,
    "created_at": "2024-01-18T10:30:00",
    "version": "1.0"
  },
  "songs": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "lyrics": "Full lyrics...",
      "genre": "MPB",
      "featuring": "Featured Artist"
    }
  ]
}
```

### 2. JSON Lines (lyrics_corpus.jsonl)
One song per line for efficient streaming:
```json
{"title": "Song 1", "artist": "Artist", "lyrics": "..."}
{"title": "Song 2", "artist": "Artist", "lyrics": "..."}
```

### 3. SQLite (lyrics_corpus.db)
Relational database with `songs` and `metadata` tables. Query with:

```python
import sqlite3
conn = sqlite3.connect('data/processed/lyrics_corpus.db')
cursor = conn.cursor()

# Find all songs by an artist
cursor.execute("SELECT title, genre FROM songs WHERE artist = ?", ("Marília Mendonça",))

# Get all MPB songs
cursor.execute("SELECT * FROM songs WHERE genre = 'MPB' LIMIT 10")
```

### 4. Training Format (training_corpus.txt)
Plain text format suitable for language model training:
```
### Song Title - Artist Name [Genre]

Full lyrics here...

================================================================================
```

### 5. Statistics (corpus_statistics.json)
Comprehensive corpus statistics including:
- Overview (total songs, artists, genres)
- Text statistics (words, characters, lines)
- Vocabulary analysis
- Genre breakdown
- Top artists

## 📈 Sample Statistics

After processing the corpus (~4,185 songs), you'll see statistics like:

```
📊 OVERVIEW
Total Songs: 4,185
Unique Artists: 1,234
Unique Genres: 6
Average Words per Song: 156.3

📚 VOCABULARY
Total Word Tokens: 654,321
Unique Words: 45,678
Vocabulary Richness: 0.0698

🎵 BY GENRE
MPB                 :  856 songs | 156 artists | Avg 178 words/song
Sertanejo          :  723 songs |  89 artists | Avg 142 words/song
Trap               :  654 songs | 234 artists | Avg 134 words/song
```

## 🔧 Module Documentation

### loader.py
- `LyricsLoader`: Handles multiple file formats
  - Simple format: `Title\nArtist\n\nLyrics<|endoftext|>`
  - Structured format: `TÍTULO: ...\nARTISTA: ...\n--- LETRA ---`
- `Song`: Data class representing a song with metadata
- Auto-detects format and genre from filename

### cleaner.py
- `LyricsCleaner`: Text cleaning and normalization
  - Removes noise patterns (URLs, contribution prompts)
  - Normalizes Unicode (preserves Portuguese diacritics)
  - Cleans excessive whitespace
  - Optional bracket removal
- `extract_chorus()`: Detect repeated sections

### metadata.py
- `MetadataExtractor`: Enhanced metadata extraction
  - Structural analysis (lines, words, paragraphs)
  - Theme detection (amor, sofrimento, festa, etc.)
  - Language analysis (pronoun usage, common words)
  - Named entity extraction (simple capitalization-based)

### storage.py
- `LyricsStorage`: Multiple output format support
  - JSON: Complete corpus in single file
  - JSONL: Streaming-friendly line-delimited format
  - SQLite: Relational database
  - Training TXT: Plain text for LM training

### stats.py
- `CorpusStatistics`: Comprehensive statistics
  - Overview stats
  - Genre-based analysis
  - Artist rankings
  - Text and vocabulary statistics
  - Formatted console output

## 🎯 Use Cases

1. **Music Research**: Analyze trends in Brazilian music lyrics
2. **NLP Projects**: Portuguese language processing experiments
3. **Text Generation**: Train models to generate new lyrics
4. **Cultural Analysis**: Study themes and language in Brazilian music
5. **Educational**: Learn about corpus processing and NLP

## 🔮 Future Enhancements (Phases 2 & 3)

### Phase 2: Advanced NLP
- [ ] Integrate spaCy for Portuguese NLP
- [ ] POS tagging and dependency parsing
- [ ] Named entity recognition (artists, places, etc.)
- [ ] Sentiment analysis per song and genre
- [ ] Rhyme scheme detection
- [ ] Meter and rhythm analysis
- [ ] Topic modeling with LDA
- [ ] Word embeddings visualization

### Phase 3: Text Generation
- [ ] Fine-tune GPT-2/GPT-3 on corpus
- [ ] Genre-conditional generation
- [ ] Artist style transfer
- [ ] Interactive lyrics generator
- [ ] Rhyme-aware generation
- [ ] Theme-based generation
- [ ] Evaluation metrics for generated lyrics

## 📝 Data Format Reference

The corpus contains lyrics in various formats:

**Format 1** (Most common):
```
Title (part. Featuring Artist)
Artist Name

Lyrics text here...
More lyrics...
<|endoftext|>
```

**Format 2** (Arrocha):
```
TÍTULO: Song Title
ARTISTA: Artist Name
--- LETRA ---
Lyrics text here...
========================================
```

The loader automatically detects and parses both formats.

## 🤝 Contributing

This is a modular pipeline designed for extension. To add new features:

1. Add new modules in `src/`
2. Update `process_corpus.py` to integrate
3. Write tests in `tests/`
4. Update this README

## 📄 License

This project is for educational and research purposes.

## 🙏 Acknowledgments

- Corpus sources: Various Brazilian music lyrics websites
- Genres covered: MPB, Sertanejo, Pagode, Trap, Arrocha, and more
- Total corpus: ~4,185 songs from 1,000+ artists

## 📞 Support

For issues or questions, please open an issue in the GitHub repository.

---

**Status**: Phase 1 Complete ✅
**Next**: Phase 2 - Advanced NLP Analysis
**Version**: 0.1.0
