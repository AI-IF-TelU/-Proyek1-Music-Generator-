# Nirava MIDI Music Generator

Status 28 Oktober 2026: **Stage 1 — PIVOT MIDI / GO tertunda**. Pengguna menyatakan penugasan dosen adalah Generative Audio & Sequence: MIDI String Generator. Model utama dirancang dan dilatih dari nol melalui LLM-guided development. Proposal LSTM belum disetujui atau diuji.

## Produk dan scope

Membuat ide melodi monofonik sebagai rangkaian token simbolik, lalu mengekspornya ke `.mid`. MIDI menyimpan event musik, bukan waveform audio. MVP: pilih panjang 4/8/16 bar, seed dan temperature → generate dengan status jujur → periksa piano-roll/event summary dan unduh MIDI. Tidak membutuhkan upload WAV, denoising atau rendering audio.

Stack tetap Next.js + TypeScript → FastAPI + Python/PyTorch → PostgreSQL metadata; file MIDI di storage privat sementara. Training offline wajib, bukan endpoint produk. Tidak ada implementasi, instalasi atau download dataset pada pivot ini.

## Dokumen aktif

- [PRD](docs/PRD.md), [gate Stage 1](docs/STAGE1_VALIDATION.md), [arsitektur aplikasi](docs/ARCHITECTURE.md).
- [Arsitektur LSTM](docs/ML_ARCHITECTURE.md), [token MIDI](docs/MIDI_TOKENIZATION.md), [data Member 2](docs/DATA_CONTRACT.md), [training Member 3](docs/TRAINING_CONTRACT.md).
- [Dataset belum dipilih](docs/DATASET_REQUIREMENTS.md), [evaluasi](docs/EVALUATION.md), [roadmap](docs/DEVELOPMENT.md), [job desk](docs/TEAM_RESPONSIBILITIES.md).
- [Proposal dosen](docs/LECTURER_APPROVAL.md), [keputusan pivot](docs/BLUEPRINT_AUDIT.md), [log LLM](docs/LLM_INTERACTION_LOG.md).

Blueprint speech sebelumnya dipertahankan lengkap dengan penanda arsip pada [archive/speech-blueprint](docs/archive/speech-blueprint/README.md). Tagline speech lama dihentikan untuk produk aktif; nama Nirava tetap, pemeriksaan merek belum selesai. Seluruh angka konfigurasi baru adalah usulan, bukan kemampuan atau hasil terukur. Instruksi menjalankan aplikasi ditulis setelah implementasi diotorisasi dan diuji.
