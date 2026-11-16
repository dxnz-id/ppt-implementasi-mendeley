# Desain Mastercard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Mengganti desain deck Mendeley ke bahasa visual Mastercard pada branch preview, tanpa mengubah isi atau urutan 16 slide.

**Architecture:** `build.py` tetap menjadi satu-satunya generator. Token dan helper diubah lebih dulu, lalu slide 1-16 ditulis ulang memakai `frame`, `portrait`, `satellite`, `shot`, `eyebrow`, dan `orbit`. `icons.js` mendapat bentuk `circle`; orbit disimpan sebagai SVG.

**Tech Stack:** Python stdlib, Node/react-icons/sharp, OfficeCLI, LibreOffice, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-16-desain-mastercard.md`

## Global Constraints

- 16 slide; isi dan urutan tetap.
- Canvas `F3F0EE`; ink `141413`; aksen `CF4500`/`F37338`.
- Font Arial.
- Screenshot 16:9; frame stadium radius 1,05 cm.
- Tidak ada animasi atau sidebar.
- Jangan memakai logo Mastercard.
- Preview release dari branch, bukan `main`.

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

- [ ] Satu sumber: kartu cream + screenshot + panah oranye.
- [ ] Kelebihan/keterbatasan: kartu cream dan ink.
- [ ] Kesimpulan: kartu ink dan cream.
- [ ] Penutup: latar ink + orbit.

### Task 6: Verifikasi dan preview release

- [ ] Build 16 slide.
- [ ] `test_check_no_anim.py`, `check_no_anim.py`, `check_layout.py`.
- [ ] `officecli validate`, `view issues`.
- [ ] Render semua slide; periksa screenshot dan kontras.
- [ ] Update README/GUIDELINE dan CI font.
- [ ] Commit, push branch, buat preview release dari artifact branch.
- [ ] Pastikan tepat tiga aset.
