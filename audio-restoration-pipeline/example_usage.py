#!/usr/bin/env python3
"""
Exemplo de uso do Pipeline de Restauração de Áudio
"""

import os
from pathlib import Path
from modules.pipeline import AudioRestorationPipeline


def exemplo_basico():
    """Exemplo básico de uso"""
    print("=" * 60)
    print("EXEMPLO BÁSICO - Processar um arquivo")
    print("=" * 60)

    # Configurar caminhos
    audio_path = "caminho/para/seu/audio.mp3"  # AJUSTE ESTE CAMINHO
    output_dir = "./output"

    # Verificar se arquivo existe
    if not os.path.exists(audio_path):
        print(f"⚠️ Arquivo não encontrado: {audio_path}")
        print("Por favor, ajuste o caminho do arquivo no script.")
        return

    # Inicializar pipeline
    pipeline = AudioRestorationPipeline(
        sr=44100,
        output_base_dir=output_dir,
        log_dir="./logs"
    )

    # Processar com configuração padrão
    result = pipeline.process_audio(audio_path)

    print(f"\n✓ Processamento completo!")
    print(f"Arquivo final: {result['stages']['mastering']['output']}")


def exemplo_configuracao_customizada():
    """Exemplo com configuração customizada"""
    print("\n" + "=" * 60)
    print("EXEMPLO AVANÇADO - Configuração Customizada")
    print("=" * 60)

    audio_path = "caminho/para/seu/audio.mp3"  # AJUSTE ESTE CAMINHO
    output_dir = "./output"

    if not os.path.exists(audio_path):
        print(f"⚠️ Arquivo não encontrado: {audio_path}")
        return

    # Configuração para áudio antigo/degradado
    config_restauracao_agressiva = {
        'remove_clicks': True,
        'reduce_noise': True,
        'noise_reduction_strength': 0.85,  # Redução mais forte
        'restore_frequencies': True,
        'freq_restoration_method': 'harmonic_synthesis',
        'enhance_bass': True,
        'bass_enhancement_amount': 1.4,
        'psychoacoustic_enhancement': True,
        'separate_stems': False,
        'target_lufs': -14.0,
        'master_eq': {
            'bass': 1.0,
            'mid': -0.5,
            'presence': 1.5,
            'treble': 1.2
        },
        'add_presence': True
    }

    pipeline = AudioRestorationPipeline(
        sr=44100,
        output_base_dir=output_dir
    )

    result = pipeline.process_audio(
        audio_path,
        config=config_restauracao_agressiva
    )

    print(f"\n✓ Restauração agressiva completa!")
    print(f"Arquivo final: {result['stages']['mastering']['output']}")


def exemplo_batch():
    """Exemplo de processamento em batch"""
    print("\n" + "=" * 60)
    print("EXEMPLO BATCH - Processar múltiplos arquivos")
    print("=" * 60)

    # Lista de arquivos para processar
    audio_files = [
        "pasta/audio1.mp3",
        "pasta/audio2.wav",
        "pasta/audio3.mp3"
    ]

    # Filtrar apenas arquivos que existem
    existing_files = [f for f in audio_files if os.path.exists(f)]

    if not existing_files:
        print("⚠️ Nenhum arquivo encontrado.")
        print("Ajuste os caminhos dos arquivos no script.")
        return

    print(f"Processando {len(existing_files)} arquivos...")

    pipeline = AudioRestorationPipeline(
        sr=44100,
        output_base_dir="./output_batch"
    )

    # Configuração para streaming
    config_streaming = {
        'reduce_noise': True,
        'noise_reduction_strength': 0.6,
        'restore_frequencies': True,
        'target_lufs': -14.0,
        'add_presence': True
    }

    results = pipeline.batch_process(
        existing_files,
        config=config_streaming
    )

    # Resumo
    successful = sum(1 for r in results if 'error' not in r)
    print(f"\n✓ Batch completo: {successful}/{len(results)} arquivos processados")


def exemplo_analise_apenas():
    """Exemplo de análise sem processamento"""
    print("\n" + "=" * 60)
    print("EXEMPLO - Análise Apenas (Sem Processamento)")
    print("=" * 60)

    from modules.spectral_analysis import SpectralAnalyzer

    audio_path = "caminho/para/seu/audio.mp3"  # AJUSTE ESTE CAMINHO

    if not os.path.exists(audio_path):
        print(f"⚠️ Arquivo não encontrado: {audio_path}")
        return

    analyzer = SpectralAnalyzer(sr=44100)

    # Analisar
    analysis = analyzer.analyze_audio(audio_path)

    # Mostrar informações
    print(f"\n📊 Análise de: {Path(audio_path).name}")
    print(f"Duração: {analysis['duration']:.2f}s")
    print(f"Sample Rate: {analysis['sample_rate']}Hz")

    # Mostrar recomendações
    print("\n💡 Recomendações:")
    if analysis['recommendations']:
        for rec in analysis['recommendations']:
            severity_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }
            emoji = severity_emoji.get(rec['severity'], '⚪')
            print(f"  {emoji} [{rec['severity'].upper()}] {rec['message']}")
    else:
        print("  ✓ Nenhum problema detectado!")

    # Salvar visualização
    viz_path = "analise_visual.png"
    analyzer.visualize_analysis(audio_path, viz_path)
    print(f"\n✓ Visualização salva em: {viz_path}")

    # Salvar análise JSON
    json_path = "analise.json"
    analyzer.save_analysis(analysis, json_path)
    print(f"✓ Análise JSON salva em: {json_path}")


def exemplo_modulos_individuais():
    """Exemplo usando módulos individuais"""
    print("\n" + "=" * 60)
    print("EXEMPLO - Uso de Módulos Individuais")
    print("=" * 60)

    import librosa
    import soundfile as sf
    from modules.audio_processing import AudioProcessor
    from modules.frequency_restoration import FrequencyRestorer

    audio_path = "caminho/para/seu/audio.mp3"  # AJUSTE ESTE CAMINHO

    if not os.path.exists(audio_path):
        print(f"⚠️ Arquivo não encontrado: {audio_path}")
        return

    # Carregar áudio
    y, sr = librosa.load(audio_path, sr=44100)
    print(f"✓ Áudio carregado: {len(y)/sr:.2f}s")

    # Usar módulo de processamento
    processor = AudioProcessor(sr=44100)

    print("Aplicando redução de ruído...")
    y = processor.reduce_noise(y, sr, reduction_strength=0.7)

    print("Aplicando compressão...")
    y = processor.compress(y, sr, threshold_db=-18, ratio=3.0)

    print("Aplicando EQ...")
    y = processor.apply_eq(y, sr, {
        'bass': 0.5,
        'presence': 1.0,
        'treble': 0.8
    })

    # Usar módulo de restauração de frequências
    restorer = FrequencyRestorer(sr=44100)

    print("Restaurando frequências altas...")
    y = restorer.restore_high_frequencies(y, sr, cutoff_freq=8000)

    print("Aplicando melhorias psicoacústicas...")
    y = restorer.apply_psychoacoustic_enhancement(y, sr)

    # Finalizar com normalização
    print("Normalizando LUFS...")
    y = processor.normalize_lufs(y, target_lufs=-14.0)

    # Salvar
    output_path = "processado_custom.wav"
    sf.write(output_path, y, sr)
    print(f"\n✓ Salvo em: {output_path}")


def main():
    """Função principal"""
    print("\n🎵 Pipeline de Restauração de Áudio - Exemplos de Uso\n")

    print("Escolha um exemplo para executar:")
    print("1. Exemplo Básico")
    print("2. Configuração Customizada")
    print("3. Processamento em Batch")
    print("4. Análise Apenas")
    print("5. Módulos Individuais")
    print("0. Executar todos os exemplos")

    try:
        escolha = input("\nDigite o número (0-5): ").strip()

        if escolha == "1":
            exemplo_basico()
        elif escolha == "2":
            exemplo_configuracao_customizada()
        elif escolha == "3":
            exemplo_batch()
        elif escolha == "4":
            exemplo_analise_apenas()
        elif escolha == "5":
            exemplo_modulos_individuais()
        elif escolha == "0":
            exemplo_basico()
            exemplo_configuracao_customizada()
            exemplo_batch()
            exemplo_analise_apenas()
            exemplo_modulos_individuais()
        else:
            print("⚠️ Opção inválida!")

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")


if __name__ == "__main__":
    main()
