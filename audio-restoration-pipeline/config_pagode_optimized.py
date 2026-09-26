"""
Configuração Otimizada para "É o gás - pagode.mp3"

Baseado na análise:
- SNR: 8.3 dB (muito ruído)
- LUFS: -38.8 (muito baixo)
- Sem perda de frequências altas
- Gênero: Pagode (precisa preservar percussão e vocal)
"""

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO OTIMIZADA SEM DEMUCS (Mais Rápida)
# ═══════════════════════════════════════════════════════════════
CONFIG_PAGODE_FAST = {
    # Limpeza
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.6,  # Moderado-Alto (SNR muito baixo)

    # Restauração de Frequências
    'restore_frequencies': True,  # Sim, mesmo sem perda detectada (melhora brilho)
    'freq_restoration_method': 'harmonic_synthesis',
    'enhance_bass': True,  # Importante para pagode (surdo, pandeiro)
    'bass_enhancement_amount': 1.3,
    'psychoacoustic_enhancement': True,

    # Sem Demucs (mais rápido, sem FFmpeg)
    'separate_stems': False,
    'process_stems_individually': False,

    # Masterização otimizada para pagode
    'target_lufs': -14.0,  # Padrão streaming
    'master_eq': {
        'bass': 1.0,       # Boost para surdo/baixo
        'mid': 0.5,        # Leve boost para cavaco/violão
        'presence': 2.0,   # Importante para vocal de pagode
        'treble': 1.5      # Pandeiro/agogô precisam de brilho
    },
    'add_presence': True  # Realçar vocal
}

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO COM DEMUCS (Máxima Qualidade)
# Requer: FFmpeg instalado (!apt-get install -y ffmpeg)
# ═══════════════════════════════════════════════════════════════
CONFIG_PAGODE_DEMUCS = {
    # Limpeza (aplicada antes da separação)
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.5,  # Mais suave (Demucs vai limpar depois)

    # Sem restauração de frequências antes (Demucs preserva melhor)
    'restore_frequencies': False,
    'enhance_bass': False,
    'psychoacoustic_enhancement': False,

    # Demucs ativado
    'separate_stems': True,
    'stem_separation_model': 'demucs',
    'process_stems_individually': True,  # Processa vocal, drums, bass, other separadamente

    # Masterização
    'target_lufs': -14.0,
    'master_eq': {
        'bass': 0.8,
        'mid': 0.3,
        'presence': 1.5,
        'treble': 1.2
    },
    'add_presence': True
}

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO MUITO AGRESSIVA (Se o ruído for insuportável)
# ═══════════════════════════════════════════════════════════════
CONFIG_PAGODE_AGGRESSIVE = {
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.75,  # Muito alto (pode criar artefatos)

    'restore_frequencies': True,
    'freq_restoration_method': 'spectral_extension',  # Mais agressivo
    'enhance_bass': True,
    'bass_enhancement_amount': 1.5,
    'psychoacoustic_enhancement': True,

    'separate_stems': False,

    'target_lufs': -14.0,
    'master_eq': {
        'bass': 1.5,
        'mid': 0.0,
        'presence': 2.5,
        'treble': 2.0
    },
    'add_presence': True
}

# ═══════════════════════════════════════════════════════════════
# COMO USAR NO COLAB
# ═══════════════════════════════════════════════════════════════

INSTRUCOES = """
# ════════════════════════════════════════════════════════════
# OPÇÃO 1: SEM DEMUCS (Recomendado - Rápido)
# ════════════════════════════════════════════════════════════

import sys
sys.path.insert(0, '/content/audio-pipeline-repo/audio-restoration-pipeline')

from modules import AudioRestorationPipeline
exec(open('/content/audio-pipeline-repo/audio-restoration-pipeline/config_pagode_optimized.py').read())

pipeline = AudioRestorationPipeline(
    sr=44100,
    output_base_dir='/content/drive/MyDrive/00-restore/restored_output'
)

# Usar configuração otimizada para pagode
CONFIG = CONFIG_PAGODE_FAST  # ⭐ Ou CONFIG_PAGODE_AGGRESSIVE se ruído muito alto

result = pipeline.process_audio(
    '/content/drive/MyDrive/00-restore/É o gás - pagode.mp3',
    config=CONFIG
)

print(f"✓ Arquivo final: {result['stages']['mastering']['output']}")

# ════════════════════════════════════════════════════════════
# OPÇÃO 2: COM DEMUCS (Máxima Qualidade)
# ════════════════════════════════════════════════════════════

# PRIMEIRO: Instalar FFmpeg
!apt-get update && apt-get install -y ffmpeg

# Depois processar:
CONFIG = CONFIG_PAGODE_DEMUCS

result = pipeline.process_audio(
    '/content/drive/MyDrive/00-restore/É o gás - pagode.mp3',
    config=CONFIG
)

# ════════════════════════════════════════════════════════════
# COMPARAÇÃO DOS CONFIGS
# ════════════════════════════════════════════════════════════

FAST:        Noise 0.6, Sem Demucs, 2-3min, ⭐⭐⭐⭐
DEMUCS:      Noise 0.5, Com Demucs, 15-20min, ⭐⭐⭐⭐⭐
AGGRESSIVE:  Noise 0.75, Sem Demucs, 2-3min, ⭐⭐⭐ (pode ter artefatos)

RECOMENDAÇÃO: Comece com FAST. Se não ficar bom, tente AGGRESSIVE.
              Use DEMUCS apenas se tiver GPU e tempo.
"""

if __name__ == '__main__':
    print(INSTRUCOES)
