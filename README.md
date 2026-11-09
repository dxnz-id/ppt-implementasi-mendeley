# Implementasi Mendeley: generator slide

Generator deck 13 slide tentang Mendeley dalam penulisan karya ilmiah, dibuat dengan OfficeCLI dan bergaya Material 3.

## Struktur
- `build.py`: isi slide, palet, dan layout
- `icons.js`: pembuat ikon Material dalam bentuk cookie atau flower
- `assets/`: ikon hasil render
- `docs/GUIDELINE.md`: panduan bahasa, desain, dan alur kerja
- `skills/`: skill yang dipakai selama pembuatan (lihat `skills/README.md`)

## Membangun ulang
Prasyarat: Python 3, Node.js (react, react-dom, react-icons, sharp), dan officecli.

    export OFFICECLI_NO_AUTO_RESIDENT=1
    python3 build.py

Hasilnya `deck.pptx`.
