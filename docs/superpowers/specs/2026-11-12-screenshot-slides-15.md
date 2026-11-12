# Deck screenshot-first 15 slide

## Tujuan

Membuat deck Mendeley lebih konkret dengan screenshot asli, merombak slide 7 yang terlalu generik, dan menghapus slide demo alur yang berulang. Jumlah slide turun dari 16 menjadi 15.

## Perubahan per slide

- **Slide 5**: tiga kartu kanan memakai screenshot Reference Manager, Mendeley Cite, dan Web Importer. Kartu kiri dan teks pengantar tetap.
- **Slide 6**: tiga kartu memakai screenshot metadata, gaya sitasi, dan daftar pustaka. Banner atas tetap.
- **Slide 7**: kartu 01/02/03 dan kartu “Yang tetap manual” dibuang. Susunan baru: satu kartu sumber di kiri, dua kartu keluaran bertumpuk di kanan, dua panah, satu baris catatan manual.
- **Slide 8**: tiga kartu persiapan memakai screenshot akun, aplikasi, dan ekstensi. Angka besar diganti badge angka kecil.
- **Slide 9**: empat kartu memakai screenshot impor, simpan dari web, cek metadata, dan folder.
- **Slide 10**: dua baris di kartu kiri memakai screenshot highlight dan catatan. Kartu “Hasilnya” tetap.
- **Slide 11**: empat kolom memakai screenshot add-in, sisipkan kutipan, gaya, dan daftar pustaka.
- **Slide 12 lama “Demo alur” dihapus**. Slide 13 sampai 16 bergeser menjadi 12 sampai 15.

## Batasan

- Palet tetap: `B0C8E0`, `C1E0E0`, `DCE7D6`, `F6F6F6`. Tidak ada bentuk hitam.
- Sampul, kesimpulan, dan penutup tetap terang.
- Satu klik per slide. Animasi masuk mulai otomatis. Tidak ada transisi, fade, atau exit.
- Motion path, easing, dan durasi tidak berubah. Hanya indeks slide yang di-remap.
- Semua screenshot berasal dari aset resmi Mendeley atau tangkapan layar Mendeley yang dikreditkan. Jangan regangkan gambar.
- Body text minimal 18 pt. Judul slide 36 pt. Keterangan minimal 10 pt.
- Teks baru mengikuti `docs/GUIDELINE.md` dan `bahasa-inti`: tanpa em dash, tanpa pembuka klise, tanpa “bukan X melainkan Y”.

## Aset screenshot

Semua aset disimpan sebagai PNG 1200 x 675 (16:9) di `assets/`.

| Aset | Sumber | Dipakai di |
|---|---|---|
| `shot-rm-add.png` | `get-your-library.png` | slide 5 |
| `shot-cite-panel.png` | `cite_desktop.5a079955.png` | slide 5 |
| `shot-web-importer.png` | `web_importer.484c7d40.png` | slide 5 |
| `shot-metadata.png` | `adding_references_4.1b6afdd6.png` | slide 6 |
| `shot-style.png` | `citation_settings.ad5ff2e1.png` | slide 6, 11 |
| `shot-bibliography.png` | `help_guide_cite_05.dcfc0068.png` | slide 6, 11 |
| `shot-source.png` | `reading_and_annotating_1.5d79deea.png` | slide 7 |
| `shot-citation.png` | `help_guide_cite_10.ca2a4d5e.png` | slide 7 |
| `shot-bib-menu.png` | `help_guide_cite_05.dcfc0068.png` | slide 7 |
| `shot-account.png` | `Mendeley_website.PNG` | slide 8 |
| `shot-app.png` | `get-your-library-4.png` | slide 8 |
| `shot-extension.png` | `get-your-library-2.png` | slide 8 |
| `shot-import.png` | `adding_references_1.d7b13ef6.png` | slide 9 |
| `shot-web-save.png` | `importing.6a8e6605.png` | slide 9 |
| `shot-details.png` | `your_mendeley_library_0.de7bf251.png` | slide 9 |
| `shot-organize.png` | `searching_your_library_2.fd4049ea.png` | slide 9 |
| `shot-highlight.png` | `reading_and_annotating_1.5d79deea.png` | slide 10 |
| `shot-notes.png` | `reading_and_annotating_4.8809ba7d.png` | slide 10 |
| `shot-addin.png` | `help_guide_cite_02.281a79c9.png` | slide 11 |
| `shot-cite.png` | `cite_desktop.5a079955.png` | slide 11 |

Sumber halaman:

- https://www.mendeley.com/guides/mendeley-reference-manager/02-adding-references
- https://www.mendeley.com/guides/mendeley-reference-manager/03-organizing-references
- https://www.mendeley.com/guides/mendeley-reference-manager/04-reading-and-annotating
- https://www.mendeley.com/guides/mendeley-cite/04-creating-a-bibliography
- https://www.mendeley.com/guides/mendeley-cite/05-choosing-and-changing-citation-styles
- https://library-guides.ucl.ac.uk/mendeley-desktop/account (tangkapan layar akun)

## Kriteria terima

- Deck berisi 15 slide; tidak ada teks “Demo alur”.
- Semua screenshot 16:9, tidak terdistorsi, dan punya alt text.
- Tidak ada teks terpotong, kartu bertumpuk, atau panah menabrak kartu.
- `check_anim.py` lulus dengan 15 slide dan remap indeks yang benar.
- `check_layout.py` lulus.
- `officecli validate` dan `officecli view issues` bersih.
- PDF berisi 15 halaman dan preview 15 slide.
- Pemutaran manual di PowerPoint 365/2021 dilakukan pengguna sebelum rilis.
