# Desain Mastercard untuk deck Mendeley

## Tujuan

Mengganti bahasa visual deck 16 slide Mendeley dengan sistem editorial yang
diadaptasi dari `DESIGN.md` Mastercard: cream hangat, ink, bentuk pill dan
stadium, potret lingkaran, satelit CTA, orbit oranye, dan eyebrow bertitik.
Isi, urutan, dan struktur 16 slide tidak berubah.

## Sasaran

- Menerapkan Canvas Cream `#F3F0EE`, Ink Black `#141413`, dan aksen oranye
  secara konsisten.
- Memakai Arial sebagai fallback resmi yang aman di PowerPoint dan CI.
- Mengganti kartu pastel menjadi lifted cream, soft bone, atau ink.
- Memakai radius 40px untuk frame screenshot dan radius penuh untuk pill.
- Memakai ikon dalam lingkaran dengan satelit panah putih.
- Menambahkan eyebrow bertitik oranye dan orbit tipis pada slide terpilih.
- Menjaga screenshot UI tetap 16:9 dan terbaca.

## Bukan sasaran

- Memakai logo Mastercard atau mengklaim afiliasi dengan Mastercard.
- Memotong screenshot UI menjadi lingkaran.
- Mengubah teks, jumlah slide, atau alur presentasi.
- Menambahkan animasi, transisi, atau sidebar.

## Batasan

- Slide 33,87 x 19,05 cm; margin konten 1,2 cm.
- Screenshot 16:9 tidak boleh diregangkan.
- Tidak ada animasi.
- Font Arial; CI memasang Liberation Sans sebagai metrik-compatible.
- Rilis preview dibuat dari branch, bukan dari `main`.

## Pendekatan

1. **Editorial penuh (dipilih)** — terapkan palet, tipografi, radius, lingkaran,
   satelit, orbit, dan eyebrow ke seluruh deck. Screenshot tetap persegi.
2. **Token saja** — hanya warna dan font. Ditolak karena tidak mengubah karakter
   layout.
3. **Lingkaran penuh** — screenshot dipotong lingkaran. Ditolak karena materi
   tutorial tidak terbaca.

## Token

- Canvas: `F3F0EE`
- Lifted cream: `FCFBFA`
- Soft bone: `F4F4F4`
- Dust: `D1CDC7`
- Ink: `141413`
- Charcoal: `262627`
- Slate: `696969`
- Signal orange: `CF4500`
- Light signal orange: `F37338`
- Clay: `9A3A0A`
- White: `FFFFFF`

## Tipografi

- Satu keluarga: Arial.
- Judul slide 32 pt, tebal, tracking negatif.
- Judul sampul 48 pt, tebal.
- Judul kartu 20-22 pt.
- Isi 15-18 pt; keterangan 10-12 pt.
- Eyebrow 10 pt, kapital, tracking positif.

## Komponen

- **Frame screenshot:** stadium dengan radius 1,05 cm dan bingkai putih.
- **Kartu:** radius 1,05 cm atau pill penuh; isi lifted cream/soft bone/ink.
- **Potret ikon:** lingkaran dengan ikon krem/ink; satelit putih 0,9-1,0 cm
  berisi panah.
- **Orbit:** SVG tipis `F37338` di belakang potret pada sampul dan penutup.
- **Eyebrow:** titik oranye 0,18 cm + label kapital 10 pt.
- **Nomor langkah:** lingkaran ink 1,3 cm dengan teks krem.
- **Tabel gaya:** header ink pill, baris lifted cream/soft bone.

## Pemetaan slide

1. Sampul cream, headline ink, badge pill hitam, potret buku, orbit.
2. Anggota: kartu cream dengan nomor besar, tanpa mask pastel.
3. Kekurangan: tiga kartu cream + callout ink.
4. Rumusan/tujuan: kartu cream dan kartu ink.
5. Fitur: grid 3 x 2 potret lingkaran + satelit.
6. Instalasi akun/aplikasi: screenshot stadium + empat langkah.
7. Instalasi Web Importer/Cite: dua screenshot stadium.
8. Antarmuka: screenshot stadium + tiga label panel.
9. PDF Reader: dua screenshot stadium.
10. Menambah referensi: screenshot menu + empat baris ikon.
11. Cite: screenshot stadium + enam langkah + tip ink.
12. Gaya sitasi: tabel pill.
13. Satu sumber: kartu cream, screenshot stadium, panah oranye.
14. Kelebihan/keterbatasan: kartu cream dan kartu ink.
15. Kesimpulan: kartu ink dan cream.
16. Penutup: latar ink, teks cream, potret dan orbit.

## Verifikasi

- Build 16 slide.
- `check_no_anim.py`: 16 slide tanpa animasi.
- `check_layout.py`: tidak ada panah menabrak kartu.
- `officecli validate` dan `view issues`: bersih.
- Render semua slide dan periksa screenshot, teks, serta kontras.
- Preview release dari branch berisi tepat `deck.pptx`, `deck.pdf`, `preview.png`.
- PowerPoint manual tetap pemeriksaan terpisah.
