"""Mantém audio/ e musicas.json em ordem.

Uso:
    python3 .github/scripts/catalogo.py           # corrige: renomeia arquivos novos e cadastra no catálogo
    python3 .github/scripts/catalogo.py --check   # só verifica, não altera nada

O que ele faz:
  1. Renomeia arquivos de audio/ para o padrão (minúsculas, sem acento, hífens).
     "Não é fraco.mp3" -> "nao-e-fraco.mp3". Se o nome já existir, vira "nao-e-fraco--2.mp3".
  2. Cadastra em musicas.json todo áudio que ainda não está lá, com o título
     tirado do nome original. Música nova NÃO entra no index sozinha.
  3. Guarda a duração de cada áudio em "duracao" (segundos), para a página
     não precisar abrir os arquivos só para mostrar o tempo.
  4. Verifica: arquivo faltando, id repetido, id do index que não existe, arquivos idênticos.
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

from mutagen import File as AudioFile  # pip install mutagen

RAIZ = Path(__file__).resolve().parents[2]
PASTA = RAIZ / "audio"
CATALOGO = RAIZ / "musicas.json"
EXTENSOES = {".mp3", ".m4a", ".wav", ".ogg"}
NOME_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(--[a-z0-9]+(-[a-z0-9]+)*)*$")


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")
    return texto or "musica"


def titulo(stem):
    t = unicodedata.normalize("NFC", stem).replace("_", " ")
    t = re.sub(r"^[^\w]+", "", t)  # tira "+ ", "★ " etc. do começo
    t = re.sub(r"\s+", " ", t).strip()
    return t[:1].upper() + t[1:] if t else stem


def main():
    check = "--check" in sys.argv
    erros, avisos, mudancas = [], [], []
    pendentes = set()  # renomeações que o --check não executa

    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    musicas = catalogo.setdefault("musicas", [])
    catalogo.setdefault("index", [])
    por_arquivo = {m["arquivo"]: m for m in musicas}

    # 1. renomear
    ocupados = {p.name for p in PASTA.iterdir()}
    for p in sorted(PASTA.iterdir()):
        if p.suffix.lower() not in EXTENSOES or NOME_OK.match(p.stem):
            continue
        base, n = slug(p.stem), 1
        novo = f"{base}{p.suffix.lower()}"
        while novo in ocupados:
            n += 1
            novo = f"{base}--{n}{p.suffix.lower()}"
        ocupados.add(novo)
        pendentes.add(f"audio/{novo}")
        mudancas.append(f"renomear audio/{p.name} -> audio/{novo}")
        antigo = f"audio/{p.name}"
        if antigo in por_arquivo:
            por_arquivo[antigo]["arquivo"] = f"audio/{novo}"
            por_arquivo[f"audio/{novo}"] = por_arquivo.pop(antigo)
        else:
            musicas.append({"id": Path(novo).stem, "titulo": titulo(p.stem),
                            "arquivo": f"audio/{novo}", "genero": "", "tags": []})
            por_arquivo[f"audio/{novo}"] = musicas[-1]
            mudancas.append(f"cadastrar {Path(novo).stem} (\"{titulo(p.stem)}\")")
        if not check:
            p.rename(PASTA / novo)

    # 2. cadastrar arquivos que já têm nome certo mas não estão no catálogo
    for p in sorted(PASTA.iterdir()):
        if p.suffix.lower() in EXTENSOES and NOME_OK.match(p.stem) and f"audio/{p.name}" not in por_arquivo:
            musicas.append({"id": p.stem, "titulo": titulo(p.stem.replace("-", " ")),
                            "arquivo": f"audio/{p.name}", "genero": "", "tags": []})
            mudancas.append(f"cadastrar {p.stem}")

    # 3. duração (também atualiza quando um arquivo é substituído pelo mesmo nome)
    for m in musicas:
        caminho = RAIZ / m["arquivo"]
        if m["arquivo"] in pendentes and check or not caminho.exists():
            continue
        audio = AudioFile(caminho)
        if audio is None or not audio.info.length:
            avisos.append(f"{m['id']}: não consegui ler a duração")
            continue
        duracao = round(audio.info.length)
        if m.get("duracao") != duracao:
            m["duracao"] = duracao
            mudancas.append(f"duração de {m['id']}: {duracao // 60}:{duracao % 60:02d}")

    # 4. verificar
    ids = [m["id"] for m in musicas]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        erros.append(f"id repetido no catálogo: {i}")
    for m in musicas:
        if check and m["arquivo"] in pendentes:
            continue
        if not (RAIZ / m["arquivo"]).exists():
            erros.append(f"{m['id']}: arquivo não encontrado ({m['arquivo']})")
    for i in catalogo["index"]:
        if i not in ids:
            erros.append(f"index cita '{i}', que não está no catálogo")
    hashes = {}
    for p in sorted(PASTA.iterdir()):
        if p.suffix.lower() in EXTENSOES:
            hashes.setdefault(hashlib.md5(p.read_bytes()).hexdigest(), []).append(p.name)
    for nomes in hashes.values():
        if len(nomes) > 1:
            avisos.append("arquivos idênticos: " + ", ".join(nomes))

    musicas.sort(key=lambda m: m["id"])
    if mudancas and not check:
        CATALOGO.write_text(json.dumps(catalogo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for linha in mudancas:
        print(("[faria] " if check else "") + linha)
    for linha in avisos:
        print("aviso:", linha)
    for linha in erros:
        print("ERRO:", linha)
    if not (mudancas or avisos or erros):
        print("tudo em ordem")
    sys.exit(1 if erros or (check and mudancas) else 0)


if __name__ == "__main__":
    main()
