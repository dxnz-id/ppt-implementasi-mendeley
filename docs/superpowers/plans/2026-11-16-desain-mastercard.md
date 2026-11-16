# Desain Mastercard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Mengganti desain deck Mendeley ke bahasa visual Mastercard pada branch preview, tanpa mengubah isi atau urutan 16 slide.

**Architecture:** `build.py` tetap menjadi satu-satunya generator. Token dan helper diubah lebih dulu, lalu slide 1-16 ditulis ulang memakai `frame`, `portrait`, `satellite`, `shot`, `eyebrow`, dan `orbit`. `icons.js` mendapat bentuk `circle`; orbit dan mask disimpan sebagai PNG.

**Tech Stack:** Python stdlib, Node/react-icons/sharp, OfficeCLI, LibreOffice, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-16-desain-mastercard.md`

## Global Constraints

- 16 slide; isi dan urutan tetap.
- Latar dominan `F37338`; teks ink `141413`; teks sekunder di atas oranye `262627`; kartu cream/ink.
- Font Arial.
- Screenshot 16:9; frame stadium radius 1,05 cm; mask luar oranye, kecuali screenshot di kartu cream.
- Tidak ada animasi atau sidebar.
- Jangan memakai logo Mastercard.
- Preview release dari branch, bukan `main`.

## Revisi oranye dominan (dieksekusi)

- [x] Ubah `BG` menjadi `F37338`; tambah `BODY=262627`.
- [x] Ganti eyebrow, titik halaman, dan nomor halaman menjadi ink.
- [x] Ganti teks sekunder langsung di atas oranye menjadi charcoal.
- [x] Tambah `orbit-cream-1/2.png` dan `shot-mask-orange.png`.
- [x] Screenshot slide 6-11 memakai mask oranye; slide 13 memakai mask cream.
- [x] Penutup menjadi latar oranye dengan teks ink dan potret cream.
- [x] Build, validasi, render, dan periksa kontras.

## Tasks

### Task 1: Token, helper, dan aset

- [ ] Ganti palet dan font di `build.py`.
- [ ] Tambah `spacing`/`lineSpacing` ke `tx`, `eyebrow`, `portrait`, `satellite`, `orbit`, `frame`.
- [ ] Ubah `shot` menjadi frame stadium putih.
- [ ] Tambah bentuk `circle` di `icons.js`.
- [ ] Buat `assets/orbit-1.svg` dan `assets/orbit-2.svg`.
- [ ] Build dan cek helper dengan satu slide.

### Task 2: Slide 1-4

- [ ] Sampul editorial dengan badge pill, potret lingkaran, satelit, orbit.
- [ ] Anggota: kartu cream dan nomor besar, tanpa mask pastel.
- [ ] Kekurangan: tiga kartu cream + callout ink.
- [ ] Rumusan/tujuan: kartu cream dan ink; hapus mask lama.

### Task 3: Slide 5-8

- [ ] Fitur: 3 x 2 potret lingkaran + satelit.
- [ ] Instalasi 1: screenshot stadium + empat langkah.
- [ ] Instalasi 2: dua screenshot stadium.
- [ ] Antarmuka: screenshot stadium + tiga label.

### Task 4: Slide 9-12

- [ ] PDF Reader: dua screenshot stadium.
- [ ] Menambah referensi: screenshot menu + empat baris.
- [ ] Cite: screenshot + enam langkah + tip ink.
- [ ] Gaya sitasi: tabel pill.

### Task 5: Slide 13-16

- [ ] Satu sumber: kartu cream + screenshot + panah ink.
- [ ] Kelebihan/keterbatasan: kartu cream dan ink.
- [ ] Kesimpulan: kartu ink dan cream.
- [ ] Penutup: latar oranye + teks ink + orbit cream.

### Task 6: Verifikasi dan preview release

- [ ] Build 16 slide.
- [ ] `test_check_no_anim.py`, `check_no_anim.py`, `check_layout.py`.
- [ ] `officecli validate`, `view issues`.
- [ ] Render semua slide; periksa screenshot dan kontras.
- [ ] Update README/GUIDELINE dan CI font.
- [ ] Commit, push branch, buat preview release dari artifact branch.
- [ ] Pastikan tepat tiga aset.
