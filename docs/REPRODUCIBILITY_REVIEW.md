# Tinjauan Reproduksibilitas (Reproducibility Review)

**Penyusun:** Muhammad Alif Italiano Syaiza (Anggota 4 / Lead Documentarian & Error Handler)  
**Tanggal Eksekusi:** 7 November 2026  
**Status Evaluasi:** Terverifikasi Penuh secara Empiris (Data Pipeline, Tokenizer, dan 54 Unit Tests)  
**Branch:** `dev/member-4-documentation`  

---

## 1. Lingkungan Eksekusi & Konfigurasi Sistem

Seluruh verifikasi dijalankan langsung pada mesin lokal di dalam isolasi virtual environment:

- **Sistem Operasi:** Windows (NT 10.0.26100) AMD64
- **Python:** Python 3.10.0 (tags/v3.10.0:b494f59, Oct 4 2021)
- **PyTorch Terpasang:** `torch==2.14.1+cpu` (melalui PyPI wheel standar)
- **Pustaka Pendukung:** `matplotlib==3.10.9`, `numpy==2.2.6`
- **Revisi Dataset Nottingham:** Git commit `0992bb6cd864f6d4b90d6663e08c0ef53ffaa08f`
- **Tokenizer Version:** `nirava-midi-step-v1`  
  **Tokenizer Hash:** `21c0930ebf49f212455600a011be2b14cd066793619b2d47c5d972495a6a9bba`

---

## 2. Catatan Instalasi Dependensi (Penanganan Issue requirements.txt)

### A. Percobaan Instalasi Sesuai `requirements.txt`
Perintah:
```powershell
.\.venv\Scripts\pip install -r requirements.txt
```
**Pesan Error Asli:**
```text
Looking in indexes: https://download.pytorch.org/whl/cpu
ERROR: Could not find a version that satisfies the requirement torch==2.15.0+cpu (from versions: ... 2.14.1+cpu)
ERROR: No matching distribution found for torch==2.15.0+cpu
```
*Temuan Teknis:* Berkas `requirements.txt` mengunci versi `torch==2.15.0+cpu`. Versi `2.15.0` tidak pernah dirilis secara resmi oleh PyTorch di index CPU.

### B. Solusi Alternatif Terotorisasi
Perintah:
```powershell
.\.venv\Scripts\pip install "torch>=2.0.0"
```
*Hasil:* Berhasil memasang `torch==2.14.1+cpu` beserta dependensinya (`typing-extensions`, `networkx`, `sympy`, `filelock`, `jinja2`). Seluruh unit test dan fungsi neural network PyTorch berjalan normal tanpa isu kompatibilitas.

---

## 3. Eksekusi Unit Tests (Empiris)

Perintah yang dijalankan:
```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python -m unittest discover -s tests -v
```

### A. Kondisi Awal (Sebelum Token Cache Riil Dibuat)
- **Hasil:** `Ran 54 tests in 2.183s — FAILED (errors=1, skipped=2)`
- **Rincian:**
  - 51 tes lulus.
  - 2 tes di `tests/test_nirava_midi_torch.py` berstatus `skipped ('processed/tokens_v1.jsonl belum dibuat')`.
  - 1 tes di `tests/test_nirava_midi_train.py` (`test_train_and_eval_single_epoch`) gagal dengan `FileNotFoundError: [Errno 2] No such file or directory: '.../processed/tokens_v1.jsonl'`.
- *Analisis:* Modul tes pelatihan mengasumsikan keberadaan file cache token riil.

### B. Kondisi Akhir (Setelah Eksekusi Pipeline Nottingham)
- **Hasil:** `Ran 54 tests in 42.476s — OK`
- **Tingkat Kelulusan:** **100% (54 dari 54 tes lulus)**

### C. Rekonsiliasi Klaim Jumlah Tes di Dokumen
- Dokumen `docs/DATA_PIPELINE_GUIDE.md` mencantumkan *"Ran 34 tests in ~1.5s"*.
- **Penjelasan:** Angka 34 tes merupakan jumlah tes dari fase Member 2 yang hanya menguji 3 modul data:
  - `test_nirava_midi_tokenizer.py`: 17 tes
  - `test_nirava_midi_data.py`: 11 tes
  - `test_nirava_midi_torch.py`: 6 tes
- Setelah Member 3 mengimplementasikan model, ditambahkan 20 tes baru:
  - `test_nirava_midi_checkpoint.py`: 5 tes
  - `test_nirava_midi_generate.py`: 5 tes
  - `test_nirava_midi_model.py`: 5 tes
  - `test_nirava_midi_train.py`: 5 tes
- **Total Keseluruhan:** $34 + 20 = 54$ unit tests. Klaim 54 tes pada riwayat Member 3 terbukti akurat dan terverifikasi 100%.

---

## 4. Reproduksi Pipeline Data & Split Nottingham

Sesuai instruksi, revisi Nottingham `0992bb6cd864f6d4b90d6663e08c0ef53ffaa08f` di-checkout di `data/nottingham-dataset`.

### A. Langkah 1: Audit Tokenizer (`src/run_tokenizer_audit.py`)
Perintah:
```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python src/run_tokenizer_audit.py
```
**Output Nyata:**
```text
tokenizer=nirava-midi-step-v1 hash=21c0930ebf49f212455600a011be2b14cd066793619b2d47c5d972495a6a9bba
total_file=1034
encoded_ok=519
rejected=515
alasan_reject:
  non_4_4_meter: 501
  overlap_after_quantization: 14
round_trip_pass=519/519
total_steps=288368
total_tokens_incl_bos_eos=289406
steps_per_piece min/median/max=96/512/3584
mean_quant_error_steps(rata2 per file)=0.0051
max_quant_error_steps(tertinggi)=0.3359
file_dengan_off_grid_events(>0.25 step)=105
total_off_grid_events=3060
file_dengan_min_duration_adjusted=0
window128_stride128_estimasi=2753
grup_duplikat_token_identik=2
  hpps24.mid, hpps25.mid
  reelsa-c22.mid, reelsm-q24.mid
```
*Hasil Komparasi terhadap `reports/tokenizer_audit_summary.txt`:* **Identik 100% pada seluruh metrik numerik dan hash.**

### B. Langkah 2: Pembuatan Split Work-Disjoint (`src/build_splits.py`)
Perintah:
```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python src/build_splits.py
```
**Output Nyata:**
```text
seed=20261028 threshold=0.25 tokenizer_hash=21c0930ebf49f212455600a011be2b14cd066793619b2d47c5d972495a6a9bba
pieces_encoded=519 excluded_duplicates=2 kept=517
work_groups=494 multi_file_groups=22
train: pieces=414 groups=395 steps=230176 tokens=231004
validation: pieces=52 groups=51 steps=28048 tokens=28152
test: pieces=51 groups=48 steps=29120 tokens=29222
leak_group_lintas_split=0
leak_token_identik_lintas_split=0
```
*Hasil Komparasi terhadap `reports/split_summary.txt`:* **Identik 100% pada seluruh jumlah pieces, work groups, steps, tokens, dan 0 leakage.**

---

## 5. Prosedur Perlindungan Integritas Repositori

Sesuai aturan kerja, skrip di atas menulis pembaruan ringkasan ke folder `reports/`. Untuk memastikan artefak asli milik A2/A3 tidak terkontaminasi oleh path absolut lokal mesin eksekusi, prosedur berikut diterapkan:
1. Hasil output dicatat dan divalidasi langsung dari terminal stdout.
2. Dijalankan perintah:
   ```powershell
   git checkout -- reports/
   ```
3. Folder `reports/` kembali bersih dan konsisten dengan commit author asli.
4. Dataset mentah di `data/` dan cache token di `processed/` tetap berada di bawah aturan `.gitignore` dan tidak pernah di-stage ke Git.

---

## 6. Apa yang Belum / Tidak Dapat Diverifikasi

1. **Training Penuh Ablasi R0–R3:**
   Sesuai aturan keras nomor 8, training penuh dari inisialisasi acak tidak dijalankan pada sesi ini tanpa izin eksplisit tambahan (untuk menghemat waktu dan komputasi menjelang tenggat). Metrik pelatihan merujuk pada log historis terverifikasi commit `7c1a259`.
2. **Evaluasi Test Set Akhir:**
   Set pengujian held-out (51 karya, 29.222 token) berstatus *frozen* dan belum pernah dievaluasi oleh tim untuk mencegah bias tuning.
3. **Mendengarkan Hasil Generasi (Subjective Listening Test):**
   Uji dengar perseptual manusia belum dilakukan karena memerlukan panel pendengar dan sintesis SoundFont di luar batas MVP simbolik.

---

## 7. Rekomendasi A4 untuk Pemilik Modul

1. **Untuk A2 (Data Pipeline):**
   - Perbarui angka "34 tests" pada `docs/DATA_PIPELINE_GUIDE.md` menjadi penjelasan bahwa 34 tes adalah sub-bagian data dari total 54 tes sistem.
2. **Untuk A3 (Training Engine):**
   - Tambahkan dekorator `@unittest.skipUnless(TOKENS_PATH.exists(), ...)` pada fungsi `test_train_and_eval_single_epoch` di `tests/test_nirava_midi_train.py` agar unit test tetap lulus (gracefully skipped) saat dijalankan di lingkungan fresh clone sebelum dataset Nottingham diunduh.
3. **Untuk A1 (Ketua / Koordinasi):**
   - Perbarui `requirements.txt` dari `torch==2.15.0+cpu` menjadi `torch>=2.0.0` untuk mencegah kegagalan instalasi pada instalasi di masa mendatang.

