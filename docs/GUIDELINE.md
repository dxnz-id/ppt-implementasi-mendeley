# Panduan deck Implementasi Mendeley

## Tujuan
Deck 14 slide untuk mata kuliah Bahasa Indonesia: Mendeley sebagai alat bantu kutipan, daftar pustaka, dan pencegahan plagiarisme.

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
- Referensi layout: pengaturan (settings) di https://github.com/satoxyan/expressive-pC, yaitu rail navigasi kiri, kartu tonal berradius besar, ikon dalam bentuk cookie, flower, clover, squircle, burst, atau sunny.
- Bentuk ikon mengikuti peran: flower untuk hero, cookie/clover/squircle untuk kartu, burst untuk peringatan atau pemeriksaan, sunny untuk ide dan waktu.
- Palet: biru, teal, dan hijau pastel dengan aksen navy. Merah hanya untuk risiko. Tanpa ungu.
- Font: Calibri. Judul 36 pt tebal, isi 18 sampai 24 pt, keterangan minimal 10 pt, sitasi kaki minimal 8 pt.
- Margin tepi minimal 1 cm, jarak antarkartu 0,8 cm. Satu gagasan per slide.
- Gradasi hanya untuk opacity gambar; permukaan, kartu, dan latar memakai warna tonal solid.
- Setiap slide membawa elemen visual berupa ikon, bentuk, atau screenshot. Sampul, kesimpulan, dan penutup terang.

## Aturan gerak
- Satu slide satu klik. Tidak ada animasi keluar; slide berikutnya langsung masuk.
- Masuk horizontal 420 ms, vertikal 500 ms, sidebar 400 ms. Konten memakai ease-in 20 dan ease-out 70; pil memakai 30 dan 50.
- Path masuk melewati target sedikit lalu kembali: 1,5% lebar atau tinggi slide, sidebar 0,3% lebar.
- Pil sidebar bergerak bersama konten memakai `withPrevious`, bukan `afterPrevious`.
- Tanpa fade, opacity, atau perubahan warna. Animasi hanya tampil di PowerPoint 365/2021.
- Referensi gerak: `MediaPager.qml` dan `SidebarPop.qml` di https://github.com/satoxyan/expressive-pC.

## Token warna (ada di bagian atas build.py)
| Peran | Hex |
|---|---|
| Latar | F6F6F6 |
| Primary / container | 46627A / B0C8E0 |
| Secondary container | C1E0E0 |
| Tertiary container | DCE7D6 |
| Error | FFDAD6 / 65000B |
| Teks | 2F3334 |

## Yang harus diisi manual
- Slide 2: nama dan NIM anggota, urut NIM; nomor besar memakai aset `num-01.png` sampai `num-07.png` yang dipotong mask kartu. Ikon ber-hash tidak disimpan di Git; `icons.js` membuatnya saat build.
- Slide 6: batas Mendeley, bukan teori sitasi; teori jenis sitasi ada di Kelompok 4.
- Slide 7: contoh satu sumber menjadi sitasi dan daftar pustaka; jangan menambah teori jenis sitasi atau aturan APA/IEEE.
- Slide 4, 5, 10, 13: masking memakai `assets/mask-*.png`; letakkan setelah kartu dan sebelum ikon atau teks. Rasio PNG harus sama dengan kartu; `build.py` gagal jika berbeda, jadi jangan meregangkan mask.
- Slide 5 sampai 11: screenshot Mendeley 16:9; tangkapan layar akun memakai UCL Library (2019); jangan regangkan; kredit di slide.
- Slide 14: penutup terang dengan bentuk tonal solid; jangan tambahkan gradasi latar.
- Verifikasi ke situs resmi Mendeley: status Desktop dan batas penyimpanan gratis.

## Catatan teknis OfficeCLI
- Jalankan dengan `OFFICECLI_NO_AUTO_RESIDENT=1` agar hasil langsung tertulis ke disk.
- Posisi dan ukuran memakai satuan cm. Slide berukuran 33,87 x 19,05 cm.
- Pakai `officecli watch deck.pptx` di komputer lokal untuk pratinjau langsung.
