# Implementasi Mendeley: generator slide

Generator deck 16 slide tentang Mendeley dalam penulisan karya ilmiah, dibuat dengan OfficeCLI dan bergaya editorial Mastercard: latar Light Signal Orange, teks ink, kartu cream, bentuk pill, potret lingkaran, satelit, dan orbit cream.

## Struktur
- `build.py`: isi slide, palet, dan layout
- `icons.js`: pembuat ikon Material dengan bentuk none, circle, cookie, flower, clover, burst, squircle, dan sunny
- `assets/`: aset sumber (screenshot, orbit, bingkai screenshot); ikon ber-hash dibuat saat build
- `docs/GUIDELINE.md`: panduan bahasa, desain, dan alur kerja
- `skills/`: skill yang dipakai selama pembuatan (lihat `skills/README.md`)

## Membangun ulang
Prasyarat: uv, Node.js, dan OfficeCLI `v1.0.160` (versi yang sama dengan workflow rilis). Unduh `officecli-linux-x64` dan `SHA256SUMS` dari [rilis v1.0.160](https://github.com/iOfficeAI/OfficeCLI/releases/tag/v1.0.160), pastikan checksum SHA-256 cocok, lalu pasang binary itu di `PATH`. `officecli --version` harus melaporkan `v1.0.160`.

    npm ci
    export OFFICECLI_NO_AUTO_RESIDENT=1
    uv run build.py

Hasilnya `deck.pptx`. Ikon ber-hash di `assets/` diabaikan Git karena selalu dibuat ulang oleh `icons.js`.

Deck statis. Tidak ada animasi atau transisi; satu klik pindah slide. Tampilan PPTX dan PDF sama.

## Uji manual sebelum rilis
Buka `deck.pptx` di PowerPoint 365/2021 dan periksa:

- Semua 16 slide tampil tanpa animasi.
- Satu klik langsung pindah ke slide berikutnya.
- Tidak ada sidebar; konten memenuhi lebar slide.

Uji manual ini wajib dilakukan sebelum menerbitkan rilis dan tidak dicakup CI.

## Rilis otomatis
Setiap push ke branch mana pun dan pull request menjalankan `.github/workflows/release.yml`: deck dibangun, divalidasi, diekspor ke `deck.pdf`, lalu artifact `deck.pptx`, `deck.pdf`, dan `preview.png` diunggah. Hanya push ke `main` yang menerbitkan release bertag `build-<sha>` dengan tiga aset tersebut. Rilis diserialkan agar build tidak saling menimpa. Tidak perlu mengisi rahasia; `GITHUB_TOKEN` sudah tersedia.

Pratinjau desain dari branch dibuat sebagai pre-release manual dari artifact branch, bukan dari `main`. Setelah desain disetujui, baru merge ke `main` untuk rilis biasa.
