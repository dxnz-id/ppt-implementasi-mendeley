# Adaptasi rancangan Mendeley ke deck 16 slide

## Tujuan

Memperluas deck Mendeley dari 14 menjadi 16 slide agar materi fitur, instalasi,
antarmuka, penambahan referensi, Mendeley Cite, dan gaya sitasi masuk tanpa
memadatkan screenshot.

## Sasaran

- Menampilkan enam fitur utama Mendeley.
- Memisahkan instalasi menjadi dua slide: akun/aplikasi dan Web Importer/Cite.
- Memisahkan antarmuka menjadi dua slide: panel library dan PDF Reader.
- Menjelaskan empat cara menambahkan referensi.
- Menjelaskan enam langkah Mendeley Cite.
- Menampilkan tabel lima gaya sitasi.
- Mempertahankan sampul, anggota, kekurangan sitasi manual, rumusan masalah,
  satu sumber dua rujukan, kelebihan/keterbatasan, kesimpulan, dan penutup.

## Bukan sasaran

- Menambah teori jenis sitasi atau aturan format APA/IEEE secara rinci.
- Mengganti identitas visual, palet, atau gaya ikon yang sudah ada.
- Menambahkan animasi atau transisi.
- Mengarang screenshot atau fitur yang tidak ada di aset.

## Batasan

- Ukuran slide 33,87 x 19,05 cm; margin kiri 1,2 cm; lebar konten 31,2 cm.
- Screenshot 16:9 tidak boleh diregangkan.
- Mask hanya dipakai pada slide 4; rasio mask harus tetap.
- Deck tetap statis dan lolos `check_no_anim.py`.
- Semua slide harus lolos `officecli validate` dan `check_layout.py`.

## Pendekatan

Tiga pilihan yang dipertimbangkan:

1. Tetap 14 slide dengan menggabungkan instalasi dan antarmuka. Ditolak karena
   screenshot menjadi kecil dan slide terlalu padat.
2. Memecah setiap bagian menjadi slide sendiri hingga 18-20 slide. Ditolak
   karena melebihi kebutuhan presentasi dan memperpanjang durasi.
3. **16 slide**: instalasi dan antarmuka masing-masing dua slide, bagian lain
   satu slide. Dipilih karena gambar tetap besar dan alur presentasi tetap
   ringkas.

## Susunan slide

1. Sampul
2. Anggota kelompok
3. Kekurangan sitasi manual
4. Rumusan masalah dan tujuan
5. Fitur utama (6 kartu)
6. Instalasi: akun dan aplikasi (4 langkah + screenshot situs)
7. Instalasi: Web Importer dan Cite (2 kartu screenshot besar)
8. Tampilan antarmuka (screenshot library + label tiga panel)
9. PDF Reader: baca dan tandai (2 screenshot besar)
10. Menambahkan referensi (screenshot menu + 4 cara)
11. Mendeley Cite di Word (screenshot + 6 langkah)
12. Gaya sitasi (tabel 5 baris)
13. Satu sumber untuk dua rujukan
14. Kelebihan dan keterbatasan
15. Kesimpulan
16. Terima kasih

## Keputusan desain

- Slide 5 memakai grid 3 x 2, kartu 9,87 x 6,6 cm.
- Slide 6 memakai screenshot 18 x 10,125 cm di kiri dan empat langkah di kanan.
- Slide 7 dan 9 memakai dua kartu 15,2 x 14 cm dengan screenshot 13,6 x 7,65 cm.
- Slide 8 memakai screenshot 19,2 x 10,8 cm dan tiga label panel di kanan.
- Slide 10 memakai screenshot 18 x 10,125 cm dan empat cara di kanan.
- Slide 11 memakai screenshot 14 x 7,875 cm dan enam langkah bernomor.
- Slide 12 memakai header tabel dan lima baris berwarna tonal.
- Semua teks mengikuti ragam resmi dan ejaan baku; istilah produk tetap memakai
  nama aslinya.

## Verifikasi

- Build menghasilkan 16 slide.
- `check_no_anim.py` melaporkan 16 slide tanpa animasi.
- `check_layout.py` tidak menemukan panah yang menabrak kartu.
- `officecli validate` bersih dan `officecli view issues` nol.
- Render semua slide diperiksa, terutama screenshot slide 6-9 dan 11.
- PowerPoint manual tetap menjadi pemeriksaan terpisah sebelum rilis.
