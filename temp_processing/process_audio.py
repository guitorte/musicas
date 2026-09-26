#!/usr/bin/env python3
"""
Script standalone para processar Job job.mp3
"""
import sys
import os

# Add modules to path
sys.path.insert(0, '/home/user/musicas/audio-restoration-pipeline')

from modules.pipeline import AudioRestorationPipeline
import json

# Configuração otimizada
CONFIG = {
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.45,  # Moderado
    'restore_frequencies': True,
    'freq_restoration_method': 'harmonic_synthesis',
    'enhance_bass': False,
    'psychoacoustic_enhancement': True,
    'separate_stems': False,
    'target_lufs': -14.0,
    'master_eq': {
        'bass': 0.2,
        'mid': 0.0,
        'presence': 0.8,
        'treble': 0.5
    },
    'add_presence': True
}

print("\n⚙️ CONFIGURAÇÃO:")
print("="*70)
print("• Noise Reduction: 0.45 (moderado)")
print("• Restauração de frequências: Sim")
print("• Target LUFS: -14.0")
print("• EQ: Bass +0.2, Presence +0.8, Treble +0.5")
print("="*70)

print("\n🎵 Processando 'Job job.mp3'...")

# Pipeline
pipeline = AudioRestorationPipeline(
    sr=44100,
    output_base_dir='/home/user/musicas/temp_processing/output',
    log_dir='/home/user/musicas/temp_processing/logs'
)

# Processar
result = pipeline.process_audio(
    '/home/user/musicas/temp_processing/Job_job.mp3',
    output_name='Job_job_restored',
    config=CONFIG
)

print("\n" + "="*70)
print("✓✓✓ SUCESSO! ✓✓✓")
print("="*70)
print(f"\n📁 Pasta: {result['output_dir']}")
print(f"\n🎵 Arquivo final:")
print(f"   {result['stages']['mastering']['output']}")

# Salvar resultado
with open('/home/user/musicas/temp_processing/result.json', 'w') as f:
    json.dump(result, f, indent=2)
