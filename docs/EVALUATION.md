# Evaluation plan (no measured results yet)

## Research questions

Kontrak model aktif Member1: [nirava-stft-cgan-v1](MODEL_PROPOSAL.md), STFT kompleks dari waveform mono16kHz dengan training segment32000 sampel/2detik. Kontrak tersebut menetapkan shape, transform/inverse, loss, checkpoint dan eksperimen; menggantikan parameter waveform awal. Protokol berikut berlaku pada hasil rekonstruksi audio. Belum ada implementasi atau hasil.
Does enhancement reduce noise while preserving speech intelligibility and timbre? How does performance vary by noise type and SNR?

## Test material
Consent-cleared or properly licensed speech clips; clean references when available; multiple noise types and SNR levels; separate demo from evaluation clips. Record sample rate, duration, language, and noise type.

## Metrics
- If clean reference exists: SI-SDR, STOI, PESQ where license/tooling permits and limitations are explained.
- Without clean reference: blinded listening study for intelligibility and artifacts; do not report reference-based metrics.
- Operational: p50/p95 processing time, failure rate, peak memory, supported formats.

## Protocol
Use identical clips and matched playback loudness; do not normalize one version to fake improvements. Blind labels when possible. Record failures and artifacts, not only wins.

## Results template
| Sample | Noise | Before | After | Metric | Observation |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | Not tested |

## Claim policy
Do not claim generative capability, % noise reduction, or universal improvement without supporting tests and an appropriate model definition.

## Training dan checkpoint

Gunakan manifest terverifikasi [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md), train/validation/test terpisah speaker atau sumber terverifikasi; test dibekukan dari split resmi jika ada atau manifest held-out tim jika tidak ada. Catat run ID, config, seed, source commit, hash manifest/checkpoint, environment, optimizer/schedule, update, epoch, stopping reason dan hardware. Grafik aktual memisahkan loss G adversarial/L1/spectral, loss D dan metrik validation terhadap step/epoch. Loss GAN bukan skor kualitas dan tidak harus monoton.

Aturan awal yang dibekukan sebelum eksperimen: pilih checkpoint dengan mean validation STOI tertinggi di antara run tanpa NaN/kerusakan output; tie diputus SI-SDR lalu biaya inference. Early stopping mengikuti validation STOI dengan patience tercatat. Listening pada validation dapat memveto artefak berat dengan alasan tertulis. Bekukan checkpoint/config sebelum test; laporkan seluruh test valid beserta pengecualian.

## Protokol metrik

Baseline wajib noisy tanpa enhancement. Bandingkan cGAN dan ablation G reconstruction-only; DeepFilterNet hanya opsional, terpisah dan berlabel pretrained. Gunakan pair/split/preprocessing sama.

- STOI terhadap clean berpasangan: catat implementasi, versi, parameter dan sample rate dukungannya. Ini proxy intelligibility, bukan bukti semua fonem benar.
- SI-SDR dB: proyeksikan prediksi zero-mean ke clean zero-mean; 10 log10 rasio energi proyeksi terhadap residual, dengan epsilon/silence policy eksplisit. Laporkan improvement terhadap noisy. Scale-invariance tidak membuktikan loudness terjaga.
- PESQ opsional jika lisensi/tooling mengizinkan: catat mode 8 kHz narrowband atau 16 kHz wideband, resampling dan versi. Jangan melaporkan jika tidak dihitung atau menggantinya dengan proxy tanpa label.
- Skor noisy/enhanced dan delta per utterance, mean/median, sebaran dan jumlah valid/gagal. Paired bootstrap memakai seed tercatat; keterbatasan speaker test membatasi generalisasi dan interval populasi speaker. Breakdown noise/SNR hanya bila label terverifikasi.
- Operasional: real-time factor = detik inference/detik audio, p50/p95, warm/cold load terpisah, chunk, concurrency, peak RAM/VRAM dan hardware; nyatakan apakah decode/encode termasuk. Belum ada angka terukur.

Listening: randomisasi/blind label, playback volume konsisten, pertanyaan intelligibility/naturalness/artefak terpisah; catat consent, bahasa, pendengar/klip dan sampling. Jangan menyebut MOS standar tanpa protokol sesuai. Periksa fonem hilang/berubah, identitas speaker, silence, noise baru, clean speech dan batas chunk.

Tes setelah gate: pairing/crop, leakage, resampling/gain identik, output shape, gradient G/D dan detach, finite loss/silence, checkpoint round-trip/resume, validation deterministik, overlap-add/padding dan alignment A/B. Tes API/audio serta lint/typecheck saat implementasi tersedia. Tabel hasil tetap belum terisi sampai eksperimen dilakukan.

## Pilot 3–5 rekaman berizin — rencana TASK 00B

Belum dijalankan. Eksekusi sebelum GO memerlukan izin pilot terbatas sesuai B5 pada [STAGE1_VALIDATION.md](STAGE1_VALIDATION.md); rencana ini tidak mengotorisasi model, instalasi atau pengembangan aplikasi. Setelah izin, A2 menyiapkan data, A3 mengukur dan A4 mengaudit. Model utama diuji hanya setelah checkpoint training tim tersedia secara sah. DeepFilterNet, bila diizinkan, memakai kolom hasil terpisah dan tidak menutup gap from scratch.

1. Pilih minimal tiga rekaman 10–30 detik: noise stasioner (kipas), noise berubah (jalan/keyboard), dan kondisi sulit tetapi ucapan masih terdengar. Jika lima tersedia, tambahkan kontrol ucapan relatif bersih dan rekaman panjang mendekati batas demo untuk stress. Minimal dua penutur bila izin memungkinkan, termasuk Bahasa Indonesia. Simpan ID opaque, SHA-256, consent/lisensi, durasi, codec, sample rate/channel, bahasa/noise dan reference availability di manifest privat.
2. Sedikitnya dua klip mempunyai clean reference sinkron (misalnya rekaman ucapan berizin yang dicampur noise berizin dengan seed/SNR tercatat); satu klip noisy nyata untuk domain mismatch. Tidak menganggap rekaman ruangan berbeda sebagai clean pair. Tanpa reference sah, gunakan listening saja dan laporkan kekurangan bukti paired. Jangan gunakan test held-out untuk tuning atau menjadikan pilot kecil sebagai estimasi benchmark umum.
3. Bekukan pemilihan klip, transkrip acuan yang dibuat dari clean/penutur, konfigurasi, latent seed, model/checkpoint hash dan ambang sebelum inference. Jangan mencoba banyak seed lalu memilih audio yang terdengar paling baik. Jangan memilih klip setelah melihat skor. Audio/consent/weights tetap di luar Git.
4. Uji input/output sepadan: trim delay/padding secara deterministik, catat output duration dan alignment, serta dengarkan kedua versi pada gain playback bersama. Hitung metrik fidelity pada output asli setelah inverse preprocessing; jangan mengoptimalkan alignment/gain per klip untuk meningkatkan skor. A/B dibutakan dan urutan diacak.
5. Tiga pendengar yang memahami bahasa menyalin kata yang terdengar tanpa melihat transkrip. Pisahkan sesi original/enhanced dan counterbalance urutan untuk mengurangi hafalan. Bandingkan kesalahan kata terhadap transkrip terverifikasi dengan normalisasi teks yang dibekukan; ini tes manual kecil, bukan fitur ASR/transkripsi produk. Laporkan error rate (substitusi + delesi + insersi)/jumlah kata, median per klip dan perubahan percentage point.
6. Catat artefak dengan skala 0 tidak ada, 1 ringan, 2 mengganggu, 3 merusak makna. Tandai phoneme/word insertion/deletion, robotik/musical noise, clipping dan perubahan speaker. Review seluruh klip; mayoritas pendengar menentukan preference, sedangkan kasus berat harus diinvestigasi, tidak dirata-ratakan hilang.
7. Pada host target, satu job, model sama: ukur cold startup/load sekali, satu warm-up, lalu lima inference terukur per klip; sinkronkan GPU timing bila digunakan. Catat wall time inference dan end-to-end decode–encode terpisah, RTF, peak process RSS termasuk model/buffer dan peak allocated/reserved VRAM. Laporkan RAM/VRAM idle serta puncak total, hardware/OS/thread/precision dan alat ukur. p95 dari sampel kecil hanya deskriptif; jangan menyebut production SLO.
8. Hasilkan tabel per klip (noisy, cGAN, ablation bila tersedia, baseline opsional), daftar gagal dan keputusan pass/revise beserta raw logs/artefak privat yang dapat ditinjau. Jangan menyimpulkan kelayakan 120 detik jika hanya klip pendek yang diuji; ukur stress terpisah bila batas itu ingin dipertahankan.

### Ambang awal untuk disepakati sebelum pilot

Angka berikut adalah usulan operasional tim untuk feasibility, bukan standar dosen atau hasil terukur. Tim/dosen boleh merevisi sebelum pengukuran dengan alasan tertulis; jangan mengubah ambang setelah melihat hasil untuk membuat run lulus.

| Dimensi | Usulan kriteria pilot | Bukti yang dicatat |
|---|---|---|
| Intelligibility manual | Median error rate enhanced tidak lebih buruk pada setiap klip; berkurang ≥5 percentage point pada ≥2 klip noisy non-kontrol | Transkrip/rating anonim dan jumlah kata, skor per pendengar |
| Fidelity paired | Rata-rata delta STOI ≥0,02 dan SI-SDR improvement ≥1 dB pada klip paired; tak ada delta STOI <−0,02 | Skor tiap pair, implementasi/versi dan failure/silence policy |
| Artefak | Tidak ada artefak level 3 yang dikonfirmasi reviewer; median level ≤1 per klip; mayoritas pendengar memilih enhanced pada ≥2 klip noisy | Rating dan anotasi waktu, termasuk kerusakan fonem/speaker |
| Runtime | Warm inference RTF ≤1 pada setiap klip pada host yang disepakati; cold-load/end-to-end tetap dilaporkan | Lima pengulangan per klip dan konfigurasi host |
| Memori | Tidak OOM; peak total process RAM ≤70% RAM yang dialokasikan dan peak VRAM reserved ≤80% VRAM tersedia untuk proses; budget absolut GiB harus ditulis sebelum pilot | Host budget dan peak RSS/VRAM, metode ukur |
| Integritas | Semua klip terpilih diproses atau kegagalannya dicatat; panjang sesuai input setelah trim, tidak ada truncation/gain manipulation | Manifest, config/checkpoint hash dan log output |

Jika baseline noisy sudah sangat jelas, syarat improvement tidak diterapkan pada kontrol bersih; kontrol tetap harus tidak memburuk. Jika tidak tersedia dua klip paired, ambang paired belum dapat dinilai dan readiness tetap kurang bukti, bukan dianggap pass. Penilaian tiga pendengar dan 3–5 klip tidak menggantikan held-out evaluation formal, generalisasi speaker, atau grafik training yang diwajibkan dosen.
