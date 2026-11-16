# Panduan deck Implementasi Mendeley

## Tujuan
Deck 16 slide untuk mata kuliah Bahasa Indonesia: Mendeley sebagai alat bantu kutipan, daftar pustaka, dan pencegahan plagiarisme.

## Alur kerja
1. Baca skill yang dipakai (urutan: bahasa-skills, stop-slop, officecli) dan `docs/superpowers/specs/2026-11-16-desain-mastercard.md`. Sebagian skill ada di `skills/`, sisanya dipasang dari sumber di `skills/README.md`.
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
- Referensi layout: editorial Mastercard dengan permukaan cream/ink, kartu beradius besar, pill, potret ikon lingkaran, satelit panah putih, dan orbit oranye tipis.
- Screenshot tetap 16:9 di dalam bingkai stadium putih; jangan dipotong lingkaran atau diregangkan.
- Palet: Canvas Cream `F3F0EE`, Lifted Cream `FCFBFA`, Soft Bone `F4F4F4`, Dust `D1CDC7`, Ink `141413`, Charcoal `262627`, Slate `696969`, Signal Orange `CF4500`, Light Signal Orange `F37338`, Clay `9A3A0A`, White `FFFFFF`.
- Oranye hanya untuk aksen, nomor, tautan, dan penanda; jangan memakai oranye sebagai latar teks panjang.
- Font: Arial. Judul slide 32 pt tebal, sampul 48 pt, isi 15 sampai 20 pt, keterangan minimal 10 pt.
- Margin tepi 1,2 cm, jarak antarkartu 0,8 cm. Satu gagasan per slide.
- Tanpa gradasi, bayangan keras, atau logo Mastercard. Permukaan memakai warna solid.
- Setiap slide membawa elemen visual berupa ikon, bentuk, atau screenshot. Sampul dan kesimpulan terang; penutup memakai latar ink.

## Aturan gerak
- Deck statis. Tidak ada animasi, transisi, fade, atau perubahan warna.
- Satu klik pindah ke slide berikutnya.
- Tidak ada sidebar; konten memenuhi lebar slide.

## Token warna (ada di bagian atas build.py)
| Peran | Hex |
|---|---|
| Canvas Cream | F3F0EE |
| Lifted Cream | FCFBFA |
| Soft Bone | F4F4F4 |
| Dust | D1CDC7 |
| Ink | 141413 |
| Charcoal | 262627 |
| Slate | 696969 |
| Signal Orange | CF4500 |
| Light Signal Orange | F37338 |
| Clay | 9A3A0A |
| White | FFFFFF |

## Yang harus diisi manual
- Slide 2: nama dan NIM anggota, urut NIM; nomor besar digambar sebagai teks oranye, bukan aset `num-*.png`. Ikon ber-hash tidak disimpan di Git; `icons.js` membuatnya saat build.
- Slide 4: tanpa mask pastel; kartu kiri lifted cream, kartu kanan ink. Jangan mengembalikan `mask-04-*.png`.
- Slide 5: enam fitur utama; jangan menambah fitur yang tidak ada di sumber.
- Slide 6-7: instalasi akun, aplikasi, Web Importer, dan Cite; pertahankan screenshot besar.
- Slide 8-9: antarmuka library dan PDF Reader; jangan mengecilkan screenshot demi memadatkan.
- Slide 10: empat cara menambahkan referensi dan menu Add reference.
- Slide 11: enam langkah Mendeley Cite; teori gaya sitasi tetap di Kelompok 4.
- Slide 12: tabel lima gaya sitasi; jangan menambah aturan format rinci.
- Slide 13: contoh satu sumber menjadi sitasi dan daftar pustaka.
- Slide 6-11: screenshot Mendeley 16:9 di dalam `shot-mask.png`; tangkapan layar akun memakai Mendeley (n.d.); jangan regangkan; crop bilah hitam; kredit di speaker notes.
- Slide 15: kesimpulan terang; slide 16: penutup berlatar ink. Jangan menambahkan gradasi latar.
- Verifikasi ke situs resmi Mendeley: batas penyimpanan gratis dan ketersediaan fitur.

## Catatan teknis OfficeCLI
- Jalankan dengan `OFFICECLI_NO_AUTO_RESIDENT=1` agar hasil langsung tertulis ke disk.
- Posisi dan ukuran memakai satuan cm. Slide berukuran 33,87 x 19,05 cm.
- Pakai `officecli watch deck.pptx` di komputer lokal untuk pratinjau langsung.
