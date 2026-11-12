# Screenshot-first 15-slide deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mengganti kartu ikon dengan screenshot Mendeley yang nyata, merombak slide 7, dan menghapus slide demo alur sehingga deck menjadi 15 slide tanpa mengubah motion baseline.

**Architecture:** Semua perubahan isi dan layout tetap di `build.py`. Screenshot disiapkan sebagai PNG 16:9 di `assets/`, lalu ditempatkan lewat helper `shot()` yang memakai bingkai putih dan `clipped()` agar rasio tidak melar. Indeks animasi di `check_anim.py` dan `build.py` di-remap karena slide 12 lama dihapus. Dokumen dan workflow mengikuti jumlah 15 slide.

**Tech Stack:** Python stdlib, OfficeCLI v1.0.160, Node.js untuk ikon, LibreOffice + Poppler + ImageMagick untuk PDF dan preview, unittest.

**Spec:** `docs/superpowers/specs/2026-11-12-screenshot-slides-15.md`

## Global Constraints

- Deck tepat 15 slide. Slide 12 lama “Demo alur: impor sampai daftar pustaka” dihapus.
- Palet tetap `B0C8E0`, `C1E0E0`, `DCE7D6`, `F6F6F6`. Tidak ada bentuk hitam.
- Sampul, kesimpulan, dan penutup tetap terang.
- Satu klik per slide. Animasi masuk mulai otomatis. Tidak ada transisi, fade, atau exit.
- Motion path, easing, dan durasi tidak berubah. Hanya indeks slide yang berubah.
- Screenshot 16:9, tidak diregangkan, dan punya alt text. Sumber dikreditkan di slide.
- Body minimal 18 pt. Judul slide 36 pt. Keterangan minimal 10 pt.
- Tanpa em dash, tanpa pembuka klise, tanpa “bukan X melainkan Y”.
- Pemutaran manual di PowerPoint 365/2021 wajib dilakukan pengguna sebelum push ke `main` atau rilis.

## Review Focus

1. Screenshot terpotong atau melar: `clipped()` menolak rasio yang tidak 16:9, lalu halaman 5 sampai 11 diperiksa lewat screenshot.
2. Teks meluber di kartu sempit: `officecli view issues` dan screenshot halaman 5 sampai 11 harus bersih.
3. Remap animasi salah setelah slide 12 dihapus: unit test `_spec(12..15)` dan `check_anim.py` pada deck 15 slide.
4. Jumlah preview atau rilis tidak cocok: workflow memeriksa 15 halaman PDF, preview 15 slide, dan teks rilis “Pratinjau 15 slide”.
5. Screenshot tanpa kredit: setiap slide bergambar punya baris sumber, dan tabel aset di spec mencantumkan halaman asal.

## File Structure

- Create: `assets/shot-*.png` (20 file, 1200 x 675).
- Modify: `build.py` (helper screenshot, slide 5 sampai 11, hapus slide 12, remap indeks).
- Modify: `check_anim.py` (`_spec` dan required groups).
- Modify: `test_check_anim.py` (test remap).
- Modify: `README.md` (15 slide, checklist manual).
- Modify: `docs/GUIDELINE.md` (nomor slide, mask, screenshot).
- Modify: `.github/workflows/release.yml` (15 halaman, preview, body rilis).
- Create: `docs/superpowers/specs/2026-11-12-screenshot-slides-15.md` (sudah ada).
- Create: `docs/superpowers/plans/2026-11-12-screenshot-slides-15.md` (file ini).

---

### Task 1: Siapkan aset screenshot 16:9

**Files:**
- Create: `assets/shot-rm-add.png`, `assets/shot-cite-panel.png`, `assets/shot-web-importer.png`, `assets/shot-metadata.png`, `assets/shot-style.png`, `assets/shot-bibliography.png`, `assets/shot-source.png`, `assets/shot-citation.png`, `assets/shot-bib-menu.png`, `assets/shot-account.png`, `assets/shot-app.png`, `assets/shot-extension.png`, `assets/shot-import.png`, `assets/shot-web-save.png`, `assets/shot-details.png`, `assets/shot-organize.png`, `assets/shot-highlight.png`, `assets/shot-notes.png`, `assets/shot-addin.png`, `assets/shot-cite.png`
- Test: shell check dimensi

**Interfaces:**
- Produces: 20 PNG 1200 x 675 dengan nama persis seperti tabel aset di spec. `build.py` memakai nama ini lewat `clipped()`.

- [ ] **Step 1: Siapkan sumber gambar**

Gunakan file sumber yang sudah diunduh di `/data/data/com.termux/files/usr/tmp/opencode/mendeley-assets/`. Jika folder itu tidak ada, unduh ulang dari URL di spec. Jangan mengunduh saat build; aset harus masuk repo.

- [ ] **Step 2: Crop setiap sumber ke 16:9**

Pakai Pillow di shell. Untuk setiap pasangan sumber dan nama aset di tabel spec, crop ke area yang memuat kontrol utama, lalu simpan ke `assets/` dengan ukuran 1200 x 675. Contoh pola:

```python
from PIL import Image, ImageOps
im = Image.open(src).convert("RGB")
im = ImageOps.fit(im, (1200, 675), method=Image.LANCZOS, centering=(0.5, 0.5))
im.save(dst, optimize=True)
```

Atur `centering` per gambar agar kontrol penting tidak terpotong. Nilai yang dipakai:

| Aset | Centering |
|---|---|
| `shot-rm-add` | `(0.5, 0.5)` |
| `shot-cite-panel` | `(0.65, 0.45)` |
| `shot-web-importer` | `(0.5, 0.5)` |
| `shot-metadata` | `(0.5, 0.4)` |
| `shot-style` | `(0.5, 0.5)` |
| `shot-bibliography` | `(0.55, 0.45)` |
| `shot-source` | `(0.35, 0.5)` |
| `shot-citation` | `(0.45, 0.5)` |
| `shot-bib-menu` | `(0.55, 0.45)` |
| `shot-account` | `(0.5, 0.3)` |
| `shot-app` | `(0.5, 0.5)` |
| `shot-extension` | `(0.5, 0.5)` |
| `shot-import` | `(0.5, 0.5)` |
| `shot-web-save` | `(0.5, 0.5)` |
| `shot-details` | `(0.8, 0.35)` |
| `shot-organize` | `(0.5, 0.5)` |
| `shot-highlight` | `(0.35, 0.5)` |
| `shot-notes` | `(0.5, 0.5)` |
| `shot-addin` | `(0.5, 0.5)` |
| `shot-cite` | `(0.65, 0.45)` |

Periksa hasil crop dengan mata sebelum lanjut.

- [ ] **Step 3: Verifikasi dimensi dan jumlah**

```bash
python3 - <<'PY'
from PIL import Image
import glob
files = sorted(glob.glob('assets/shot-*.png'))
assert len(files) == 20, len(files)
for f in files:
    assert Image.open(f).size == (1200, 675), (f, Image.open(f).size)
print('20 aset 16:9 valid')
PY
```

Expected: `20 aset 16:9 valid`.

- [ ] **Step 4: Periksa contact sheet**

Buat contact sheet 4 kolom dari 20 aset, lalu buka gambarnya. Pastikan tidak ada kontrol terpotong, tidak ada gambar buram, dan tidak ada screenshot yang masih memuat margin putih besar.

- [ ] **Step 5: Commit**

```bash
git add assets/shot-*.png
git commit -m "assets: tambah screenshot Mendeley 16:9"
```

### Task 2: Remap spesifikasi animasi

**Files:**
- Modify: `test_check_anim.py:1-5, 61-93`
- Modify: `check_anim.py:24-41, 113, 221`

**Interfaces:**
- Consumes: `_spec(index)` yang mengembalikan daftar tuple `(name, path, duration, accel, decel)`.
- Produces: `_spec(12)` = konten + rail pill; `_spec(13)` = HIN; `_spec(14)` = sidebar split; `_spec(15)` = HIN. Required groups untuk slide split menjadi `(3, 12, 14)`.

- [ ] **Step 1: Tulis test yang gagal**

Ubah import di `test_check_anim.py` menjadi:

```python
from check_anim import HIN, PDOWN, SIN, VIN, _spec, check_slide
```

Tambahkan test di class `CheckAnimTest`:

```python
    def test_slides_remapped_after_demo_removed(self):
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(12)],
            [("#s12-content", VIN), ("#s12-rail-pill", PDOWN)],
        )
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(13)],
            [("#s13-content", HIN)],
        )
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(14)],
            [
                ("#s14-sidebar-bg", SIN),
                ("#s14-sidebar-fg", SIN),
                ("#s14-rail-pill", SIN),
                ("#s14-content", VIN),
            ],
        )
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(15)],
            [("#s15-content", HIN)],
        )
```

- [ ] **Step 2: Jalankan test dan pastikan gagal**

```bash
uv run python test_check_anim.py
```

Expected: FAIL pada `test_slides_remapped_after_demo_removed`, karena `_spec(12)` masih memakai VIN biasa dan `_spec(13)` masih memakai pill.

- [ ] **Step 3: Implementasi remap di `check_anim.py`**

Ganti isi `_spec()` menjadi:

```python
    content = f"#s{index}-content"
    if index in (1, 2, 13, 15):
        return [(content, HIN, 420, 20, 70)]
    if index in (3, 14):
        return [
            (f"#s{index}-sidebar-bg", SIN, 400, 20, 70),
            (f"#s{index}-sidebar-fg", SIN, 400, 20, 70),
            (f"#s{index}-rail-pill", SIN, 400, 20, 70),
            (content, VIN, 500, 20, 70),
        ]
    if index in (5, 8, 12):
        return [
            (content, VIN, 500, 20, 70),
            (f"#s{index}-rail-pill", PDOWN, 500, 30, 50),
        ]
    return [(content, VIN, 500, 20, 70)]
```

Ganti required groups di `check_slide()`:

```python
    required = ["content"] + (
        ["sidebar-bg", "sidebar-fg"] if index in (3, 12, 14) else []
    )
```

Ganti jumlah slide di `main()`:

```python
    if len(roots) != 15:
        bad.append(f"jumlah slide {len(roots)}, seharusnya 15")
```

- [ ] **Step 4: Jalankan test dan pastikan lulus**

```bash
uv run python test_check_anim.py
```

Expected: 6 test lulus di file ini, 0 gagal. Total dengan `test_retarget.py` menjadi 11 test.

- [ ] **Step 5: Commit**

```bash
git add check_anim.py test_check_anim.py
git commit -m "test: remap animasi setelah slide demo dihapus"
```

### Task 3: Hapus slide 12 dan sesuaikan build

**Files:**
- Modify: `build.py:3, 157-294`

**Interfaces:**
- Consumes: `_spec` baru dari Task 2.
- Produces: `TOTAL=15`; slide 13 lama menjadi 12, 14 menjadi 13, 15 menjadi 14, 16 menjadi 15; tidak ada blok slide demo.

- [ ] **Step 1: Ubah jumlah slide**

Ganti `TOTAL=16` menjadi `TOTAL=15`.

- [ ] **Step 2: Hapus blok slide demo**

Hapus seluruh blok dari komentar `# 12 demo` sampai sebelum `# 13 kelebihan keterbatasan`. Jangan hapus slide 13 sampai 16; blok itu otomatis bergeser.

- [ ] **Step 3: Remap kondisi sidebar, HIN, dan pill**

Di `frame()`, ganti:

```python
    split=i in (3,13,15)
```

menjadi:

```python
    split=i in (3,12,14)
```

Di bagian animasi, ganti:

```python
    if i in (1,2,14,16):
```

menjadi:

```python
    if i in (1,2,13,15):
```

Ganti:

```python
    if i in (3,15):
```

menjadi:

```python
    if i in (3,14):
```

Ganti:

```python
    if i in (5,8,13):
```

menjadi:

```python
    if i in (5,8,12):
```

- [ ] **Step 4: Build deck 15 slide**

```bash
uv run build.py
```

Expected: build selesai, `n==TOTAL` tidak melempar `ValueError`.

- [ ] **Step 5: Jalankan gate animasi**

```bash
uv run python check_anim.py
```

Expected: `15 slide: satu klik, easing, arah, dan urutan animasi valid`.

- [ ] **Step 6: Pastikan slide demo hilang**

```bash
officecli view deck.pptx text | grep -i "demo alur" || true
```

Expected: tidak ada output.

- [ ] **Step 7: Commit**

```bash
git add build.py
git commit -m "feat: hapus slide demo dan sesuaikan animasi 15 slide"
```

### Task 4: Tambah helper screenshot dan ubah slide 5-6

**Files:**
- Modify: `build.py:38-43, 116-140`

**Interfaces:**
- Produces: `shot(s, f, x, y, w, alt)` yang menambahkan bingkai putih 0,08 cm, memanggil `clipped()` dengan tinggi `w*9/16`, dan mengembalikan tinggi gambar.
- Consumes: aset `shot-rm-add.png`, `shot-cite-panel.png`, `shot-web-importer.png`, `shot-metadata.png`, `shot-style.png`, `shot-bibliography.png`.

- [ ] **Step 1: Tambah helper**

Setelah `clipped()`, tambahkan:

```python
def shot(s,f,x,y,w,alt):
    h=w*9/16
    box(s,x-0.08,y-0.08,w+0.16,h+0.16,'FFFFFF',0.4,name='bingkai')
    clipped(s,f,x,y,w,h,alt)
    return h
```

- [ ] **Step 2: Ubah slide 5**

Pertahankan kartu kiri. Ganti loop tiga baris kanan menjadi:

```python
for k,(f,hd,bd) in enumerate([
    ('shot-rm-add.png','Mendeley Reference Manager','Pustaka pribadi untuk menyimpan, mengelompokkan, dan menganotasi PDF jurnal.'),
    ('shot-cite-panel.png','Mendeley Cite','Add-in Microsoft Word untuk menyisipkan kutipan dan membuat daftar pustaka.'),
    ('shot-web-importer.png','Web Importer','Ekstensi peramban untuk menyimpan referensi dari halaman web.')]):
    y=4.0+k*4.9;box(s,X0+10.8,y,17.2,4.2,CARD,1.2)
    shot(s,f,X0+11.5,y+0.5,5.6,hd)
    tx(s,X0+17.5,y+0.4,10.0,1.6,hd,22,TX,True)
    tx(s,X0+17.5,y+2.0,10.0,1.9,bd,18,MUT)
```

- [ ] **Step 3: Ubah slide 6**

Pertahankan banner atas. Ganti `card3()` dengan loop kartu bergambar:

```python
w3=(W-1.6)/3
for k,(f,hd,bd) in enumerate([
    ('shot-metadata.png','Metadata','Judul, penulis, tahun, DOI, dan nama jurnal menjadi bahan sitasi.'),
    ('shot-style.png','Gaya sitasi','Mendeley menerapkan gaya yang dipilih, misalnya APA atau IEEE.'),
    ('shot-bibliography.png','Daftar pustaka','Entri disusun otomatis dari metadata dan gaya yang sama.')]):
    x=X0+k*(w3+0.8);box(s,x,9.4,w3,8.6,CARD,1.2)
    shot(s,f,x+0.5,9.9,w3-1.0,hd)
    tx(s,x+0.8,14.7,w3-1.6,1.2,hd,24,TX,True)
    tx(s,x+0.8,15.9,w3-1.6,2.0,bd,18,MUT)
```

- [ ] **Step 4: Build dan periksa dua slide**

```bash
uv run build.py
officecli view deck.pptx screenshot --page 5 -o /data/data/com.termux/files/usr/tmp/opencode/slide5.png
officecli view deck.pptx screenshot --page 6 -o /data/data/com.termux/files/usr/tmp/opencode/slide6.png
```

Buka kedua PNG. Perbaiki teks yang terpotong atau gambar yang terlalu kecil sebelum lanjut. Jika perintah screenshot gagal, ekspor PDF dan render halaman 5 dan 6 dengan `pdftoppm`.

- [ ] **Step 5: Periksa issues**

```bash
officecli view deck.pptx issues --limit 50
```

Expected: tidak ada issue layout pada slide 5 dan 6.

- [ ] **Step 6: Commit**

```bash
git add build.py
git commit -m "feat: screenshot pada slide komponen dan olahan Mendeley"
```

### Task 5: Rombak slide 7

**Files:**
- Modify: `build.py:141-156`

**Interfaces:**
- Consumes: `shot-source.png`, `shot-citation.png`, `shot-bib-menu.png`.
- Produces: layout satu sumber di kiri, dua keluaran di kanan, dua panah, satu baris catatan.

- [ ] **Step 1: Ganti seluruh blok slide 7**

Gunakan koordinat berikut:

| Elemen | x | y | w | h |
|---|---:|---:|---:|---:|
| Kartu sumber | 4,4 | 4,2 | 11,0 | 13,2 |
| Kartu sitasi | 16,2 | 4,2 | 16,2 | 6,3 |
| Kartu daftar pustaka | 16,2 | 11,1 | 16,2 | 6,3 |
| Panah atas | 15,45 | 7,1 | 0,7 | 0,7 |
| Panah bawah | 15,45 | 14,0 | 0,7 | 0,7 |
| Catatan manual | 4,4 | 17,7 | 20,0 | 0,5 |
| Sumber | 4,4 | 18,3 | 20,0 | 0,5 |

Isi teks:

- Kartu sumber: label “Satu sumber”, screenshot `shot-source.png` (9,6 x 5,4), teks “PDF jurnal dan metadata” (16 pt), lalu “Penulis, tahun, judul, dan DOI menjadi bahan kedua keluaran.” (16 pt).
- Kartu sitasi: label “Sitasi dalam teks”, screenshot `shot-citation.png` (7,2 x 4,05), teks “Mendeley Cite menyisipkan sitasi ke kalimat.” (18 pt).
- Kartu daftar pustaka: label “Daftar pustaka”, screenshot `shot-bib-menu.png` (7,2 x 4,05), teks “Entri lengkap disusun dari metadata yang sama.” (18 pt).
- Catatan: “Yang tetap manual: periksa metadata dan sesuaikan gaya sitasi.” (10 pt, MUT).
- Sumber: “Sumber: Mendeley Support (2025); tangkapan layar Mendeley.” (10 pt, MUT).

Kartu sumber memakai PC dengan teks ON_PC, kartu sitasi memakai SC dengan ON_SC, dan kartu daftar pustaka memakai TC dengan ON_TC. Ganti `notes()` slide 7 menjadi: “Satu referensi di Library menjadi sumber untuk sitasi di Word dan entri daftar pustaka. Screenshot menunjukkan panel Cite dan menu Insert Bibliography; teori gaya sitasi tetap di Kelompok 4.”

Gunakan `box()` untuk tiga kartu, `shot()` untuk gambar, `tx()` untuk teks, dan `pic()` ikon `MdArrowForward` untuk dua panah dengan alt `Panah`.

- [ ] **Step 2: Build dan periksa slide 7**

```bash
uv run build.py
officecli view deck.pptx screenshot --page 7 -o /data/data/com.termux/files/usr/tmp/opencode/slide7.png
```

Buka PNG. Pastikan panah tidak menabrak kartu, tidak ada teks terpotong, dan kedua kartu keluaran sejajar.

- [ ] **Step 3: Periksa tabrakan panah**

```bash
uv run python check_layout.py
```

Expected: exit 0, tanpa pesan panah menabrak kartu.

- [ ] **Step 4: Commit**

```bash
git add build.py
git commit -m "feat: rombak slide satu sumber dua keluaran"
```

### Task 6: Screenshot pada slide 8-11

**Files:**
- Modify: `build.py:157-194`

**Interfaces:**
- Consumes: `shot-account.png`, `shot-app.png`, `shot-extension.png`, `shot-import.png`, `shot-web-save.png`, `shot-details.png`, `shot-organize.png`, `shot-highlight.png`, `shot-notes.png`, `shot-addin.png`, `shot-cite.png`, `shot-style.png`, `shot-bibliography.png`.

- [ ] **Step 1: Ubah slide 8**

Hapus panggilan `clipped()` untuk `mask-08-*.png`. Ganti isi loop kartu menjadi:

```python
for k,(f,hd,bd) in enumerate([
    ('shot-account.png','Buat akun','Daftar dengan email aktif.'),
    ('shot-app.png','Pasang aplikasi','Unduh Reference Manager, lalu pasang add-in Mendeley Cite di Word.'),
    ('shot-extension.png','Pasang ekstensi','Tambahkan Web Importer ke peramban untuk menyimpan referensi dari web.')]):
    x=X0+k*(w3+0.8);box(s,x,4.2,w3,12.6,[CARD,SC,TC][k],1.4)
    shot(s,f,x+0.5,4.7,w3-1.0,hd)
    num(s,x+0.7,9.4,1.2,str(k+1),P,'FFFFFF')
    tx(s,x+2.1,9.3,w3-2.8,1.6,hd,22,[TX,ON_SC,TX][k],True)
    tx(s,x+0.8,10.9,w3-1.6,5.0,bd,18,[MUT,ON_SC,MUT][k])
```

Ubah baris sumber menjadi:

```python
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley (n.d.); UCL Library (2019) untuk tangkapan layar akun.',10,MUT)
```

- [ ] **Step 2: Ubah slide 9**

Ganti loop empat kartu menjadi:

```python
for k,(f,hd,bd) in enumerate([
    ('shot-import.png','Impor PDF','Tambahkan PDF jurnal ke Library.'),
    ('shot-web-save.png','Simpan dari web','Gunakan Web Importer pada halaman artikel.'),
    ('shot-details.png','Periksa metadata','Cek judul, penulis, tahun, dan DOI; koreksi yang salah.'),
    ('shot-organize.png','Rapikan','Kelompokkan dengan folder dan tag per bab atau topik.')]):
    x=X0+(k%2)*14.4;y=4.0+(k//2)*7.4;box(s,x,y,13.6,6.6,[CARD,SC,TC,CARD][k],1.3)
    shot(s,f,x+0.6,y+0.5,6.2,hd)
    tx(s,x+7.2,y+0.5,5.8,1.6,hd,20,TX,True)
    tx(s,x+7.2,y+2.2,5.8,3.8,bd,18,MUT)
```

Tambahkan sumber:

```python
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley Support (2025); tangkapan layar Mendeley.',10,MUT)
```

- [ ] **Step 3: Ubah slide 10**

Ganti dua panggilan ikon di kartu kiri dengan screenshot:

```python
for k,(f,hd,bd) in enumerate([
    ('shot-highlight.png','Highlight dan anotasi','Tandai bagian penting langsung pada PDF.'),
    ('shot-notes.png','Catatan per referensi','Tulis ide utama dengan kata sendiri sebelum menulis naskah.')]):
    y=4.9+k*6.6;shot(s,f,X0+0.8,y+0.5,6.6,hd)
    tx(s,X0+7.9,y+0.5,8.7,1.3,hd,22,TX,True)
    tx(s,X0+7.9,y+1.9,8.7,4.0,bd,18,MUT)
```

Tambahkan sumber:

```python
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley Support (2025); tangkapan layar Mendeley.',10,MUT)
```

- [ ] **Step 4: Ubah slide 11**

Ganti loop empat kolom menjadi:

```python
for k,(f,hd,bd) in enumerate([
    ('shot-addin.png','Buka add-in','Buka Mendeley Cite di Microsoft Word.'),
    ('shot-cite.png','Sisipkan kutipan','Pilih referensi, lalu tempatkan pada kalimat.'),
    ('shot-style.png','Pilih gaya','Sesuaikan dengan pedoman kampus.'),
    ('shot-bibliography.png','Buat daftar pustaka','Daftar pustaka tersusun otomatis.')]):
    x=X0+k*(w4+1.6);box(s,x,4.4,w4,13.0,[CARD,SC,TC,PC][k],1.3)
    num(s,x+0.7,5.1,1.5,str(k+1),P,'FFFFFF')
    shot(s,f,x+0.5,7.0,w4-1.0,hd)
    tcol=ON_PC if k==3 else TX
    bcol=ON_PC if k==3 else MUT
    tx(s,x+0.6,10.0,w4-1.2,2.2,hd,20,tcol,True)
    tx(s,x+0.6,12.2,w4-1.2,4.2,bd,18,bcol)
    if k<3:pic(s,icon('MdArrowForward','none','x',P),x+w4+0.3,10.2,1.0,'Panah')
```

Tambahkan sumber:

```python
tx(s,X0,18.3,20,0.5,'Sumber: Mendeley Support (2025); tangkapan layar Mendeley.',10,MUT)
```

- [ ] **Step 5: Build dan periksa empat slide**

```bash
uv run build.py
for p in 8 9 10 11; do officecli view deck.pptx screenshot --page "$p" -o "/data/data/com.termux/files/usr/tmp/opencode/slide$p.png"; done
```

Buka keempat PNG. Periksa teks terpotong, gambar melar, dan panah yang menabrak kartu. Jika perintah screenshot gagal, ekspor PDF dan render halaman 8 sampai 11 dengan `pdftoppm`.

- [ ] **Step 6: Periksa issues dan panah**

```bash
officecli view deck.pptx issues --limit 50
uv run python check_layout.py
```

Expected: tidak ada issue dan exit 0.

- [ ] **Step 7: Commit**

```bash
git add build.py
git commit -m "feat: screenshot pada slide persiapan dan langkah"
```

### Task 7: Dokumen, workflow, dan verifikasi penuh

**Files:**
- Modify: `README.md:1-31`
- Modify: `docs/GUIDELINE.md:4, 47-55`
- Modify: `.github/workflows/release.yml:96-104, 133-143`

- [ ] **Step 1: Perbarui README**

Ganti “Generator deck 16 slide” menjadi “Generator deck 15 slide”. Ganti checklist manual menjadi slide 1, 3, 5, 12, 13, dan 15. Ganti “Sidebar dan pill pada slide 3, 5, dan 13” menjadi “slide 3, 5, dan 12”. Pertahankan pernyataan bahwa pemutaran manual wajib.

- [ ] **Step 2: Perbarui GUIDELINE**

Ganti “Deck 16 slide” menjadi “Deck 15 slide”. Ganti daftar mask menjadi “Slide 4, 5, 10, 13”. Hapus baris lama tentang slide 12 dan `img-library-fade.png`. Tambahkan baris: “Slide 5 sampai 11: screenshot Mendeley 16:9; tangkapan layar akun memakai UCL Library (2019); jangan regangkan; kredit di slide.” Ganti “Slide 15: daftar pustaka” menjadi “Slide 14: daftar pustaka”. Ganti “Slide 16: penutup” menjadi “Slide 15: penutup”. Tambahkan aturan desain: “Setiap slide membawa elemen visual berupa ikon, bentuk, atau screenshot.”

- [ ] **Step 3: Perbarui workflow**

Ganti `test "${#slides[@]}" -eq 16` menjadi `test "${#slides[@]}" -eq 15`. Pertahankan `montage ... -tile 2x8` karena 15 slide mengisi 8 baris dengan satu slot kosong. Ganti `Pratinjau 16 slide` dan alt text menjadi `Pratinjau 15 slide`.

- [ ] **Step 4: Jalankan seluruh gate otomatis**

```bash
uv run build.py
uv run python test_retarget.py
uv run python test_check_anim.py
uv run python check_anim.py
uv run python check_layout.py
officecli validate deck.pptx
officecli view deck.pptx issues --limit 50
```

Expected: semua test lulus, `check_anim.py` melaporkan 15 slide, `check_layout.py` exit 0, validate bersih, issues tidak memuat masalah layout.

- [ ] **Step 5: Ekspor PDF dan preview**

```bash
rm -rf preview
soffice --headless --convert-to pdf --outdir . deck.pptx
mkdir -p preview
pdftoppm -png -r 120 deck.pdf preview/slide
test "$(find preview -maxdepth 1 -name 'slide-*.png' | wc -l)" -eq 15
find preview -maxdepth 1 -name 'slide-*.png' | sort -V | xargs montage -tile 2x8 -geometry 800x450+8+8 -background '#F6F6F6' preview.png
```

Expected: `deck.pdf` 15 halaman dan `preview.png` memuat 15 slide.

- [ ] **Step 6: Audit visual 15 slide**

Buka `preview.png` atau screenshot per halaman. Periksa setiap slide dengan checklist: tidak ada teks terpotong, tidak ada gambar melar, tidak ada panah menabrak kartu, tidak ada kontras gelap di atas gelap, dan tidak ada sumber yang hilang. Perbaiki temuan, lalu ulangi build dan audit.

- [ ] **Step 7: Commit**

```bash
git add README.md docs/GUIDELINE.md .github/workflows/release.yml
git commit -m "docs: sesuaikan deck 15 slide dan preview rilis"
```

- [ ] **Step 8: Minta uji manual pengguna**

Minta pengguna membuka `deck.pptx` di PowerPoint 365/2021 dan memeriksa slide 1, 3, 5, 12, 13, dan 15. Setelah pengguna mengonfirmasi, baru push ke `main` atau jalankan rilis. Jangan mengklaim animasi sudah terverifikasi tanpa konfirmasi ini.
