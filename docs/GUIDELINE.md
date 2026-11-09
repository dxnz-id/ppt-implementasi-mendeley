# Panduan deck Implementasi Mendeley

## Tujuan
Deck 13 slide untuk mata kuliah Bahasa Indonesia: Mendeley sebagai alat bantu kutipan, daftar pustaka, dan pencegahan plagiarisme.

## Alur kerja
1. Baca skill yang dipakai (urutan: bahasa-skills, stop-slop, material-3, officecli). Sebagian ada di `skills/`, sisanya dipasang dari sumber di `skills/README.md`.
2. Tulis teks slide di `build.py` mengikuti aturan bahasa di bawah.
3. Jalankan `uv run build.py`. Skrip membuat ikon (`icons.js`) lalu menyusun deck lewat batch OfficeCLI.
4. Validasi: `officecli validate deck.pptx` dan `officecli view deck.pptx issues`.
5. Render ke PDF lalu cek tiap slide secara visual sebelum diserahkan.

## Aturan bahasa
- Ragam resmi, ejaan baku (EYD V). Contoh: silakan, risiko, praktik, analisis, mengubah.
- Judul memakai huruf kapital hanya pada kata pertama dan nama diri. Tanpa titik di akhir.
- Tanpa em dash, tanpa pembuka klise, tanpa "bukan X melainkan Y", tanpa tiga kata sifat beruntun.
- Satu istilah untuk satu konsep. Istilah asing yang belum terserap ditulis miring atau dipertahankan sebagai nama produk.
- Jangan mengarang rujukan, angka, atau fitur. Klaim yang belum diverifikasi ditandai di catatan pembicara.

## Aturan desain
- Referensi layout: pengaturan (settings) di https://github.com/satoxyan/expressive-pC, yaitu rail navigasi kiri, kartu tonal berradius besar, ikon dalam bentuk cookie atau flower.
- Palet: hijau zaitun dengan aksen teal, merah hanya untuk risiko. Tanpa ungu.
- Font: Calibri. Judul 36 pt tebal, isi 18 sampai 24 pt, keterangan minimal 10 pt.
- Margin tepi minimal 1 cm, jarak antarkartu 0,8 cm. Satu gagasan per slide.
- Setiap slide membawa elemen visual (ikon, bentuk). Sampul dan kesimpulan gelap, slide isi terang.

## Token warna (ada di bagian atas build.py)
| Peran | Hex |
|---|---|
| Latar | F9FAEF |
| Primary / container | 4C662B / CDEDA3 |
| Secondary container | DCE7C8 |
| Tertiary container | BCECE7 |
| Error container | FFDAD6 |
| Latar gelap | 12140E |

## Yang harus diisi manual
- Slide 1: nama, NIM, kelas, dosen pengampu.
- Slide 10: tangkapan layar dari penggunaan sendiri.
- Slide 13: 2 sampai 3 jurnal hasil pencarian dan verifikasi sendiri.
- Verifikasi ke situs resmi Mendeley: status Desktop dan batas penyimpanan gratis.

## Catatan teknis OfficeCLI
- Jalankan dengan `OFFICECLI_NO_AUTO_RESIDENT=1` agar hasil langsung tertulis ke disk.
- Posisi dan ukuran memakai satuan cm. Slide berukuran 33,87 x 19,05 cm.
- Pakai `officecli watch deck.pptx` di komputer lokal untuk pratinjau langsung.
