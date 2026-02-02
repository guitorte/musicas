# 🎵 Universal Lyrics Parser

Intelligent parser that converts **any** lyrics file format into a single unified JSON file.

## ✨ Features

- **🔍 Auto-detects** multiple file formats
- **📦 Merges** all files into a single JSON
- **🚀 Works in Google Colab** for easy cloud processing
- **🧠 Smart parsing** - handles various text formats
- **📊 Statistics** - shows what was parsed

## 🎯 What Was Parsed

Successfully parsed **6,496 songs** from your `/letras` folder:

```
📚 Total songs: 6496
🎤 Unique artists: 645
📊 File size: 15 MB

🔝 Top 10 Artists:
   • Chico Buarque: 552 songs
   • Djavan: 370 songs
   • Artista Desconhecido: 354 songs
   • Marília Mendonça: 339 songs
   • Caetano Veloso: 155 songs
   • Pablo: 133 songs
   • Sorriso Maroto: 96 songs
   • Exaltasamba: 74 songs
   • Júlio Nascimento: 68 songs
   • Natanzinho Lima: 66 songs
```

## 📋 Supported Formats

The parser intelligently detects and handles:

### Format 1: TÍTULO/ARTISTA
```
TÍTULO: Song Title
ARTISTA: Artist Name
--- LETRA ---
Lyrics here...
========================================
```

### Format 2: Title/Artist with endoftext
```
Song Title
Artist Name

Lyrics here...
<|endoftext|>
```

### Format 3: JSON Files
Already formatted JSON files are automatically merged.

### Format 4: Generic Text
Best-effort parsing for unknown formats.

## 🚀 Usage

### Option 1: Google Colab (Recommended)

1. **Upload** `Parse_Lyrics_to_JSON.ipynb` to Google Colab
2. **Upload your files** when prompted
3. **Run all cells** (Runtime → Run all)
4. **Download** the generated JSON file

[Open in Colab](https://colab.research.google.com/)

### Option 2: Local Python Script

```bash
# Update INPUT_FOLDER and OUTPUT_FILE in the script
python3 parse_lyrics_to_json.py
```

Edit these lines in `parse_lyrics_to_json.py`:
```python
INPUT_FOLDER = "/path/to/your/letras"
OUTPUT_FILE = "/path/to/output.json"
```

## 📄 Output Format

The generated JSON has this structure:

```json
[
  {
    "titulo": "Song Title",
    "artista": "Artist Name",
    "letra": "Full lyrics here...",
    "fonte": "source_file.txt"
  },
  {
    "titulo": "Another Song",
    "artista": "Another Artist",
    "letra": "More lyrics...",
    "fonte": "another_file.txt"
  }
]
```

## 🎯 Use Cases

- **Music Apps**: Build a lyrics database
- **ML/AI**: Train models on Portuguese lyrics
- **Search**: Create searchable lyrics collections
- **Analysis**: Analyze lyrical patterns and themes
- **Archive**: Preserve lyrics in structured format

## 📊 Current Output

The script has already generated `all_lyrics.json` with all songs from your `/letras` folder:

- ✅ **6,496 songs** parsed
- ✅ **645 unique artists**
- ✅ **15 MB** JSON file
- ✅ Ready to use!

## 💡 Tips

- **Mixed formats**: Throw any combination of files - the parser handles them all
- **Subfolders**: Files in subfolders are automatically processed
- **Large files**: The parser efficiently handles large files (tested with 1MB+ files)
- **Encoding**: Automatically handles UTF-8 and Latin-1 encodings
- **PDFs**: PDF files are automatically skipped (only text/JSON supported)

## 🔧 Customization

You can modify the parser to add:

- Custom fields (genre, year, album, etc.)
- Different cleaning rules
- Additional format detection
- Custom output formats (CSV, SQL, etc.)

## 📝 Files Included

- `parse_lyrics_to_json.py` - Standalone Python script
- `Parse_Lyrics_to_JSON.ipynb` - Google Colab notebook
- `all_lyrics.json` - Generated output (6,496 songs)
- `README_PARSER.md` - This file

## 🎉 Success!

Your lyrics have been successfully parsed into a single, usable JSON file. You can now:

1. ✅ Use `all_lyrics.json` directly in your projects
2. ✅ Upload more files and re-run the parser anytime
3. ✅ Share the Colab notebook with others
4. ✅ Build apps, train models, or analyze the data

---

**Made with ❤️ for organizing lyrics**
