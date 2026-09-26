"""
Optimal configuration for "Ser mais (Edit)_1.mp3"

Analysis Results:
- Duration: 2.7 minutes
- LUFS: -15.0 dB (already close to target)
- SNR: 35.9 dB (very clean signal)
- Peak: 0.873 (no clipping)
- Dynamic Range: 14.5 dB (high, acoustic style)

CRITICAL ISSUE: Extremely bass-heavy frequency distribution
- Bass (20-250 Hz): 68.3% ⚠️
- Mids (250-2000 Hz): 25.3%
- Highs (2-8 kHz): 5.3% ⚠️
- Air (8+ kHz): 1.1% ⚠️

Strategy:
1. Light noise reduction (signal is already clean)
2. Aggressive high-frequency restoration to restore missing treble/air
3. EQ to balance frequencies (reduce bass, boost mids/highs/air)
4. Gentle compression to preserve natural dynamics
5. Light LUFS normalization (-15 to -14)
"""

# =============================================================================
# OPTIMAL CONFIG FOR SER MAIS
# =============================================================================

CONFIG_SER_MAIS_OPTIMAL = {
    # Noise Reduction - Light (signal is clean)
    'remove_clicks': True,
    'reduce_noise': True,
    'noise_reduction_strength': 0.3,  # Light only

    # Frequency Restoration - CRITICAL for this track
    'restore_frequencies': True,
    'freq_restoration_method': 'harmonic_synthesis',
    'restoration_strength': 0.8,  # Strong restoration for missing highs

    # Bass Enhancement - OFF (already too much bass!)
    'enhance_bass': False,
    'bass_enhancement_amount': 1.0,

    # Psychoacoustic Enhancement - Help restore presence
    'psychoacoustic_enhancement': True,

    # Stem Separation - Not needed
    'separate_stems': False,

    # Mastering - Gentle, preserve dynamics
    'target_lufs': -14.0,  # Light boost from -15.0

    # EQ - Aggressive correction for frequency imbalance
    'master_eq': {
        'sub_bass': -1.5,    # Cut sub-bass (too dominant)
        'bass': -1.0,        # Reduce bass (68.3% is way too much)
        'low_mid': 0.5,      # Slight boost
        'mid': 1.5,          # Boost mids (only 25%)
        'high_mid': 2.0,     # Strong boost
        'presence': 3.0,     # Very strong boost (only 5.3% highs!)
        'treble': 3.5,       # Maximum boost for treble
        'air': 4.0           # Maximum boost for air (only 1.1%!)
    },

    # Presence boost - Add clarity
    'add_presence': True,
    'presence_freq': 3000,
    'presence_q': 1.5,
    'presence_gain': 2.5,  # Strong presence boost

    # Compression - Gentle to preserve dynamics
    'compression_ratio': 2.5,  # Light compression
    'compression_threshold': -18,

    # Limiting - Gentle
    'limiter_threshold': -1.5,
    'limiter_release': 0.05
}

# =============================================================================
# ALTERNATIVE CONFIG - More Conservative
# =============================================================================

CONFIG_SER_MAIS_CONSERVATIVE = {
    **CONFIG_SER_MAIS_OPTIMAL,
    'noise_reduction_strength': 0.2,
    'restoration_strength': 0.6,
    'master_eq': {
        'sub_bass': -1.0,
        'bass': -0.5,
        'low_mid': 0.3,
        'mid': 1.0,
        'high_mid': 1.5,
        'presence': 2.0,
        'treble': 2.5,
        'air': 3.0
    },
    'presence_gain': 1.5
}

# =============================================================================
# BASS LOVER CONFIG - Keep the bass character
# =============================================================================

CONFIG_SER_MAIS_BASS_HEAVY = {
    **CONFIG_SER_MAIS_OPTIMAL,
    'master_eq': {
        'sub_bass': 0.0,     # Keep the bass
        'bass': 0.0,         # Keep the bass
        'low_mid': 0.5,
        'mid': 1.5,
        'high_mid': 2.0,
        'presence': 3.0,     # Still boost highs
        'treble': 3.5,
        'air': 4.0
    }
}

# =============================================================================
# EXPORT CONFIG
# =============================================================================

# Use OPTIMAL by default (this track needs frequency rebalancing)
CONFIG = CONFIG_SER_MAIS_OPTIMAL

if __name__ == '__main__':
    import json
    print("="*70)
    print("SER MAIS (EDIT) - OPTIMAL CONFIGURATION")
    print("="*70)
    print("\nSelected: CONFIG_SER_MAIS_OPTIMAL")
    print("\nKey Settings:")
    print(f"  • Noise Reduction: {CONFIG['noise_reduction_strength']} (light)")
    print(f"  • Frequency Restoration: {CONFIG['restoration_strength']} (strong)")
    print(f"  • Target LUFS: {CONFIG['target_lufs']} dB")
    print(f"  • Bass Cut: {CONFIG['master_eq']['bass']} dB")
    print(f"  • Treble Boost: +{CONFIG['master_eq']['treble']} dB")
    print(f"  • Air Boost: +{CONFIG['master_eq']['air']} dB")
    print("\nRationale:")
    print("  • Track is 68.3% bass - needs rebalancing")
    print("  • Only 5.3% highs + 1.1% air - needs strong boost")
    print("  • Clean signal (SNR 35.9) - minimal noise reduction")
    print("  • Good dynamics (14.5 dB) - gentle compression")
    print("="*70)
