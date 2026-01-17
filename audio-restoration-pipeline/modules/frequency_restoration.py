"""
Módulo de Restauração de Frequências
Restaura frequências perdidas ou danificadas usando técnicas avançadas
"""

import numpy as np
import librosa
import scipy.signal as signal
from scipy import interpolate
from typing import Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class FrequencyRestorer:
    """Restaura frequências perdidas ou danificadas em áudio"""

    def __init__(self, sr: int = 44100):
        """
        Inicializa o restaurador de frequências

        Args:
            sr: Sample rate
        """
        self.sr = sr

    def restore_high_frequencies(
        self,
        y: np.ndarray,
        sr: int,
        cutoff_freq: float = 8000,
        method: str = 'harmonic_synthesis'
    ) -> np.ndarray:
        """
        Restaura frequências altas perdidas

        Args:
            y: Sinal de áudio
            sr: Sample rate
            cutoff_freq: Frequência de corte onde começar a restauração
            method: Método de restauração ('harmonic_synthesis', 'spectral_extension')

        Returns:
            Áudio com frequências altas restauradas
        """
        if method == 'harmonic_synthesis':
            return self._harmonic_synthesis(y, sr, cutoff_freq)
        elif method == 'spectral_extension':
            return self._spectral_extension(y, sr, cutoff_freq)
        else:
            raise ValueError(f"Método desconhecido: {method}")

    def _harmonic_synthesis(
        self,
        y: np.ndarray,
        sr: int,
        cutoff_freq: float
    ) -> np.ndarray:
        """
        Síntese harmônica para restaurar frequências altas
        Gera harmônicos baseados nas frequências existentes
        """
        # Converter para domínio da frequência
        D = librosa.stft(y, n_fft=2048, hop_length=512)
        magnitude, phase = np.abs(D), np.angle(D)

        # Identificar bins de frequência
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        cutoff_bin = np.argmin(np.abs(freqs - cutoff_freq))

        # Criar cópia da magnitude para modificação
        restored_magnitude = magnitude.copy()

        # Síntese de harmônicos
        # Para cada bin abaixo do cutoff, gerar harmônicos acima
        for i in range(cutoff_bin):
            if freqs[i] > 100:  # Ignorar frequências muito baixas
                # Gerar 2º e 3º harmônicos
                harmonic_2_bin = min(i * 2, len(freqs) - 1)
                harmonic_3_bin = min(i * 3, len(freqs) - 1)

                if harmonic_2_bin >= cutoff_bin:
                    # Atenuar o harmônico baseado na distância
                    attenuation = 0.3  # 2º harmônico mais fraco
                    restored_magnitude[harmonic_2_bin] = np.maximum(
                        restored_magnitude[harmonic_2_bin],
                        magnitude[i] * attenuation
                    )

                if harmonic_3_bin >= cutoff_bin:
                    attenuation = 0.15  # 3º harmônico ainda mais fraco
                    restored_magnitude[harmonic_3_bin] = np.maximum(
                        restored_magnitude[harmonic_3_bin],
                        magnitude[i] * attenuation
                    )

        # Suavizar a transição no cutoff
        transition_width = 50  # bins
        transition_start = max(0, cutoff_bin - transition_width)
        transition_end = min(len(freqs), cutoff_bin + transition_width)

        if transition_end > transition_start:
            transition_curve = np.linspace(0, 1, transition_end - transition_start)
            for t, idx in enumerate(range(transition_start, transition_end)):
                restored_magnitude[idx] = (
                    magnitude[idx] * (1 - transition_curve[t]) +
                    restored_magnitude[idx] * transition_curve[t]
                )

        # Reconstruir áudio
        D_restored = restored_magnitude * np.exp(1j * phase)
        y_restored = librosa.istft(D_restored, hop_length=512)

        # Garantir mesmo tamanho
        if len(y_restored) > len(y):
            y_restored = y_restored[:len(y)]
        elif len(y_restored) < len(y):
            y_restored = np.pad(y_restored, (0, len(y) - len(y_restored)))

        return y_restored

    def _spectral_extension(
        self,
        y: np.ndarray,
        sr: int,
        cutoff_freq: float
    ) -> np.ndarray:
        """
        Extensão espectral usando extrapolação
        """
        # STFT
        D = librosa.stft(y, n_fft=2048, hop_length=512)
        magnitude, phase = np.abs(D), np.angle(D)

        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        cutoff_bin = np.argmin(np.abs(freqs - cutoff_freq))

        # Para cada frame temporal
        for frame_idx in range(magnitude.shape[1]):
            # Pegar espectro abaixo do cutoff
            spectrum_below = magnitude[:cutoff_bin, frame_idx]

            if len(spectrum_below) < 10:
                continue

            # Criar modelo de decaimento espectral
            # Ajustar curva exponencial
            x = np.arange(len(spectrum_below))
            y_spec = spectrum_below + 1e-10

            # Pegar últimos valores para extrapolação
            fit_range = min(100, len(spectrum_below))
            x_fit = x[-fit_range:]
            y_fit = y_spec[-fit_range:]

            # Ajustar decaimento exponencial
            try:
                # log(y) = a*x + b -> y = exp(b) * exp(a*x)
                log_y = np.log(y_fit + 1e-10)
                coeffs = np.polyfit(x_fit, log_y, 1)

                # Extrapolar para frequências altas
                x_extrapolate = np.arange(cutoff_bin, len(magnitude))
                y_extrapolate = np.exp(coeffs[1]) * np.exp(coeffs[0] * x_extrapolate)

                # Combinar com ruído para naturalidade
                noise = np.random.randn(len(y_extrapolate)) * 0.1 * np.mean(y_extrapolate)
                y_extrapolate = y_extrapolate + noise
                y_extrapolate = np.maximum(y_extrapolate, 0)

                # Aplicar com fade
                fade = np.linspace(1, 0.2, len(y_extrapolate))
                y_extrapolate = y_extrapolate * fade

                magnitude[cutoff_bin:, frame_idx] = np.maximum(
                    magnitude[cutoff_bin:, frame_idx],
                    y_extrapolate
                )
            except:
                # Se falhar, apenas continuar
                pass

        # Reconstruir
        D_restored = magnitude * np.exp(1j * phase)
        y_restored = librosa.istft(D_restored, hop_length=512)

        if len(y_restored) > len(y):
            y_restored = y_restored[:len(y)]
        elif len(y_restored) < len(y):
            y_restored = np.pad(y_restored, (0, len(y) - len(y_restored)))

        return y_restored

    def enhance_bass(
        self,
        y: np.ndarray,
        sr: int,
        amount: float = 1.5
    ) -> np.ndarray:
        """
        Realça frequências graves

        Args:
            y: Sinal de áudio
            sr: Sample rate
            amount: Quantidade de realce (1.0 = nenhum, >1.0 = realce)

        Returns:
            Áudio com graves realçados
        """
        # Filtro passa-baixa para extrair graves
        sos = signal.butter(4, 200, btype='low', fs=sr, output='sos')
        bass = signal.sosfilt(sos, y)

        # Adicionar harmônicos
        bass_enhanced = bass * amount

        # Filtro passa-alta para o resto
        sos_high = signal.butter(4, 200, btype='high', fs=sr, output='sos')
        highs = signal.sosfilt(sos_high, y)

        # Combinar
        result = bass_enhanced + highs

        # Normalizar para evitar clipping
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result

    def restore_band(
        self,
        y: np.ndarray,
        sr: int,
        low_freq: float,
        high_freq: float,
        boost_db: float = 6.0
    ) -> np.ndarray:
        """
        Restaura uma banda de frequência específica

        Args:
            y: Sinal de áudio
            sr: Sample rate
            low_freq: Frequência baixa da banda
            high_freq: Frequência alta da banda
            boost_db: Boost em dB

        Returns:
            Áudio com banda restaurada
        """
        # Extrair banda
        sos = signal.butter(4, [low_freq, high_freq], btype='band', fs=sr, output='sos')
        band = signal.sosfilt(sos, y)

        # Aplicar boost
        boost_linear = 10 ** (boost_db / 20)
        band_boosted = band * boost_linear

        # Filtro notch para remover a banda original
        sos_notch = signal.butter(4, [low_freq, high_freq], btype='bandstop', fs=sr, output='sos')
        y_without_band = signal.sosfilt(sos_notch, y)

        # Combinar
        result = y_without_band + band_boosted

        # Normalizar
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result

    def spectral_repair(
        self,
        y: np.ndarray,
        sr: int,
        freq_gaps: list = None
    ) -> np.ndarray:
        """
        Repara gaps no espectro de frequências

        Args:
            y: Sinal de áudio
            sr: Sample rate
            freq_gaps: Lista de tuplas (freq_low, freq_high) indicando gaps

        Returns:
            Áudio com gaps reparados
        """
        if freq_gaps is None:
            return y

        D = librosa.stft(y, n_fft=2048, hop_length=512)
        magnitude, phase = np.abs(D), np.angle(D)

        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)

        for low, high in freq_gaps:
            # Encontrar bins correspondentes
            low_bin = np.argmin(np.abs(freqs - low))
            high_bin = np.argmin(np.abs(freqs - high))

            if high_bin <= low_bin:
                continue

            # Para cada frame temporal
            for frame_idx in range(magnitude.shape[1]):
                # Interpolar entre as bordas do gap
                if low_bin > 0 and high_bin < len(magnitude):
                    # Valores nas bordas
                    val_before = magnitude[low_bin - 1, frame_idx]
                    val_after = magnitude[high_bin + 1, frame_idx]

                    # Interpolação linear
                    gap_length = high_bin - low_bin + 1
                    interpolated = np.linspace(val_before, val_after, gap_length)

                    # Adicionar ruído para naturalidade
                    noise = np.random.randn(gap_length) * 0.05 * np.mean(interpolated)
                    interpolated = interpolated + noise

                    magnitude[low_bin:high_bin + 1, frame_idx] = interpolated

        # Reconstruir
        D_restored = magnitude * np.exp(1j * phase)
        y_restored = librosa.istft(D_restored, hop_length=512)

        if len(y_restored) > len(y):
            y_restored = y_restored[:len(y)]
        elif len(y_restored) < len(y):
            y_restored = np.pad(y_restored, (0, len(y) - len(y_restored)))

        return y_restored

    def apply_psychoacoustic_enhancement(
        self,
        y: np.ndarray,
        sr: int
    ) -> np.ndarray:
        """
        Aplica melhorias psicoacústicas para melhorar percepção de qualidade

        Args:
            y: Sinal de áudio
            sr: Sample rate

        Returns:
            Áudio com melhorias psicoacústicas
        """
        # Exciter harmônico (adiciona harmônicos sutis)
        D = librosa.stft(y, n_fft=2048, hop_length=512)
        magnitude, phase = np.abs(D), np.angle(D)

        # Realçar harmônicos musicais
        enhanced_magnitude = magnitude.copy()

        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)

        # Adicionar brilho (realçar área 4-8kHz sutilmente)
        brightness_range = (freqs >= 4000) & (freqs <= 8000)
        enhanced_magnitude[brightness_range] *= 1.15

        # Adicionar calor (realçar área 200-500Hz sutilmente)
        warmth_range = (freqs >= 200) & (freqs <= 500)
        enhanced_magnitude[warmth_range] *= 1.1

        # Reconstruir
        D_enhanced = enhanced_magnitude * np.exp(1j * phase)
        y_enhanced = librosa.istft(D_enhanced, hop_length=512)

        if len(y_enhanced) > len(y):
            y_enhanced = y_enhanced[:len(y)]
        elif len(y_enhanced) < len(y):
            y_enhanced = np.pad(y_enhanced, (0, len(y) - len(y_enhanced)))

        # Mix sutil com original (30% enhanced, 70% original)
        result = 0.7 * y + 0.3 * y_enhanced

        # Normalizar
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result
