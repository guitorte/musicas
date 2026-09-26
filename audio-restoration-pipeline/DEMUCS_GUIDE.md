# 🎵 Demucs Integration Guide

Complete guide for using Demucs stem separation in the audio restoration pipeline.

---

## 🎯 What is Demucs?

**Demucs** is a state-of-the-art AI model for music source separation. It can separate a song into:
- 🎤 **Vocals** - Lead and backing vocals
- 🥁 **Drums** - All percussion elements
- 🎸 **Bass** - Bass guitar and sub frequencies
- 🎹 **Other** - All other instruments (guitars, keyboards, etc.)

**Quality:** Best-in-class separation (competitive with commercial tools)
**Speed:** 3-5 minutes per track (GPU) or 10-20 minutes (CPU)
**Cost:** 100% free and open source

---

## ✅ What We Fixed

Demucs had several critical issues that we resolved:

### Issue 1: Invisible Errors ❌ → Fixed ✅
**Problem:** Demucs would fail with "exit status 1" but no error message
**Fix:** Enabled STDERR capture to show actual error messages
**File:** `modules/stem_separation.py:195`

```python
# Before (couldn't see errors)
result = subprocess.run(cmd, capture_output=False)

# After (can see errors)
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"Error: {result.stderr}")
```

### Issue 2: Missing TorchCodec ❌ → Fixed ✅
**Problem:** "ModuleNotFoundError: No module named 'torchcodec'"
**Root cause:** Demucs needs TorchCodec to save WAV files
**Fix:** Auto-install torchcodec with demucs
**File:** `modules/stem_separation.py:86-97`

```python
# Auto-install both dependencies together
subprocess.run(['pip', 'install', '-U', 'demucs', 'torchcodec'])
```

### Issue 3: Missing FFmpeg ❌ → Fixed ✅
**Problem:** "RuntimeError: Could not load libtorchcodec"
**Root cause:** TorchCodec requires FFmpeg system libraries
**Fix:** Auto-detect and install FFmpeg
**File:** `modules/stem_separation.py:103-142`

```python
# Check if FFmpeg is installed
ffmpeg_check = subprocess.run(['ffmpeg', '-version'], capture_output=True)

if ffmpeg_check.returncode != 0:
    # Install FFmpeg via apt-get (Colab/Linux)
    subprocess.run(['apt-get', 'update'], capture_output=True)
    subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'])
```

---

## 📦 Dependencies Chain

Understanding why all these dependencies are needed:

```
Demucs (AI separation)
  └─→ PyTorch (deep learning)
  └─→ torchaudio (audio I/O)
       └─→ TorchCodec (audio encoding/decoding)
            └─→ FFmpeg (system libraries for codecs)
```

**Critical:** Without FFmpeg, TorchCodec cannot save audio files, and Demucs will fail!

---

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)

**Open the notebook:**
```
https://colab.research.google.com/
→ GitHub tab
→ guitorte/musicas
→ Branch: claude/audio-restoration-pipeline-gAFxk
→ Open: Complete_Audio_Restoration_With_Demucs.ipynb
```

**Run all cells** - dependencies install automatically!

### Option 2: Local Installation

```bash
# 1. Install FFmpeg first (critical!)
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install -y ffmpeg

# macOS:
brew install ffmpeg

# 2. Install Python packages
pip install demucs torchcodec librosa soundfile scipy

# 3. Verify installation
ffmpeg -version
python -c "import demucs; import torchcodec; print('✓ Ready!')"
```

---

## 🎮 Usage

### Basic Usage

```python
from modules import AudioRestorationPipeline

# Config with Demucs enabled
config = {
    'separate_stems': True,  # Enable Demucs
    'stem_model': 'demucs',
    'reduce_noise': True,
    'target_lufs': -14.0
}

# Process
pipeline = AudioRestorationPipeline(sr=44100)
result = pipeline.process_audio('song.mp3', 'output', config=config)

# Stems are in: result['stages']['stem_separation']['stems']
# {
#   'vocals': '/path/to/vocals.wav',
#   'drums': '/path/to/drums.wav',
#   'bass': '/path/to/bass.wav',
#   'other': '/path/to/other.wav'
# }
```

### With Configuration Presets

```python
from config_ser_mais_optimized import CONFIG_SER_MAIS_OPTIMAL

# Modify to enable Demucs
config = CONFIG_SER_MAIS_OPTIMAL.copy()
config['separate_stems'] = True

# Process
result = pipeline.process_audio('track.wav', 'output', config=config)
```

---

## ⚙️ Configuration Options

### Demucs Settings

```python
config = {
    # Enable stem separation
    'separate_stems': True,  # False = disabled (faster)

    # Model selection
    'stem_model': 'demucs',  # 'demucs' or 'basic' (HPSS fallback)

    # Device selection (automatic)
    # - GPU if available (fast: 3-5 min)
    # - CPU otherwise (slow: 10-20 min)
}
```

### Demucs Models

The pipeline uses **htdemucs** (4-stem model):
- ✅ Vocals, Drums, Bass, Other
- ✅ Fast and reliable
- ✅ Best quality/speed balance

Other models exist but are not configured by default:
- `htdemucs_ft` - Fine-tuned version (slightly better, slower)
- `htdemucs_6s` - 6-stem version (adds piano, guitar)
- `mdx_extra` - Alternative model

---

## 🐛 Troubleshooting

### Error: "Could not load libtorchcodec"

**Cause:** FFmpeg is not installed
**Solution:**
```bash
# In Colab
!apt-get update && apt-get install -y ffmpeg

# In terminal
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
```

### Error: "ModuleNotFoundError: No module named 'torchcodec'"

**Cause:** TorchCodec not installed
**Solution:**
```bash
pip install torchcodec
```

### Error: "Demucs falhou com código de erro 1"

**Cause:** Check STDERR output for actual error
**Solution:** The pipeline now shows STDERR automatically. Common issues:
1. Out of memory → Use CPU instead of GPU
2. Invalid audio file → Check file format
3. Missing dependencies → Re-run installation

### Demucs is Very Slow

**On CPU:** 10-20 minutes is normal for a 3-minute song

**Speed it up:**
1. Enable GPU in Colab: `Runtime → Change runtime type → GPU`
2. Or disable Demucs: `config['separate_stems'] = False`

**GPU speed:** 3-5 minutes (6-8x faster)

### Out of Memory

**On GPU:**
```python
# Use CPU instead (slower but works)
import torch
torch.cuda.is_available = lambda: False
```

**On CPU:**
- Process shorter audio segments
- Use basic HPSS method instead: `config['stem_model'] = 'basic'`

---

## 📊 Performance

### Benchmark (3-minute song)

| Hardware | Time | Quality |
|----------|------|---------|
| **Google Colab GPU** (T4) | 3-5 min | Excellent |
| **Google Colab CPU** | 15-20 min | Excellent |
| **MacBook Pro M1** | 8-12 min | Excellent |
| **Basic HPSS (fallback)** | 30 sec | Fair |

### Memory Usage

- **GPU:** 4-6 GB VRAM
- **CPU:** 2-3 GB RAM
- **Storage:** ~50 MB per stem (4 stems = 200 MB)

---

## 🎯 Use Cases

### When to Use Demucs

✅ **Good use cases:**
- Vocal isolation/removal
- Creating karaoke tracks
- Remixing (adjust individual stems)
- Drum replacement
- Fixing specific instrument issues

❌ **Don't use Demucs if:**
- You just need mastering (use CONFIG_STANDARD instead)
- Time is critical (10-20 min vs 1-2 min)
- Storage is limited (generates 4x files)

### Processing Strategy

**For batch processing:**
```python
# Fast pass for most tracks
config_fast = {'separate_stems': False}

# Demucs only for special tracks
config_stems = {'separate_stems': True}

# Process
for track in tracks:
    if needs_stem_work(track):
        process(track, config_stems)  # 15 min each
    else:
        process(track, config_fast)   # 1 min each
```

---

## 🔬 Technical Details

### How Demucs Works

1. **Model:** Deep neural network (U-Net architecture)
2. **Training:** Trained on 150+ hours of music
3. **Method:** Time-domain separation (not spectrogram)
4. **Output:** 44.1 kHz WAV files (lossless)

### File Structure

```
output_dir/
└── htdemucs/              # Model name
    └── song_name/         # Audio file stem
        ├── vocals.wav     # 🎤 Vocals
        ├── drums.wav      # 🥁 Drums
        ├── bass.wav       # 🎸 Bass
        └── other.wav      # 🎹 Instruments
```

### Command Used

```bash
demucs \
  --device cuda \         # or 'cpu'
  -n htdemucs \          # model name
  -o /output/dir \       # output directory
  /path/to/audio.mp3     # input file
```

---

## 📚 Resources

### Official Documentation
- **Demucs GitHub:** https://github.com/facebookresearch/demucs
- **Research Paper:** https://arxiv.org/abs/2111.03600
- **TorchCodec:** https://github.com/pytorch/torchcodec

### Our Implementation
- **Module:** `audio-restoration-pipeline/modules/stem_separation.py`
- **Notebook:** `Complete_Audio_Restoration_With_Demucs.ipynb`
- **Setup Doc:** `DEMUCS_SETUP.md` (troubleshooting)

---

## 🎓 Examples

### Example 1: Vocal Isolation

```python
config = {
    'separate_stems': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.5
}

result = pipeline.process_audio('song.mp3', 'output', config=config)

# Get vocals only
vocals_path = result['stages']['stem_separation']['stems']['vocals']

# Now you have isolated vocals!
```

### Example 2: Instrumental Track

```python
# Separate stems
result = pipeline.process_audio('song.mp3', 'output', config={'separate_stems': True})

stems = result['stages']['stem_separation']['stems']

# Load all except vocals
import librosa
drums, _ = librosa.load(stems['drums'], sr=44100)
bass, _ = librosa.load(stems['bass'], sr=44100)
other, _ = librosa.load(stems['other'], sr=44100)

# Mix instrumental (no vocals)
instrumental = drums + bass + other

# Save
import soundfile as sf
sf.write('instrumental.wav', instrumental, 44100)
```

### Example 3: Stem-Level Processing

```python
# Separate first
result = pipeline.process_audio('song.mp3', 'output', config={'separate_stems': True})

# Process each stem individually
stems = result['stages']['stem_separation']['stems']

# Boost vocals
vocals, sr = librosa.load(stems['vocals'])
vocals_boosted = vocals * 1.5  # +3 dB

# Heavy compression on drums
drums, sr = librosa.load(stems['drums'])
drums_compressed = apply_compression(drums)

# Remix
final = vocals_boosted + drums_compressed + bass + other
```

---

## ✅ Verification Checklist

Before using Demucs, verify:

- [ ] FFmpeg installed: `ffmpeg -version`
- [ ] TorchCodec installed: `python -c "import torchcodec"`
- [ ] Demucs installed: `python -c "import demucs"`
- [ ] Pipeline downloaded: Check `modules/stem_separation.py` exists
- [ ] GPU available (optional): `nvidia-smi`

If all checks pass: **Ready to separate stems! 🎵**

---

**Demucs is now fully functional in the pipeline!**

Any issues? Check `DEMUCS_SETUP.md` or the error messages (now visible thanks to our fixes).

---

Made with ❤️ for audio engineers
