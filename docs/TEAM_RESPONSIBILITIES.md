# Team Responsibilities Nirava MIDI

Empat job desk mengikuti panduan dosen; identitas/NIM belum diberikan. Semua anggota wajib memahami kontribusi dan menyimpan log sesi sendiri, A4 mengompilasi.

| Anggota/peran | Tanggung jawab | Handoff/bukti |
|---|---|---|
| A1 Prompt Engineer & LLM Navigator/ketua | Scope/strategi prompt, keputusan token/LSTM/gates/shape, review API-model | ML_ARCHITECTURE/MIDI_TOKENIZATION, alasan alternatif, review A2/A3, konsultasi dosen |
| A2 Data Pipeline & Preprocessing Engineer | Lisensi MIDI/work grouping, parsing/filter/grid/tokenizer/window/split | Audit/manifest/hash, canonical round-trip, vocabulary/fixtures dan DATA_CONTRACT untuk A3 |
| A3 Training Loop & Hyperparameter Tuning Engineer | LSTM/CE loop/checkpoint/sweep, metrik/profiling/sampling | Config/run/source/checkpoint hash, kurva aktual/failure log, model freeze untuk integrasi |
| A4 Lead Documentarian & Error Handler | Ekspor LLM, kronologi prompt/error/analisis, reproducibility review dan laporan | Chat asli, log kerja/commit/reviewer, isu tersisa dan materi presentasi4anggota |

A2 tidak mewarisi tugas paired speech/noise; A3 tidak membangun GAN; A4 tidak membuat error fiktif. A1 review vocabulary/shape, A2 review split/quantization, A3 review loss/causality; setiap perubahan satu owner+reviewer berbeda. Sesudah gate produk terbuka, integrasi Next.js/FastAPI/PostgreSQL dibagi ulang sesuai kemampuan tanpa menggantikan kontribusi ML akademik.
