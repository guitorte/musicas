"""
Audio Restoration Pipeline - Módulos
"""

from .spectral_analysis import SpectralAnalyzer
from .frequency_restoration import FrequencyRestorer
from .stem_separation import StemSeparator
from .audio_processing import AudioProcessor
from .pipeline import AudioRestorationPipeline
from .advanced_processing import AdvancedAudioProcessor
from .smart_presets import SmartPresetSelector, auto_configure

# Import opcional do interactive_config (requer ipywidgets - apenas para Colab)
try:
    from .interactive_config import InteractiveConfig, create_quick_config
    _has_interactive = True
except ImportError:
    _has_interactive = False
    InteractiveConfig = None
    create_quick_config = None

__all__ = [
    'SpectralAnalyzer',
    'FrequencyRestorer',
    'StemSeparator',
    'AudioProcessor',
    'AudioRestorationPipeline',
    'AdvancedAudioProcessor',
    'SmartPresetSelector',
    'auto_configure',
]

# Adicionar interactive apenas se disponível
if _has_interactive:
    __all__.extend(['InteractiveConfig', 'create_quick_config'])
