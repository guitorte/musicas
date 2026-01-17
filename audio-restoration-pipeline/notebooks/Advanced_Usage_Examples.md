# 📚 Exemplos Avançados de Uso - Google Colab

## Índice Rápido
1. [Interface Interativa](#1-interface-interativa)
2. [Auto-Configuração Inteligente](#2-auto-configuração-inteligente)
3. [Processamento Avançado Manual](#3-processamento-avançado-manual)
4. [Workflow Profissional Completo](#4-workflow-profissional-completo)

---

## 1. Interface Interativa

### Uso Básico

```python
# ════════════════════════════════════════════════════════════
# CONFIGURAÇÃO VISUAL COM WIDGETS
# ════════════════════════════════════════════════════════════

from modules import create_quick_config

# Criar interface
CONFIG = create_quick_config()

# Processar com configuração criada
result = pipeline.process_audio(
    audio_files[0],
    config=CONFIG
)
```

### Personalização Avançada

```python
# Criar interface e armazenar objeto
from modules import InteractiveConfig

interface = InteractiveConfig()
config = interface.create_interface()

# Modificar manualmente após interface
config['advanced'] = {
    'multiband_compress': True,
    'de_esser': True
}

# Processar
result = pipeline.process_audio(audio_file, config=config)
```

---

## 2. Auto-Configuração Inteligente

### Uso Simples

```python
# ════════════════════════════════════════════════════════════
# AUTO-CONFIGURAÇÃO BASEADA EM ANÁLISE
# ════════════════════════════════════════════════════════════

from modules import auto_configure, SpectralAnalyzer

# 1. Analisar áudio
analyzer = SpectralAnalyzer()
analysis = analyzer.analyze_audio(test_file)

# 2. Gerar configuração inteligente
config = auto_configure(analysis, verbose=True)

# 3. Processar
result = pipeline.process_audio(test_file, config=config)
```

### Análise em Batch

```python
# ════════════════════════════════════════════════════════════
# ANÁLISE E CONFIGURAÇÃO AUTOMÁTICA PARA MÚLTIPLOS ARQUIVOS
# ════════════════════════════════════════════════════════════

analyzer = SpectralAnalyzer()
configs = {}

# Gerar configuração específica para cada arquivo
for audio_file in audio_files:
    analysis = analyzer.analyze_audio(audio_file)
    configs[audio_file] = auto_configure(analysis, verbose=False)

# Processar cada um com sua configuração otimizada
for audio_file, config in configs.items():
    print(f"\n{'='*60}")
    print(f"Processando: {Path(audio_file).name}")
    print(f"Configuração: {config['_metadata']['recommended_preset'].upper()}")
    print(f"{'='*60}")

    result = pipeline.process_audio(audio_file, config=config)
```

### Análise Comparativa

```python
# Comparar diferentes estratégias
strategies = {
    'Auto': auto_configure(analysis, verbose=False),
    'Suave': CONFIG_SUAVE,
    'Agressivo': CONFIG_AGRESSIVO,
    'Demucs': CONFIG_DEMUCS
}

results = {}
for name, config in strategies.items():
    print(f"\n Processando com: {name}")
    results[name] = pipeline.process_audio(
        test_file,
        output_name=f"{Path(test_file).stem}_{name}",
        config=config
    )
```

---

## 3. Processamento Avançado Manual

### Compressão Multi-Banda

```python
# ════════════════════════════════════════════════════════════
# COMPRESSÃO MULTI-BANDA PROFISSIONAL
# ════════════════════════════════════════════════════════════

from modules import AdvancedAudioProcessor
import librosa
import soundfile as sf

processor = AdvancedAudioProcessor(sr=44100)

# Carregar áudio
y, sr = librosa.load(test_file, sr=44100)

# Compressão multi-banda
y_compressed = processor.multiband_compress(
    y, sr,
    bands=[
        (20, 200),      # Low - para punch de kick/bass
        (200, 1000),    # Low-Mid - para body de instrumentos
        (1000, 5000),   # Mid-High - para vocais
        (5000, 20000)   # High - para brilho
    ],
    ratios=[3.0, 4.0, 3.0, 2.0],  # Mais compressão nos médios
    thresholds=[-24, -20, -18, -20]
)

# Salvar
output_path = '/content/multiband_compressed.wav'
sf.write(output_path, y_compressed, sr)

print(f"✓ Salvo: {output_path}")
display(Audio(output_path))
```

### De-Esser para Vocais

```python
# ════════════════════════════════════════════════════════════
# DE-ESSER PROFISSIONAL
# ════════════════════════════════════════════════════════════

# Processar com stems primeiro para separar vocal
config_stems = {
    'separate_stems': True,
    'stem_separation_model': 'demucs'
}

result = pipeline.process_audio(test_file, config=config_stems)

# Pegar vocal separado
vocal_path = result['stages']['stem_separation']['vocals']
y_vocal, sr = librosa.load(vocal_path, sr=44100)

# Aplicar de-esser
processor = AdvancedAudioProcessor()
y_deessed = processor.de_esser(
    y_vocal, sr,
    freq_range=(5000, 8000),  # Range de sibilância
    threshold_db=-15,
    ratio=4.0
)

# Salvar
output_path = '/content/vocal_deessed.wav'
sf.write(output_path, y_deessed, sr)

print("🎤 ANTES (com sibilância):")
display(Audio(vocal_path))

print("\n🎤 DEPOIS (de-essed):")
display(Audio(output_path))
```

### Exciter Harmônico

```python
# ════════════════════════════════════════════════════════════
# EXCITER HARMÔNICO - Adicionar brilho e "warmth"
# ════════════════════════════════════════════════════════════

y, sr = librosa.load(test_file, sr=44100)

processor = AdvancedAudioProcessor()

# Exciter suave
y_excited = processor.harmonic_exciter(
    y, sr,
    drive=0.3,   # Quantidade de distorção harmônica
    mix=0.2      # 20% wet, 80% dry
)

# Salvar
output_path = '/content/with_exciter.wav'
sf.write(output_path, y_excited, sr)

print("🔊 ORIGINAL:")
display(Audio(test_file))

print("\n✨ COM EXCITER:")
display(Audio(output_path))
```

### Transient Shaper para Bateria

```python
# ════════════════════════════════════════════════════════════
# TRANSIENT SHAPER - Mais punch na bateria
# ════════════════════════════════════════════════════════════

# Separar bateria primeiro
result = pipeline.process_audio(test_file, config={'separate_stems': True})
drums_path = result['stages']['stem_separation']['drums']

y_drums, sr = librosa.load(drums_path, sr=44100)

# Aplicar transient shaper
processor = AdvancedAudioProcessor()
y_shaped = processor.transient_shaper(
    y_drums, sr,
    attack_gain=1.5,    # Mais punch nos ataques
    sustain_gain=0.7    # Sustain mais seco
)

# Salvar
output_path = '/content/drums_shaped.wav'
sf.write(output_path, y_shaped, sr)

print("🥁 BATERIA ORIGINAL:")
display(Audio(drums_path))

print("\n💥 BATERIA COM PUNCH:")
display(Audio(output_path))
```

### Alargamento Estéreo Avançado

```python
# ════════════════════════════════════════════════════════════
# STEREO ENHANCEMENT AVANÇADO
# ════════════════════════════════════════════════════════════

y, sr = librosa.load(test_file, sr=44100, mono=False)

# Se for mono, converter para estéreo
if len(y.shape) == 1:
    y = np.stack([y, y])

processor = AdvancedAudioProcessor()
y_wide = processor.stereo_enhance(
    y,
    width=1.7,      # 70% mais largo
    focus_freq=200  # Manter graves mono abaixo de 200Hz
)

# Salvar
output_path = '/content/stereo_wide.wav'
sf.write(output_path, y_wide.T, sr)  # Transpor para formato correto

print("🎧 Use fones de ouvido para melhor percepção!\n")

print("ORIGINAL:")
display(Audio(test_file))

print("\n🎵 STEREO ALARGADO:")
display(Audio(output_path))
```

### Auto-EQ Analyzer

```python
# ════════════════════════════════════════════════════════════
# ANÁLISE AUTOMÁTICA DE EQ
# ════════════════════════════════════════════════════════════

y, sr = librosa.load(test_file, sr=44100)

processor = AdvancedAudioProcessor()
eq_suggestions = processor.auto_eq_analyzer(y, sr)

print("📊 SUGESTÕES DE EQ BASEADAS NA ANÁLISE:")
print("="*50)

for band, gain_db in eq_suggestions.items():
    sign = "+" if gain_db > 0 else ""
    bar = "█" * int(abs(gain_db))
    print(f"{band:12s}: {sign}{gain_db:+5.1f} dB {bar}")

print("\n💡 Use essas sugestões em 'master_eq':")
print(f"master_eq = {eq_suggestions}")
```

---

## 4. Workflow Profissional Completo

### Workflow 1: Auto-Configuração + Ajustes Manuais

```python
# ════════════════════════════════════════════════════════════
# WORKFLOW HÍBRIDO: Auto + Manual
# ════════════════════════════════════════════════════════════

# PASSO 1: Análise e auto-config
analyzer = SpectralAnalyzer()
analysis = analyzer.analyze_audio(test_file)
config_base = auto_configure(analysis, verbose=True)

# PASSO 2: Ajustes manuais baseados no tipo de música
# Para música eletrônica:
if 'electronic' in Path(test_file).name.lower():
    config_base['enhance_bass'] = True
    config_base['bass_enhancement_amount'] = 1.6
    config_base['master_eq']['bass'] = 2.0

    # Adicionar processamento avançado
    config_base['advanced'] = {
        'harmonic_exciter': True,
        'stereo_enhance': True
    }

# Para vocal/acústico:
elif 'vocal' in Path(test_file).name.lower():
    config_base['advanced'] = {
        'de_esser': True,
        'multiband_compress': True
    }

# PASSO 3: Processar
result = pipeline.process_audio(test_file, config=config_base)

# PASSO 4: Processamento adicional no resultado
y_final, sr = librosa.load(result['stages']['mastering']['output'])

processor = AdvancedAudioProcessor()

# Adicionar exciter sutil
y_final = processor.harmonic_exciter(y_final, sr, drive=0.2, mix=0.1)

# Alargamento estéreo suave
if len(y_final.shape) > 1:
    y_final = processor.stereo_enhance(y_final, width=1.3)

# Salvar versão final
final_path = os.path.join(result['output_dir'], 'FINAL_ENHANCED.wav')
sf.write(final_path, y_final if len(y_final.shape) == 1 else y_final.T, sr)

print(f"✓ Processamento completo: {final_path}")
```

### Workflow 2: Processamento por Stems Customizado

```python
# ════════════════════════════════════════════════════════════
# WORKFLOW: Processamento Customizado por Stem
# ════════════════════════════════════════════════════════════

# PASSO 1: Separar stems
config_stems = {
    'separate_stems': True,
    'stem_separation_model': 'demucs',
    'process_stems_individually': False  # Não processar ainda
}

result = pipeline.process_audio(test_file, config=config_stems)
stems = result['stages']['stem_separation']

processor = AdvancedAudioProcessor()

# PASSO 2: Processar cada stem individualmente
processed_stems = {}

# VOCAL: De-esser + compressão + EQ
print("🎤 Processando VOCAL...")
y_vocal, sr = librosa.load(stems['vocals'])
y_vocal = processor.de_esser(y_vocal, sr, threshold_db=-12, ratio=5.0)
y_vocal = processor.multiband_compress(y_vocal, sr)
vocal_path = '/content/vocal_processed.wav'
sf.write(vocal_path, y_vocal, sr)
processed_stems['vocals'] = vocal_path

# DRUMS: Transient shaper + compressão
print("🥁 Processando BATERIA...")
y_drums, sr = librosa.load(stems['drums'])
y_drums = processor.transient_shaper(y_drums, sr, attack_gain=1.4, sustain_gain=0.8)
y_drums = processor.multiband_compress(
    y_drums, sr,
    ratios=[4.0, 5.0, 3.0, 2.0],  # Mais compressão nas baixas
    thresholds=[-20, -18, -22, -24]
)
drums_path = '/content/drums_processed.wav'
sf.write(drums_path, y_drums, sr)
processed_stems['drums'] = drums_path

# BASS: Exciter harmônico + limitação
print("🎸 Processando BAIXO...")
y_bass, sr = librosa.load(stems['bass'])
y_bass = processor.harmonic_exciter(y_bass, sr, drive=0.4, mix=0.3)
y_bass = processor.adaptive_dynamics(y_bass, sr, target_crest_factor=3.0)
bass_path = '/content/bass_processed.wav'
sf.write(bass_path, y_bass, sr)
processed_stems['bass'] = bass_path

# OTHER: EQ automático + stereo enhance
print("🎹 Processando OUTROS...")
y_other, sr = librosa.load(stems['other'])
eq_suggestions = processor.auto_eq_analyzer(y_other, sr)
# Aplicar sugestões de EQ (implementar aplicação de EQ)
other_path = '/content/other_processed.wav'
sf.write(other_path, y_other, sr)
processed_stems['other'] = other_path

# PASSO 3: Reconstruir
from modules import StemSeparator

separator = StemSeparator()
final_mix_path = '/content/custom_mix.wav'

# Ganhos customizados por stem
stem_gains = {
    'vocals': 0.0,    # Sem alteração
    'drums': -0.5,    # Reduzir levemente
    'bass': +1.0,     # Realçar
    'other': -1.5     # Reduzir
}

separator.reconstruct_from_stems(
    processed_stems,
    final_mix_path,
    stem_gains
)

# PASSO 4: Masterização final
from modules import AudioProcessor

final_processor = AudioProcessor()
y_mix, sr = librosa.load(final_mix_path)

# Masterização
y_mastered = final_processor.master(
    y_mix, sr,
    target_lufs=-14.0,
    master_eq={'bass': 0.5, 'mid': 0.0, 'presence': 1.5, 'treble': 1.2},
    add_presence=True
)

# Salvar versão final masterizada
mastered_path = '/content/FINAL_MASTERED_CUSTOM.wav'
sf.write(mastered_path, y_mastered, sr)

print("\n" + "="*60)
print("✓ WORKFLOW COMPLETO!")
print("="*60)
print(f"\nStems processados:")
for name, path in processed_stems.items():
    print(f"  • {name}: {path}")
print(f"\nMix reconstruído: {final_mix_path}")
print(f"Masterizado final: {mastered_path}")

# Ouvir resultado
print("\n🎧 RESULTADO FINAL:")
display(Audio(mastered_path))
```

### Workflow 3: Comparação de Múltiplas Versões

```python
# ════════════════════════════════════════════════════════════
# WORKFLOW: Comparação A/B/C/D
# ════════════════════════════════════════════════════════════

versions = {
    'Original': test_file,
    'Auto-Config': None,
    'Suave': None,
    'Demucs': None,
    'Custom': None
}

# Gerar versões
print("Gerando versões para comparação...\n")

# Auto-config
analysis = analyzer.analyze_audio(test_file)
config_auto = auto_configure(analysis, verbose=False)
result = pipeline.process_audio(test_file, output_name='version_auto', config=config_auto)
versions['Auto-Config'] = result['stages']['mastering']['output']

# Suave
result = pipeline.process_audio(test_file, output_name='version_suave', config=CONFIG_SUAVE)
versions['Suave'] = result['stages']['mastering']['output']

# Demucs
result = pipeline.process_audio(test_file, output_name='version_demucs', config=CONFIG_DEMUCS)
versions['Demucs'] = result['stages']['mastering']['output']

# Custom (seu workflow preferido)
# ... (seu código customizado)
# versions['Custom'] = custom_output_path

# Comparação
print("\n" + "="*60)
print("🎧 COMPARAÇÃO DE VERSÕES")
print("="*60)

for name, path in versions.items():
    print(f"\n📀 {name}:")
    if path:
        # Análise rápida
        y, sr = librosa.load(path, sr=44100)
        rms = np.sqrt(np.mean(y**2))
        peak = np.max(np.abs(y))
        lufs_est = -23 + 20 * np.log10(rms + 1e-10)

        print(f"   LUFS: {lufs_est:.1f} | Peak: {peak:.3f} | RMS: {rms:.4f}")
        display(Audio(path))
    else:
        print("   (não gerado)")

print("\n💡 Ouça todas as versões e escolha a melhor!")
```

---

## 💾 Salvar e Compartilhar Configurações

```python
# ════════════════════════════════════════════════════════════
# SALVAR CONFIGURAÇÕES FAVORITAS
# ════════════════════════════════════════════════════════════

import json

# Sua configuração favorita
MY_FAVORITE_CONFIG = {
    'reduce_noise': True,
    'noise_reduction_strength': 0.7,
    'restore_frequencies': True,
    'separate_stems': True,
    'stem_separation_model': 'demucs',
    'target_lufs': -14.0,
    'master_eq': {
        'bass': 1.0,
        'mid': 0.0,
        'presence': 2.0,
        'treble': 2.5
    },
    'advanced': {
        'de_esser': True,
        'harmonic_exciter': True
    }
}

# Salvar no Drive
config_path = '/content/drive/MyDrive/00-restore/my_favorite_config.json'
with open(config_path, 'w') as f:
    json.dump(MY_FAVORITE_CONFIG, f, indent=2)

print(f"✓ Configuração salva: {config_path}")

# Carregar depois
with open(config_path, 'r') as f:
    loaded_config = json.load(f)

print("✓ Configuração carregada e pronta para uso!")
```

---

**Estes exemplos cobrem todos os casos de uso profissionais do pipeline!** 🎵🚀
