# Daftar Isu Terbuka & Rencana Tindak Lanjut (Open Issues by A4)

**Penyusun:** Muhammad Alif Italiano Syaiza (Anggota 4 / Lead Documentarian & Error Handler)  
**Tanggal:** 7 November 2026  
**Prinsip Dokumentasi:** Sesuai aturan kerja [AGENTS.md](../AGENTS.md), hal-hal yang belum memiliki bukti empiris atau belum diselesaikan dicatat secara transparan dan jujur sebagai isu terbuka (*open issues*), tanpa mengarang hasil atau approval fiktif.

---

## 1. Matriks Isu Terbuka

| ID Isu | Kategori | Deskripsi Kesenjangan Bukti | Pemilik Tindakan | Tindakan Berikutnya |
|---|---|---|---|---|
| **ISSUE-01** | Identitas & Git | Variasi nama author Git A1 (`Muh Fajri` vs `Muhammad Fajri`) dan akun `haikal56` (A2) serta `tmuhammadsanubari-cell` (A3) belum dikonfirmasi resmi oleh masing-masing pemilik. | A1, A2, A3 | Menunggu balasan anggota atas draf pesan di `docs/A4_PESAN_KE_ANGGOTA.md`. |
| **ISSUE-02** | Akuntabilitas AI | Bukti interaksi AI pada `llm_chat_export_member1` s.d. `member3` berupa rekonstruksi terkurasi, belum menyertakan share link aktif platform atau ekspor mentah (JSON/HTML). | A1, A2, A3, A4 | Anggota melampirkan share link percakapan LLM asli dari ChatGPT/Claude/Codex/Gemini. |
| **ISSUE-03** | Tata Kelola Akademik | Dokumen `docs/STAGE1_VALIDATION.md` masih mencatat "GO tertunda" dan checklist `docs/LECTURER_APPROVAL.md` kosong, padahal implementasi teknis telah selesai. | A1 & Seluruh Tim | Mengajukan review retroaktif dan konfirmasi kelayakan kepada dosen pengampu saat evaluasi. |
| **ISSUE-04** | Metodologi Evaluasi | Test set held-out (51 karya unik Nottingham, 29.222 token) masih berstatus *frozen* dan belum pernah dievaluasi untuk metrik NLL/Perplexity akhir. | A3 (Training) | Menjalankan satu kali evaluasi (*one-shot test evaluation*) pada model freeze R1 setelah model resmi disetujui. |
| **ISSUE-05** | Persepsi Musik | Belum dilakukan uji dengar subjektif (*blind listening test*) dengan panel manusia untuk memvalidasi klaim estetika melodi pada variasi temperature 0.8, 1.0, 1.2. | Seluruh Tim | Melakukan survei uji dengar sederhana (skala 1–5 untuk koherensi, ritme, variasi) kepada 3–5 responden. |
| **ISSUE-06** | Artefak Runtime | File checkpoint model bersih `runtime/nirava_midi_lstm_v1_export.pt` dan contoh berkas `.mid` tidak di-commit ke repositori Git demi mematuhi batas ukuran file. | A3 & A4 | Menyiapkan lampiran hash SHA-256 dan instruksi regenerasi mandiri melalui skrip runner. |
| **ISSUE-07** | Dependensi & Konfigurasi | `requirements.txt` mengunci versi `torch==2.15.0+cpu` (non-eksisten) dan `.env.example` masih membawa variabel konfigurasi speech audio upload lama. | A1 (Ketua) | Memperbarui `requirements.txt` menjadi `torch>=2.0.0` dan membersihkan `.env.example` dari residu audio upload. |

---

## 2. Rincian Isu & Dampak Akademik

### ISSUE-01: Konfirmasi Akun Git Anggota Tim
- **Dampak:** Penilaian kontribusi individu (rubrik 20% kerja tim) mensyaratkan commit dapat diatribusikan dengan jelas ke nama dan NIM mahasiswa yang bersangkutan.
- **Langkah Mitigasi A4:** A4 telah memetakan commit yang terlihat di `docs/CONTRIBUTION_MATRIX.md` dan menyiapkan pesan konfirmasi pada `docs/A4_PESAN_KE_ANGGOTA.md`.

### ISSUE-02: Bukti Interaksi AI Primer (Vibe Coding Log)
- **Dampak:** Bobot 25% penilaian bergantung pada bukti interaksi LLM. File Markdown terkurasi yang ada di repository dapat dianggap oleh penguji sebagai ringkasan retrospektif, bukan bukti dialog langsung.
- **Langkah Mitigasi A4:** A4 mengimbau seluruh anggota untuk menyimpan riwayat chat dalam bentuk link publik (misal *ChatGPT Shared Link* atau ekspor percakapan Claude/Gemini) untuk diserahkan sebagai lampiran pendukung.

### ISSUE-03: Kesenjangan Gate Stage 1
- **Dampak:** Adanya diskrepansi antara dokumen tata kelola (Stage 1 belum GO) dan implementasi riil (Stage 2 sudah selesai) dapat memicu pertanyaan dosen mengenai kepatuhan alur kerja.
- **Langkah Mitigasi A4:** Menyampaikan secara terbuka kepada dosen bahwa implementasi dijalankan sebagai eksperimen kelayakan (*proof of concept*) mendesak sebelum batas waktu pengumpulan, dan tim siap menerima arahan penyesuaian.

### ISSUE-04: Pengujian Test Set Akhir
- **Dampak:** Metrik ilmiah yang dilaporkan saat ini (Val NLL 1.1955, Val PPL 3.31) berasal dari set validasi. Belum ada angka final pada set data uji (*held-out test set*).
- **Langkah Mitigasi A4:** Memastikan tim tidak melakukan *data peeking* atau men-tuning hyperparameter pada data uji, dan hanya menjalankan evaluasi test set pada saat demonstrasi final.

### ISSUE-05: Validasi Kualitas Musik Generatif
- **Dampak:** Keberhasilan menurunkan nilai NLL secara matematis belum membuktikan bahwa melodi yang dihasilkan enak didengar atau memiliki pola musikal yang logis bagi telinga manusia.
- **Langkah Mitigasi A4:** Menyiapkan file audio/MIDI hasil generasi untuk diperdengarkan secara langsung pada saat presentasi.

