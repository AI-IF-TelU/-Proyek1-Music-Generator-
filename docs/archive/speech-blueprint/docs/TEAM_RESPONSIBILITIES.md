> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# Tanggung jawab empat anggota

Mengikuti contoh job desk pada panduan dosen §2. Nama/NIM dan kapasitas perangkat belum diberikan; identitas A1–A4 adalah slot, bukan nama yang diasumsikan. Semua anggota bertanggung jawab memahami desain dan mempresentasikan kontribusinya sendiri.

| Slot dan peran dosen | Tanggung jawab Nirava | Bukti kontribusi | Review dan handoff |
|---|---|---|---|
| A1 Prompt Engineer & LLM Navigator (Ketua) | Strategi prompt, desain G/D dan tensor shape, keputusan cGAN/diffusion, konsistensi kontrak ML–API | Prompt beralasan, diagram, keputusan arsitektur, commit desain | A3 review objective; menyepakati input/output dengan A2 |
| A2 Data Pipeline & Preprocessing Engineer | Provenance/lisensi Kaggle, pairing, split speaker, resampling, crop, loader dan augmentasi train | Manifest/checksum, audit leakage, log prompt pipeline, tes data | A4 review validasi; handoff tensor dan manifest ke A3 |
| A3 Training Loop & Hyperparameter Tuning Engineer | Loop G/D, loss, optimizer, checkpoint/resume, sweep terkontrol, metrik dan profiling | Config/run ID, curve nyata, tabel eksperimen termasuk gagal, hash checkpoint | A1 review matematika; A2 review split; handoff checkpoint ke integrasi |
| A4 Lead Documentarian & Error Handler | Kompilasi log LLM, reproduksi bug, koordinasi debugging, laporan akhir dan bukti integrasi | Ekspor chat, error asli, analisis solusi, hasil verifikasi dan log kerja | Pemilik modul memverifikasi perbaikan; A1 review laporan |

Setiap anggota mencatat sesi sendiri; A4 mengompilasi, bukan mengambil alih seluruh debugging/penulisan. Setiap perubahan memiliki satu pemilik dan satu reviewer berbeda; commit/log kerja menghubungkan anggota, modul, sesi LLM dan run. Keseimbangan kontribusi diperiksa pada milestone, bukan hanya jumlah commit.

Frontend/backend adalah pekerjaan sekunder setelah bukti training tersedia dan gate produk terbuka: usulan A1 koordinasi FastAPI/adaptor, A2 kontrak validasi audio/storage, A3 ekspor inference checkpoint, A4 koordinasi Next.js A/B dan QA dengan review silang. Pembagian ini tidak menggantikan job desk ML dosen dan perlu disesuaikan kemampuan aktual.
