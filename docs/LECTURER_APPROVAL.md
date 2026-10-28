# Proposal singkat dan checklist persetujuan dosen

**Nirava — Generative Speech Denoising and Enhancement. Stage 1, GO tertunda.**

Member 1 mengusulkan **nirava-stft-cgan-v1**, conditional GAN PyTorch yang dirancang tim dan dilatih dari inisialisasi acak tanpa pretrained encoder/vocoder/teacher. Input awal mono16kHz sepanjang32000 sampel (2detik), pasangan noisy–clean aligned dan speaker-aware split. STFT512/hop128/Hann menghasilkan257×251 kompleks; G U-Net Conv2d kanal16/32/64/128 dengan latent Gaussian memprediksi residual real–imaginer. D patch membandingkan noisy dengan clean/prediksi. iSTFT langsung merekonstruksi panjang eksplisit tanpa vocoder atau fallback fase noisy. Ini menggantikan proposal waveform awal.

Objective: adversarial BCEWithLogits, complex RI L1, waveform L1 dan multi-resolution STFT loss. Bobot/config adalah hipotesis awal. Member3 membangun loop/checkpoint/eksperimen setelah izin; Member2 mengaudit pasangan/mixing dan split. Evaluasi mencakup ablation reconstruction-only, LR/batch/loss, STOI/SI-SDR, PESQ bila diizinkan, listening fonem/artefak, RTF dan peak RAM/VRAM. Belum ada hasil/profiling. Risiko: GAN tidak stabil, latent diabaikan, distorsi suara, data kecil dan generalisasi bahasa.

Dataset dipilih pengguna: [Kaggle speech-noise-dataset](https://www.kaggle.com/datasets/abdullahhaydarkadolu/speech-noise-dataset). Menggantikan pilihan sebelumnya karena ukuran. Struktur, ukuran aktual, lisensi dan sumber komponennya belum terverifikasi. Gunakan pasangan sah bila tersedia atau rencanakan mixing clean speech + noise; split speaker/source dan test dibekukan setelah inventory, tanpa asumsi test resmi. Risiko utama adalah collapse GAN, distorsi fonem, generalisasi bahasa Indonesia dan keterbatasan GPU. Conditional DDPM kecil menjadi alternatif konseptual dengan biaya sampling lebih besar, bukan implementasi kedua yang sudah dijanjikan.

Produk tetap Next.js → FastAPI → model hasil training tim; PostgreSQL hanya metadata dan audio di storage sementara privat. Pekerjaan diprioritaskan pada data, training, eksperimen, dan log LLM empat anggota sebelum pengembangan aplikasi. Tidak ada hasil atau persetujuan yang telah diklaim. Detail teknis: [model](MODEL_PROPOSAL.md), [dataset](DATASET_REQUIREMENTS.md), [tim](TEAM_RESPONSIBILITIES.md), [roadmap](DEVELOPMENT.md).

## Konfirmasi dosen yang diperlukan

Paket review TASK 01: [model dan tensor interfaces](ML_ARCHITECTURE.md), [data pipeline](DATA_CONTRACT.md), [training/loss/checkpoint/reproduksibilitas](TRAINING_CONTRACT.md). Detail dipisah dari MODEL_PROPOSAL tanpa mengganti status atau mengklaim persetujuan. Tiga kontrak harus direview bersama.

- [ ] Speech enhancement STFT kompleks/cGAN diterima sebagai usulan di luar contoh §3, termasuk definisi generatif dan risiko latent diabaikan.
- [ ] Rancangan cGAN dinilai cukup menengah/lanjut dan sesuai kategori model 10 tahun terakhir; penggunaan SEGAN 2017 sebagai dasar konseptual diterima.
- [ ] Definisi from scratch dan batas operasi pustaka dasar disepakati; tidak ada pretrained weights pada model utama.
- [ ] Operasi dasar PyTorch Conv2d/GroupNorm/STFT/iSTFT/autograd/optimizer diperbolehkan, sedangkan forward/arsitektur/loss/loop dirancang tim; shape/inverse/training kontrak v1 diterima.
- [ ] Segmen awal2detik, speaker-aware separation dan synthetic mixing fallback diterima. Speaker ID/clean target yang hilang memerlukan perubahan data atau pengecualian dosen eksplisit sebelum training formal.
- [ ] Dataset Kaggle beserta provenance/lisensi, split dan bahasa evaluasi diterima.
- [ ] Loss, loop, ablation, variasi hyperparameter, metrik dan bukti training yang direncanakan memadai.
- [ ] Empat slot job desk, bukti individu, log LLM dan format ekspor memenuhi rubrik.
- [ ] GPU, plafon komputasi, tenggat, dan ruang lingkup aplikasi realistis.
- [ ] Dosen/tim menerima prosedur pilot 3–5 klip, ambang intelligibility/artefak/runtime/memori yang diusulkan pada [EVALUATION.md](EVALUATION.md), atau mencatat revisi sebelum pengujian.
- [ ] Urutan bukti pilot dan GO disepakati; dosen tidak dianggap memberi izin implementasi atas nama pengguna. Izin pengguna tersendiri diperlukan untuk pilot offline pra-GO.

## Bukti dari tim dan pengguna

Lengkapi [checklist B1–B10](STAGE1_VALIDATION.md) dengan nama/NIM empat anggota, perangkat dan budget RAM/VRAM absolut, akses GPU/jam komputasi, tenggat/milestone, host/concurrency, metadata consent 3–5 rekaman, versi/lisensi Kaggle, kebijakan server/retensi dan ekspor chat. Setelah pilot yang diotorisasi, lampirkan hasil aktual/catatan gagal. Checklist ini belum diisi oleh konfirmasi nyata; persetujuan demo concept dan verdict GO adalah keputusan akhir terpisah.

## Catatan keputusan

Tanggal konsultasi: belum ada. Nama dosen: belum dicatat. Keputusan/catatan/revisi/bukti tertulis: belum ada. Persetujuan dosen atas proposal tidak otomatis berarti Stage 1 GO; verdict GO dan persetujuan eksplisit pengguna atas demo concept tetap gate terpisah. Tidak mengirim proposal atau menghubungi dosen dalam TASK 00C.
