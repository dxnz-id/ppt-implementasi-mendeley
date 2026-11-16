# Adaptasi Rancangan Mendeley Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mengubah deck Mendeley menjadi 16 slide sesuai rancangan fitur, instalasi, antarmuka, penambahan referensi, Cite, dan gaya sitasi.

**Architecture:** Semua slide tetap dibangun di `build.py` memakai helper `frame`, `box`, `shot`, `clipped`, `num`, dan `icon`. Slide 5-12 ditulis ulang; slide 13-16 memakai ulang slide satu sumber, kelebihan/keterbatasan, kesimpulan, dan penutup dengan nomor baru. Gate jumlah slide diperbarui di `check_no_anim.py`, workflow, dan dokumentasi.

**Tech Stack:** Python stdlib, Node/react-icons, OfficeCLI, LibreOffice untuk PDF, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-16-adaptasi-rancangan-mendeley.md`

## Global Constraints

- Jumlah slide final 16.
- Ukuran slide 33,87 x 19,05 cm; konten X0=1,2 cm, W=31,2 cm.
- Screenshot 16:9 tidak boleh diregangkan; gunakan `shot()`.
- Mask hanya slide 4; rasio mask tidak boleh diubah.
- Tidak ada animasi atau transisi.
- Teks mengikuti ragam resmi, ejaan baku, dan nama produk asli.
- Jangan mengarang screenshot atau fitur.

## Review Focus

- Screenshot pada slide 6-9 dan 11 harus tetap besar dan tidak terpotong.
- Kartu 3 x 2 dan 2 x 2 tidak boleh tumpang tindih atau meluber.
- Tabel gaya sitasi harus terbaca dan tidak menabrak nomor slide.
- Nomor slide dan total harus konsisten di PPTX, PDF, dan preview.
- Teks panjang seperti "Sinkronisasi cloud" dan langkah Cite tidak boleh terpotong.

---

### Task 1: Perbarui gate jumlah slide

**Files:**
- Modify: `build.py:3`
- Modify: `check_no_anim.py`
- Modify: `.github/workflows/release.yml`
- Modify: `README.md`
- Modify: `docs/GUIDELINE.md`
- Test: `test_check_no_anim.py`

**Interfaces:**
- Produces: `TOTAL=16`; checker mengharapkan 16 slide; CI merender 16 slide.

- [ ] **Step 1: Ubah `TOTAL` menjadi 16 di `build.py`.**
- [ ] **Step 2: Ubah jumlah slide yang diharapkan di `check_no_anim.py` dari 14 menjadi 16.**
- [ ] **Step 3: Ubah `test "${#slides[@]}" -eq 14` menjadi `-eq 16` dan `montage ... -tile 2x7` menjadi `2x8`.**
- [ ] **Step 4: Ubah teks dokumentasi 14 slide menjadi 16 dan perbarui referensi nomor slide.**
- [ ] **Step 5: Jalankan `python3 test_check_no_anim.py`; harapkan 3 test lulus.**

### Task 2: Tulis ulang slide 5-7

**Files:**
- Modify: `build.py` (bagian `# 5 mengenal` sampai sebelum `# 8 persiapan`)

**Interfaces:**
- Consumes: helper `frame`, `box`, `pic`, `icon`, `shot`, `num`, `notes`.
- Produces: slide 5 fitur utama, slide 6 instalasi akun/aplikasi, slide 7 instalasi Web Importer/Cite.

- [ ] **Step 1: Ganti slide 5 dengan grid 3 x 2 berisi enam fitur.**
- [ ] **Step 2: Ganti slide 6 dengan screenshot `shot-account.png` 18 x 10,125 cm dan empat langkah instalasi.**
- [ ] **Step 3: Ganti slide 7 dengan dua kartu screenshot `shot-extension.png` dan `shot-addin.png`.**
- [ ] **Step 4: Jalankan `PATH="$HOME/.local/bin:$PATH" python3 build.py`; harapkan exit 0.**
- [ ] **Step 5: Render slide 5-7 dan periksa teks serta screenshot tidak terpotong.**

### Task 3: Tulis ulang slide 8-10

**Files:**
- Modify: `build.py` (bagian `# 8 persiapan` sampai sebelum `# 11 langkah 3`)

**Interfaces:**
- Consumes: `shot-details.png`, `shot-highlight.png`, `shot-notes.png`.
- Produces: slide 8 antarmuka, slide 9 PDF Reader, slide 10 menambahkan referensi.

- [ ] **Step 1: Ganti slide 8 dengan screenshot `shot-details.png` 19,2 x 10,8 cm dan tiga label panel.**
- [ ] **Step 2: Ganti slide 9 dengan dua kartu screenshot `shot-highlight.png` dan `shot-notes.png`.**
- [ ] **Step 3: Ganti slide 10 dengan screenshot `shot-rm-add.png` 18 x 10,125 cm dan empat cara di kanan.**
- [ ] **Step 4: Build dan render slide 8-10; periksa keterbacaan dan margin.**

### Task 4: Tulis ulang slide 11-12 dan renumber slide 13-16

**Files:**
- Modify: `build.py` (bagian `# 11 langkah 3` sampai akhir)

**Interfaces:**
- Consumes: `shot-addin.png`, data gaya sitasi.
- Produces: slide 11 Cite, slide 12 tabel gaya, slide 13 satu sumber, slide 14 kelebihan, slide 15 kesimpulan, slide 16 penutup.

- [ ] **Step 1: Ganti slide 11 dengan screenshot `shot-addin.png` 14 x 7,875 cm dan enam langkah Cite.**
- [ ] **Step 2: Ganti slide 12 dengan tabel lima gaya sitasi.**
- [ ] **Step 3: Ubah komentar/nomor slide 13-16 agar sesuai urutan baru.**
- [ ] **Step 4: Build dan render seluruh deck.**

### Task 5: Verifikasi dan dokumentasi

**Files:**
- Modify: `docs/GUIDELINE.md` bila nomor slide masih lama.

- [ ] **Step 1: Jalankan `python3 check_no_anim.py deck.pptx`; harapkan `16 slide: tidak ada animasi`.**
- [ ] **Step 2: Jalankan `python3 check_layout.py`; harapkan exit 0.**
- [ ] **Step 3: Jalankan `officecli validate deck.pptx`; harapkan `Validation passed`.**
- [ ] **Step 4: Jalankan `officecli view deck.pptx issues --limit 50`; harapkan 0 issue.**
- [ ] **Step 5: Render contact sheet 16 slide dan periksa semua slide.**
- [ ] **Step 6: Commit dan push branch; jangan rilis tanpa permintaan.**
