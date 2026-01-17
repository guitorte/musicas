"""
Pipeline Principal de Restauração de Áudio
Orquestra todos os módulos para processamento completo
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import librosa
import soundfile as sf
from datetime import datetime

from .spectral_analysis import SpectralAnalyzer
from .frequency_restoration import FrequencyRestorer
from .stem_separation import StemSeparator
from .audio_processing import AudioProcessor


class AudioRestorationPipeline:
    """Pipeline completo de restauração e masterização de áudio"""

    def __init__(
        self,
        sr: int = 44100,
        output_base_dir: str = './output',
        log_dir: str = './logs'
    ):
        """
        Inicializa o pipeline

        Args:
            sr: Sample rate padrão
            output_base_dir: Diretório base para saídas
            log_dir: Diretório para logs
        """
        self.sr = sr
        self.output_base_dir = output_base_dir
        self.log_dir = log_dir

        # Inicializar módulos
        self.analyzer = SpectralAnalyzer(sr=sr)
        self.freq_restorer = FrequencyRestorer(sr=sr)
        self.stem_separator = StemSeparator(sr=sr)
        self.processor = AudioProcessor(sr=sr)

        # Criar diretórios
        os.makedirs(output_base_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)

    def process_audio(
        self,
        audio_path: str,
        output_name: Optional[str] = None,
        config: Optional[Dict] = None
    ) -> Dict:
        """
        Processa um arquivo de áudio completo

        Args:
            audio_path: Caminho do arquivo de áudio
            output_name: Nome para os arquivos de saída
            config: Configurações do pipeline

        Returns:
            Dicionário com resultados e caminhos
        """
        # Configuração padrão
        if config is None:
            config = self._get_default_config()

        # Nome de saída
        if output_name is None:
            output_name = Path(audio_path).stem

        # Criar diretório para este áudio
        audio_output_dir = os.path.join(
            self.output_base_dir,
            output_name,
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        os.makedirs(audio_output_dir, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Processando: {audio_path}")
        print(f"Output: {audio_output_dir}")
        print(f"{'='*60}\n")

        results = {
            'input_path': audio_path,
            'output_dir': audio_output_dir,
            'timestamp': datetime.now().isoformat(),
            'config': config,
            'stages': {}
        }

        # ESTÁGIO 1: Análise
        print("ESTÁGIO 1: Análise Espectral")
        print("-" * 40)
        analysis = self._stage_analysis(audio_path, audio_output_dir)
        results['stages']['analysis'] = analysis
        print(f"✓ Análise completa\n")

        # ESTÁGIO 2: Limpeza e Restauração Inicial
        print("ESTÁGIO 2: Limpeza e Restauração Inicial")
        print("-" * 40)
        cleaned_path = self._stage_cleanup(
            audio_path,
            audio_output_dir,
            analysis,
            config
        )
        results['stages']['cleanup'] = {'output': cleaned_path}
        print(f"✓ Limpeza completa: {Path(cleaned_path).name}\n")

        # ESTÁGIO 3: Restauração de Frequências
        if config.get('restore_frequencies', True):
            print("ESTÁGIO 3: Restauração de Frequências")
            print("-" * 40)
            restored_path = self._stage_frequency_restoration(
                cleaned_path,
                audio_output_dir,
                analysis,
                config
            )
            results['stages']['frequency_restoration'] = {'output': restored_path}
            print(f"✓ Restauração de frequências completa: {Path(restored_path).name}\n")
        else:
            restored_path = cleaned_path

        # ESTÁGIO 4: Separação de Stems (opcional)
        if config.get('separate_stems', False):
            print("ESTÁGIO 4: Separação de Stems")
            print("-" * 40)
            stems = self._stage_stem_separation(
                restored_path,
                audio_output_dir,
                config
            )
            results['stages']['stem_separation'] = stems
            print(f"✓ Separação de stems completa\n")

            # ESTÁGIO 5: Processamento Individual de Stems
            if config.get('process_stems_individually', False):
                print("ESTÁGIO 5: Processamento Individual de Stems")
                print("-" * 40)
                processed_stems = self._stage_process_stems(
                    stems,
                    audio_output_dir,
                    config
                )
                results['stages']['processed_stems'] = processed_stems
                print(f"✓ Processamento de stems completo\n")

                # Reconstruir dos stems processados
                print("Reconstruindo dos stems processados...")
                restored_path = self._reconstruct_from_stems(
                    processed_stems,
                    audio_output_dir,
                    'reconstructed.wav'
                )
                results['stages']['reconstruction'] = {'output': restored_path}

        # ESTÁGIO 6: Masterização
        print("ESTÁGIO 6: Masterização")
        print("-" * 40)
        mastered_path = self._stage_mastering(
            restored_path,
            audio_output_dir,
            config
        )
        results['stages']['mastering'] = {'output': mastered_path}
        print(f"✓ Masterização completa: {Path(mastered_path).name}\n")

        # Salvar resultados
        results_path = os.path.join(audio_output_dir, 'results.json')
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"✓ PROCESSAMENTO COMPLETO!")
        print(f"Arquivo final: {mastered_path}")
        print(f"Resultados: {results_path}")
        print(f"{'='*60}\n")

        return results

    def _stage_analysis(self, audio_path: str, output_dir: str) -> Dict:
        """Estágio de análise espectral"""
        analysis = self.analyzer.analyze_audio(audio_path)

        # Salvar análise
        analysis_path = os.path.join(output_dir, 'analysis.json')
        self.analyzer.save_analysis(analysis, analysis_path)

        # Criar visualização
        viz_path = os.path.join(output_dir, 'analysis_visualization.png')
        self.analyzer.visualize_analysis(audio_path, viz_path)

        # Imprimir recomendações
        if analysis['recommendations']:
            print("\nRecomendações:")
            for rec in analysis['recommendations']:
                print(f"  [{rec['severity'].upper()}] {rec['message']}")

        return analysis

    def _stage_cleanup(
        self,
        audio_path: str,
        output_dir: str,
        analysis: Dict,
        config: Dict
    ) -> str:
        """Estágio de limpeza inicial"""
        y, sr = librosa.load(audio_path, sr=self.sr)

        # Remover clicks/pops
        if config.get('remove_clicks', True):
            print("  - Removendo clicks e pops...")
            y = self.processor.remove_clicks_and_pops(y, sr)

        # Reduzir ruído
        if config.get('reduce_noise', True):
            noise_strength = config.get('noise_reduction_strength', 0.7)
            print(f"  - Reduzindo ruído (força: {noise_strength})...")
            y = self.processor.reduce_noise(y, sr, reduction_strength=noise_strength)

        # De-clip se necessário
        if analysis['clipping_detection']['has_clipping']:
            print("  - Corrigindo clipping...")
            y = self.processor.declip(y, sr)

        # Salvar
        output_path = os.path.join(output_dir, '01_cleaned.wav')
        sf.write(output_path, y, sr)

        return output_path

    def _stage_frequency_restoration(
        self,
        audio_path: str,
        output_dir: str,
        analysis: Dict,
        config: Dict
    ) -> str:
        """Estágio de restauração de frequências"""
        y, sr = librosa.load(audio_path, sr=self.sr)

        # Restaurar frequências altas se necessário
        if analysis['frequency_analysis']['high_freq_loss']:
            cutoff = analysis['frequency_analysis']['high_freq_cutoff']
            method = config.get('freq_restoration_method', 'harmonic_synthesis')
            print(f"  - Restaurando frequências altas (corte em {cutoff:.0f}Hz, método: {method})...")
            y = self.freq_restorer.restore_high_frequencies(y, sr, cutoff, method)

        # Realçar graves se configurado
        if config.get('enhance_bass', False):
            bass_amount = config.get('bass_enhancement_amount', 1.3)
            print(f"  - Realçando graves (quantidade: {bass_amount})...")
            y = self.freq_restorer.enhance_bass(y, sr, bass_amount)

        # Aplicar melhorias psicoacústicas
        if config.get('psychoacoustic_enhancement', True):
            print("  - Aplicando melhorias psicoacústicas...")
            y = self.freq_restorer.apply_psychoacoustic_enhancement(y, sr)

        # Salvar
        output_path = os.path.join(output_dir, '02_frequency_restored.wav')
        sf.write(output_path, y, sr)

        return output_path

    def _stage_stem_separation(
        self,
        audio_path: str,
        output_dir: str,
        config: Dict
    ) -> Dict[str, str]:
        """Estágio de separação de stems"""
        stems_dir = os.path.join(output_dir, 'stems')
        os.makedirs(stems_dir, exist_ok=True)

        model = config.get('stem_separation_model', 'basic')
        print(f"  - Usando modelo: {model}")

        stems = self.stem_separator.separate_stems(
            audio_path,
            stems_dir,
            model=model
        )

        for stem_name, stem_path in stems.items():
            print(f"  - {stem_name}: {Path(stem_path).name}")

        return stems

    def _stage_process_stems(
        self,
        stems: Dict[str, str],
        output_dir: str,
        config: Dict
    ) -> Dict[str, str]:
        """Estágio de processamento individual de stems"""
        processed_dir = os.path.join(output_dir, 'stems_processed')
        os.makedirs(processed_dir, exist_ok=True)

        processed_stems = {}

        for stem_name, stem_path in stems.items():
            print(f"  - Processando {stem_name}...")

            y, sr = librosa.load(stem_path, sr=self.sr)

            # Aplicar processamento específico por tipo de stem
            if stem_name == 'vocals':
                # De-essing, compressão vocal
                y = self.processor.compress(
                    y, sr,
                    threshold_db=-15,
                    ratio=3.0,
                    attack_ms=5,
                    release_ms=50
                )
            elif stem_name == 'drums':
                # Compressão de bateria
                y = self.processor.compress(
                    y, sr,
                    threshold_db=-12,
                    ratio=4.0,
                    attack_ms=1,
                    release_ms=100
                )
            elif stem_name == 'bass':
                # Realçar graves
                y = self.freq_restorer.enhance_bass(y, sr, 1.2)

            # Salvar
            output_path = os.path.join(processed_dir, f'{stem_name}_processed.wav')
            sf.write(output_path, y, sr)
            processed_stems[stem_name] = output_path

        return processed_stems

    def _reconstruct_from_stems(
        self,
        stems: Dict[str, str],
        output_dir: str,
        filename: str
    ) -> str:
        """Reconstrói áudio dos stems"""
        output_path = os.path.join(output_dir, filename)

        # Ganhos customizados (opcional)
        stem_gains = {
            'vocals': 0.0,
            'drums': -1.0,
            'bass': 0.0,
            'other': -2.0
        }

        self.stem_separator.reconstruct_from_stems(
            stems,
            output_path,
            stem_gains
        )

        return output_path

    def _stage_mastering(
        self,
        audio_path: str,
        output_dir: str,
        config: Dict
    ) -> str:
        """Estágio de masterização"""
        y, sr = librosa.load(audio_path, sr=self.sr)

        # EQ de masterização
        master_eq = config.get('master_eq', {
            'bass': 0.5,
            'mid': 0.0,
            'presence': 1.0,
            'treble': 0.8
        })

        # Target LUFS
        target_lufs = config.get('target_lufs', -14.0)

        print(f"  - Aplicando cadeia de masterização (target: {target_lufs} LUFS)...")

        # Aplicar masterização
        y_mastered = self.processor.master(
            y, sr,
            target_lufs=target_lufs,
            master_eq=master_eq,
            add_presence=config.get('add_presence', True)
        )

        # Salvar
        output_path = os.path.join(output_dir, '99_mastered_FINAL.wav')
        sf.write(output_path, y_mastered, sr)

        return output_path

    def _get_default_config(self) -> Dict:
        """Retorna configuração padrão do pipeline"""
        return {
            'remove_clicks': True,
            'reduce_noise': True,
            'noise_reduction_strength': 0.7,
            'restore_frequencies': True,
            'freq_restoration_method': 'harmonic_synthesis',
            'enhance_bass': False,
            'bass_enhancement_amount': 1.3,
            'psychoacoustic_enhancement': True,
            'separate_stems': False,
            'stem_separation_model': 'basic',
            'process_stems_individually': False,
            'target_lufs': -14.0,
            'master_eq': {
                'bass': 0.5,
                'mid': 0.0,
                'presence': 1.0,
                'treble': 0.8
            },
            'add_presence': True
        }

    def batch_process(
        self,
        audio_paths: List[str],
        config: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Processa múltiplos arquivos em batch

        Args:
            audio_paths: Lista de caminhos de áudio
            config: Configuração do pipeline

        Returns:
            Lista de resultados
        """
        results = []

        print(f"\n{'='*60}")
        print(f"PROCESSAMENTO EM BATCH - {len(audio_paths)} arquivos")
        print(f"{'='*60}\n")

        for i, audio_path in enumerate(audio_paths, 1):
            print(f"\n[{i}/{len(audio_paths)}] Processando: {Path(audio_path).name}")

            try:
                result = self.process_audio(audio_path, config=config)
                results.append(result)
            except Exception as e:
                print(f"✗ ERRO ao processar {audio_path}: {e}")
                results.append({
                    'input_path': audio_path,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })

        print(f"\n{'='*60}")
        print(f"BATCH COMPLETO - {len(results)} arquivos processados")
        print(f"{'='*60}\n")

        return results
