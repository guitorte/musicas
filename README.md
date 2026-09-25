# Músicas @guitorte

Site: https://guitorte.github.io/musicas/

## Como funciona

- **`audio/`** — todos os áudios, numa pasta só.
- **`musicas.json`** — o catálogo. Cada música tem uma ficha:

  ```json
  { "id": "nao-e-fraco", "titulo": "Não é fraco", "arquivo": "audio/nao-e-fraco.mp3", "genero": "", "tags": [] }
  ```

  No topo do arquivo, a lista **`index`** diz quais músicas aparecem na página principal, e em que ordem.
- **`index.html`** — o player. Lê o `musicas.json`; não precisa ser editado para trocar músicas.

## Nomes dos arquivos

Minúsculas, sem acento, hífen no lugar de espaço: `nao-e-fraco.mp3`.
O título bonito, com acento, fica no catálogo.

Versões da mesma música usam `--` e um rótulo:

| arquivo | significa |
|---|---|
| `queima.mp3` | a versão principal |
| `queima--v5.mp3` | versão 5 |
| `volta--alt.mp3` | outra versão |
| `golpe--samba.mp3` | versão em samba |
| `finalmente--copia.mp3` | cópia idêntica, a conferir |

O `id` de cada música é o nome do arquivo sem `.mp3`. É ele que vai no link de compartilhar (`?songId=nao-e-fraco`), então o link continua valendo mesmo se a ordem mudar.

## Adicionar uma música

1. No GitHub, abra a pasta `audio/` → **Add file → Upload files** e envie o MP3 (o nome pode ter acento e espaço).
2. Em cerca de um minuto, a automação ("Catálogo de músicas", em *Actions*) renomeia o arquivo para o padrão e cria a ficha no `musicas.json`, com o título tirado do nome original.
3. Para ela aparecer na página principal, coloque o `id` na lista `index` do `musicas.json`, na posição desejada.

Se o nome já existir, o arquivo novo **não** substitui o antigo: vira `nome--2.mp3`.
Para substituir de verdade, envie com exatamente o mesmo nome do arquivo existente (ex.: `queima.mp3`).

## Outras tarefas

- **Mudar a ordem / tirar do index:** edite a lista `index` do `musicas.json`.
- **Corrigir um título:** edite `titulo` na ficha.
- **Apagar uma música:** apague o arquivo em `audio/` *e* a ficha no `musicas.json` (e tire do `index`).
- **Conferir se está tudo certo:** `python3 .github/scripts/catalogo.py --check`

Ou simplesmente peça ao Claude ("adicione X ao index", "troque a ordem", etc.).
