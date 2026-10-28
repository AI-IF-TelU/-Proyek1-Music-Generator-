# Nirava — Generative Speech Denoising and Enhancement

> Nama kerja: **Nirava**. Nama ini telah digunakan pihak lain; penggunaan komersial dan ketersediaan merek/domain belum terverifikasi.
> Tagline: **Keep the voice. Lose the noise.**

## Status
Stage 1: **PIVOT TERARAH / GO tertunda**. Panduan dosen telah dibaca pada 28 Oktober 2026 dari berkas Downloads yang diberikan pengguna. Model utama wajib dirancang dan dilatih dari nol; cGAN speech enhancement masih usulan yang memerlukan konsultasi dosen. Jangan memulai Stage 2 tanpa verdict GO dan persetujuan eksplisit pengguna atas demo concept.

## Problem statement
Bagaimana membersihkan rekaman percakapan yang terganggu noise sambil mempertahankan kejelasan dan karakter suara asli?

## MVP (3 fitur)
1. Unggah audio dan validasi format/durasi/ukuran.
2. Jalankan enhancement dengan status pemrosesan dan penanganan error.
3. Bandingkan audio asli/hasil secara sinkron dan unduh hasil.

## Stack
Next.js + TypeScript; FastAPI + Python; PostgreSQL; PyTorch conditional GAN STFT kompleks dari nol, kontrak `nirava-stft-cgan-v1`, input awal mono16kHz/2detik (kandidat utama, belum disetujui/diimplementasikan). DeepFilterNet pretrained hanya pembanding opsional, tidak memenuhi model utama.

## Blueprint TASK 00C

- [Proposal model dan trade-off diffusion](docs/MODEL_PROPOSAL.md).
- TASK 01: [arsitektur ML](docs/ML_ARCHITECTURE.md), [kontrak data Member 2](docs/DATA_CONTRACT.md), [kontrak training Member 3](docs/TRAINING_CONTRACT.md). Spesifikasi saja, belum training/approval.
- [Dataset Kaggle pilihan pengguna dan checklist](docs/DATASET_REQUIREMENTS.md).
- [Job desk empat anggota](docs/TEAM_RESPONSIBILITIES.md), [roadmap training-first](docs/DEVELOPMENT.md), dan [log LLM](docs/LLM_INTERACTION_LOG.md).
- [Proposal singkat dan checklist dosen](docs/LECTURER_APPROVAL.md); [audit rubrik dan risiko](docs/BLUEPRINT_AUDIT.md).
- [Checklist penutupan Stage 1 dan bukti GO](docs/STAGE1_VALIDATION.md), [rencana pilot 3–5 rekaman](docs/EVALUATION.md). Pilot belum dijalankan atau diotorisasi; gate tetap tertutup.

Training adalah deliverable akademik wajib; antarmuka MVP tetap upload, enhancement, A/B dan download. Belum ada hasil eksperimen.

Dataset aktif: [speech-noise-dataset](https://www.kaggle.com/datasets/abdullahhaydarkadolu/speech-noise-dataset), menggantikan Valentini Noisy karena ukuran menurut pengguna. Isi, ukuran aktual, lisensi dan kesiapan pasangan training belum diverifikasi; lihat checklist dataset.

## Struktur
`frontend/` UI; `backend/` API/inference; `docs/` kontrak dan keputusan; `infra/` Docker Compose PostgreSQL; `scripts/` utilitas; `tests/` tes integrasi bila diperlukan.

## Menjalankan (target, belum diimplementasikan)
1. Salin `.env.example` ke `.env` lokal; jangan commit rahasia.
2. Jalankan PostgreSQL dari `infra/compose.yaml`.
3. Instal dependensi backend dan jalankan migrasi Alembic.
4. Jalankan FastAPI dan Next.js pada terminal terpisah.
5. Periksa `/api/v1/health` dan alur upload → job → hasil.

Instruksi CLI persis akan ditambahkan setelah scaffold dibuat dan diuji.

## Audit blueprint
[Hasil audit dan audit ulang blueprint](docs/BLUEPRINT_AUDIT.md) memisahkan konsistensi rancangan dari validasi empiris. Blueprint belum membuktikan kelayakan model dan belum membuka gate Stage 2.
