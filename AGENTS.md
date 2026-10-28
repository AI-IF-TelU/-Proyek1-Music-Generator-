# AGENTS.md — Kontrak kerja coding assistant

## Identitas proyek
Nama produk: **Nirava**. Tagline: **Keep the voice. Lose the noise.**
Nama proyek masih perlu pemeriksaan merek dan tidak mengubah status Stage 1.

## Urutan baca
1. `README.md` dan `docs/PRD.md`.
2. `docs/STAGE1_VALIDATION.md` (gate sebelum implementasi).
3. `docs/ARCHITECTURE.md`, `docs/API_SPEC.md`, `docs/DATABASE_SCHEMA.md`.
4. `docs/ML_ARCHITECTURE.md`, `docs/DATA_CONTRACT.md`, `docs/TRAINING_CONTRACT.md` untuk pekerjaan ML.
5. `docs/DESIGN_SYSTEM.md`, `docs/DEVELOPMENT.md`, `docs/EVALUATION.md` sesuai tugas.

## Aturan wajib
- Kebutuhan akademik panduan resmi dosen mengungguli blueprint hackathon lama. Baca panduan bila tersedia; jangan menganggap referensi literatur sebagai persetujuan dosen.
- Model utama wajib dirancang tim dan dilatih dari inisialisasi acak melalui Vibe Coding; jangan gunakan pretrained weights, teacher atau vocoder sebagai pemenuhan model utama. Simpan prompt asli, alasan keputusan, log error/solusi nyata dan ekspor/link chat.
- Kontrak ML aktif `nirava-stft-cgan-v1` di `docs/ML_ARCHITECTURE.md`: PyTorch dasar, STFT kompleks, waveform mono 16 kHz, segmen awal 32000 sampel (2 detik). `docs/DATA_CONTRACT.md` mengatur pairing/alignment/speaker split; `docs/TRAINING_CONTRACT.md` mengatur loss/loop/checkpoint/reproduksibilitas. MODEL_PROPOSAL hanya ringkasan, DATASET_REQUIREMENTS hanya audit/provenance. Semua masih usulan; perubahan teknis perlu review A1/A2/A3 dan versioning kontrak.
- Jangan mulai Stage 2 sampai Stage 1 mendapat verdict GO dan demo concept disetujui pengguna.
- Jangan mengklaim DeepFilterNet sebagai Generative AI tanpa justifikasi ilmiah dan kecocokan rubrik.
- Next.js hanya memanggil FastAPI; inference ML hanya di backend.
- PostgreSQL menyimpan metadata, bukan bytes audio; berkas di storage sementara.
- Perubahan skema memakai migrasi Alembic; jangan `create_all` pada production.
- Validasi ukuran, durasi, MIME aktual/decoder, sample rate; sanitasi nama file.
- Gunakan UUID sebagai identitas job, bukan path dari pengguna.
- Pastikan job milik pemohon dengan token akses job acak; jangan berasumsi UUID = otorisasi.
- Jangan commit audio pribadi, model weights, `.env`, database dump, atau direktori runtime.
- Tulis tes untuk perubahan API dan audio pipeline; jalankan lint/typecheck yang relevan.
- Hindari dependensi baru dan perubahan besar tanpa menjelaskan trade-off.
- UI harus aksesibel, responsif, jujur tentang status/hasil, dan tidak memakai metrik fiktif.
- Sebelum coding, jelaskan file terdampak, pendekatan minimal, serta cara verifikasi.

## Scope MVP
Upload, enhancement, A/B comparison + download. Tanpa akun, billing, admin dashboard, Redis, Celery, atau Three.js kecuali terbukti perlu.

Training offline, data audit, eksperimen hyperparameter dan metrik aktual adalah deliverable akademik wajib; bukan fitur training dalam UI. Persyaratan estetika/kompetisi tambahan tidak menggantikan bukti model/training dan log dosen.
