# Matriks Kontribusi Tim Nirava MIDI

Dokumen ini memetakan identitas anggota tim, peran akademik, pemetaan akun Git yang teramati pada riwayat repositori, serta daftar kontribusi commit.

> **Catatan Verifikasi Identitas:**
> - Nama dan NIM empat anggota di bawah diperoleh dari data tugas per 7 November 2026.
> - Dev 1 memiliki dua variasi nama author Git (`Muh Fajri` dan `Muhammad Fajri`); status: **perlu konfirmasi apakah berasal dari akun/orang yang sama**.
> - Pemetaan akun Git `haikal56` ke A2 dan `tmuhammadsanubari-cell` ke A3 dibuat berdasarkan label pesan commit `feat(member-2)` dan `feat(member-3)` serta isi dokumen riwayat, **belum dikonfirmasi langsung oleh masing-masing anggota**.
> - Commit `264f783` (laporan awal, slide PPTX, riwayat Member 1) dan `5bb7b80` (rekap chat arahan) berada di bawah author `Muh Fajri` dan disusun dengan asistensi AI; kedua commit tersebut **bukan kontribusi A4**.
> - Seluruh email pribadi dan data sensitif diredaksi dengan `[DIREDAKSI]`.

---

## 1. Tabel Identitas dan Peran Anggota

| Peran | Nama Anggota | NIM | Akun Git Teramati | Branch Terkait | Status Konfirmasi |
|---|---|---|---|---|---|
| **A1 — Prompt Engineer & LLM Navigator / Ketua** | Muhammad Fajri | 10301230062 | `Muh Fajri` / `Muhammad Fajri` | `dev/member-1-architecture`, `main` | Terkonfirmasi nama/NIM; variasi 2 author Git menunggu konfirmasi anggota |
| **A2 — Data Pipeline & Preprocessing Engineer** | Muhammad Izza Haikal | 103012300092 | `haikal56` | `dev/member-2-data` | Terkonfirmasi nama/NIM; pemetaan akun Git menunggu konfirmasi anggota |
| **A3 — Training Loop & Hyperparameter Tuning Engineer** | Taura Muhammad Sanubari | 103012330280 | `tmuhammadsanubari-cell` | `dev/member-3-training` | Terkonfirmasi nama/NIM; pemetaan akun Git menunggu konfirmasi anggota |
| **A4 — Lead Documentarian & Error Handler** | Muhammad Alif Italiano Syaiza | 103012400321 | `alifitaliano` | `dev/member-4-documentation` | Terkonfirmasi (aktif pada tugas dokumentasi A4) |

---

## 2. Rincian Riwayat Commit per Anggota

*Catatan: Jumlah commit bukan ukuran kualitas atau persentase kontribusi.*

### A1 — Muhammad Fajri (`Muh Fajri` / `Muhammad Fajri`)
- `c90b04b` (2026-10-11) — *Initial commit* (author: `Muhammad Fajri`)
- `f852946` (2026-10-23) — *docs: audit and refine Stage 1 project blueprint*
- `56ceba3` (2026-10-23) — *update satge1*
- `f5f54d7` (2026-10-23) — *docs: re-audit blueprint lifecycle and validation gaps*
- `03732fb` (2026-10-28) — *docs: finalize Nirava Stage 1 ML architecture and team contracts*
- `02ff463` (2026-10-28) — *docs: separate Nirava ML architecture and member contracts*
- `3856a8e` (2026-10-28) — *docs: trim trailing blank line in data contract*
- `d1259a2` (2026-10-28) — *docs: pivot Nirava to from-scratch MIDI LSTM generation*
- `758fbb3` (2026-10-28) — *docs: restructure Nirava README for academic project review*
- `9c64cbb` (2026-10-28) — *docs: select Nottingham melody dataset and update audit requirements*
- `264f783` (2026-11-06) — *docs: add Nirava project report, presentation, and member 1 history* (disusun dengan asistensi AI; bukan kontribusi A4)
- `5bb7b80` (2026-11-07) — *docs: consolidate chat directions for dev 1 through dev 4* (disusun dengan asistensi AI; bukan kontribusi A4)
- **File utama yang dihasilkan**: Dokumen arsitektur awal (`docs/ML_ARCHITECTURE.md`, `docs/DATA_CONTRACT.md`, `docs/TRAINING_CONTRACT.md`, `README.md`, draft `report/README.md`, draft `report/Nirava-Presentasi.pptx`, draft `report/REKAP_ARAHAN_DEV_1-4.md`).
- **Reviewer tercatat**: Review lintas peran A2/A3/A4.
- **Pemahaman anggota**: Menunggu penjelasan anggota (A1).

### A2 — Muhammad Izza Haikal (`haikal56`)
- `216aed4` (2026-10-28) — *feat(member-2): complete data pipeline — tokenizer, split, loader, augmentation*
- `4c48d2f` (2026-10-29) — *docs(member-2): TASK 02B reconcile dataset counts, verify leakage, and add execution guide*
- `4730635` (2026-10-29) — *docs(member-2): update LLM chat export with full conversation up to TASK 02B*
- **File utama yang dihasilkan**: `src/nirava_midi_tokenizer.py`, `src/build_splits.py`, `src/nirava_midi_data.py`, `src/nirava_midi_grouping.py`, `src/augment_transpose.py`, `src/run_tokenizer_audit.py`, `tests/test_nirava_midi_tokenizer.py`, `tests/test_nirava_midi_data.py`, `reports/DATASET_AUDIT_REPORT.md`, `reports/split_summary.txt`, `reports/tokenizer_audit_summary.txt`, `docs/DATA_PIPELINE_GUIDE.md`, `docs/llm_chat_export_member2.md`.
- **Reviewer tercatat**: Review lintas peran A1/A3.
- **Pemahaman anggota**: Menunggu penjelasan anggota (A2).

### A3 — Taura Muhammad Sanubari (`tmuhammadsanubari-cell`)
- `2f67f17` (2026-10-29) — *feat(member-3): complete LSTM from-scratch training engine, checkpointing, sampling, and ablation study*
- `7c1a259` (2026-10-29) — *feat(member-3): TASK 03C audit synthetic fallback, real Nottingham training, EOS mask fix, and report correction*
- **File utama yang dihasilkan**: `src/nirava_midi_lstm.py`, `src/nirava_midi_train.py`, `src/nirava_midi_checkpoint.py`, `src/nirava_midi_generate.py`, `src/run_experiments.py`, `src/plot_training_curves.py`, `tests/test_nirava_midi_model.py`, `tests/test_nirava_midi_train.py`, `tests/test_nirava_midi_checkpoint.py`, `tests/test_nirava_midi_generate.py`, `reports/EXPERIMENT_REPORT.md`, `reports/experiment_results.csv`, `reports/training_curves.png`, `docs/llm_chat_export_member3.md`.
- **Reviewer tercatat**: Review lintas peran A1/A2/A4.
- **Pemahaman anggota**: Menunggu penjelasan anggota (A3).

### A4 — Muhammad Alif Italiano Syaiza (`alifitaliano`)
- *Commit dalam persiapan pada branch `dev/member-4-documentation`* (menunggu konfirmasi pengguna pada akhir Fase 7).
- **File utama yang dihasilkan**: `docs/CONTRIBUTION_MATRIX.md`, `docs/CHAT_EVIDENCE_INVENTORY.md`, `docs/A4_PESAN_KE_ANGGOTA.md`, `docs/ERROR_LOG.md`, `docs/DECISION_TIMELINE.md`, `docs/REPRODUCIBILITY_REVIEW.md`, `docs/REVIEW_FINDINGS_A4.md`, `docs/REPORT_REVIEW_A4.md`, `docs/PRESENTATION_NOTES.md`, `docs/OPEN_ISSUES_A4.md`, `docs/llm_chat_export_member4.md`, update `docs/LLM_INTERACTION_LOG.md`.
- **Reviewer tercatat**: Seluruh anggota tim (A1, A2, A3) dan asisten dosen.
- **Pemahaman anggota**: Aktif diverifikasi melalui task ini.

