"""
Sistema de Presets Inteligentes
Seleciona automaticamente a melhor configuração baseada na análise do áudio
"""

from typing import Dict
import numpy as np


class SmartPresetSelector:
    """Seletor inteligente de presets baseado em análise"""

    def __init__(self):
        pass

    def analyze_and_suggest(self, analysis: Dict) -> Dict:
        """
        Analisa áudio e sugere configuração otimizada

        Args:
            analysis: Resultado da análise espectral

        Returns:
            Configuração otimizada baseada na análise
        """
        # Extrair métricas da análise
        snr = analysis['noise_profile']['snr_db']
        has_clipping = analysis['clipping_detection']['has_clipping']
        clip_percentage = analysis['clipping_detection']['clip_percentage']
        high_freq_loss = analysis['frequency_analysis']['high_freq_loss']
        high_freq_cutoff = analysis['frequency_analysis']['high_freq_cutoff']
        lufs = analysis['dynamic_range']['lufs_estimate']
        crest_factor = analysis['dynamic_range']['crest_factor']

        # Inicializar configuração
        config = {
            'remove_clicks': True,  # Sempre ativo
            'reduce_noise': False,
            'noise_reduction_strength': 0.0,
            'restore_frequencies': False,
            'freq_restoration_method': 'harmonic_synthesis',
            'enhance_bass': False,
            'bass_enhancement_amount': 1.3,
            'psychoacoustic_enhancement': True,
            'separate_stems': False,
            'stem_separation_model': 'basic',
            'process_stems_individually': False,
            'target_lufs': -14.0,
            'master_eq': {
                'bass': 0.0,
                'mid': 0.0,
                'presence': 0.0,
                'treble': 0.0
            },
            'add_presence': False,
            'advanced': {}
        }

        reasons = []

        # ═══════════════════════════════════════════════════════════
        # ANÁLISE DE RUÍDO
        # ═══════════════════════════════════════════════════════════
        if snr < 40:
            config['reduce_noise'] = True

            if snr < 15:
                # Ruído MUITO alto
                config['noise_reduction_strength'] = 0.85
                reasons.append(f"🔴 Ruído MUITO alto (SNR: {snr:.1f}dB) → Redução forte (0.85)")
            elif snr < 25:
                # Ruído alto
                config['noise_reduction_strength'] = 0.75
                reasons.append(f"🟡 Ruído alto (SNR: {snr:.1f}dB) → Redução moderada (0.75)")
            else:
                # Ruído moderado
                config['noise_reduction_strength'] = 0.6
                reasons.append(f"🟢 Ruído moderado (SNR: {snr:.1f}dB) → Redução suave (0.6)")
        else:
            reasons.append(f"✓ Áudio limpo (SNR: {snr:.1f}dB) → Sem redução de ruído")

        # ═══════════════════════════════════════════════════════════
        # ANÁLISE DE CLIPPING
        # ═══════════════════════════════════════════════════════════
        if has_clipping:
            reasons.append(f"⚠️ Clipping detectado ({clip_percentage:.2f}%) → De-clipping automático")

        # ═══════════════════════════════════════════════════════════
        # ANÁLISE DE FREQUÊNCIAS
        # ═══════════════════════════════════════════════════════════
        if high_freq_loss:
            config['restore_frequencies'] = True

            if high_freq_cutoff < 10000:
                # Perda SEVERA
                config['freq_restoration_method'] = 'harmonic_synthesis'
                config['master_eq']['presence'] = 3.0
                config['master_eq']['treble'] = 3.5
                config['add_presence'] = True
                reasons.append(f"🔴 Perda SEVERA de altas ({high_freq_cutoff:.0f}Hz) → Restauração agressiva")

                # Considerar separação de stems para melhor resultado
                config['separate_stems'] = True
                config['stem_separation_model'] = 'demucs'
                reasons.append("→ Separação de stems recomendada para melhor restauração")

            elif high_freq_cutoff < 14000:
                # Perda moderada
                config['freq_restoration_method'] = 'harmonic_synthesis'
                config['master_eq']['presence'] = 2.0
                config['master_eq']['treble'] = 2.5
                config['add_presence'] = True
                reasons.append(f"🟡 Perda moderada de altas ({high_freq_cutoff:.0f}Hz) → Restauração moderada")

            else:
                # Perda leve
                config['freq_restoration_method'] = 'harmonic_synthesis'
                config['master_eq']['presence'] = 1.0
                config['master_eq']['treble'] = 1.2
                config['add_presence'] = True
                reasons.append(f"🟢 Perda leve de altas ({high_freq_cutoff:.0f}Hz) → Restauração suave")
        else:
            config['master_eq']['presence'] = 0.5
            config['master_eq']['treble'] = 0.3
            reasons.append("✓ Espectro completo → Apenas ajustes sutis")

        # ═══════════════════════════════════════════════════════════
        # ANÁLISE DE VOLUME (LUFS)
        # ═══════════════════════════════════════════════════════════
        if lufs < -30:
            reasons.append(f"🔴 Áudio MUITO silencioso ({lufs:.1f} LUFS) → Normalização para -14 LUFS")
        elif lufs < -20:
            reasons.append(f"🟡 Áudio silencioso ({lufs:.1f} LUFS) → Normalização para -14 LUFS")
        elif lufs > -10:
            reasons.append(f"⚠️ Áudio MUITO alto ({lufs:.1f} LUFS) → Redução para -14 LUFS")
        else:
            reasons.append(f"✓ Volume adequado ({lufs:.1f} LUFS)")

        # ═══════════════════════════════════════════════════════════
        # ANÁLISE DE DINÂMICA
        # ═══════════════════════════════════════════════════════════
        if crest_factor < 2:
            reasons.append(f"⚠️ Áudio muito comprimido (CF: {crest_factor:.1f}) → Sem compressão adicional")
            config['advanced']['adaptive_compression'] = False
        elif crest_factor > 8:
            reasons.append(f"🔴 Áudio muito dinâmico (CF: {crest_factor:.1f}) → Compressão adaptativa")
            config['advanced']['adaptive_compression'] = True
            config['advanced']['multiband_compress'] = True
        else:
            reasons.append(f"✓ Dinâmica adequada (CF: {crest_factor:.1f})")

        # ═══════════════════════════════════════════════════════════
        # ANÁLISE DE BANDAS DE FREQUÊNCIA
        # ═══════════════════════════════════════════════════════════
        band_energy = analysis['frequency_analysis']['band_energy']

        # Checar se graves estão fracos
        low_energy = band_energy.get('sub_bass', 0) + band_energy.get('bass', 0)
        if low_energy < 0.15:  # Menos de 15% da energia
            config['enhance_bass'] = True
            config['master_eq']['bass'] = 1.5
            reasons.append(f"🔴 Graves fracos ({low_energy*100:.1f}%) → Realce de graves")
        elif low_energy < 0.20:
            config['master_eq']['bass'] = 0.5
            reasons.append(f"🟡 Graves moderados ({low_energy*100:.1f}%) → Leve realce")

        # Checar se médios estão excessivos
        mid_energy = band_energy.get('mid', 0) + band_energy.get('low_mid', 0)
        if mid_energy > 0.45:  # Mais de 45% da energia
            config['master_eq']['mid'] = -1.0
            reasons.append(f"⚠️ Médios excessivos ({mid_energy*100:.1f}%) → Redução de médios")

        # ═══════════════════════════════════════════════════════════
        # DECISÃO DE SEPARAÇÃO DE STEMS
        # ═══════════════════════════════════════════════════════════
        quality_issues = sum([
            snr < 20,  # Ruído alto
            high_freq_loss and high_freq_cutoff < 10000,  # Perda severa
            has_clipping,  # Clipping
            lufs < -35  # Muito silencioso
        ])

        if quality_issues >= 2 and not config['separate_stems']:
            # Múltiplos problemas, separação de stems vai ajudar
            config['separate_stems'] = True
            config['stem_separation_model'] = 'demucs'
            config['process_stems_individually'] = True
            reasons.append(f"🎯 Múltiplos problemas detectados ({quality_issues}) → Separação de stems recomendada")

        # ═══════════════════════════════════════════════════════════
        # PROCESSAMENTO AVANÇADO
        # ═══════════════════════════════════════════════════════════
        if config['separate_stems'] and config['stem_separation_model'] == 'demucs':
            # Se vai usar Demucs, aproveitar para processamento avançado
            config['advanced']['de_esser'] = True  # Para vocais
            config['advanced']['stereo_enhance'] = True
            reasons.append("→ Processamento avançado ativado (de-esser, stereo enhance)")

        # ═══════════════════════════════════════════════════════════
        # RESUMO E CLASSIFICAÇÃO
        # ═══════════════════════════════════════════════════════════
        if quality_issues == 0:
            quality_category = "EXCELENTE"
            recommended_preset = "suave"
        elif quality_issues == 1:
            quality_category = "BOA"
            recommended_preset = "padrao"
        elif quality_issues == 2:
            quality_category = "MODERADA"
            recommended_preset = "demucs"
        else:
            quality_category = "BAIXA"
            recommended_preset = "agressivo"

        # Adicionar metadados
        config['_metadata'] = {
            'quality_category': quality_category,
            'quality_issues_count': quality_issues,
            'recommended_preset': recommended_preset,
            'analysis_reasons': reasons,
            'auto_generated': True
        }

        return config

    def print_analysis_report(self, config: Dict):
        """
        Imprime relatório detalhado da análise e configuração sugerida

        Args:
            config: Configuração gerada
        """
        if '_metadata' not in config:
            print("⚠️ Configuração não foi gerada pelo sistema inteligente")
            return

        metadata = config['_metadata']

        print("\n" + "═" * 70)
        print("🤖 ANÁLISE INTELIGENTE DE ÁUDIO")
        print("═" * 70)

        print(f"\n📊 CLASSIFICAÇÃO: {metadata['quality_category']}")
        print(f"📝 Problemas detectados: {metadata['quality_issues_count']}")
        print(f"🎯 Preset recomendado: {metadata['recommended_preset'].upper()}")

        print("\n" + "─" * 70)
        print("🔍 RAZÕES DA CONFIGURAÇÃO:")
        print("─" * 70)

        for reason in metadata['analysis_reasons']:
            print(f"  {reason}")

        print("\n" + "─" * 70)
        print("⚙️ CONFIGURAÇÃO GERADA:")
        print("─" * 70)

        # Mostrar principais configurações
        print(f"  Redução de ruído: {'✓' if config['reduce_noise'] else '✗'} ", end="")
        if config['reduce_noise']:
            print(f"(força: {config['noise_reduction_strength']:.2f})")
        else:
            print()

        print(f"  Restauração de freq: {'✓' if config['restore_frequencies'] else '✗'}")
        print(f"  Separação de stems: {'✓' if config['separate_stems'] else '✗'} ", end="")
        if config['separate_stems']:
            print(f"({config['stem_separation_model']})")
        else:
            print()

        print(f"  LUFS alvo: {config['target_lufs']} dB")

        print("\n  EQ Master:")
        for band, value in config['master_eq'].items():
            if value != 0:
                sign = "+" if value > 0 else ""
                print(f"    • {band}: {sign}{value:.1f} dB")

        if config.get('advanced'):
            print("\n  Processamento Avançado:")
            for proc, enabled in config['advanced'].items():
                if enabled:
                    print(f"    • {proc}")

        print("\n" + "═" * 70)
        print("✓ Configuração pronta para uso!")
        print("═" * 70 + "\n")


def auto_configure(analysis: Dict, verbose: bool = True) -> Dict:
    """
    Função de conveniência para auto-configuração

    Args:
        analysis: Resultado da análise espectral
        verbose: Imprimir relatório

    Returns:
        Configuração otimizada
    """
    selector = SmartPresetSelector()
    config = selector.analyze_and_suggest(analysis)

    if verbose:
        selector.print_analysis_report(config)

    return config
