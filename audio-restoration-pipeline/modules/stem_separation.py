"""
Módulo de Separação de Stems
Separa áudio em componentes individuais (vocal, bateria, baixo, outros)
"""

import numpy as np
import librosa
import soundfile as sf
from typing import Dict, List, Optional
import os
from pathlib import Path


class StemSeparator:
    """Separa áudio em stems individuais"""

    def __init__(self, sr: int = 44100):
        """
        Inicializa o separador de stems

        Args:
            sr: Sample rate
        """
        self.sr = sr
        self.available_models = ['demucs', 'basic']

    def separate_stems(
        self,
        audio_path: str,
        output_dir: str,
        model: str = 'demucs',
        stems: List[str] = None
    ) -> Dict[str, str]:
        """
        Separa áudio em stems

        Args:
            audio_path: Caminho para o arquivo de áudio
            output_dir: Diretório de saída para os stems
            model: Modelo a usar ('demucs' ou 'basic')
            stems: Lista de stems desejados (None = todos)

        Returns:
            Dicionário com caminhos dos stems separados
        """
        os.makedirs(output_dir, exist_ok=True)

        if model == 'demucs':
            return self._separate_with_demucs(audio_path, output_dir, stems)
        elif model == 'basic':
            return self._separate_basic(audio_path, output_dir)
        else:
            raise ValueError(f"Modelo desconhecido: {model}")

    def _separate_with_demucs(
        self,
        audio_path: str,
        output_dir: str,
        stems: List[str] = None
    ) -> Dict[str, str]:
        """
        Separa usando Demucs (state-of-the-art)
        Nota: Requer instalação do Demucs no ambiente

        Args:
            audio_path: Caminho do áudio
            output_dir: Diretório de saída
            stems: Stems desejados

        Returns:
            Dicionário com caminhos dos stems
        """
        try:
            import subprocess
            import torch

            # Verificar se demucs está instalado
            try:
                result = subprocess.run(['demucs', '--help'], capture_output=True, check=True, text=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ Demucs não encontrado. Instalando...")
                subprocess.run(['pip', 'install', '-U', 'demucs'], check=True)
                print("✓ Demucs instalado!")

            # Detectar dispositivo (GPU/CPU)
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

            # Configurar comando Demucs com melhores parâmetros
            cmd = [
                'demucs',
                '--device', device,
                '--two-stems', 'vocals',  # Começar com 2 stems (mais rápido)
                '-n', 'htdemucs',  # Modelo de alta qualidade
                '--float32',  # Melhor qualidade
                '--out', output_dir,
                audio_path
            ]

            # Se não especificar stems, usar modelo completo de 4 stems
            if stems is None or (isinstance(stems, list) and len(stems) > 2):
                cmd = [
                    'demucs',
                    '--device', device,
                    '-n', 'htdemucs_ft',  # Modelo fine-tuned completo (4 stems)
                    '--float32',
                    '--out', output_dir,
                    audio_path
                ]

            print(f"🎵 Executando Demucs...")
            print(f"   Modelo: {'htdemucs_ft (4 stems)' if len(cmd) > 10 else 'htdemucs (2 stems)'}")
            print(f"   Dispositivo: {device.upper()}")
            if device == 'cuda':
                print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   Comando: {' '.join(cmd)}")

            # Executar com output visível
            result = subprocess.run(cmd, check=True, capture_output=False, text=True)

            # Encontrar arquivos de saída
            # Demucs salva em: output_dir / model_name / audio_name / *.wav
            audio_name = Path(audio_path).stem

            # Tentar diferentes nomes de modelo
            possible_model_names = ['htdemucs_ft', 'htdemucs', 'mdx_extra', 'mdx']
            demucs_output = None

            for model_name in possible_model_names:
                test_path = Path(output_dir) / model_name / audio_name
                if test_path.exists():
                    demucs_output = test_path
                    print(f"✓ Encontrado output em: {model_name}/{audio_name}")
                    break

            if demucs_output is None:
                raise Exception(f"Não foi possível encontrar output do Demucs em {output_dir}")

            # Coletar stems
            stem_paths = {}
            for stem_file in demucs_output.glob('*.wav'):
                stem_name = stem_file.stem
                stem_paths[stem_name] = str(stem_file)
                print(f"  ✓ {stem_name}: {stem_file.name}")

            if not stem_paths:
                raise Exception("Demucs não gerou nenhum arquivo de saída")

            return stem_paths

        except Exception as e:
            print(f"✗ Erro ao usar Demucs: {e}")
            print("  Detalhes do erro:", str(e))
            print("\n⚠️ Fallback: Usando método básico de separação...")
            return self._separate_basic(audio_path, output_dir)

    def _separate_basic(
        self,
        audio_path: str,
        output_dir: str
    ) -> Dict[str, str]:
        """
        Separação básica usando processamento de sinais
        Menos preciso que Demucs, mas não requer modelos pesados

        Args:
            audio_path: Caminho do áudio
            output_dir: Diretório de saída

        Returns:
            Dicionário com caminhos dos stems
        """
        # Carregar áudio
        y, sr = librosa.load(audio_path, sr=self.sr, mono=False)

        # Se estéreo, converter para mono para processamento
        if len(y.shape) > 1:
            y_mono = librosa.to_mono(y)
        else:
            y_mono = y

        # Separar componentes usando diferentes técnicas
        stems = {}

        # 1. Separar vocais (frequências médias-altas + centro estéreo)
        vocals = self._extract_vocals_basic(y, sr)
        vocal_path = os.path.join(output_dir, 'vocals.wav')
        sf.write(vocal_path, vocals, sr)
        stems['vocals'] = vocal_path

        # 2. Separar bateria (percussivo)
        drums = self._extract_drums_basic(y_mono, sr)
        drums_path = os.path.join(output_dir, 'drums.wav')
        sf.write(drums_path, drums, sr)
        stems['drums'] = drums_path

        # 3. Separar baixo (frequências baixas harmônicas)
        bass = self._extract_bass_basic(y_mono, sr)
        bass_path = os.path.join(output_dir, 'bass.wav')
        sf.write(bass_path, bass, sr)
        stems['bass'] = bass_path

        # 4. "Outros" = original - (vocals + drums + bass)
        # Reconstruir outros por subtração
        if len(y.shape) > 1:
            y_for_subtraction = librosa.to_mono(y)
        else:
            y_for_subtraction = y

        # Garantir mesmo tamanho
        min_len = min(len(y_for_subtraction), len(vocals), len(drums), len(bass))
        other = y_for_subtraction[:min_len] - (
            vocals[:min_len] + drums[:min_len] + bass[:min_len]
        )

        other_path = os.path.join(output_dir, 'other.wav')
        sf.write(other_path, other, sr)
        stems['other'] = other_path

        return stems

    def _extract_vocals_basic(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extrai vocais usando separação de centro estéreo e filtragem"""

        if len(y.shape) > 1:
            # Stereo: extrair centro (onde geralmente está o vocal)
            # Centro = (L + R) / 2, Sides = (L - R) / 2
            center = np.mean(y, axis=0)

            # Filtrar range vocal (100Hz - 8kHz)
            from scipy import signal
            sos = signal.butter(4, [100, 8000], btype='band', fs=sr, output='sos')
            vocals = signal.sosfilt(sos, center)

            # Realçar usando compressão espectral
            D = librosa.stft(vocals)
            magnitude = np.abs(D)

            # Realçar formantes vocais (1-4 kHz)
            freqs = librosa.fft_frequencies(sr=sr)
            vocal_range = (freqs >= 1000) & (freqs <= 4000)
            magnitude[vocal_range] *= 1.3

            # Reconstruir
            D_enhanced = magnitude * np.exp(1j * np.angle(D))
            vocals = librosa.istft(D_enhanced)

            return vocals
        else:
            # Mono: apenas filtrar range vocal
            from scipy import signal
            sos = signal.butter(4, [100, 8000], btype='band', fs=sr, output='sos')
            vocals = signal.sosfilt(sos, y)
            return vocals

    def _extract_drums_basic(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extrai bateria usando separação harmônico-percussiva"""

        # Usar HPSS do librosa
        y_harmonic, y_percussive = librosa.effects.hpss(y, margin=3.0)

        # Bateria é principalmente percussiva
        # Realçar ainda mais removendo muito das frequências baixas sustentadas
        from scipy import signal

        # Filtro para remover sub-bass sustentado
        sos = signal.butter(2, 60, btype='high', fs=sr, output='sos')
        drums = signal.sosfilt(sos, y_percussive)

        return drums

    def _extract_bass_basic(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extrai baixo usando filtragem de frequências baixas"""

        # Usar HPSS para pegar parte harmônica
        y_harmonic, _ = librosa.effects.hpss(y, margin=3.0)

        # Filtrar apenas frequências de baixo (20Hz - 250Hz)
        from scipy import signal
        sos = signal.butter(4, [20, 250], btype='band', fs=sr, output='sos')
        bass = signal.sosfilt(sos, y_harmonic)

        return bass

    def reconstruct_from_stems(
        self,
        stem_paths: Dict[str, str],
        output_path: str,
        stem_gains: Dict[str, float] = None
    ) -> str:
        """
        Reconstrói áudio a partir de stems separados

        Args:
            stem_paths: Dicionário com caminhos dos stems
            output_path: Caminho de saída do áudio reconstruído
            stem_gains: Ganhos individuais para cada stem (dB)

        Returns:
            Caminho do áudio reconstruído
        """
        if stem_gains is None:
            stem_gains = {stem: 0.0 for stem in stem_paths.keys()}

        # Carregar todos os stems
        stems_audio = {}
        max_length = 0

        for stem_name, stem_path in stem_paths.items():
            y, sr = librosa.load(stem_path, sr=self.sr)

            # Aplicar ganho se especificado
            if stem_name in stem_gains:
                gain_linear = 10 ** (stem_gains[stem_name] / 20)
                y = y * gain_linear

            stems_audio[stem_name] = y
            max_length = max(max_length, len(y))

        # Garantir que todos tenham o mesmo tamanho
        for stem_name in stems_audio:
            if len(stems_audio[stem_name]) < max_length:
                stems_audio[stem_name] = np.pad(
                    stems_audio[stem_name],
                    (0, max_length - len(stems_audio[stem_name]))
                )

        # Somar todos os stems
        mixed = np.sum(list(stems_audio.values()), axis=0)

        # Normalizar para evitar clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 0.95:
            mixed = mixed * (0.95 / max_val)

        # Salvar
        sf.write(output_path, mixed, self.sr)

        return output_path

    def process_stem_individually(
        self,
        stem_path: str,
        output_path: str,
        processing_func,
        **kwargs
    ) -> str:
        """
        Processa um stem individual com uma função customizada

        Args:
            stem_path: Caminho do stem
            output_path: Caminho de saída
            processing_func: Função de processamento
            **kwargs: Argumentos para a função

        Returns:
            Caminho do stem processado
        """
        # Carregar stem
        y, sr = librosa.load(stem_path, sr=self.sr)

        # Processar
        y_processed = processing_func(y, sr, **kwargs)

        # Salvar
        sf.write(output_path, y_processed, sr)

        return output_path

    def analyze_stem_quality(self, stem_path: str) -> Dict:
        """
        Analisa qualidade de um stem separado

        Args:
            stem_path: Caminho do stem

        Returns:
            Dicionário com métricas de qualidade
        """
        y, sr = librosa.load(stem_path, sr=self.sr)

        # Calcular métricas
        rms = librosa.feature.rms(y=y)[0]
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        quality = {
            'rms_mean': float(np.mean(rms)),
            'rms_std': float(np.std(rms)),
            'spectral_centroid_mean': float(np.mean(spectral_centroid)),
            'peak_amplitude': float(np.max(np.abs(y))),
            'duration': len(y) / sr,
            'has_content': bool(np.mean(rms) > 0.001)  # Threshold para detectar se tem conteúdo
        }

        return quality
