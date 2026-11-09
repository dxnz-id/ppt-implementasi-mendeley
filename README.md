# Implementasi Mendeley: generator slide

Generator deck 16 slide tentang Mendeley dalam penulisan karya ilmiah, dibuat dengan OfficeCLI dan bergaya Material 3.

## Struktur
- `build.py`: isi slide, palet, dan layout
- `icons.js`: pembuat ikon Material dalam bentuk cookie atau flower
- `assets/`: ikon hasil render
- `docs/GUIDELINE.md`: panduan bahasa, desain, dan alur kerja
- `skills/`: skill yang dipakai selama pembuatan (lihat `skills/README.md`)

## Membangun ulang
Prasyarat: uv, Node.js, dan officecli.

    npm ci
    export OFFICECLI_NO_AUTO_RESIDENT=1
    uv run build.py

Hasilnya `deck.pptx`.

## Rilis otomatis
Setiap push ke `main` menjalankan `.github/workflows/release.yml`: deck dibangun, divalidasi, diekspor ke `deck.pdf`, lalu diterbitkan sebagai release bertag `build-<sha>` dengan kedua berkas. Tidak perlu mengisi rahasia; `GITHUB_TOKEN` sudah tersedia.
