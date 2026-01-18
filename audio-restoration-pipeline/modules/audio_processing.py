"""
Módulo de Processamento e Masterização de Áudio
Inclui redução de ruído, compressão, EQ, limitação e masterização
"""

import numpy as np
import librosa
import scipy.signal as signal
from typing import Tuple, Optional, Dict
import warnings

warnings.filterwarnings('ignore')


class AudioProcessor:
    """Processador de áudio com ferramentas profissionais"""

    def __init__(self, sr: int = 44100):
        """
        Inicializa o processador de áudio

        Args:
            sr: Sample rate
        """
        self.sr = sr

    def reduce_noise(
        self,
        y: np.ndarray,
        sr: int,
        noise_profile: Optional[np.ndarray] = None,
        reduction_strength: float = 0.7
    ) -> np.ndarray:
        """
        Reduz ruído do áudio usando espectral gating melhorado

        Args:
            y: Sinal de áudio
            sr: Sample rate
            noise_profile: Perfil de ruído (None = auto-detect)
            reduction_strength: Força da redução (0-1, recomendado: 0.3-0.6)

        Returns:
            Áudio com ruído reduzido
        """
        # IMPORTANTE: Se reduction_strength for 0, pular processamento
        if reduction_strength <= 0.0:
            return y

        # STFT com parâmetros otimizados
        n_fft = 2048
        hop_length = 512
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        magnitude, phase = np.abs(D), np.angle(D)

        # Se não tiver perfil de ruído, estimar dos frames mais silenciosos
        if noise_profile is None:
            # Calcular energia por frame
            frame_energy = np.sum(magnitude, axis=0)

            # Pegar 5% mais silencioso como ruído (era 10%, muito agressivo)
            noise_threshold = np.percentile(frame_energy, 5)
            noise_frames = frame_energy < noise_threshold

            # Estimar perfil de ruído
            if np.any(noise_frames):
                noise_profile = np.median(magnitude[:, noise_frames], axis=1)  # Median é mais robusto que mean
            else:
                noise_profile = np.percentile(magnitude, 2, axis=1)

        # Spectral gating SUAVE para preservar qualidade
        # Ajuste conservador: multiplicador maior = menos redução
        safety_multiplier = 3.0 - (reduction_strength * 2.0)  # Range: 3.0 a 1.0
        noise_threshold = noise_profile[:, np.newaxis] * safety_multiplier

        # Aplicar gating MUITO suave com transição gradual
        # Evita "cortes" abruptos que criam artefatos
        mask = np.clip((magnitude - noise_threshold) / (noise_threshold + 1e-10), 0, 1)

        # Suavizar máscara MUITO para evitar artefatos (sigma maior)
        from scipy.ndimage import gaussian_filter
        mask = gaussian_filter(mask, sigma=2.5)  # Era 1.0, agora muito mais suave

        # Nunca remover completamente - sempre manter pelo menos 10% do sinal
        mask = np.maximum(mask, 0.1)

        # Aplicar máscara
        magnitude_cleaned = magnitude * mask

        # Reconstruir
        D_cleaned = magnitude_cleaned * np.exp(1j * phase)
        y_cleaned = librosa.istft(D_cleaned, hop_length=hop_length, length=len(y))

        # Mix wet/dry baseado em reduction_strength para preservar mais do original
        # Quanto menor a strength, mais do original é preservado
        mix_ratio = reduction_strength * 0.7  # Máximo 70% de wet
        y_cleaned = y_cleaned * mix_ratio + y * (1 - mix_ratio)

        return y_cleaned

    def remove_clicks_and_pops(
        self,
        y: np.ndarray,
        sr: int,
        threshold: float = 3.0
    ) -> np.ndarray:
        """
        Remove clicks e pops usando detecção de outliers

        Args:
            y: Sinal de áudio
            sr: Sample rate
            threshold: Threshold em desvios padrão

        Returns:
            Áudio sem clicks/pops
        """
        # Calcular diferença entre samples
        diff = np.diff(y, prepend=y[0])

        # Detectar outliers
        std = np.std(diff)
        mean = np.mean(diff)

        outliers = np.abs(diff - mean) > (threshold * std)

        # Reparar outliers por interpolação
        y_repaired = y.copy()

        outlier_indices = np.where(outliers)[0]

        for idx in outlier_indices:
            # Interpolar entre vizinhos
            if idx > 0 and idx < len(y) - 1:
                y_repaired[idx] = (y[idx - 1] + y[idx + 1]) / 2

        return y_repaired

    def declip(
        self,
        y: np.ndarray,
        sr: int,
        threshold: float = 0.99
    ) -> np.ndarray:
        """
        Restaura áudio com clipping

        Args:
            y: Sinal de áudio
            sr: Sample rate
            threshold: Threshold de clipping

        Returns:
            Áudio com clipping reduzido
        """
        # Detectar samples clippados
        clipped = np.abs(y) >= threshold

        if not np.any(clipped):
            return y

        y_declipped = y.copy()

        # Encontrar regiões clippadas
        clipped_indices = np.where(clipped)[0]

        # Agrupar índices consecutivos
        groups = []
        current_group = [clipped_indices[0]]

        for i in range(1, len(clipped_indices)):
            if clipped_indices[i] - clipped_indices[i-1] == 1:
                current_group.append(clipped_indices[i])
            else:
                groups.append(current_group)
                current_group = [clipped_indices[i]]
        groups.append(current_group)

        # Reparar cada grupo
        for group in groups:
            if len(group) < 2:
                continue

            start_idx = group[0]
            end_idx = group[-1]

            # Pegar valores antes e depois
            if start_idx > 5 and end_idx < len(y) - 5:
                # Interpolar cubicamente
                x_before = np.arange(start_idx - 5, start_idx)
                y_before = y[start_idx - 5:start_idx]

                x_after = np.arange(end_idx + 1, end_idx + 6)
                y_after = y[end_idx + 1:end_idx + 6]

                # Combinar
                x_points = np.concatenate([x_before, x_after])
                y_points = np.concatenate([y_before, y_after])

                # Interpolar
                x_interp = np.arange(start_idx, end_idx + 1)

                from scipy.interpolate import interp1d
                f = interp1d(x_points, y_points, kind='cubic', fill_value='extrapolate')
                y_declipped[x_interp] = f(x_interp)

        return y_declipped

    def apply_eq(
        self,
        y: np.ndarray,
        sr: int,
        eq_bands: Dict[str, float]
    ) -> np.ndarray:
        """
        Aplica equalização paramétrica

        Args:
            y: Sinal de áudio
            sr: Sample rate
            eq_bands: Dicionário com bandas de EQ
                     Ex: {'bass': 2.0, 'mid': -1.0, 'treble': 3.0}

        Returns:
            Áudio equalizado
        """
        # Definir bandas de frequência padrão
        band_definitions = {
            'sub_bass': (20, 60, 2),      # freq_low, freq_high, Q
            'bass': (60, 250, 2),
            'low_mid': (250, 500, 1.5),
            'mid': (500, 2000, 1),
            'high_mid': (2000, 4000, 1.5),
            'presence': (4000, 6000, 2),
            'treble': (6000, 20000, 2)
        }

        result = y.copy()

        # Aplicar cada banda
        for band_name, gain_db in eq_bands.items():
            if band_name not in band_definitions:
                continue

            low, high, Q = band_definitions[band_name]

            # Criar filtro
            center = np.sqrt(low * high)

            # Aplicar boost/cut
            if abs(gain_db) > 0.1:  # Só aplicar se ganho significativo
                # Usar filtro peaking
                result = self._apply_peaking_filter(result, sr, center, Q, gain_db)

        return result

    def _apply_peaking_filter(
        self,
        y: np.ndarray,
        sr: int,
        center_freq: float,
        Q: float,
        gain_db: float
    ) -> np.ndarray:
        """Aplica filtro peaking (bell) EQ"""

        # Converter para STFT
        D = librosa.stft(y, n_fft=2048, hop_length=512)
        magnitude, phase = np.abs(D), np.angle(D)

        # Calcular ganho linear
        gain_linear = 10 ** (gain_db / 20)

        # Criar curva de ganho
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)

        # Bell curve
        bandwidth = center_freq / Q
        bell_curve = 1 + (gain_linear - 1) * np.exp(
            -((freqs - center_freq) ** 2) / (2 * (bandwidth / 2) ** 2)
        )

        # Aplicar ganho
        magnitude_eq = magnitude * bell_curve[:, np.newaxis]

        # Reconstruir
        D_eq = magnitude_eq * np.exp(1j * phase)
        y_eq = librosa.istft(D_eq, hop_length=512)

        if len(y_eq) > len(y):
            y_eq = y_eq[:len(y)]
        elif len(y_eq) < len(y):
            y_eq = np.pad(y_eq, (0, len(y) - len(y_eq)))

        return y_eq

    def compress(
        self,
        y: np.ndarray,
        sr: int,
        threshold_db: float = -20,
        ratio: float = 4.0,
        attack_ms: float = 5.0,
        release_ms: float = 100.0,
        makeup_gain_db: float = 0.0
    ) -> np.ndarray:
        """
        Aplica compressão dinâmica

        Args:
            y: Sinal de áudio
            sr: Sample rate
            threshold_db: Threshold em dB
            ratio: Razão de compressão
            attack_ms: Tempo de ataque em ms
            release_ms: Tempo de release em ms
            makeup_gain_db: Ganho de compensação

        Returns:
            Áudio comprimido
        """
        # Converter para envelope
        hop_length = 512
        envelope = librosa.feature.rms(y=y, hop_length=hop_length)[0]

        # Converter para dB
        envelope_db = 20 * np.log10(envelope + 1e-10)

        # Calcular ganho de compressão
        gain_db = np.zeros_like(envelope_db)

        # Aplicar compressão onde excede threshold
        over_threshold = envelope_db > threshold_db
        gain_db[over_threshold] = (
            threshold_db - envelope_db[over_threshold]
        ) * (1 - 1/ratio)

        # Suavizar ganho (attack/release)
        attack_samples = int(attack_ms * sr / 1000 / hop_length)
        release_samples = int(release_ms * sr / 1000 / hop_length)

        gain_smoothed = np.zeros_like(gain_db)
        current_gain = 0

        for i in range(len(gain_db)):
            target_gain = gain_db[i]

            if target_gain < current_gain:
                # Attack
                step = (target_gain - current_gain) / max(attack_samples, 1)
            else:
                # Release
                step = (target_gain - current_gain) / max(release_samples, 1)

            current_gain += step
            gain_smoothed[i] = current_gain

        # Converter ganho para linear
        gain_linear = 10 ** (gain_smoothed / 20)

        # Aplicar makeup gain
        makeup_gain_linear = 10 ** (makeup_gain_db / 20)
        gain_linear *= makeup_gain_linear

        # Interpolar ganho para match tamanho original
        gain_interp = np.interp(
            np.arange(len(y)),
            np.arange(len(gain_linear)) * hop_length,
            gain_linear
        )

        # Aplicar ganho
        y_compressed = y * gain_interp

        return y_compressed

    def limit(
        self,
        y: np.ndarray,
        threshold_db: float = -0.5,
        release_ms: float = 50.0
    ) -> np.ndarray:
        """
        Aplica limitação (brick wall limiter)

        Args:
            y: Sinal de áudio
            threshold_db: Threshold em dB
            release_ms: Tempo de release

        Returns:
            Áudio limitado
        """
        # Threshold linear
        threshold = 10 ** (threshold_db / 20)

        # Detectar picos
        envelope = np.abs(y)

        # Calcular ganho necessário
        gain = np.ones_like(y)
        gain[envelope > threshold] = threshold / (envelope[envelope > threshold] + 1e-10)

        # Suavizar ganho
        from scipy.ndimage import minimum_filter1d

        # Aplicar release
        release_samples = int(release_ms * self.sr / 1000)
        if release_samples > 0:
            gain = minimum_filter1d(gain, size=release_samples)

        # Aplicar limitação
        y_limited = y * gain

        return y_limited

    def normalize_lufs(
        self,
        y: np.ndarray,
        target_lufs: float = -14.0
    ) -> np.ndarray:
        """
        Normaliza áudio para target LUFS

        Args:
            y: Sinal de áudio
            target_lufs: LUFS alvo (padrão: -14.0 para streaming)

        Returns:
            Áudio normalizado
        """
        # Calcular LUFS estimado (simplificado)
        rms = np.sqrt(np.mean(y ** 2))
        current_lufs = -23 + 20 * np.log10(rms + 1e-10)

        # Calcular ganho necessário
        gain_db = target_lufs - current_lufs
        gain_linear = 10 ** (gain_db / 20)

        # Aplicar ganho
        y_normalized = y * gain_linear

        # Garantir que não clipa
        max_val = np.max(np.abs(y_normalized))
        if max_val > 0.99:
            y_normalized = y_normalized * (0.99 / max_val)

        return y_normalized

    def master(
        self,
        y: np.ndarray,
        sr: int,
        target_lufs: float = -14.0,
        master_eq: Dict[str, float] = None,
        add_presence: bool = True
    ) -> np.ndarray:
        """
        Aplica cadeia completa de masterização

        Args:
            y: Sinal de áudio
            sr: Sample rate
            target_lufs: LUFS alvo
            master_eq: EQ de masterização
            add_presence: Adicionar presença/brilho

        Returns:
            Áudio masterizado
        """
        result = y.copy()

        # 1. Limpeza
        result = self.remove_clicks_and_pops(result, sr)

        # 2. EQ de masterização
        if master_eq is None:
            master_eq = {
                'bass': 0.5,      # Leve boost nos graves
                'mid': 0.0,       # Neutro
                'presence': 1.0,  # Boost em presença
                'treble': 0.8     # Leve boost nos agudos
            }

        result = self.apply_eq(result, sr, master_eq)

        # 3. Compressão suave de masterização
        result = self.compress(
            result, sr,
            threshold_db=-18,
            ratio=2.0,
            attack_ms=10,
            release_ms=200,
            makeup_gain_db=2.0
        )

        # 4. Adicionar presença se solicitado
        if add_presence:
            # Exciter sutil
            D = librosa.stft(result, n_fft=2048, hop_length=512)
            magnitude, phase = np.abs(D), np.angle(D)

            freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
            presence_range = (freqs >= 3000) & (freqs <= 8000)
            magnitude[presence_range] *= 1.1

            D_enhanced = magnitude * np.exp(1j * phase)
            result = librosa.istft(D_enhanced, hop_length=512)

            if len(result) > len(y):
                result = result[:len(y)]
            elif len(result) < len(y):
                result = np.pad(result, (0, len(y) - len(result)))

        # 5. Normalização LUFS
        result = self.normalize_lufs(result, target_lufs)

        # 6. Limitação final
        result = self.limit(result, threshold_db=-0.5, release_ms=50)

        return result

    def apply_stereo_widening(
        self,
        y: np.ndarray,
        amount: float = 1.3
    ) -> np.ndarray:
        """
        Aplica alargamento de campo estéreo (apenas para estéreo)

        Args:
            y: Sinal de áudio (estéreo)
            amount: Quantidade de alargamento (1.0 = nenhum)

        Returns:
            Áudio com campo estéreo alargado
        """
        if len(y.shape) == 1:
            # Mono, não pode alargar
            return y

        # Mid/Side processing
        mid = (y[0] + y[1]) / 2
        side = (y[0] - y[1]) / 2

        # Alargar aumentando componente side
        side_widened = side * amount

        # Reconstruir
        left = mid + side_widened
        right = mid - side_widened

        # Normalizar
        result = np.stack([left, right])
        max_val = np.max(np.abs(result))
        if max_val > 0.95:
            result = result * (0.95 / max_val)

        return result
