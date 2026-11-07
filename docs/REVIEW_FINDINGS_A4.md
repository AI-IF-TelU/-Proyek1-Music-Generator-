# Temuan Review Lintas Anggota (Review Findings by A4)

**Penyusun:** Muhammad Alif Italiano Syaiza (Anggota 4 / Lead Documentarian & Error Handler)  
**Tanggal:** 7 November 2026  
**Peran:** Verifikasi Kritis Independen & Audit Kualitas Dokumen Proyek Nirava  
**Prinsip Kerja:** Setiap temuan diverifikasi langsung terhadap kode/dokumen asli (dilengkapi lokasi file dan nomor baris). A4 tidak mengubah berkas milik anggota lain; temuan disajikan beserta tindakan rekomendasi dan pemilik modul (*module owner*).

---

## 1. Ringkasan Matriks Temuan

| No | Kategori Temuan | Status Verifikasi | Tingkat Kritis | Pemilik Modul | Tindakan yang Disarankan |
|---|---|---|---|---|---|
| **1** | Ketidaksesuaian Baris/Langkah Chat Member 2 | **Terkonfirmasi Nyata** | Sedang | A2 & A1 | Klarifikasi versi berkas di `docs/LLM_INTERACTION_LOG.md` |
| **2** | Perbedaan Hitungan Token (230.590 vs 231.004) | **Terkonfirmasi & Terpecahkan** | Rendah (Eksplanatif) | A2 & A3 | Beri catatan eksplanasi matematis pergeseran target BOS |
| **3** | Diskrepansi Jumlah Unit Tests (34 vs 54) | **Terkonfirmasi Nyata** | Rendah | A2 | Perbarui catatan cakupan di `docs/DATA_PIPELINE_GUIDE.md` |
| **4** | Pin Versi PyTorch Ilegal pada `requirements.txt` | **Terkonfirmasi Nyata** | **Tinggi (Instalasi)** | A1 / Tim | Ubah pin versi menjadi `torch>=2.0.0` dan hapus komentar lokal mesin |
| **5** | Sisa Variabel Speech pada `.env.example` | **Terkonfirmasi Nyata** | Sedang | A1 / Tim | Hapus konfigurasi audio upload dari template lingkungan |
| **6** | Klaim Hasil Melebihi Bukti di `EXPERIMENT_REPORT.md` | **Terkonfirmasi Nyata** | **Tinggi (Akademik)** | A3 | Lunakkan istilah; koreksi kata "polifonik"; jelaskan ketiadaan R4 |
| **7** | Kesenjangan Tata Kelola Stage 1 vs Implementasi | **Terkonfirmasi Nyata** | **Tinggi (Tata Kelola)** | A1 & Dosen | Laporkan ke dosen untuk otorisasi formal retrospectif |
| **8** | Ketiadaan Bukti SHA/Ukuran Artefak Model Runtime | **Terkonfirmasi Nyata** | Sedang | A3 & A4 | Dokumentasikan hash, ukuran, dan instruksi ekspor reproduksi |
| **9** | Residu Istilah Domain Speech pada Dokumen Aktif | **Terkonfirmasi Nyata** | Rendah | A1 | Bersihkan rujukan ukuran WAV pada dokumen spesifikasi |
| **10** | Diskrepansi Penamaan Folder/Repo Historis | **Terkonfirmasi Nyata** | Rendah (Historis) | A1 / Tim | Tambahkan catatan transisi pemindahan repository GitHub |

---

## 2. Rincian Temuan & Analisis Teknis

### Temuan 1: Ketidaksesuaian Jumlah Baris dan Langkah Chat Member 2
- **Lokasi Berkas:**
  - `docs/LLM_INTERACTION_LOG.md` (baris 160)
  - `docs/llm_chat_export_member2.md`
  - `report/REKAP_ARAHAN_DEV_1-4.md` (baris 28, 96–97)
- **Kondisi Riil:**
  - `docs/LLM_INTERACTION_LOG.md` menulis: `docs/llm_chat_export_member2.md (846 baris, kronologi lengkap 173+ langkah)`.
  - Penghitungan riil pada `docs/llm_chat_export_member2.md` menghasilkan **2.124 baris**.
  - `report/REKAP_ARAHAN_DEV_1-4.md` mencatat **18 langkah prompt pengguna**.
- **Akar Masalah:** Log Member 2 diperbarui secara masif pada commit `4730635` (menambahkan dialog TASK 02B) sehingga jumlah baris bertambah dari 846 menjadi 2.124 baris. Angka "173+ langkah" mencakup seluruh turn internal AI/tool calls, sedangkan rekap arahan merangkumnya menjadi 18 interaksi prompt utama.
- **Rekomendasi Pemilik (A1 & A2):** Tambahkan catatan di `docs/LLM_INTERACTION_LOG.md` bahwa 846 baris adalah versi awal sebelum pembaruan TASK 02B commit `4730635`.

---

### Temuan 2: Sumber Perbedaan Jumlah Token Pelatihan (230.590 vs 231.004)
- **Lokasi Berkas:**
  - `reports/split_summary.txt` (baris 4–5): `train tokens=231004`, `validation tokens=28152`
  - `reports/EXPERIMENT_REPORT.md` (baris 6): `train 230.590`, `val 28.100`
  - `src/build_splits.py` (baris 94, 136)
  - `src/run_experiments.py` (baris 127–133)
  - `src/nirava_midi_data.py` (baris 17–38)
- **Hasil Verifikasi Kode & Matematika:**
  - Di `src/build_splits.py`, token dihitung per sequence lengkap: $\text{len}(\text{tokens})$, yang mencakup token `[BOS]` di awal dan `[EOS]` di akhir.
  - Di `src/run_experiments.py`, token dihitung dari akumulasi `mask.sum()` pada DataLoader target:
    ```python
    train_tokens += int(mask.sum().item())
    ```
  - Pada model autoregresif shifted-target (`src/nirava_midi_data.py`), target sequence adalah `tokens[1:]`. Token `[BOS]` (indeks 0) hanya berfungsi sebagai *input context* pertama dan tidak pernah menjadi *target prediction*.
  - Akibatnya, setiap lagu kehilangan tepat 1 target token (token BOS).
  - **Kalkulasi Matematis:**
    $$\text{Train Tokens Target} = 231.004 - 414 \text{ pieces} = 230.590 \text{ tokens}$$
    $$\text{Val Tokens Target} = 28.152 - 52 \text{ pieces} = 28.100 \text{ tokens}$$
- **Kesimpulan:** Tidak ada bug data atau kehilangan token. Selisih tepat 414 token pada train dan 52 token pada validation merupakan konsekuensi matematis dari pergeseran target autoregresif next-token prediction.
- **Rekomendasi Pemilik (A2 & A3):** Dokumentasikan penurunan formula $N_{\text{target}} = N_{\text{tokens}} - N_{\text{pieces}}$ pada catatan metodologi agar penguji tidak menganggapnya inkonsistensi.

---

### Temuan 3: Diskrepansi Jumlah Unit Tests (34 Tests vs 54 Tests)
- **Lokasi Berkas:**
  - `docs/DATA_PIPELINE_GUIDE.md` (baris 64, 86)
  - `docs/llm_chat_export_member3.md` (baris 25)
  - Direktori `tests/`
- **Kondisi Riil:**
  - `docs/DATA_PIPELINE_GUIDE.md` menulis: *"Eksekusi Uji Coba Unit Test (34 Tests)"*.
  - Eksekusi penuh `python -m unittest discover -s tests -v` menjalankan **54 tes**.
- **Akar Masalah:** Panduan data ditulis oleh A2 pada fase M1/TASK 02, di mana modul tes baru mencakup 3 berkas data (tokenizer 17 tes, data 11 tes, torch 6 tes = 34 tes). Anggota 3 kemudian menambahkan 4 berkas tes baru untuk arsitektur, training, checkpoint, dan generation (20 tes), sehingga total menjadi 54 tes.
- **Rekomendasi Pemilik (A2):** Perbarui dokumen panduan data dengan memberi label bahwa 34 tes adalah pengujian subsistem data pipeline, sedangkan repositori memiliki total 54 unit tests.

---

### Temuan 4: Kuncian Versi Ilegal pada `requirements.txt`
- **Lokasi Berkas:**
  - `requirements.txt` (baris 1–7)
  - `docs/DATA_PIPELINE_GUIDE.md` (baris 14–17)
- **Kondisi Riil:**
  - `requirements.txt` mengunci:
    ```text
    --index-url https://download.pytorch.org/whl/cpu
    torch==2.15.0+cpu
    ```
    disertai komentar lokal mesin: `# Venv di D:\nirava-venv, Python 3.12.10, Windows`.
  - Instalasi via pip langsung gagal fatal: `ERROR: No matching distribution found for torch==2.15.0+cpu`.
  - Sebaliknya, `docs/DATA_PIPELINE_GUIDE.md` menulis `torch>=2.0.0`.
- **Akar Masalah:** Versi PyTorch 2.15.0 tidak ada. PyTorch melompat dari versi 2.5 ke 2.6 (atau penulisan bermaksud 2.1.0/2.5.0).
- **Rekomendasi Pemilik (A1 & Tim):** Perbaiki `requirements.txt` menjadi format portabel:
  ```text
  torch>=2.0.0
  matplotlib>=3.8.0
  ```
  serta hapus path hardcoded `D:\nirava-venv`.

---

### Temuan 5: Residu Konfigurasi Proyek Audio Speech pada `.env.example`
- **Lokasi Berkas:**
  - `.env.example` (baris 3–5)
- **Kondisi Riil:**
  ```text
  AUDIO_STORAGE_DIR=./data/audio
  MAX_UPLOAD_MB=25
  MAX_AUDIO_SECONDS=120
  ```
- **Akar Masalah:** Sisa template proyek *AI Voice Cleaner* lama. Pada produk aktif Nirava MIDI, tidak ada unggahan file audio WAV/MP3, tidak ada batasan detik audio, dan berkas yang dikelola murni file `.mid`.
- **Rekomendasi Pemilik (A1):** Sesuaikan `.env.example` menjadi variabel relevan untuk domain MIDI:
  ```text
  MIDI_STORAGE_DIR=./runtime/generated
  MAX_GENERATION_BARS=16
  DEFAULT_TEMPO_BPM=120
  ```

---

### Temuan 6: Klaim Berlebihan & Ketidakakuratan Istilah pada `reports/EXPERIMENT_REPORT.md`
- **Lokasi Berkas:**
  - `reports/EXPERIMENT_REPORT.md` (baris 40, 43, 47)
- **Kondisi Riil:**
  1. *Penggunaan Istilah Kontradiktif:* Baris 43 menyebut model memberikan representasi lebih kaya untuk *"interval pitch polifonik/melodik folk"*. Nirava secara fundamental adalah model monofonik (satu nada aktif per step). Penggunaan kata "polifonik" tidak tepat secara teori.
  2. *Klaim Hyperparameter Optimal:* Baris 40 menyatakan LR $1\times 10^{-3}$ *"merupakan titik kerja yang optimal"*. Faktanya, tim hanya menguji 2 nilai LR (1e-3 dan 3e-4) pada 1 seed acak tanpa grid/random search komprehensif.
  3. *Klaim Estetika Musik:* Baris 47 menyebut temperature 1.0 menghasilkan *"keseimbangan ideal"*. Klaim ini subjektif dan belum divalidasi oleh panel uji dengar manusia (*listening test*).
  4. *Ketiadaan Run R4:* Di tabel laporan dan di skrip `src/run_experiments.py`, urutan langsung melompat dari R3 ke R5. Eksperimen R4 (yang semula direncanakan untuk regularisasi dropout atau kapasitas 256) tidak dieksekusi di kode.
- **Rekomendasi Pemilik (A3):**
  - Ganti frasa "interval pitch polifonik" menjadi "kontur melodi dan transisi interval pitch".
  - Lunakkan klaim "optimal" menjadi "menunjukkan konvergensi yang lebih baik dibandingkan baseline konservatif pada parameter yang diuji".
  - Beri catatan kaki bahwa R4 ditiadakan karena keterbatasan waktu dan difokuskan langsung ke sampling sweep R5.

---

### Temuan 7: Kesenjangan Tata Kelola Akademik (Governance Gap)
- **Lokasi Berkas:**
  - `docs/STAGE1_VALIDATION.md` (baris 3)
  - `docs/LECTURER_APPROVAL.md` (seluruh baris)
- **Kondisi Riil:**
  - Status resmi repositori pada `docs/STAGE1_VALIDATION.md` masih mencatat: `Verdict: PIVOT MIDI / GO tertunda`.
  - Seluruh kotak persetujuan dosen pada `docs/LECTURER_APPROVAL.md` masih bertanda `[ ]` (belum dicentang).
  - Namun di repositori, pipeline data (Member 2) dan model/training (Member 3) sudah selesai diimplementasikan beserta laporan eksperimen.
- **Akar Masalah:** Pekerjaan teknis mendahului otorisasi administratif akibat tenggat tugas yang mendesak.
- **Rekomendasi Pemilik (A1 & Seluruh Tim):** Sampaikan secara transparan kepada dosen pengampu saat evaluasi bahwa implementasi offline dilakukan sebagai pembuktian kelayakan (*feasibility study*), dan mintakan validasi retroaktif untuk membuka gate secara sah. Jangan mengisi checklist seolah-olah sudah disetujui sebelumnya.

---

### Temuan 8: Ketiadaan Hash & Bukti Ukuran File Model Runtime
- **Lokasi Berkas:**
  - `.gitignore` (baris `runtime/`, `*.pt`)
  - `src/run_experiments.py` (baris 480–484)
- **Kondisi Riil:**
  - File model biner `runtime/nirava_midi_lstm_v1_export.pt` dan file MIDI hasil sampling `reports/nirava_sample_temp_*.mid` tidak dapat di-commit ke Git karena aturan `.gitignore`.
  - Hal ini menyebabkan penguji yang meng-clone repo tidak dapat langsung memverifikasi bobot model tanpa melatih ulang.
- **Rekomendasi Pemilik (A3 & A4):** Tambahkan lampiran metadata verifikasi aman pada laporan:
  - Ukuran file bobot bersih (dalam KB/MB).
  - Hash SHA-256 dari `nirava_midi_lstm_v1_export.pt`.
  - Perintah satu baris untuk meregenerasi file model dari cache token.

---

### Temuan 9: Residu Istilah Domain Audio Mentah pada Dokumen Spesifikasi
- **Lokasi Berkas:**
  - `docs/API_SPEC.md` (baris 17)
  - `docs/ARCHITECTURE.md` (baris 19, 21)
- **Kondisi Riil:**
  - `docs/API_SPEC.md` masih memuat kalimat: *"tidak memakai angka ukuran WAV lama"*.
  - `docs/ARCHITECTURE.md` memuat: *"storage WAV tidak lagi digunakan"*, *"Audio/sample rate validation lama diganti JSON bounds"*.
- **Akar Masalah:** Pola penyusunan dokumen transisi yang menjelaskan apa yang dibatalkan dibandingkan apa yang berlaku.
- **Rekomendasi Pemilik (A1):** Pada pembaruan API v1 berikutnya, hapus kalimat yang merujuk pada masa lalu speech dan formulasikan batasan murni dari perspektif MIDI simbolik (misal: batasan ukuran file JSON $\le 64\text{ KB}$, batas sequence $\le 256\text{ steps}$, validasi header SMF Type 0).

---

### Temuan 10: Ketidaksinkronan Penamaan Folder dan Riwayat Repositori
- **Lokasi Berkas:**
  - Path lokal pada log: `C:\Users\...\-Proyek1-AI-Voice-Cleaner-`
  - URL remote upstream: `https://github.com/AI-IF-TelU/-Proyek1-Music-Generator-.git`
  - Rekap arahan: `report/REKAP_ARAHAN_DEV_1-4.md` (Bagian 7.2)
- **Kondisi Riil:**
  - Repositori lokal pada komputer anggota diinisialisasi saat proyek masih bernama *AI Voice Cleaner*.
  - Repositori GitHub kemudian dipindahkan / di-rename menjadi `-Proyek1-Music-Generator-`.
- **Rekomendasi Pemilik (Tim):** Tidak perlu mengubah path atau URL commit lama untuk menjaga integritas Git hash, cukup catat sebagai riwayat evolusi penamaan repositori.

