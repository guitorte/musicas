# 🎵 Pipeline Profissional de Restauração de Áudio

Pipeline automatizado completo para restauração, reconstrução e masterização de arquivos de áudio MP3 e WAV.

## ✨ Recursos

### 📊 Análise Espectral Completa
- Análise de conteúdo de frequências
- Detecção de perda de qualidade
- Identificação de ruído e clipping
- Análise de dinâmica (LUFS, crest factor)
- Visualizações detalhadas (espectrogramas, waveforms)
- Recomendações automáticas de processamento

### 🔧 Processamento Avançado
- **Redução de Ruído**: Spectral gating avançado
- **Remoção de Clicks/Pops**: Detecção e correção de artefatos
- **De-clipping**: Restauração de áudio com clipping
- **EQ Paramétrica**: 7 bandas de equalização profissional
- **Compressão Dinâmica**: Com attack/release configuráveis
- **Limitação Brick-wall**: Proteção contra clipping

### 🎼 Restauração de Frequências
- **Síntese Harmônica**: Gera harmônicos naturais para frequências perdidas
- **Extensão Espectral**: Extrapolação inteligente do espectro
- **Realce de Graves**: Melhoria controlada de frequências baixas
- **Reparação Espectral**: Correção de gaps no espectro
- **Melhorias Psicoacústicas**: Otimizações para percepção auditiva

### 🎸 Separação de Stems
- Separação em 4 componentes: **Vocal, Bateria, Baixo, Outros**
- Suporte a Demucs (state-of-the-art, requer GPU)
- Método básico usando HPSS (Harmonic-Percussive Source Separation)
- Processamento individual de stems
- Reconstrução com ganhos customizados

### 🎚️ Masterização Profissional
- Normalização LUFS (padrões de streaming)
- Cadeia completa de masterização
- Exciter para adicionar presença e brilho
- Alargamento de campo estéreo
- Limitação final transparente

## 🚀 Uso Rápido (Google Colab)

### Opção 1: Notebook Completo

1. Abra o notebook no Google Colab:
   ```
   audio-restoration-pipeline/notebooks/Audio_Restoration_Pipeline.ipynb
   ```

2. Monte seu Google Drive

3. Ajuste o caminho da pasta `00-restore`

4. Execute as células sequencialmente

### Opção 2: Código Python

```python
from modules.pipeline import AudioRestorationPipeline

# Inicializar pipeline
pipeline = AudioRestorationPipeline(
    sr=44100,
    output_base_dir='./output',
    log_dir='./logs'
)

# Processar um arquivo
result = pipeline.process_audio(
    audio_path='caminho/para/audio.mp3',
    config={
        'reduce_noise': True,
        'restore_frequencies': True,
        'target_lufs': -14.0
    }
)

print(f"Arquivo masterizado: {result['stages']['mastering']['output']}")
```

## 📦 Instalação

### Dependências Principais

```bash
pip install librosa soundfile scipy matplotlib numpy noisereduce
```

### Opcional: Demucs para Separação de Stems

```bash
pip install demucs
```

Ou use o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### Configuração Padrão

```python
config = {
    # Limpeza
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.7,  # 0.0 - 1.0

    # Restauração de Frequências
    'restore_frequencies': True,
    'freq_restoration_method': 'harmonic_synthesis',  # ou 'spectral_extension'
    'enhance_bass': False,
    'bass_enhancement_amount': 1.3,
    'psychoacoustic_enhancement': True,

    # Separação de Stems
    'separate_stems': False,
    'stem_separation_model': 'basic',  # ou 'demucs'
    'process_stems_individually': False,

    # Masterização
    'target_lufs': -14.0,  # -14 para streaming, -16 para broadcast
    'master_eq': {
        'bass': 0.5,       # dB
        'mid': 0.0,
        'presence': 1.0,
        'treble': 0.8
    },
    'add_presence': True
}
```

### Perfis Pré-configurados

#### Para Música de Streaming (Spotify, YouTube)
```python
streaming_config = {
    'reduce_noise': True,
    'noise_reduction_strength': 0.6,
    'restore_frequencies': True,
    'target_lufs': -14.0,
    'add_presence': True
}
```

#### Para Broadcast (TV, Rádio)
```python
broadcast_config = {
    'reduce_noise': True,
    'noise_reduction_strength': 0.8,
    'restore_frequencies': True,
    'target_lufs': -16.0,
    'add_presence': False
}
```

#### Para Restauração Agressiva (Áudio Antigo/Degradado)
```python
restoration_config = {
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.9,
    'restore_frequencies': True,
    'freq_restoration_method': 'spectral_extension',
    'enhance_bass': True,
    'bass_enhancement_amount': 1.5,
    'psychoacoustic_enhancement': True,
    'target_lufs': -14.0
}
```

## 📁 Estrutura de Saída

```
output/
├── nome_do_audio/
│   └── YYYYMMDD_HHMMSS/
│       ├── 01_cleaned.wav                    # Áudio limpo
│       ├── 02_frequency_restored.wav         # Com frequências restauradas
│       ├── 99_mastered_FINAL.wav            # Masterizado (FINAL)
│       ├── analysis.json                     # Análise detalhada
│       ├── analysis_visualization.png        # Visualizações
│       ├── results.json                      # Resultados do pipeline
│       └── stems/                            # Stems separados (se ativado)
│           ├── vocals.wav
│           ├── drums.wav
│           ├── bass.wav
│           └── other.wav
└── logs/                                     # Logs de execução
```

## 🎯 Casos de Uso

### 1. Análise Apenas (Sem Processamento)

```python
from modules.spectral_analysis import SpectralAnalyzer

analyzer = SpectralAnalyzer()
analysis = analyzer.analyze_audio('audio.mp3')

# Ver recomendações
for rec in analysis['recommendations']:
    print(f"[{rec['severity']}] {rec['message']}")

# Salvar visualização
analyzer.visualize_analysis('audio.mp3', 'analysis.png')
```

### 2. Processamento em Batch

```python
audio_files = ['audio1.mp3', 'audio2.wav', 'audio3.mp3']

results = pipeline.batch_process(
    audio_files,
    config=config
)

# Verificar resultados
for result in results:
    if 'error' not in result:
        print(f"✓ {result['input_path']}")
    else:
        print(f"✗ {result['input_path']}: {result['error']}")
```

### 3. Processamento com Stems

```python
config = {
    'separate_stems': True,
    'stem_separation_model': 'basic',
    'process_stems_individually': True
}

result = pipeline.process_audio('musica.mp3', config=config)

# Acessar stems
stems = result['stages']['stem_separation']
print(f"Vocal: {stems['vocals']}")
print(f"Drums: {stems['drums']}")
```

### 4. Masterização Customizada

```python
from modules.audio_processing import AudioProcessor
import librosa
import soundfile as sf

processor = AudioProcessor()
y, sr = librosa.load('audio.wav', sr=44100)

# Aplicar cadeia customizada
y = processor.reduce_noise(y, sr, reduction_strength=0.8)
y = processor.compress(y, sr, threshold_db=-18, ratio=3.0)
y = processor.apply_eq(y, sr, {
    'bass': 2.0,
    'presence': 1.5,
    'treble': 1.0
})
y = processor.normalize_lufs(y, target_lufs=-14.0)
y = processor.limit(y, threshold_db=-0.5)

sf.write('masterizado.wav', y, sr)
```

## 🔬 Módulos Individuais

### SpectralAnalyzer
Análise detalhada de características espectrais.

```python
from modules.spectral_analysis import SpectralAnalyzer

analyzer = SpectralAnalyzer(sr=44100)
analysis = analyzer.analyze_audio('audio.mp3')
```

### FrequencyRestorer
Restauração de frequências perdidas ou danificadas.

```python
from modules.frequency_restoration import FrequencyRestorer
import librosa

restorer = FrequencyRestorer(sr=44100)
y, sr = librosa.load('audio.mp3')

# Restaurar altas frequências
y_restored = restorer.restore_high_frequencies(y, sr, cutoff_freq=8000)

# Realçar graves
y_enhanced = restorer.enhance_bass(y, sr, amount=1.5)
```

### StemSeparator
Separação de componentes do áudio.

```python
from modules.stem_separation import StemSeparator

separator = StemSeparator(sr=44100)
stems = separator.separate_stems('audio.mp3', './output/stems')

# Processar stem individual
separator.process_stem_individually(
    stems['vocals'],
    'vocal_processed.wav',
    processing_func=lambda y, sr: y * 1.2  # Exemplo simples
)

# Reconstruir
separator.reconstruct_from_stems(
    stems,
    'reconstruido.wav',
    stem_gains={'vocals': 2.0, 'drums': -1.0}
)
```

### AudioProcessor
Processamento profissional de áudio.

```python
from modules.audio_processing import AudioProcessor
import librosa

processor = AudioProcessor(sr=44100)
y, sr = librosa.load('audio.mp3')

# Reduzir ruído
y = processor.reduce_noise(y, sr, reduction_strength=0.7)

# Compressão
y = processor.compress(y, sr, threshold_db=-20, ratio=4.0)

# EQ
y = processor.apply_eq(y, sr, {'bass': 1.0, 'treble': 0.5})

# Masterização completa
y = processor.master(y, sr, target_lufs=-14.0)
```

## 📊 Entendendo os Parâmetros

### LUFS (Loudness Units Full Scale)
- **-14 LUFS**: Padrão para Spotify, YouTube, Apple Music
- **-16 LUFS**: Padrão para broadcast (TV, rádio)
- **-23 LUFS**: Padrão para cinema e produção cinematográfica

### Noise Reduction Strength
- **0.3 - 0.5**: Redução suave, preserva naturalidade
- **0.6 - 0.7**: Redução moderada (recomendado)
- **0.8 - 1.0**: Redução agressiva, pode criar artefatos

### Compressão Ratio
- **2:1**: Compressão suave
- **4:1**: Compressão moderada
- **8:1+**: Limitação/compressão pesada

## 🎓 Dicas Profissionais

1. **Sempre analise primeiro**: Use a análise espectral para entender o áudio antes de processar
2. **Processamento incremental**: Não aplique todas as correções de uma vez
3. **Teste com diferentes configs**: O que funciona para um áudio pode não funcionar para outro
4. **Preserve o original**: Sempre mantenha uma cópia do arquivo original
5. **Use seus ouvidos**: Métricas são úteis, mas a qualidade sonora percebida é o que importa
6. **Menos é mais**: Não processe demais - pode degradar a qualidade
7. **Stems para mixagem**: Use separação de stems quando precisar de controle fino

## ⚠️ Limitações Conhecidas

- Separação de stems básica não é tão precisa quanto Demucs
- Demucs requer GPU e é mais lento
- Restauração agressiva pode criar artefatos
- LUFS é uma estimativa simplificada (não é BS.1770-4 completo)
- Não suporta arquivos multicanal (>2 canais)

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas de melhoria:

- Implementação de LUFS BS.1770-4 completo
- Mais métodos de restauração de frequências
- Suporte a arquivos multicanal
- Interface gráfica (GUI)
- Integração com mais modelos de separação de stems

## 📝 Licença

Este projeto é fornecido "como está" para uso educacional e profissional.

## 🙏 Agradecimentos

Construído com tecnologias de ponta:
- **librosa**: Análise de áudio
- **Demucs**: Separação de stems
- **scipy**: Processamento de sinais
- **soundfile**: I/O de áudio

---

**Desenvolvido com 🎵 para profissionais e entusiastas de áudio**
