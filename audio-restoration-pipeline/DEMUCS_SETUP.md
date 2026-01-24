# 🎸 Guia de Setup do Demucs

## ❌ Problema Comum: TorchCodec / FFmpeg

Se você ver este erro ao usar Demucs:

```
RuntimeError: Could not load libtorchcodec. Likely causes:
1. FFmpeg is not properly installed in your environment.
```

## ✅ SOLUÇÃO RÁPIDA (Google Colab):

### **Execute esta célula ANTES de processar:**

```python
# Instalar FFmpeg (necessário para Demucs salvar arquivos)
!apt-get update && apt-get install -y ffmpeg

print("✓ FFmpeg instalado!")
print("✓ Agora você pode usar Demucs normalmente")
```

---

## 📋 Ordem Correta de Execução no Colab:

### **1. Instalação de Dependências:**
```python
!pip install -q librosa soundfile scipy matplotlib numpy noisereduce
!pip install -U demucs torchcodec
```

### **2. Instalar FFmpeg (NOVO - OBRIGATÓRIO para Demucs):**
```python
!apt-get update && apt-get install -y ffmpeg
```

### **3. Setup do Drive e Pipeline:**
```python
from google.colab import drive
drive.mount('/content/drive')

!rm -rf /content/audio-pipeline-repo
!git clone -b claude/audio-restoration-pipeline-gAFxk \
  https://github.com/guitorte/musicas.git \
  /content/audio-pipeline-repo
```

### **4. Processar normalmente:**
```python
# Agora CONFIG_DEMUCS_QUALITY vai funcionar!
CONFIG = CONFIG_DEMUCS_QUALITY
result = pipeline.process_audio(test_file, config=CONFIG)
```

---

## 🔧 Por que isso acontece?

- **Demucs** usa **torchaudio** para salvar arquivos WAV
- **torchaudio** (versões recentes) usa **torchcodec**
- **torchcodec** precisa do **FFmpeg** instalado no sistema operacional
- Google Colab **NÃO** tem FFmpeg por padrão
- Solução: instalar FFmpeg com `apt-get`

---

## 🎯 Alternativa: Usar Configuração SEM Demucs

Se não quiser usar Demucs (mais simples e rápido):

```python
# Use configuração conservadora (sem separação de stems)
from SAFE_CONFIGS import CONFIG_CONSERVATIVE

CONFIG = CONFIG_CONSERVATIVE  # Não usa Demucs, mais rápido
result = pipeline.process_audio(test_file, config=CONFIG)
```

**Vantagens:**
- ✅ Não precisa de FFmpeg
- ✅ Processamento mais rápido (1-2 minutos vs 10-15 minutos)
- ✅ Sem erros de dependências
- ✅ Boa qualidade para maioria dos casos

**Desvantagens:**
- ❌ Não separa stems individualmente
- ❌ Qualidade ligeiramente inferior para áudios muito degradados

---

## 💡 Recomendação:

**Para MAIORIA dos casos:**
- Use `CONFIG_CONSERVATIVE` (sem Demucs)
- Rápido e sem complicações

**Para MÁXIMA qualidade:**
- Instale FFmpeg primeiro: `!apt-get update && apt-get install -y ffmpeg`
- Use `CONFIG_DEMUCS_QUALITY`
- Tenha GPU ativa no Colab
- Aguarde 10-20 minutos por arquivo

---

## 🆘 Troubleshooting:

### Erro persiste mesmo após instalar FFmpeg?

**Solução 1: Reiniciar Runtime**
```
Runtime → Restart runtime
```
Depois reexecute tudo desde o início (incluindo instalar FFmpeg)

**Solução 2: Verificar instalação**
```python
!ffmpeg -version
```

Se mostrar a versão, FFmpeg está instalado corretamente.

**Solução 3: Usar configuração sem Demucs**
```python
CONFIG = CONFIG_CONSERVATIVE  # Fallback seguro
```

---

## 📊 Comparação:

| Config | Demucs | Tempo | Qualidade | FFmpeg |
|--------|--------|-------|-----------|--------|
| `CONSERVATIVE` | ❌ | 1-2min | ⭐⭐⭐⭐ | Não precisa |
| `DEMUCS_QUALITY` | ✅ | 10-20min | ⭐⭐⭐⭐⭐ | **Obrigatório** |

---

**Atualizado: Janeiro 2026**
**Versão: 3.0 FIXED**
