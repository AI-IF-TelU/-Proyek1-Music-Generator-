# Ekspor Sesi Vibe Coding — Anggota 4 (Lead Documentarian & Error Handler)

**Proyek:** Nirava — MIDI Music Generator  
**Peran:** Anggota 4 (Lead Documentarian & Error Handler)  
**Nama Mahasiswa:** Muhammad Alif Italiano Syaiza  
**NIM:** 103012400321  
**Git User:** `alifitaliano` (`[DIREDAKSI]`)  
**Tanggal Eksekusi:** 7 November 2026  
**Status Sesi:** Selesai (Fase 0 s.d. Fase 7 Terverifikasi Penuh)  
**Branch Kerja:** `dev/member-4-documentation`  

> **Catatan Kejujuran Bukti:**  
> Berkas ini disusun langsung dari sesi interaksi Vibe Coding aktif yang dijalankan oleh Anggota 4 bersama asisten AI (Antigravity / Gemini 3.8 Flash). Ini merupakan catatan kronologis terstruktur dari seluruh instruksi prompt, tindakan, verifikasi empiris, dan penanganan error riil yang dihadapi. Mahasiswa akan melampirkan tautan ekspor (*share link*) platform asli sebagai bukti primer pendukung.

---

## 1. Ringkasan Eksekutif Peran & Tanggung Jawab Anggota 4

Sesuai kontrak kerja [AGENTS.md](../AGENTS.md) dan [docs/TEAM_RESPONSIBILITIES.md](TEAM_RESPONSIBILITIES.md), Anggota 4 memegang tanggung jawab atas:
1. **Tata Kelola Akuntabilitas & Log AI (Bobot Rubrik 25%):** Mengumpulkan, mengaudit, dan menyatukan bukti interaksi Vibe Coding dari seluruh anggota (A1, A2, A3) serta menyusun log mandiri A4 untuk menutup kesenjangan ketiadaan chat Dev 4 sebelumnya.
2. **Katalog Penanganan Error Nyata (*Error Handling*):** Mengidentifikasi dan mendokumentasikan error riil tanpa karangan fiktif, mencakup 7 kasus kegagalan teknis dan solusinya.
3. **Audit Reproduksibilitas Empiris:** Memvalidasi bahwa repositori dapat di-clone, diinstal dependensinya, dan dijalankan unit test serta data pipeline-nya pada lingkungan bersih (54 unit tests lulus 100%, 517 karya Nottingham divalidasi).
4. **Penyusunan Materi Laporan & Presentasi:** Menghasilkan catatan panduan presentasi individual untuk 4 anggota kelompok dan meninjau laporan `report/README.md` serta slide PowerPoint `report/Nirava-Presentasi.pptx`.

---

## 2. Kronologi Interaksi & Tindakan Teknis per Fase

### Sesi Awal — Klarifikasi Job Desk & Audit Kesenjangan
- **Prompt Pengguna (Kutipan Asli):**
  > "saya disini berperan sebagai anggota 4 yang tugasnya itu tertera di folder ini kamu baca aja semuanya. nah kira\" saya harus apa yaa sebagai anggota 4 berikan saya job desk dan apa yg harus saya lakukan sebagai anggota 4. beritahu secara detail, lengkap, dan jelas"
- **Tindakan Assistant & Analisis:**
  - Mengaudit repositori dan menemukan bahwa Anggota 4 berstatus *"Belum teridentifikasi"* pada laporan dan riwayat commit.
  - Memetakan 4 pilar job desk A4 dan menyajikan rencana kerja awal.

---

### Pelaksanaan TASK A4 (Fase 0 s.d. Fase 7)
- **Prompt Pengguna (Kutipan Tugas Utama):**
  > "# TASK A4 — Lead Documentarian & Error Handler (Nirava MIDI Music Generator)
  > ## 1. Peran dan konteks
  > Kamu bertindak sebagai asisten saya, Anggota 4 (A4): Lead Documentarian & Error Handler...
  > Data saya: Nama: Muhammad Alif Italiano Syaiza, NIM: 103012400321, Git user.name: alifitaliano, Git user.email: [DIREDAKSI]...
  > Kerjakan SEMUA fase (0 sampai 7) secara berurutan dan otomatis, tanpa menunggu konfirmasi saya di antara fase..."

#### Fase 0: Pemeriksaan Lingkungan & Status Git
- **Perintah:**
  ```powershell
  git status
  git branch -vv
  git remote -v
  Get-Content .gitignore
  ```
- **Hasil Nyata:**
  - Terkonfirmasi berada pada branch `dev/member-4-documentation` yang melacak `origin/dev/member-4-documentation`.
  - Terkonfirmasi bahwa branch `dev/member-4-documentation` identik dengan `origin/main` pada commit `5bb7b80`.
  - Berkas `.gitignore` telah mencakup `**/.venv/`, `data/`, `runtime/`, `processed/`, `**/.env`, `*.pt`, dan `*.mid`.

#### Fase 1: Konfigurasi Identitas Git & Matriks Kontribusi
- **Perintah:**
  ```powershell
  git config --local user.name "alifitaliano"
  git config --local user.email "[DIREDAKSI]"
  ```
- **Tindakan:**
  - Membuat berkas [`docs/CONTRIBUTION_MATRIX.md`](CONTRIBUTION_MATRIX.md) yang memetakan identitas resmi 4 anggota (Nama, NIM, akun Git teramati, branch).
  - Mencatat variasi author Dev 1 (`Muh Fajri` dan `Muhammad Fajri`), status akun `haikal56` (A2), dan `tmuhammadsanubari-cell` (A3).
  - Menegaskan bahwa commit `264f783` dan `5bb7b80` di akun Dev 1 disusun bersama AI dan bukan kontribusi A4.

#### Fase 2: Inventarisasi Bukti Chat LLM & Rekonsiliasi Sumber
- **Tindakan & Temuan:**
  - Membandingkan `report/REKAP_ARAHAN_DEV_1-4.md` dengan `origin/main` (terbukti 100% identik, 591 baris).
  - Melakukan penghitungan baris riil pada seluruh file chat export:
    - `docs/llm_chat_export_member1.md`: 229 baris (11 sesi M1-01 s.d. M1-11).
    - `docs/llm_chat_export_member2.md`: 2.124 baris (18 langkah prompt terformat).
    - `docs/llm_chat_export_member3.md`: 186 baris (8 sesi S1 s.d. S8).
    - `docs/llm_chat_export_member4.md`: Berkas aktif sesi A4 ini.
  - Menginvestigasi diskrepansi klaim: `docs/LLM_INTERACTION_LOG.md` baris 160 menyebut 846 baris untuk Member 2, sementara file riilnya 2.124 baris karena pembaruan TASK 02B commit `4730635`.
  - Menghasilkan berkas [`docs/CHAT_EVIDENCE_INVENTORY.md`](CHAT_EVIDENCE_INVENTORY.md) dan [`docs/A4_PESAN_KE_ANGGOTA.md`](A4_PESAN_KE_ANGGOTA.md).

#### Fase 3: Log Error Nyata, Kronologi Keputusan & Append Log
- **Tindakan:**
  - Menambahkan sesi `Sesi A4-01` pada [`docs/LLM_INTERACTION_LOG.md`](LLM_INTERACTION_LOG.md) tanpa menghapus isi lama.
  - Menyusun [`docs/ERROR_LOG.md`](ERROR_LOG.md) mendokumentasikan 7 insiden teknis riil:
    1. ERR-01: Penolakan palsu pitch-bend netral (8192) di tick 0.
    2. ERR-02: Disparitas rekonsiliasi data Nottingham (515 vs 519 vs 517 file).
    3. ERR-03: Silent fallback ke data sintetis pada skrip runner training.
    4. ERR-04: ValueError sequence akibat terminasi dini token EOS saat sampling.
    5. ERR-05: Kendala perintah `gh` tidak dikenali saat autentikasi.
    6. ERR-06: Hambatan izin penulisan Git refs dan penguncian berkas DOCX.
    7. ERR-07: Kegagalan resolusi DNS/network sandbox saat git clone.
  - Menyusun [`docs/DECISION_TIMELINE.md`](DECISION_TIMELINE.md) merangkum 8 tonggak keputusan besar proyek dari blueprint speech hingga laporan akhir.

#### Fase 4: Reproducibility Review (Eksekusi Empiris Nyata)
- **Perintah & Temuan Instalasi:**
  - Membuat virtual environment `.venv` dengan Python 3.10.0.
  - Eksekusi `pip install -r requirements.txt` gagal dengan pesan: `ERROR: No matching distribution found for torch==2.15.0+cpu` (versi 2.15.0 non-eksisten).
  - Menjalankan alternatif resmi sesuai aturan nomor 8: `pip install "torch>=2.0.0"` dan memasang `matplotlib`. Berhasil memasang `torch==2.14.1+cpu`.
- **Eksekusi 54 Unit Tests:**
  - Kondisi awal (sebelum token dibuat): 51 lulus, 2 skip, 1 error (`FileNotFoundError` pada `test_train_and_eval_single_epoch`).
  - Mengklon Nottingham dataset ke `data/nottingham-dataset` dan checkout revisi `0992bb6cd864f6d4b90d6663e08c0ef53ffaa08f`.
  - Menjalankan `src/run_tokenizer_audit.py` (519 ter-encode, 515 ditolak [501 non-4/4, 14 overlap], 519/519 round-trip lulus).
  - Menjalankan `src/build_splits.py` (517 karya disimpan, 494 work groups, 414 train / 52 val / 51 test, 0 leakage).
  - Menguji ulang unit test: **Ran 54 tests in 42.476s — OK (100% lulus)**.
  - Mengembalikan folder `reports/` via `git checkout -- reports/` agar artefak asli milik A2/A3 tidak terkontaminasi path mesin lokal.
  - Menyusun laporan lengkap di [`docs/REPRODUCIBILITY_REVIEW.md`](REPRODUCIBILITY_REVIEW.md).

#### Fase 5: Temuan Review Lintas Anggota
- **Tindakan:**
  - Memeriksa dan memvalidasi 10 temuan kritis pada berkas [`docs/REVIEW_FINDINGS_A4.md`](REVIEW_FINDINGS_A4.md).
  - Memecahkan teka-teki selisih token:
    $$\text{Train Target Tokens} = 231.004 - 414 = 230.590$$
    $$\text{Val Target Tokens} = 28.152 - 52 = 28.100$$
    (Selisih tepat 1 token per lagu adalah token BOS yang tidak pernah menjadi target prediksi next-token).
  - Menandai ketiadaan eksperimen R4, residu speech pada `.env.example`, dan kuncian versi di `requirements.txt`.

#### Fase 6: Laporan Akhir, Slide Review & Panduan Presentasi
- **Tindakan:**
  - Memvalidasi dan menyusun draf perbaikan laporan di [`docs/REPORT_REVIEW_A4.md`](REPORT_REVIEW_A4.md) dengan tabel perubahan Teks Lama vs Teks Usulan untuk Bagian 7, 8, 10, dan slide PPTX.
  - Menyusun panduan presentasi komprehensif untuk seluruh 4 anggota di [`docs/PRESENTATION_NOTES.md`](PRESENTATION_NOTES.md), dilengkapi alur end-to-end terpadu dan 5 pertanyaan potensial dosen beserta jawabannya.
  - Mendokumentasikan isu-isu yang belum selesai pada [`docs/OPEN_ISSUES_A4.md`](OPEN_ISSUES_A4.md).

---

## 3. Matriks Hasil Pengujian Empiris

| Komponen Pengujian | Perintah Eksekusi | Output Nyata | Status |
|---|---|---|---|
| **Python & PyTorch Version** | `python -c "import torch; print(torch.__version__)"` | `Python 3.10.0` / `Torch 2.14.1+cpu` | **Terverifikasi** |
| **Seluruh Unit Tests (54 Tes)** | `python -m unittest discover -s tests -v` | `Ran 54 tests in 42.476s - OK` | **100% Lulus** |
| **Tokenizer Audit Nottingham** | `python src/run_tokenizer_audit.py` | `encoded_ok=519, rejected=515, round_trip=519/519` | **100% Identik** |
| **Work-Disjoint Split Generator** | `python src/build_splits.py` | `kept=517, groups=494, train=414, val=52, test=51, leak=0` | **100% Identik** |

---

## 4. Handoff & Rekomendasi A4

1. Seluruh artefak dokumentasi telah disimpan pada folder `docs/` di bawah branch `dev/member-4-documentation`.
2. Anggota 1, 2, dan 3 dipersilakan meninjau draf pesan pada `docs/A4_PESAN_KE_ANGGOTA.md` untuk melengkapi konfirmasi identitas dan share link chat asli.
3. Seluruh anggota disarankan membaca `docs/PRESENTATION_NOTES.md` sebelum sesi presentasi di hadapan dosen pengampu.
