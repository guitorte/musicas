"""
Módulo de Análise Espectral
Analisa características espectrais do áudio para guiar o processo de restauração
"""

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy import signal
from typing import Dict, Tuple, Optional
import json


class SpectralAnalyzer:
    """Analisa características espectrais de arquivos de áudio"""

    def __init__(self, sr: int = 44100):
        """
        Inicializa o analisador espectral

        Args:
            sr: Sample rate padrão
        """
        self.sr = sr

    def analyze_audio(self, audio_path: str) -> Dict:
        """
        Realiza análise espectral completa do áudio

        Args:
            audio_path: Caminho para o arquivo de áudio

        Returns:
            Dicionário com análises espectrais
        """
        # Carregar áudio
        y, sr = librosa.load(audio_path, sr=self.sr)

        analysis = {
            'file_path': audio_path,
            'sample_rate': sr,
            'duration': len(y) / sr,
            'spectral_features': self._analyze_spectral_features(y, sr),
            'frequency_analysis': self._analyze_frequency_content(y, sr),
            'dynamic_range': self._analyze_dynamic_range(y),
            'noise_profile': self._analyze_noise(y, sr),
            'clipping_detection': self._detect_clipping(y),
            'recommendations': []
        }

        # Gerar recomendações baseadas na análise
        analysis['recommendations'] = self._generate_recommendations(analysis)

        return analysis

    def _analyze_spectral_features(self, y: np.ndarray, sr: int) -> Dict:
        """Analisa features espectrais do áudio"""

        # Spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]

        # Spectral bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]

        # Spectral contrast
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]

        return {
            'centroid_mean': float(np.mean(spectral_centroids)),
            'centroid_std': float(np.std(spectral_centroids)),
            'rolloff_mean': float(np.mean(spectral_rolloff)),
            'rolloff_std': float(np.std(spectral_rolloff)),
            'bandwidth_mean': float(np.mean(spectral_bandwidth)),
            'bandwidth_std': float(np.std(spectral_bandwidth)),
            'contrast_mean': float(np.mean(spectral_contrast)),
            'zcr_mean': float(np.mean(zcr)),
            'zcr_std': float(np.std(zcr))
        }

    def _analyze_frequency_content(self, y: np.ndarray, sr: int) -> Dict:
        """Analisa o conteúdo de frequências do áudio"""

        # Calcular FFT
        fft = np.fft.fft(y)
        magnitude = np.abs(fft)
        frequency = np.fft.fftfreq(len(y), 1/sr)

        # Pegar apenas frequências positivas
        positive_freq_idx = frequency > 0
        frequency = frequency[positive_freq_idx]
        magnitude = magnitude[positive_freq_idx]

        # Analisar bandas de frequência
        bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'presence': (4000, 6000),
            'brilliance': (6000, 20000)
        }

        band_energy = {}
        for band_name, (low, high) in bands.items():
            band_mask = (frequency >= low) & (frequency <= high)
            band_energy[band_name] = float(np.sum(magnitude[band_mask]))

        # Normalizar energias
        total_energy = sum(band_energy.values())
        band_energy_normalized = {k: v/total_energy for k, v in band_energy.items()}

        # Detectar frequências ausentes ou fracas
        nyquist = sr / 2
        high_freq_cutoff = np.max(frequency[magnitude > np.max(magnitude) * 0.01])

        return {
            'band_energy': band_energy_normalized,
            'dominant_frequency': float(frequency[np.argmax(magnitude)]),
            'high_freq_cutoff': float(high_freq_cutoff),
            'high_freq_loss': bool(high_freq_cutoff < nyquist * 0.8),
            'nyquist_frequency': float(nyquist)
        }

    def _analyze_dynamic_range(self, y: np.ndarray) -> Dict:
        """Analisa a dinâmica do áudio"""

        # RMS
        rms = librosa.feature.rms(y=y)[0]

        # Peak
        peak = np.max(np.abs(y))

        # Crest factor
        crest_factor = peak / (np.mean(rms) + 1e-10)

        # LUFS estimado (simplificado)
        lufs_estimate = -23 + 20 * np.log10(np.mean(rms) + 1e-10)

        return {
            'peak_amplitude': float(peak),
            'rms_mean': float(np.mean(rms)),
            'rms_std': float(np.std(rms)),
            'crest_factor': float(crest_factor),
            'lufs_estimate': float(lufs_estimate),
            'headroom_db': float(20 * np.log10(1.0 / (peak + 1e-10)))
        }

    def _analyze_noise(self, y: np.ndarray, sr: int) -> Dict:
        """Analisa perfil de ruído do áudio"""

        # Detectar seções silenciosas para estimar ruído
        rms = librosa.feature.rms(y=y)[0]
        threshold = np.percentile(rms, 10)  # 10% mais silencioso

        silent_frames = rms < threshold

        # Calcular SNR estimado usando valores RMS
        # Usar os valores RMS dos frames em vez do áudio bruto
        signal_rms = rms[~silent_frames] if np.any(~silent_frames) else np.array([0])
        noise_rms = rms[silent_frames] if np.any(silent_frames) else np.array([0])

        signal_power = np.mean(signal_rms ** 2)
        noise_power = np.mean(noise_rms ** 2)

        snr = 10 * np.log10((signal_power + 1e-10) / (noise_power + 1e-10))

        # Detectar ruído de fundo constante
        S = np.abs(librosa.stft(y))
        noise_floor = np.percentile(S, 5, axis=1)

        return {
            'snr_db': float(snr),
            'noise_floor_mean': float(np.mean(noise_floor)),
            'has_noise': bool(snr < 40),
            'noise_severity': 'high' if snr < 20 else 'medium' if snr < 40 else 'low'
        }

    def _detect_clipping(self, y: np.ndarray) -> Dict:
        """Detecta clipping no áudio"""

        # Detectar samples próximos ao máximo
        clip_threshold = 0.99
        clipped_samples = np.sum(np.abs(y) > clip_threshold)
        total_samples = len(y)
        clip_percentage = (clipped_samples / total_samples) * 100

        return {
            'clipped_samples': int(clipped_samples),
            'clip_percentage': float(clip_percentage),
            'has_clipping': bool(clip_percentage > 0.1)
        }

    def _generate_recommendations(self, analysis: Dict) -> list:
        """Gera recomendações baseadas na análise"""

        recommendations = []

        # Verificar clipping
        if analysis['clipping_detection']['has_clipping']:
            recommendations.append({
                'type': 'clipping',
                'severity': 'high',
                'message': f"Clipping detectado em {analysis['clipping_detection']['clip_percentage']:.2f}% do áudio. Recomenda-se de-clipping."
            })

        # Verificar perda de frequências altas
        if analysis['frequency_analysis']['high_freq_loss']:
            recommendations.append({
                'type': 'frequency_restoration',
                'severity': 'medium',
                'message': f"Perda de frequências altas detectada (corte em {analysis['frequency_analysis']['high_freq_cutoff']:.0f}Hz). Recomenda-se restauração espectral."
            })

        # Verificar ruído
        if analysis['noise_profile']['has_noise']:
            recommendations.append({
                'type': 'noise_reduction',
                'severity': analysis['noise_profile']['noise_severity'],
                'message': f"Ruído detectado (SNR: {analysis['noise_profile']['snr_db']:.1f}dB). Recomenda-se redução de ruído."
            })

        # Verificar dinâmica
        if analysis['dynamic_range']['lufs_estimate'] < -30:
            recommendations.append({
                'type': 'gain',
                'severity': 'medium',
                'message': f"Áudio muito silencioso (LUFS: {analysis['dynamic_range']['lufs_estimate']:.1f}). Recomenda-se normalização."
            })

        if analysis['dynamic_range']['crest_factor'] < 2:
            recommendations.append({
                'type': 'dynamics',
                'severity': 'low',
                'message': "Áudio muito comprimido. Pode ser necessário expansão dinâmica."
            })

        return recommendations

    def visualize_analysis(self, audio_path: str, output_path: str):
        """
        Cria visualizações da análise espectral

        Args:
            audio_path: Caminho para o arquivo de áudio
            output_path: Caminho para salvar a visualização
        """
        y, sr = librosa.load(audio_path, sr=self.sr)

        fig, axes = plt.subplots(4, 1, figsize=(14, 12))

        # Waveform
        librosa.display.waveshow(y, sr=sr, ax=axes[0])
        axes[0].set_title('Waveform')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('Amplitude')

        # Spectrogram
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', ax=axes[1])
        axes[1].set_title('Spectrogram')
        fig.colorbar(img, ax=axes[1], format='%+2.0f dB')

        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        frames = range(len(spectral_centroids))
        t = librosa.frames_to_time(frames, sr=sr)
        axes[2].plot(t, spectral_centroids)
        axes[2].set_title('Spectral Centroid')
        axes[2].set_xlabel('Time (s)')
        axes[2].set_ylabel('Hz')

        # Frequency spectrum
        fft = np.fft.fft(y)
        magnitude = np.abs(fft)
        frequency = np.fft.fftfreq(len(y), 1/sr)
        positive_freq_idx = frequency > 0
        axes[3].semilogx(frequency[positive_freq_idx], 20 * np.log10(magnitude[positive_freq_idx] + 1e-10))
        axes[3].set_title('Frequency Spectrum')
        axes[3].set_xlabel('Frequency (Hz)')
        axes[3].set_ylabel('Magnitude (dB)')
        axes[3].grid(True)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

    def save_analysis(self, analysis: Dict, output_path: str):
        """Salva a análise em JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
