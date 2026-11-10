# Implementasi Mendeley: generator slide

Generator deck 16 slide tentang Mendeley dalam penulisan karya ilmiah, dibuat dengan OfficeCLI dan bergaya Material 3.

## Struktur
- `build.py`: isi slide, palet, dan layout
- `icons.js`: pembuat ikon Material dengan bentuk cookie, flower, clover, squircle, burst, dan sunny
- `assets/`: aset sumber (nomor, masking, ilustrasi); ikon ber-hash dibuat saat build
- `docs/GUIDELINE.md`: panduan bahasa, desain, dan alur kerja
- `skills/`: skill yang dipakai selama pembuatan (lihat `skills/README.md`)

## Membangun ulang
Prasyarat: uv, Node.js, dan officecli.

    npm ci
    export OFFICECLI_NO_AUTO_RESIDENT=1
    uv run build.py

Hasilnya `deck.pptx`. Ikon ber-hash di `assets/` diabaikan Git karena selalu dibuat ulang oleh `icons.js`.

Animasi memakai motion path per objek tanpa fade atau perubahan warna. Animasi hanya tampil di PowerPoint 365/2021; PDF tetap statis di posisi akhir.

## Rilis otomatis
Setiap push ke `main` menjalankan `.github/workflows/release.yml`: deck dibangun, divalidasi, diekspor ke `deck.pdf`, lalu diterbitkan sebagai release bertag `build-<sha>` dengan kedua berkas. Tidak perlu mengisi rahasia; `GITHUB_TOKEN` sudah tersedia.
