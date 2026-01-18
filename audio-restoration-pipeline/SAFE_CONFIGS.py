"""
Configurações Seguras e Conservadoras para Preservar Qualidade
Use estas configurações quando quiser PRESERVAR a qualidade máxima
"""

# ═══════════════════════════════════════════════════════════════
# ULTRA CONSERVADOR - Mínimo Processamento
# Use quando o áudio já está bom e só precisa de masterização
# ═══════════════════════════════════════════════════════════════
CONFIG_ULTRA_SAFE = {
    'remove_clicks': True,  # Apenas remove clicks óbvios
    'reduce_noise': False,  # NÃO aplica noise reduction
    'noise_reduction_strength': 0.0,
    'restore_frequencies': False,  # NÃO mexe nas frequências
    'freq_restoration_method': 'harmonic_synthesis',
    'enhance_bass': False,
    'psychoacoustic_enhancement': False,  # NÃO aplica melhorias psicoacústicas
    'separate_stems': False,  # NÃO separa stems
    'target_lufs': -14.0,  # Apenas normaliza volume
    'master_eq': {
        'bass': 0.0,      # SEM boost/cut
        'mid': 0.0,       # SEM boost/cut
        'presence': 0.0,  # SEM boost/cut
        'treble': 0.0     # SEM boost/cut
    },
    'add_presence': False  # NÃO adiciona presença artificial
}

# ═══════════════════════════════════════════════════════════════
# CONSERVADOR - Processamento Leve
# Limpa o áudio mas preserva o caráter original
# ═══════════════════════════════════════════════════════════════
CONFIG_CONSERVATIVE = {
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.3,  # MUITO suave (era 0.6-0.7)
    'restore_frequencies': True,
    'freq_restoration_method': 'harmonic_synthesis',
    'enhance_bass': False,
    'psychoacoustic_enhancement': True,
    'separate_stems': False,
    'target_lufs': -14.0,
    'master_eq': {
        'bass': 0.0,
        'mid': 0.0,
        'presence': 0.5,  # Apenas leve realce
        'treble': 0.3     # Apenas leve realce
    },
    'add_presence': False  # Não força presença
}

# ═══════════════════════════════════════════════════════════════
# DEMUCS QUALITY - Máxima qualidade com separação de stems
# IMPORTANTE: Requer GPU, demora 10-20 minutos
# Separa stems mas com processamento MÍNIMO
# ═══════════════════════════════════════════════════════════════
CONFIG_DEMUCS_QUALITY = {
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.4,  # Moderado mas seguro
    'restore_frequencies': True,
    'freq_restoration_method': 'harmonic_synthesis',
    'enhance_bass': False,
    'psychoacoustic_enhancement': True,
    'separate_stems': True,
    'stem_separation_model': 'demucs',
    'process_stems_individually': True,  # Processa cada stem separadamente
    'target_lufs': -14.0,
    'master_eq': {
        'bass': 0.0,
        'mid': 0.0,
        'presence': 1.0,  # Moderado
        'treble': 0.5     # Suave
    },
    'add_presence': True
}

# ═══════════════════════════════════════════════════════════════
# MASTERING ONLY - Apenas Masterização
# Não faz limpeza, apenas normaliza e aplica EQ de masterização
# ═══════════════════════════════════════════════════════════════
CONFIG_MASTERING_ONLY = {
    'remove_clicks': False,
    'reduce_noise': False,
    'noise_reduction_strength': 0.0,
    'restore_frequencies': False,
    'enhance_bass': False,
    'psychoacoustic_enhancement': False,
    'separate_stems': False,
    'target_lufs': -14.0,
    'master_eq': {
        'bass': 0.3,
        'mid': 0.0,
        'presence': 0.8,
        'treble': 0.5
    },
    'add_presence': False
}

# ═══════════════════════════════════════════════════════════════
# ANÁLISE - Apenas analisa sem processar
# Para ver os problemas antes de decidir o processamento
# ═══════════════════════════════════════════════════════════════
CONFIG_ANALYSIS_ONLY = {
    'remove_clicks': False,
    'reduce_noise': False,
    'noise_reduction_strength': 0.0,
    'restore_frequencies': False,
    'enhance_bass': False,
    'psychoacoustic_enhancement': False,
    'separate_stems': False,
    'target_lufs': -14.0,  # Apenas normaliza volume
    'master_eq': {
        'bass': 0.0,
        'mid': 0.0,
        'presence': 0.0,
        'treble': 0.0
    },
    'add_presence': False
}

# ═══════════════════════════════════════════════════════════════
# GUIA DE USO
# ═══════════════════════════════════════════════════════════════
USAGE_GUIDE = """
🎯 QUANDO USAR CADA CONFIGURAÇÃO:

1. CONFIG_ULTRA_SAFE
   ✅ Áudio já está com boa qualidade
   ✅ Só precisa ajustar volume (LUFS)
   ✅ Quer manter 100% do caráter original
   ❌ Não use se tiver ruído ou problemas

2. CONFIG_CONSERVATIVE
   ✅ Áudio tem qualidade razoável
   ✅ Tem um pouco de ruído mas não muito
   ✅ Quer limpeza suave mantendo naturalidade
   ✅ USO RECOMENDADO PARA MAIORIA DOS CASOS

3. CONFIG_DEMUCS_QUALITY
   ✅ Quer máxima qualidade possível
   ✅ Tem GPU disponível
   ✅ Pode esperar 10-20 minutos
   ✅ Áudio precisa de processamento individual de stems
   ❌ Não use sem GPU (vai demorar horas)

4. CONFIG_MASTERING_ONLY
   ✅ Áudio já foi limpo
   ✅ Só precisa de EQ e normalização final
   ✅ Já foi processado em outro software

5. CONFIG_ANALYSIS_ONLY
   ✅ Quer apenas analisar o áudio
   ✅ Ver os problemas antes de processar
   ✅ Comparar métricas

⚠️ DICA IMPORTANTE:
   Comece SEMPRE com CONFIG_CONSERVATIVE ou CONFIG_ULTRA_SAFE
   Só use configurações mais agressivas se necessário!
   Menos é mais quando se trata de preservar qualidade.
"""

# Dicionário para fácil acesso
ALL_SAFE_CONFIGS = {
    'ultra_safe': CONFIG_ULTRA_SAFE,
    'conservative': CONFIG_CONSERVATIVE,
    'demucs_quality': CONFIG_DEMUCS_QUALITY,
    'mastering_only': CONFIG_MASTERING_ONLY,
    'analysis_only': CONFIG_ANALYSIS_ONLY
}

def get_safe_config(name='conservative'):
    """
    Retorna configuração segura pelo nome

    Args:
        name: 'ultra_safe', 'conservative', 'demucs_quality', 'mastering_only', ou 'analysis_only'

    Returns:
        Dict com configuração
    """
    if name not in ALL_SAFE_CONFIGS:
        print(f"⚠️ Configuração '{name}' não encontrada. Usando 'conservative'")
        return CONFIG_CONSERVATIVE

    return ALL_SAFE_CONFIGS[name].copy()

if __name__ == '__main__':
    print(USAGE_GUIDE)
