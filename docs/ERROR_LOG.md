# Log Penanganan Error Nyata (Real Error Log)

Dokumen ini mencatat seluruh insiden teknis, pesan error asli, akar masalah (*root cause*), perbaikan, dan bukti verifikasi riil yang terjadi selama siklus hidup pengembangan proyek Nirava MIDI Music Generator.

> **Prinsip Kejujuran Rubrik:**
> - Seluruh entri di bawah diambil langsung dari catatan riil anggota (riwayat Member 1, Member 2, Member 3, log interaksi, dan rekapan).
> - Tidak ada error fiktif yang dibuat untuk memenuhi format.
> - Setiap detail yang tidak tercatat di sumber asli ditandai secara jujur sebagai *"tidak tercatat di sumber"*.

---

### Error 01 — 2026-10-28 — A2 (Muhammad Izza Haikal)
- **Perintah/langkah:** Menjalankan audit awal terhadap folder Nottingham `MIDI/melody` (1.034 file MIDI) menggunakan parser MIDI internal di `src/nirava_midi_tokenizer.py`.
- **Environment:** Windows PowerShell, Python 3.12 (lingkungan lokal A2).
- **Pesan error asli:** Tidak ada crash fatal, namun hasil log audit melaporkan seluruh 533 file dengan meter 4/4 ditolak:
  > *"Semua file ditolak karena pitch bend"*
- **Expected vs actual:**
  - *Expected:* Ratusan melodi 4/4 Nottingham berstatus usable karena merupakan melodi folk sederhana tanpa modulasi pitch bend dinamis.
  - *Actual:* 0 dari 533 file 4/4 diterima; semua ditandai mengandung event pitch-bend ilegal.
- **Hipotesis penyebab:** Event MIDI status byte `0xE0 0x00 0x40` (pitch-bend value 8192 = posisi tengah netral/tanpa deviasi) disisipkan secara standar pada tick 0 oleh konverter ABC-ke-MIDI Nottingham. Parser memeriksa keberadaan event pitch-bend secara biner tanpa mengecek apakah nilainya netral (8192). Hal serupa terjadi pada pedal sustain CC64 dengan value < 64 (kondisi off).
- **Prompt perbaikan ke LLM:**
  > "Semua file ditolak karena pitch bend, padahal ini neutral bend. Perlu perbaiki filter agar bend value 8192 dan pedal CC64 off diterima."
- **Solusi dipilih + alasan:** Modifikasi fungsi `_parse_smf()` pada `src/nirava_midi_tokenizer.py`. Nilai pitch-bend diizinkan jika `value == 8192`, dan pedal damper/sustain CC64 diizinkan jika `value < 64`. Ditambahkan 3 unit tests untuk memverifikasi penolakan bend aktif dan penerimaan bend netral.
- **Bukti sudah beres:** Audit tokenizer ulang berhasil meng-encode 519 dari 533 file (14 sisanya ditolak murni karena nada bertumpuk/overlap pada grid 16 step/bar). Seluruh 519 file lolos uji round-trip 100%.
- **Commit terkait / reviewer:** Commit `216aed4` / Reviewer: A1 & A3.
- **Sumber bukti:** `docs/LLM_INTERACTION_LOG.md` baris 187–196; `docs/llm_chat_export_member2.md` baris 412.

---

### Error 02 — 2026-10-29 — A2 (Muhammad Izza Haikal)
- **Perintah/langkah:** Evaluasi rekonsiliasi data antara `reports/dataset_usable.csv` (515 file), `reports/tokenizer_audit.csv` (519 file), dan `reports/split_manifest.csv` (517 file).
- **Environment:** Windows PowerShell, Python 3.12.
- **Pesan error asli:** Tidak berupa exception runtime, melainkan ketidaksesuaian hitungan kuantitatif data (*dataset count reconciliation disparity*):
  > *"Terdapat disparitas angka usable MIDI antara laporan audit awal (515 file) dengan manifest split (517 file) dan audit tokenizer (519 file ter-encode)."*
- **Expected vs actual:**
  - *Expected:* Satu angka otoritatif tunggal yang seragam di seluruh laporan pra-pemrosesan data.
  - *Actual:* Angka usable 515, hasil tokenizer 519, dan hasil split 517.
- **Hipotesis penyebab:**
  1. Skrip audit lama (`audit_dataset.py`) memeriksa overlap nada dalam detik/tick kontinu, sehingga file `reelsh-l66.mid` dan `xmas4.mid` ditolak akibat rounding slop 1-tick (~1 ms) dari konverter ABC Nottingham.
  2. Pada grid kuantisasi 16 step/bar, selisih 1-tick tersebut jatuh pada slot waktu yang sama tanpa tumpang tindih nada, sehingga 519 file sah ter-encode.
  3. Dari 519 file, ditemukan 2 pasang duplikat kanonikal token yang identik persis (`ashover22.mid` identik dengan `ashover20.mid`; `morris91.mid` identik dengan `morris90.mid`). Penghapusan 2 duplikat menghasilkan 517 karya unik.
- **Prompt perbaikan ke LLM:**
  > "Reconcile the dataset counts (515 versus 517 usable MIDI files). Explain which files account for the difference and identify the authoritative final manifest."
- **Solusi dipilih + alasan:** Menetapkan bahwa `reports/split_manifest.csv` (517 karya unik) adalah manifest resmi final, `reports/tokenizer_audit.csv` (519) adalah audit tokenizer, dan 515 adalah artefak pra-kuantisasi historis. Menulis dokumen rekonsiliasi lengkap di `reports/DATASET_AUDIT_REPORT.md`.
- **Bukti sudah beres:** Dihasilkan `reports/split_summary.txt` yang memvalidasi pembagian 517 karya ke dalam 414 train (1.808 window), 52 val (220 window), dan 51 test (220 window) dengan 0 leakage pada level karya.
- **Commit terkait / reviewer:** Commit `4c48d2f` / Reviewer: A1 & A3.
- **Sumber bukti:** `docs/LLM_INTERACTION_LOG.md` baris 323–340; `docs/llm_chat_export_member2.md` baris 1312 & 2066–2072.

---

### Error 03 — 2026-10-29 — A3 (Taura Muhammad Sanubari)
- **Perintah/langkah:** Menjalankan eksperimen training model LSTM melalui skrip runner `python src/run_experiments.py`.
- **Environment:** Windows PowerShell, Python 3.12, PyTorch 2.15.0+cpu.
- **Pesan error asli:** Tidak ada crash, namun terdeteksi kejanggalan metrik (*silent synthetic fallback*):
  > *"Terdeteksi bahwa ensure_tokens_exist() diam-diam memanggil data sintetis fixture karena file processed/tokens_v1.jsonl riil belum ada di workspace... Training menghasilkan metrik anomali (NLL R1 > R0 namun diklaim mengungguli)."*
- **Expected vs actual:**
  - *Expected:* Pelatihan berjalan pada dataset Nottingham riil (517 karya, ~231.000 token).
  - *Actual:* Model berlatih pada fixture 12 sequence sintetis mainan (1.480 token) yang digenerate otomatis tanpa peringatan.
- **Hipotesis penyebab:** Fungsi `ensure_tokens_exist()` diimplementasikan dengan logika toleran yang membuat data dummy sintetis jika token riil belum dibuat di folder `processed/`. Hal ini mengaburkan validitas ilmiah evaluasi.
- **Prompt perbaikan ke LLM:**
  > "# TASK 03C — Critical Audit, Real Nottingham Training & Report Correction
  > 1. Audit src/run_experiments.py dan pastikan tidak pernah secara diam-diam menghasilkan/menggunakan data sintetis ketika token riil hilang.
  > 2. Pisahkan smoke test sintetis dari eksperimen riil.
  > 3. Bangun ulang dataset token Nottingham riil menggunakan pipeline Member 2.
  > 4. Latih ulang model dari inisialisasi acak dan perbaiki seluruh metrik evaluasi ilmiah."
- **Solusi dipilih + alasan:** Menghapus fallback sintetis otomatis dari `src/run_experiments.py`. Wajibkan parameter eksplisit `--synthetic-smoke-test` jika ingin menguji pipeline secara cepat, dan hentikan proses dengan pesan error jelas jika file token riil tidak ditemukan.
- **Bukti sudah beres:** Pelatihan ulang dari nol menggunakan dataset Nottingham riil (414 train, 52 val, 51 test) berhasil menghasilkan kurva validasi Cross-Entropy Loss yang sah (R1 Val NLL 1.1955 vs R0 Baseline Unigram 1.5182).
- **Commit terkait / reviewer:** Commit `7c1a259` / Reviewer: A1, A2, A4.
- **Sumber bukti:** `docs/LLM_INTERACTION_LOG.md` baris 486–495; `docs/llm_chat_export_member3.md` baris 119–150.

---

### Error 04 — 2026-10-29 — A3 (Taura Muhammad Sanubari)
- **Perintah/langkah:** Menjalankan sweep sampling generasi melodi pada Run R5 (temperature sampling).
- **Environment:** Windows PowerShell, Python 3.12, `src/nirava_midi_generate.py`.
- **Pesan error asli:**
  ```text
  ValueError: sequence harus [BOS, steps..., EOS]
  ```
- **Expected vs actual:**
  - *Expected:* Generator menghasilkan rangkaian token terstruktur sepanjang kelipatan birama (misal 64, 128 langkah) yang diawali token BOS dan diakhiri token EOS.
  - *Actual:* Generator menghasilkan sequence yang terpotong sangat pendek (hanya beberapa token) karena model memilih token EOS di langkah ke-2 atau ke-3, memicu ValueError saat diekspor.
- **Hipotesis penyebab:** Logits probabilitas untuk token `EOS` (ID 2) tidak dibatasi pada langkah-langkah awal generasi autoregresif, sehingga pada sampling bertemperatur tinggi model dapat memilih EOS sebelum mencapai panjang birama minimal.
- **Prompt perbaikan ke LLM:**
  > "Error: ValueError: sequence harus [BOS, steps..., EOS] saat sampling R5. Evaluasi masking EOS dan pastikan panjang minimum bar terpenuhi."
- **Solusi dipilih + alasan:** Memperbarui fungsi `apply_grammar_mask()` pada `src/nirava_midi_generate.py`. Parameter `allow_eos` disetel ke `False` (nilai logits EOS di-masking ke `-inf`) selama sequence belum mencapai panjang minimal 1 birama (16 langkah). Setelah birama pertama terlampaui, EOS diizinkan secara bertahap atau ditutup pada `max_bars` menggunakan REST padding kelipatan 16 langkah.
- **Bukti sudah beres:** Pengujian sampling pada 10 random seed berbeda dengan variasi temperatur (0.8, 1.0, 1.2) berhasil mengekspor melodi MIDI 8 birama utuh (128 langkah) tanpa hanging notes atau crash ekspor.
- **Commit terkait / reviewer:** Commit `7c1a259` / Reviewer: A1 & A4.
- **Sumber bukti:** `docs/LLM_INTERACTION_LOG.md` baris 505–512; `docs/llm_chat_export_member3.md` baris 164–175.

---

### Error 05 — 2026-10-29 — A2 (Muhammad Izza Haikal)
- **Perintah/langkah:** Percobaan autentikasi ke GitHub menggunakan tool GitHub CLI: `gh auth login`.
- **Environment:** Windows PowerShell pada mesin lokal A2 (`C:\Users\Haikal\Downloads\-Proyek1-AI-Voice-Cleaner-`).
- **Pesan error asli:**
  ```text
  gh: The term 'gh' is not recognized as a name of a cmdlet, function, script file, or executable program.
  ```
- **Expected vs actual:**
  - *Expected:* CLI membuka alur login peramban (*web-based OAuth*).
  - *Actual:* Perintah tidak ditemukan karena binary `gh` belum terpasang atau belum masuk ke environment variable `PATH`.
- **Hipotesis penyebab:** GitHub CLI belum selesai diinstal melalui paket MSI atau sesi terminal PowerShell belum di-restart setelah instalasi.
- **Prompt perbaikan ke LLM:**
  Pengguna menempelkan pesan error PowerShell tersebut langsung ke LLM.
- **Solusi dipilih + alasan:** Mengarahkan A2 untuk memanggil path eksekusi absolut `& "C:\Program Files\GitHub CLI\gh.exe" auth login` atau alternatif autentikasi Git via HTTPS Personal Access Token (PAT) menggunakan git credential helper bawaan.
- **Bukti sudah beres:** Sesi Git terautentikasi dan branch `dev/member-2-data` berhasil di-push ke remote repository.
- **Commit terkait / reviewer:** Commit `216aed4` / Reviewer: A1.
- **Sumber bukti:** `docs/llm_chat_export_member2.md` baris 1106–1110; `report/REKAP_ARAHAN_DEV_1-4.md` baris 431–434.

---

### Error 06 — 2026-10-23 / 2026-10-28 — A1 (Muhammad Fajri)
- **Perintah/langkah:** Operasi penulisan Git refs dan pembacaan panduan tugas dosen berformat DOCX pada awal repositori.
- **Environment:** Windows PowerShell / Python.
- **Pesan error asli:**
  1. Hambatan Git refs:
     ```text
     error: cannot open '.git/FETCH_HEAD': Permission denied; Failed to connect to github.com port 443
     ```
  2. Hambatan pembacaan DOCX:
     ```text
     [Errno 13] Permission denied: '.../Panduan Proyek 1 - Vibe Coding.docx'
     ```
- **Expected vs actual:**
  - *Expected:* Git fetch/branch switch berjalan mulus dan dokumen DOCX dapat dibaca untuk diekstrak teks rubriknya.
  - *Actual:* Operasi terblokir izin akses file (file sedang dikunci oleh aplikasi Word/proses lain).
- **Hipotesis penyebab:**
  - Untuk Git: batasan koneksi jaringan dan hak akses file refs lokal.
  - Untuk DOCX: Microsoft Word mengunci berkas secara eksklusif saat berkas sedang dibuka di Windows.
- **Prompt perbaikan ke LLM:**
  Tidak tercatat prompt spesifik di sumber; dilaporkan sebagai hambatan lingkungan (*tooling obstacle*).
- **Solusi dipilih + alasan:**
  - Untuk Git: menggunakan mode pemanggilan alat yang memiliki hak otorisasi yang sesuai tanpa mengubah histori.
  - Untuk DOCX: membaca file secara read-only menggunakan mode `FileShare.ReadWrite` (tanpa memaksa menutup aplikasi Word pengguna).
- **Bukti sudah beres:** Isi rubrik DOCX berhasil dibaca untuk menyusun `docs/BLUEPRINT_AUDIT.md` dan branch arsitektur berhasil dibuat.
- **Commit terkait / reviewer:** Commit `f852946` & `03732fb` / Reviewer: Tim.
- **Sumber bukti:** `docs/LLM_INTERACTION_LOG.md` baris 109; `docs/llm_chat_export_member1.md` baris 210.

---

### Error 07 — 2026-11-07 — A4 (Muhammad Alif Italiano Syaiza)
- **Perintah/langkah:** Percobaan clone awal repositori dari upstream `https://github.com/AI-IF-TelU/-Proyek1-Music-Generator-.git` di terminal sandbox.
- **Environment:** Windows PowerShell, Terminal Sandbox Antigravity.
- **Pesan error asli:**
  ```text
  Cloning into '.'...
  fatal: unable to access 'https://github.com/AI-IF-TelU/-Proyek1-Music-Generator-.git/': getaddrinfo() thread failed to start
  ```
- **Expected vs actual:**
  - *Expected:* Repositori ter-clone ke direktori kerja `Tubes`.
  - *Actual:* Gagal resolusi DNS/akses jaringan karena sandbox default mengisolasi akses jaringan luar.
- **Hipotesis penyebab:** Sesuai aturan terminal, Standard Sandbox Mode tidak memiliki akses jaringan keluar.
- **Prompt perbaikan ke LLM:**
  Evaluasi aturan terminal: jalankan perintah clone dengan otorisasi akses jaringan (`BypassSandbox: true`).
- **Solusi dipilih + alasan:** Mengeksekusi perintah git clone dengan bypass sandbox tunggal untuk operasi fetch network, lalu kembali ke mode sandbox standar untuk seluruh pemrosesan berkas lokal berikutnya.
- **Bukti sudah beres:** Repositori berhasil di-clone lengkap (commit `5bb7b80`) dan branch `dev/member-4-documentation` berhasil di-checkout.
- **Commit terkait / reviewer:** Persiapan commit A4 / Reviewer: Pengguna (Alif).
- **Sumber bukti:** Transkrip eksekusi Fase 0 A4.

