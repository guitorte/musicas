# Notes for Claude

The owner writes in Portuguese; the site and docs are in Portuguese.

## Music site (see README.md for the full workflow)

- All audio lives flat in `audio/`. Names: lowercase ASCII, hyphens, versions as `name--label.mp3`.
- `musicas.json` is the single source of truth: `index` (ordered ids shown on `index.html`), `musicas` (one entry per file), `playlists` (used only by the old `index6.html`/`script.js`).
- `id` = file name without extension; share links use it (`?songId=<id>`). `index.html` still resolves legacy `?songId=songN` by position.
- Entries with `obs: "VERIFICAR: ..."` are byte-identical duplicates awaiting the owner's review.
- `.github/scripts/catalogo.py` renames non-conforming uploads and catalogs new files; the `catalogo.yml` Action runs it on pushes to `main`. Run `python3 .github/scripts/catalogo.py --check` after touching audio or the catalog.
- Other pages that play audio from `audio/`: `sambas/index.html`, `tarocore.html`, `versoes.html`, and old player drafts (`2.html`, `index01.html`, `index06.html`). Renaming a file means updating them too.

## Everything else

The lyrics research (notebooks, `.py`, CSVs, `lyrics_analysis/`, `letras/`, `report/`), `biblia/`, `manual/`, `letras.html` and `lost.html` are separate projects the owner will reorganize later. Leave them alone unless asked.
