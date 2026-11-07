# Tinjauan Laporan & Slide Presentasi (Report & Slide Review by A4)

**Penyusun:** Muhammad Alif Italiano Syaiza (Anggota 4 / Lead Documentarian & Error Handler)  
**Tanggal:** 7 November 2026  
**Status Dokumen Target:**
- `report/README.md` (Laporan Proyek Utama)
- `report/Nirava-Presentasi.pptx` (Slide Presentasi 16 Halaman)
- `report/REKAP_ARAHAN_DEV_1-4.md` (Rekap Arahan Seluruh Anggota)

> **Catatan Tata Kelola:** Sesuai aturan kerja, A4 **tidak menimpa langsung** berkas laporan atau presentasi yang sudah ada. Temuan dan usulan perbaikan disajikan dalam bentuk daftar komparasi teks (Teks Lama vs Teks Usulan beserta Alasannya) agar dapat ditinjau oleh tim sebelum difinalisasi.

---

## 1. Bagian yang Sudah Akurat terhadap Sumber Data & Eksperimen

Setelah diverifikasi silang terhadap kode di `src/`, unit tests di `tests/`, serta artefak di `reports/`, bagian-bagian berikut pada `report/README.md` telah terbukti akurat:
1. **Latar Belakang & Batas Lingkup (Bagian 1 & 2):** Penegasan bahwa Nirava berfokus pada melodi monofonik simbolik MIDI 4/4 120 BPM tanpa audio rendering WAV/MP3 dan tanpa fitur upload pengguna sudah sesuai dengan kontrak `PRD.md`.
2. **Representasi Tokenisasi (Bagian 3):** Spesifikasi 133 token (128 pitch, PAD 0, BOS 1, EOS 2, REST 3, HOLD 4) dengan kuantisasi 16 step/bar akurat terhadap implementasi `nirava_midi_tokenizer.py`.
3. **Rekonsiliasi Dataset Nottingham (Bagian 4):** Penjelasan mengenai 1.034 file awal, penolakan 501 file meter non-4/4, penolakan 14 file overlap nada, 519 file ter-encode, dan eliminasi 2 duplikat identik sehingga menghasilkan **517 karya unik** (494 work groups) telah terbukti empiris 100% pada eksekusi Fase 4.
4. **Hasil Komparasi R0 vs R1 (Bagian 7):** Pengakuan bahwa unigram baseline R0 menghasilkan NLL 1.5182 (PPL 4.56) dan model usulan R1 mengunggulinya dengan NLL 1.1955 (PPL 3.31) sesuai dengan hasil eksperimen pada commit `7c1a259`.
5. **Transparansi Keterbatasan (Bagian 11):** Pengakuan jujur bahwa evaluasi test set akhir (51 karya), listening test manusia, dan integrasi frontend/backend belum selesai dilakukan mencerminkan integritas akademik yang tinggi.

---

## 2. Bagian yang Perlu Identitas dan Bukti Tambahan

1. **Pemetaan Identitas Anggota Resmi (Tabel Bagian 10):**
   - Saat ini tabel masih mencantumkan *"Belum teridentifikasi"* untuk A4 dan belum memuat nama lengkap serta NIM resmi untuk seluruh 4 anggota.
   - Perlu dimasukkan identitas resmi:
     - **A1:** Muhammad Fajri / NIM: 10301230062
     - **A2:** Muhammad Izza Haikal / NIM: 103012300092
     - **A3:** Taura Muhammad Sanubari / NIM: 103012330280
     - **A4:** Muhammad Alif Italiano Syaiza / NIM: 103012400321
2. **Pencantuman Bukti Chat A4:**
   - Bagian 8 dan 10 pada `report/README.md` serta Bagian 6 dan 9.4 pada `report/REKAP_ARAHAN_DEV_1-4.md` mencatat *"chat khusus Dev 4 belum ditemukan"*.
   - Perlu ditautkan ke berkas baru: [`docs/llm_chat_export_member4.md`](../docs/llm_chat_export_member4.md).

---

## 3. Klaim yang Perlu Dilunakkan (Softening Overclaims)

1. **Klaim Hyperparameter Optimal:**
   - *Teks di laporan:* Pernyataan bahwa LR $1\times 10^{-3}$ adalah titik kerja "optimal".
   - *Evaluasi:* Tim hanya menguji 2 nilai LR (1e-3 dan 3e-4) pada 1 seed acak tanpa grid search luas.
   - *Arah revisi:* Nyatakan sebagai *"menunjukkan konvergensi yang lebih cepat dan stabil dibandingkan LR 3e-4 pada konfigurasi yang diuji"*.
2. **Klaim "Keseimbangan Ideal" pada Temperature 1.0:**
   - *Teks di laporan:* Menyebut temperature 1.0 menghasilkan "keseimbangan ideal".
   - *Evaluasi:* Tidak ada data empiris penilaian musik (blind listening test) dari manusia.
   - *Arah revisi:* Nyatakan secara objektif: *"menghasilkan rata-rata 37 nada dengan variasi interval nada yang lebih seimbang dibandingkan 0.8 (32 nada) dan 1.2 (48 nada)"*.
3. **Ketiadaan Eksperimen R4:**
   - Pada tabel ablasi laporan, tidak ada baris R4 (langsung R0, R1, R2, R3, lalu generasi R5).
   - Perlu penjelasan eksplisit bahwa konfigurasi R4 ditiadakan karena keterbatasan komputasi dan difokuskan pada pengujian sampling R5.

---

## 4. Daftar Usulan Perubahan Konkret

Berikut adalah daftar usulan perubahan per bagian untuk ditinjau oleh tim:

### Usulan 1: Pembaruan Tabel Identitas dan Peran (File: `report/README.md`, Bagian 10)
- **Teks Lama (baris 221–226):**
  ```markdown
  | Peran | Identitas yang terlihat | Tanggung jawab | Bukti kontribusi |
  |---|---|---|---|
  | A1 — Prompt Engineer & LLM Navigator/ketua | `Muh Fajri` / `Muhammad Fajri` | Arah produk, strategi prompt, kontrak model/data, keputusan dan review | [Pivot MIDI `d1259a2`](...), [struktur README `758fbb3`](...), [pilihan Nottingham `9c64cbb`](...) |
  | A2 — Data Pipeline & Preprocessing Engineer | `haikal56` | Audit sumber, parsing, tokenisasi, split, penyiapan data | [Pipeline `216aed4`](...), [rekonsiliasi data `4c48d2f`](...), [log AI `4730635`](...) |
  | A3 — Training Loop & Hyperparameter Tuning Engineer | `tmuhammadsanubari-cell` | Model, loop belajar, checkpoint, sampling, eksperimen dan koreksi hasil | [Implementasi training `2f67f17`](...), [audit dan koreksi eksperimen `7c1a259`](...) |
  | A4 — Lead Documentarian & Error Handler | **Belum teridentifikasi** | Kompilasi chat asli, error dan solusi, verifikasi laporan, presentasi | Belum ditemukan commit author terpisah yang dapat dipetakan ke A4 pada HEAD yang diperiksa |
  ```
- **Teks Usulan:**
  ```markdown
  | Peran | Anggota & NIM | Identitas Git Teramati | Tanggung Jawab Utama | Bukti Kontribusi Utama |
  |---|---|---|---|---|
  | **A1 — Prompt Engineer & Ketua** | Muhammad Fajri (10301230062) | `Muh Fajri` / `Muhammad Fajri` | Arah produk, strategi prompt, kontrak arsitektur & tokenisasi v1, review | Commit `c90b04b` s.d. `9c64cbb`, `docs/ML_ARCHITECTURE.md`, `README.md` |
  | **A2 — Data Pipeline Engineer** | Muhammad Izza Haikal (103012300092) | `haikal56` | Audit dataset Nottingham, tokenizer 133, work-disjoint split | Commit `216aed4`, `4c48d2f`, `4730635`, `src/nirava_midi_tokenizer.py`, `reports/DATASET_AUDIT_REPORT.md` |
  | **A3 — Training Loop Engineer** | Taura Muhammad Sanubari (103012330280) | `tmuhammadsanubari-cell` | Model NiravaLSTM from scratch, masked loss, training loop, ablasi | Commit `2f67f17`, `7c1a259`, `src/nirava_midi_lstm.py`, `reports/EXPERIMENT_REPORT.md`, `training_curves.png` |
  | **A4 — Lead Documentarian** | Muhammad Alif Italiano Syaiza (103012400321) | `alifitaliano` | Audit reproduksibilitas, log error riil, integrasi bukti chat, laporan | Branch `dev/member-4-documentation`, `docs/llm_chat_export_member4.md`, `docs/ERROR_LOG.md`, `docs/REPRODUCIBILITY_REVIEW.md` |
  ```
- **Alasan:** Memasukkan nama lengkap dan NIM resmi keempat anggota sesuai rubrik akuntabilitas tim 20%, serta mencatat peran nyata dan branch aktif Anggota 4.

---

### Usulan 2: Pembaruan Status Ketersediaan Bukti Chat A4 (File: `report/README.md`, Bagian 8 & `report/REKAP_ARAHAN_DEV_1-4.md`, Bagian 6 & 9.4)
- **Teks Lama:**
  > *"Status sumber: belum ditemukan file ekspor percakapan khusus Dev 4... Kelengkapan ekspor asli, analisis kelompok, serta kontribusi Member 4 masih perlu dilengkapi."*
- **Teks Usulan:**
  > *"Bukti percakapan Vibe Coding dan penanganan error untuk Anggota 4 telah didokumentasikan secara mandiri pada [docs/llm_chat_export_member4.md](../docs/llm_chat_export_member4.md), mencakup proses audit reproduksibilitas 54 unit tests, verifikasi tokenisasi Nottingham, rekonsiliasi data, serta penyusunan materi presentasi."*
- **Alasan:** Menutup catatan kesenjangan dokumentasi Dev 4 secara sah dengan menautkan ke artefak kerja riil yang telah dibuat.

---

### Usulan 3: Penjelasan Matematis Selisih Token pada Bagian 7 (File: `report/README.md`, Bagian 7)
- **Teks Usulan Tambahan:**
  > *"Catatan Teknis Jumlah Token: Laporan data mencatat 231.004 token latih dan 28.152 token validasi, sedangkan laporan evaluasi model mencatat 230.590 token latih dan 28.100 token validasi. Selisih tepat 414 token pada train (sesuai jumlah karya train) dan 52 token pada val (sesuai jumlah karya val) terjadi karena token awal `[BOS]` hanya berfungsi sebagai context input pertama dan tidak dihitung sebagai target prediksi berikutnya dalam Masked Cross-Entropy Loss ($N_{\text{target}} = N_{\text{tokens}} - N_{\text{pieces}}$)."*
- **Alasan:** Mencegah salah paham dari dosen atau reviewer yang mengira ada token yang hilang atau tidak sinkron.

---

### Usulan 4: Catatan Presentasi Slide PowerPoint (`report/Nirava-Presentasi.pptx`)
- **Evaluasi Slide:**
  - Slide presentasi berisi 16 halaman yang mencakup alur lengkap dari latar belakang hingga keterbatasan.
  - Namun, slide belum mencantumkan pembagian nama pembicara (*speaker assignment*) untuk masing-masing anggota.
- **Usulan Tindakan:**
  - Tetapkan pembagian slide per pembicara pada slide cover atau panduan presentasi:
    - **Slide 1–4:** Muhammad Fajri (A1) — Pengenalan, Masalah, Arsitektur, Kontrak
    - **Slide 5–8:** Muhammad Izza Haikal (A2) — Dataset Nottingham, Filtering 4/4, Tokenizer 133, Work-Disjoint
    - **Slide 9–12:** Taura Muhammad Sanubari (A3) — Model From Scratch, Training Loss, Ablasi R0–R5, Kurva
    - **Slide 13–16:** Muhammad Alif Italiano Syaiza (A4) — Debugging Real Error, Vibe Coding Log, Evaluasi Reproduksibilitas, Keterbatasan & Next Steps
- **Alasan:** Memastikan saat presentasi di hadapan dosen, seluruh 4 anggota berbicara dengan alokasi waktu dan substansi yang seimbang.

