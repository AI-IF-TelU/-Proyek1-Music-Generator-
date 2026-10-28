# AGENTS.md Kontrak kerja Nirava

## Identitas dan urutan baca

Produk aktif **Nirava — MIDI Music Generator**. Domain Generative Audio & Sequence, tugas autoregressive MIDI String Generation. Blueprint speech dalam docs/archive/speech-blueprint adalah riwayat, bukan instruksi aktif; jangan mengimplementasikan kontrak denoising yang diarsipkan.

Baca README.md, docs/PRD.md, docs/STAGE1_VALIDATION.md, lalu docs/ML_ARCHITECTURE.md, docs/MIDI_TOKENIZATION.md, docs/DATA_CONTRACT.md, docs/TRAINING_CONTRACT.md. Untuk aplikasi baca docs/ARCHITECTURE.md, API_SPEC.md dan DATABASE_SCHEMA.md. Roadmap, evaluasi, tanggung jawab dan log mengikuti dokumen aktif masing-masing.

## Aturan wajib

- Panduan resmi dan penugasan MIDI yang diberikan pengguna mengungguli blueprint hackathon/speech lama. Penugasan domain bukan persetujuan LSTM, dataset atau GO.
- Stage 1 tetap berlaku sampai verdict GO dan persetujuan eksplisit pengguna atas demo concept. Task dokumentasi tidak mengizinkan implementasi, instalasi atau training. Pilot pra-GO memerlukan izin terbatas tersendiri.
- Model utama dirancang tim dan dilatih dari inisialisasi acak menggunakan PyTorch dasar. Usulan sel LSTM manual dengan Linear/tensor/autograd perlu konfirmasi dosen. Jangan menyalin implementasi eksternal atau memakai pretrained weights/embeddings/teacher.
- Simpan prompt asli, respons/ekspor chat, alasan keputusan, error aktual, analisis dan verifikasi kelompok. Jangan membuat error/hasil atau approval fiktif.
- Kontrak aktif nirava-midi-step-v1 / nirava-midi-lstm-v1 / nirava-midi-data-v1 / nirava-midi-training-v1. Perubahan token IDs, quantization, shape atau checkpoint memerlukan versioning dan review A1/A2/A3.
- Next.js hanya memanggil FastAPI. Training/inference Python berada di backend/offline trainer. PostgreSQL metadata, bukan bytes MIDI/weights; file privat sementara.
- UUID adalah identitas job, token akses acak adalah otorisasi. Hash token, redaksi log, rate limit, bounded queue, expiry dan cleanup tetap wajib.
- Perubahan skema nanti melalui Alembic, bukan create_all production. Pivot dokumentasi tidak membuat migrasi atau menganggap skema baru sudah ada.
- Validasi output MIDI dengan parser dan batas event/tick/file/runtime; jangan memakai persyaratan sample rate/MIME WAV pada domain MIDI. MVP tidak menerima upload file pengguna.
- Jangan commit dataset MIDI berhak cipta/pribadi, weights, .env, dump atau direktori runtime. Manifest anonim/config/log tanpa rahasia dapat ditinjau.
- Sebelum coding jelaskan file, pendekatan minimal dan verifikasi; tulis tes model/tokenizer/export/API yang relevan setelah izin. Hindari dependensi baru tanpa trade-off.
- UI aksesibel/responsif, status dan hasil jujur. Tidak menjanjikan musik bebas hak cipta atau kualitas tanpa evaluasi.

## Scope MVP

Parameter generation → status → hasil simbolik/piano-roll dan download MIDI monofonik. Tanpa denoising, WAV/MP3, audio rendering, multi-track/polyphony, upload prompt MIDI, akun, billing, admin, Redis, Celery atau Three.js. Data/training/eksperimen/evaluasi/log adalah deliverable akademik utama.
