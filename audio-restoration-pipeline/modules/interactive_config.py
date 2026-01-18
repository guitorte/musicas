"""
Interface Interativa para Configuração do Pipeline
Widgets do Google Colab para configuração visual
"""

from typing import Dict, Any
import ipywidgets as widgets
from IPython.display import display, HTML


class InteractiveConfig:
    """Interface interativa para configuração do pipeline"""

    def __init__(self):
        self.config = {}
        self.widgets = {}

    def create_interface(self) -> Dict:
        """
        Cria interface interativa completa

        Returns:
            Configuração baseada nas seleções do usuário
        """
        # Estilo CSS
        display(HTML("""
        <style>
        .widget-label { font-weight: bold; color: #2c3e50; }
        .widget-box { border: 2px solid #3498db; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .section-header { background: #3498db; color: white; padding: 10px; margin: 15px 0 10px 0; border-radius: 5px; font-weight: bold; }
        </style>
        """))

        # ═══════════════════════════════════════════════════════════
        # PERFIL PRÉ-CONFIGURADO
        # ═══════════════════════════════════════════════════════════
        display(HTML('<div class="section-header">🎯 1. SELECIONE UM PERFIL BASE</div>'))

        self.widgets['preset'] = widgets.Dropdown(
            options=[
                ('🔹 Padrão - Restauração balanceada', 'padrao'),
                ('⭐ Alta Qualidade - Demucs (recomendado)', 'demucs'),
                ('🔥 Restauração Agressiva - Áudio degradado', 'agressivo'),
                ('⚡ Stems Básico - Separação rápida', 'stems_basico'),
                ('💎 Máxima Qualidade - Processamento completo', 'maxima'),
                ('🎵 Suave - Apenas ajustes leves', 'suave'),
                ('🎚️ Personalizado - Configurar manualmente', 'custom')
            ],
            value='demucs',
            description='Perfil:',
            style={'description_width': '120px'},
            layout=widgets.Layout(width='600px')
        )

        preset_info = widgets.HTML(
            value='<p><b>Alta Qualidade:</b> Separação de stems com Demucs + restauração completa. Tempo: 5-20min com GPU.</p>'
        )

        def on_preset_change(change):
            info_map = {
                'padrao': '<p><b>Padrão:</b> Restauração balanceada sem separação de stems. Rápido (~2-5min).</p>',
                'demucs': '<p><b>Alta Qualidade:</b> Separação de stems com Demucs + restauração completa. Tempo: 5-20min com GPU.</p>',
                'agressivo': '<p><b>Agressivo:</b> Redução forte de ruído + boost agressivo para áudio muito degradado.</p>',
                'stems_basico': '<p><b>Stems Básico:</b> Separação rápida sem Demucs. Tempo: 3-8min.</p>',
                'maxima': '<p><b>Máxima:</b> Todos os processamentos ativados. Melhor qualidade, maior tempo.</p>',
                'suave': '<p><b>Suave:</b> Apenas ajustes mínimos para áudio que já tem boa qualidade.</p>',
                'custom': '<p><b>Personalizado:</b> Configure todos os parâmetros manualmente abaixo.</p>'
            }
            preset_info.value = info_map.get(change['new'], '')

        self.widgets['preset'].observe(on_preset_change, names='value')

        display(self.widgets['preset'], preset_info)

        # ═══════════════════════════════════════════════════════════
        # LIMPEZA E RESTAURAÇÃO
        # ═══════════════════════════════════════════════════════════
        display(HTML('<div class="section-header">🧹 2. LIMPEZA E RESTAURAÇÃO</div>'))

        self.widgets['remove_clicks'] = widgets.Checkbox(
            value=True,
            description='Remover clicks e pops',
            style={'description_width': 'initial'}
        )

        self.widgets['reduce_noise'] = widgets.Checkbox(
            value=True,
            description='Reduzir ruído de fundo',
            style={'description_width': 'initial'}
        )

        self.widgets['noise_strength'] = widgets.FloatSlider(
            value=0.6,
            min=0.0,
            max=1.0,
            step=0.05,
            description='Força redução ruído:',
            style={'description_width': '150px'},
            layout=widgets.Layout(width='500px'),
            readout_format='.2f'
        )

        self.widgets['restore_frequencies'] = widgets.Checkbox(
            value=True,
            description='Restaurar frequências perdidas',
            style={'description_width': 'initial'}
        )

        self.widgets['freq_method'] = widgets.Dropdown(
            options=[
                ('Síntese Harmônica (recomendado)', 'harmonic_synthesis'),
                ('Extensão Espectral', 'spectral_extension')
            ],
            value='harmonic_synthesis',
            description='Método:',
            style={'description_width': '120px'}
        )

        display(
            self.widgets['remove_clicks'],
            self.widgets['reduce_noise'],
            self.widgets['noise_strength'],
            self.widgets['restore_frequencies'],
            self.widgets['freq_method']
        )

        # ═══════════════════════════════════════════════════════════
        # SEPARAÇÃO DE STEMS
        # ═══════════════════════════════════════════════════════════
        display(HTML('<div class="section-header">🎸 3. SEPARAÇÃO DE STEMS</div>'))

        self.widgets['separate_stems'] = widgets.Checkbox(
            value=True,
            description='Separar em stems (vocal, drums, bass, other)',
            style={'description_width': 'initial'}
        )

        self.widgets['stem_model'] = widgets.Dropdown(
            options=[
                ('⭐ Demucs - Máxima qualidade (requer GPU)', 'demucs'),
                ('⚡ Básico - Rápido e leve', 'basic')
            ],
            value='demucs',
            description='Modelo:',
            style={'description_width': '120px'}
        )

        self.widgets['process_stems_individually'] = widgets.Checkbox(
            value=True,
            description='Processar cada stem individualmente',
            style={'description_width': 'initial'}
        )

        display(
            self.widgets['separate_stems'],
            self.widgets['stem_model'],
            self.widgets['process_stems_individually']
        )

        # ═══════════════════════════════════════════════════════════
        # EQUALIZAÇÃO E DINÂMICA
        # ═══════════════════════════════════════════════════════════
        display(HTML('<div class="section-header">🎛️ 4. EQUALIZAÇÃO E DINÂMICA</div>'))

        self.widgets['eq_bass'] = widgets.FloatSlider(
            value=0.0,
            min=-6.0,
            max=6.0,
            step=0.5,
            description='Graves (60-250Hz):',
            style={'description_width': '150px'},
            layout=widgets.Layout(width='500px'),
            readout_format='.1f'
        )

        self.widgets['eq_mid'] = widgets.FloatSlider(
            value=0.0,
            min=-6.0,
            max=6.0,
            step=0.5,
            description='Médios (500-2kHz):',
            style={'description_width': '150px'},
            layout=widgets.Layout(width='500px'),
            readout_format='.1f'
        )

        self.widgets['eq_presence'] = widgets.FloatSlider(
            value=2.0,
            min=-6.0,
            max=6.0,
            step=0.5,
            description='Presença (4-6kHz):',
            style={'description_width': '150px'},
            layout=widgets.Layout(width='500px'),
            readout_format='.1f'
        )

        self.widgets['eq_treble'] = widgets.FloatSlider(
            value=2.5,
            min=-6.0,
            max=6.0,
            step=0.5,
            description='Agudos (6-20kHz):',
            style={'description_width': '150px'},
            layout=widgets.Layout(width='500px'),
            readout_format='.1f'
        )

        self.widgets['enhance_bass'] = widgets.Checkbox(
            value=False,
            description='Realçar graves (harmônico)',
            style={'description_width': 'initial'}
        )

        self.widgets['bass_amount'] = widgets.FloatSlider(
            value=1.3,
            min=1.0,
            max=2.0,
            step=0.1,
            description='Quantidade:',
            style={'description_width': '150px'},
            layout=widgets.Layout(width='500px'),
            readout_format='.1f'
        )

        display(
            self.widgets['eq_bass'],
            self.widgets['eq_mid'],
            self.widgets['eq_presence'],
            self.widgets['eq_treble'],
            self.widgets['enhance_bass'],
            self.widgets['bass_amount']
        )

        # ═══════════════════════════════════════════════════════════
        # MASTERIZAÇÃO
        # ═══════════════════════════════════════════════════════════
        display(HTML('<div class="section-header">🎚️ 5. MASTERIZAÇÃO</div>'))

        self.widgets['target_lufs'] = widgets.FloatSlider(
            value=-14.0,
            min=-23.0,
            max=-8.0,
            step=0.5,
            description='LUFS alvo:',
            style={'description_width': '150px'},
            layout=widgets.Layout(width='500px'),
            readout_format='.1f'
        )

        lufs_info = widgets.HTML(
            value='''
            <p style="margin: 5px 0; font-size: 12px;">
            <b>-14 LUFS:</b> Spotify, YouTube, Apple Music<br>
            <b>-16 LUFS:</b> TV, Rádio, Broadcast<br>
            <b>-23 LUFS:</b> Cinema
            </p>
            '''
        )

        self.widgets['add_presence'] = widgets.Checkbox(
            value=True,
            description='Adicionar brilho e presença (exciter)',
            style={'description_width': 'initial'}
        )

        self.widgets['psychoacoustic'] = widgets.Checkbox(
            value=True,
            description='Melhorias psicoacústicas',
            style={'description_width': 'initial'}
        )

        display(
            self.widgets['target_lufs'],
            lufs_info,
            self.widgets['add_presence'],
            self.widgets['psychoacoustic']
        )

        # ═══════════════════════════════════════════════════════════
        # PROCESSAMENTO AVANÇADO
        # ═══════════════════════════════════════════════════════════
        display(HTML('<div class="section-header">⚡ 6. PROCESSAMENTO AVANÇADO (Opcional)</div>'))

        self.widgets['multiband_compress'] = widgets.Checkbox(
            value=False,
            description='Compressão multi-banda',
            style={'description_width': 'initial'}
        )

        self.widgets['stereo_enhance'] = widgets.Checkbox(
            value=False,
            description='Alargamento estéreo avançado',
            style={'description_width': 'initial'}
        )

        self.widgets['de_esser'] = widgets.Checkbox(
            value=False,
            description='De-esser (reduzir sibilância em vocais)',
            style={'description_width': 'initial'}
        )

        self.widgets['transient_shaper'] = widgets.Checkbox(
            value=False,
            description='Transient shaper (mais punch)',
            style={'description_width': 'initial'}
        )

        self.widgets['harmonic_exciter'] = widgets.Checkbox(
            value=False,
            description='Exciter harmônico (mais harmônicos)',
            style={'description_width': 'initial'}
        )

        display(
            self.widgets['multiband_compress'],
            self.widgets['stereo_enhance'],
            self.widgets['de_esser'],
            self.widgets['transient_shaper'],
            self.widgets['harmonic_exciter']
        )

        # ═══════════════════════════════════════════════════════════
        # BOTÃO GERAR CONFIGURAÇÃO
        # ═══════════════════════════════════════════════════════════
        generate_button = widgets.Button(
            description='✓ GERAR CONFIGURAÇÃO',
            button_style='success',
            layout=widgets.Layout(width='300px', height='50px'),
            style={'font_weight': 'bold'}
        )

        output_area = widgets.Output()

        def on_generate_click(b):
            with output_area:
                output_area.clear_output()
                config = self._build_config()

                print("═" * 60)
                print("✓ CONFIGURAÇÃO GERADA!")
                print("═" * 60)

                import json
                print(json.dumps(config, indent=2))

                print("\n" + "═" * 60)
                print("💡 Use esta configuração:")
                print("═" * 60)
                print("CONFIG = " + str(config).replace("'", '"'))
                print("\n✓ Pronto para processar!")

        generate_button.on_click(on_generate_click)

        display(HTML('<br>'))
        display(generate_button)
        display(output_area)

        return self._build_config()

    def _build_config(self) -> Dict:
        """Constrói configuração baseada nos widgets"""

        preset = self.widgets['preset'].value

        # Se for preset pré-definido, retornar config correspondente
        if preset != 'custom':
            return self._get_preset_config(preset)

        # Config personalizado
        config = {
            'remove_clicks': self.widgets['remove_clicks'].value,
            'reduce_noise': self.widgets['reduce_noise'].value,
            'noise_reduction_strength': self.widgets['noise_strength'].value,

            'restore_frequencies': self.widgets['restore_frequencies'].value,
            'freq_restoration_method': self.widgets['freq_method'].value,

            'enhance_bass': self.widgets['enhance_bass'].value,
            'bass_enhancement_amount': self.widgets['bass_amount'].value,

            'psychoacoustic_enhancement': self.widgets['psychoacoustic'].value,

            'separate_stems': self.widgets['separate_stems'].value,
            'stem_separation_model': self.widgets['stem_model'].value,
            'process_stems_individually': self.widgets['process_stems_individually'].value,

            'target_lufs': self.widgets['target_lufs'].value,

            'master_eq': {
                'bass': self.widgets['eq_bass'].value,
                'mid': self.widgets['eq_mid'].value,
                'presence': self.widgets['eq_presence'].value,
                'treble': self.widgets['eq_treble'].value
            },

            'add_presence': self.widgets['add_presence'].value,

            # Processamento avançado
            'advanced': {
                'multiband_compress': self.widgets['multiband_compress'].value,
                'stereo_enhance': self.widgets['stereo_enhance'].value,
                'de_esser': self.widgets['de_esser'].value,
                'transient_shaper': self.widgets['transient_shaper'].value,
                'harmonic_exciter': self.widgets['harmonic_exciter'].value
            }
        }

        return config

    def _get_preset_config(self, preset: str) -> Dict:
        """Retorna configuração de um preset"""

        presets = {
            'padrao': {
                'remove_clicks': True,
                'reduce_noise': True,
                'noise_reduction_strength': 0.6,
                'restore_frequencies': True,
                'freq_restoration_method': 'harmonic_synthesis',
                'enhance_bass': False,
                'psychoacoustic_enhancement': True,
                'separate_stems': False,
                'target_lufs': -14.0,
                'master_eq': {'bass': 0.0, 'mid': 0.0, 'presence': 1.0, 'treble': 0.8},
                'add_presence': True,
                'advanced': {}
            },
            'demucs': {
                'remove_clicks': True,
                'reduce_noise': True,
                'noise_reduction_strength': 0.6,
                'restore_frequencies': True,
                'freq_restoration_method': 'harmonic_synthesis',
                'enhance_bass': False,
                'psychoacoustic_enhancement': True,
                'separate_stems': True,
                'stem_separation_model': 'demucs',
                'process_stems_individually': True,
                'target_lufs': -14.0,
                'master_eq': {'bass': 0.0, 'mid': 0.0, 'presence': 2.0, 'treble': 2.5},
                'add_presence': True,
                'advanced': {}
            },
            'agressivo': {
                'remove_clicks': True,
                'reduce_noise': True,
                'noise_reduction_strength': 0.85,
                'restore_frequencies': True,
                'freq_restoration_method': 'spectral_extension',
                'enhance_bass': True,
                'bass_enhancement_amount': 1.5,
                'psychoacoustic_enhancement': True,
                'separate_stems': False,
                'target_lufs': -14.0,
                'master_eq': {'bass': 0.5, 'mid': -1.0, 'presence': 3.0, 'treble': 3.5},
                'add_presence': True,
                'advanced': {}
            },
            'stems_basico': {
                'remove_clicks': True,
                'reduce_noise': True,
                'noise_reduction_strength': 0.6,
                'restore_frequencies': True,
                'freq_restoration_method': 'harmonic_synthesis',
                'enhance_bass': False,
                'psychoacoustic_enhancement': True,
                'separate_stems': True,
                'stem_separation_model': 'basic',
                'process_stems_individually': True,
                'target_lufs': -14.0,
                'master_eq': {'bass': 0.0, 'mid': 0.0, 'presence': 2.0, 'treble': 2.5},
                'add_presence': True,
                'advanced': {}
            },
            'maxima': {
                'remove_clicks': True,
                'reduce_noise': True,
                'noise_reduction_strength': 0.7,
                'restore_frequencies': True,
                'freq_restoration_method': 'harmonic_synthesis',
                'enhance_bass': False,
                'psychoacoustic_enhancement': True,
                'separate_stems': True,
                'stem_separation_model': 'demucs',
                'process_stems_individually': True,
                'target_lufs': -14.0,
                'master_eq': {'bass': 0.5, 'mid': 0.0, 'presence': 2.0, 'treble': 2.5},
                'add_presence': True,
                'advanced': {
                    'multiband_compress': True,
                    'stereo_enhance': True,
                    'de_esser': False,
                    'transient_shaper': False,
                    'harmonic_exciter': True
                }
            },
            'suave': {
                'remove_clicks': True,
                'reduce_noise': False,
                'noise_reduction_strength': 0.0,
                'restore_frequencies': True,
                'freq_restoration_method': 'harmonic_synthesis',
                'enhance_bass': False,
                'psychoacoustic_enhancement': True,
                'separate_stems': False,
                'target_lufs': -14.0,
                'master_eq': {'bass': 0.0, 'mid': 0.0, 'presence': 0.5, 'treble': 0.3},
                'add_presence': False,
                'advanced': {}
            }
        }

        return presets.get(preset, presets['padrao'])


def create_quick_config() -> Dict:
    """Cria interface rápida e retorna configuração"""
    interface = InteractiveConfig()
    return interface.create_interface()
