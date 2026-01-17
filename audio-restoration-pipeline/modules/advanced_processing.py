"""
Módulo de Processamento Avançado
Técnicas profissionais adicionais de processamento de áudio
"""

import numpy as np
import librosa
import scipy.signal as signal
from typing import Tuple, Optional, Dict
import warnings

warnings.filterwarnings('ignore')


class AdvancedAudioProcessor:
    """Processamento avançado de áudio"""

    def __init__(self, sr: int = 44100):
        self.sr = sr

    def multiband_compress(
        self,
        y: np.ndarray,
        sr: int,
        bands: list = None,
        ratios: list = None,
        thresholds: list = None
    ) -> np.ndarray:
        """
        Compressão multi-banda profissional

        Args:
            y: Sinal de áudio
            sr: Sample rate
            bands: Lista de bandas [(low, high), ...]
            ratios: Razões de compressão por banda
            thresholds: Thresholds em dB por banda

        Returns:
            Áudio com compressão multi-banda
        """
        if bands is None:
            # Bandas padrão: Low, Low-Mid, Mid-High, High
            bands = [
                (20, 200),      # Low
                (200, 1000),    # Low-Mid
                (1000, 5000),   # Mid-High
                (5000, 20000)   # High
            ]

        if ratios is None:
            ratios = [3.0, 4.0, 3.0, 2.0]

        if thresholds is None:
            thresholds = [-24, -20, -18, -20]

        # Separar em bandas
        band_signals = []
        for (low, high) in bands:
            sos = signal.butter(4, [low, high], btype='band', fs=sr, output='sos')
            band = signal.sosfilt(sos, y)
            band_signals.append(band)

        # Comprimir cada banda
        from .audio_processing import AudioProcessor
        processor = AudioProcessor(sr=sr)

        compressed_bands = []
        for i, band_signal in enumerate(band_signals):
            compressed = processor.compress(
                band_signal,
                sr,
                threshold_db=thresholds[i],
                ratio=ratios[i],
                attack_ms=5,
                release_ms=100
            )
            compressed_bands.append(compressed)

        # Combinar bandas
        result = np.sum(compressed_bands, axis=0)

        # Normalizar
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result

    def stereo_enhance(
        self,
        y: np.ndarray,
        width: float = 1.5,
        focus_freq: float = 200
    ) -> np.ndarray:
        """
        Melhoria avançada do campo estéreo

        Args:
            y: Sinal de áudio (estéreo)
            width: Largura estéreo (1.0 = normal, >1.0 = mais largo)
            focus_freq: Frequência abaixo da qual manter mono

        Returns:
            Áudio com campo estéreo melhorado
        """
        if len(y.shape) == 1:
            # Mono, criar pseudo-estéreo
            y_stereo = np.stack([y, y])
            return y_stereo

        # Mid/Side processing
        mid = (y[0] + y[1]) / 2
        side = (y[0] - y[1]) / 2

        # Filtrar graves para manter mono (evita problemas de fase)
        sos_low = signal.butter(4, focus_freq, btype='low', fs=self.sr, output='sos')
        mid_low = signal.sosfilt(sos_low, mid)

        sos_high = signal.butter(4, focus_freq, btype='high', fs=self.sr, output='sos')
        mid_high = signal.sosfilt(sos_high, mid)
        side_high = signal.sosfilt(sos_high, side)

        # Alargar apenas frequências altas
        side_enhanced = side_high * width

        # Reconstruir
        mid_final = mid_low + mid_high
        side_final = side_enhanced

        left = mid_final + side_final
        right = mid_final - side_final

        result = np.stack([left, right])

        # Normalizar
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result

    def de_esser(
        self,
        y: np.ndarray,
        sr: int,
        freq_range: Tuple[float, float] = (5000, 8000),
        threshold_db: float = -15,
        ratio: float = 4.0
    ) -> np.ndarray:
        """
        De-esser para reduzir sibilância em vocais

        Args:
            y: Sinal de áudio
            sr: Sample rate
            freq_range: Range de frequências sibilantes
            threshold_db: Threshold em dB
            ratio: Razão de compressão

        Returns:
            Áudio com sibilância reduzida
        """
        # Extrair banda de sibilância
        sos = signal.butter(4, freq_range, btype='band', fs=sr, output='sos')
        sibilance_band = signal.sosfilt(sos, y)

        # Detectar envelope da sibilância
        envelope = np.abs(sibilance_band)
        envelope_smooth = signal.medfilt(envelope, kernel_size=441)  # ~10ms at 44.1kHz

        # Converter para dB
        envelope_db = 20 * np.log10(envelope_smooth + 1e-10)

        # Calcular ganho de redução
        gain_reduction = np.zeros_like(envelope_db)
        over_threshold = envelope_db > threshold_db

        gain_reduction[over_threshold] = (
            threshold_db - envelope_db[over_threshold]
        ) * (1 - 1/ratio)

        # Converter para linear
        gain_linear = 10 ** (gain_reduction / 20)

        # Aplicar ganho apenas na banda
        sibilance_reduced = sibilance_band * gain_linear

        # Reconstruir
        sos_notch = signal.butter(4, freq_range, btype='bandstop', fs=sr, output='sos')
        y_without_sibilance = signal.sosfilt(sos_notch, y)

        result = y_without_sibilance + sibilance_reduced

        return result

    def transient_shaper(
        self,
        y: np.ndarray,
        sr: int,
        attack_gain: float = 1.0,
        sustain_gain: float = 1.0
    ) -> np.ndarray:
        """
        Transient shaping para controlar ataques e sustains

        Args:
            y: Sinal de áudio
            sr: Sample rate
            attack_gain: Ganho dos transientes (>1.0 = mais punch)
            sustain_gain: Ganho do sustain (<1.0 = mais seco)

        Returns:
            Áudio com transientes processados
        """
        # Detectar envelope rápido (transientes) e lento (sustain)
        hop_length = 512

        # Envelope rápido (attack)
        rms_fast = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop_length)[0]

        # Envelope lento (sustain)
        rms_slow = librosa.feature.rms(y=y, frame_length=8192, hop_length=hop_length)[0]

        # Detectar transientes (diferença entre envelopes)
        transient_strength = np.maximum(rms_fast - rms_slow, 0)
        sustained_strength = rms_slow

        # Normalizar
        transient_strength = transient_strength / (np.max(transient_strength) + 1e-10)
        sustained_strength = sustained_strength / (np.max(sustained_strength) + 1e-10)

        # Criar máscaras de ganho
        transient_mask = transient_strength * (attack_gain - 1) + 1
        sustain_mask = sustained_strength * (sustain_gain - 1) + 1

        # Combinar
        gain_mask = transient_mask * sustain_mask

        # Interpolar para match tamanho do áudio
        gain_interp = np.interp(
            np.arange(len(y)),
            np.arange(len(gain_mask)) * hop_length,
            gain_mask
        )

        # Aplicar
        result = y * gain_interp

        # Normalizar
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result

    def phase_correction(
        self,
        y: np.ndarray,
        sr: int
    ) -> np.ndarray:
        """
        Correção de fase usando filtro all-pass

        Args:
            y: Sinal de áudio
            sr: Sample rate

        Returns:
            Áudio com fase corrigida
        """
        # Análise de fase
        D = librosa.stft(y)
        magnitude, phase = np.abs(D), np.angle(D)

        # Unwrap fase
        phase_unwrapped = np.unwrap(phase, axis=1)

        # Calcular derivada de fase (group delay)
        group_delay = -np.diff(phase_unwrapped, axis=1)

        # Detectar anomalias (saltos grandes)
        # Suavizar fase onde há problemas
        median_group_delay = np.median(group_delay, axis=1, keepdims=True)

        # Criar fase corrigida
        phase_corrected = phase.copy()

        # Aplicar correção suave
        for i in range(phase_corrected.shape[0]):
            phase_corrected[i] = np.unwrap(phase[i])

        # Reconstruir
        D_corrected = magnitude * np.exp(1j * phase_corrected)
        y_corrected = librosa.istft(D_corrected)

        # Garantir mesmo tamanho
        if len(y_corrected) > len(y):
            y_corrected = y_corrected[:len(y)]
        elif len(y_corrected) < len(y):
            y_corrected = np.pad(y_corrected, (0, len(y) - len(y_corrected)))

        return y_corrected

    def harmonic_exciter(
        self,
        y: np.ndarray,
        sr: int,
        drive: float = 0.3,
        mix: float = 0.2
    ) -> np.ndarray:
        """
        Exciter harmônico para adicionar harmônicos

        Args:
            y: Sinal de áudio
            sr: Sample rate
            drive: Quantidade de distorção (0-1)
            mix: Mix wet/dry (0-1)

        Returns:
            Áudio com exciter aplicado
        """
        # Aplicar distorção suave (tanh) para gerar harmônicos
        y_driven = np.tanh(y * (1 + drive * 10))

        # Filtro passa-alta para pegar apenas harmônicos gerados
        sos = signal.butter(4, 3000, btype='high', fs=sr, output='sos')
        harmonics = signal.sosfilt(sos, y_driven)

        # Mix com original
        result = y * (1 - mix) + harmonics * mix

        # Normalizar
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result

    def auto_eq_analyzer(
        self,
        y: np.ndarray,
        sr: int
    ) -> Dict[str, float]:
        """
        Analisa áudio e sugere correções de EQ automaticamente

        Args:
            y: Sinal de áudio
            sr: Sample rate

        Returns:
            Dicionário com sugestões de EQ por banda
        """
        # Calcular espectro
        fft = np.fft.fft(y)
        magnitude = np.abs(fft)
        frequency = np.fft.fftfreq(len(y), 1/sr)

        positive_freq_idx = frequency > 0
        frequency = frequency[positive_freq_idx]
        magnitude = magnitude[positive_freq_idx]

        # Definir bandas
        bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'presence': (4000, 6000),
            'treble': (6000, 20000)
        }

        # Calcular energia por banda
        band_energy = {}
        for band_name, (low, high) in bands.items():
            band_mask = (frequency >= low) & (frequency <= high)
            band_energy[band_name] = np.mean(magnitude[band_mask])

        # Normalizar
        total_energy = sum(band_energy.values())
        band_energy_norm = {k: v/total_energy for k, v in band_energy.items()}

        # Calcular desvios de um espectro "ideal"
        ideal_distribution = {
            'sub_bass': 0.08,
            'bass': 0.15,
            'low_mid': 0.12,
            'mid': 0.25,
            'high_mid': 0.20,
            'presence': 0.12,
            'treble': 0.08
        }

        # Sugerir correções
        eq_suggestions = {}
        for band in band_energy_norm:
            current = band_energy_norm[band]
            ideal = ideal_distribution[band]

            # Calcular diferença e converter para dB
            ratio = current / ideal
            db_correction = 20 * np.log10(ratio)

            # Inverter (se tem muito, reduzir; se tem pouco, aumentar)
            suggested_gain = -db_correction * 0.5  # Fator 0.5 para correção suave

            # Limitar a ±6dB
            suggested_gain = np.clip(suggested_gain, -6, 6)

            eq_suggestions[band] = float(suggested_gain)

        return eq_suggestions

    def adaptive_dynamics(
        self,
        y: np.ndarray,
        sr: int,
        target_crest_factor: float = 4.0
    ) -> np.ndarray:
        """
        Processamento dinâmico adaptativo baseado no crest factor

        Args:
            y: Sinal de áudio
            sr: Sample rate
            target_crest_factor: Crest factor alvo

        Returns:
            Áudio com dinâmica otimizada
        """
        # Calcular crest factor atual
        rms = np.sqrt(np.mean(y ** 2))
        peak = np.max(np.abs(y))
        current_crest = peak / (rms + 1e-10)

        if current_crest > target_crest_factor:
            # Muito dinâmico, comprimir
            ratio = current_crest / target_crest_factor
            compression_ratio = np.clip(ratio, 1.5, 8.0)

            from .audio_processing import AudioProcessor
            processor = AudioProcessor(sr=sr)

            result = processor.compress(
                y, sr,
                threshold_db=-18,
                ratio=compression_ratio,
                attack_ms=5,
                release_ms=100
            )
        else:
            # Já está bom, apenas limitar
            from .audio_processing import AudioProcessor
            processor = AudioProcessor(sr=sr)

            result = processor.limit(y, threshold_db=-0.5)

        return result
