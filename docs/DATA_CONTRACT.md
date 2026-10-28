# Data Contract Nirava

TASK 01, 28 Oktober 2026. Pemilik Member 2; review Member 1/3. Status Stage 1, belum ada download/loader atau hasil audit. Provenance, keputusan sumber dan checklist dataset tetap pada [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md). Model pada [ML_ARCHITECTURE.md](ML_ARCHITECTURE.md), trainer pada [TRAINING_CONTRACT.md](TRAINING_CONTRACT.md).

## Kontrak data Member 2 untuk Member 1 dan 3

Versi **nirava-data-v1**, kompatibel dengan **nirava-stft-cgan-v1**. Ini spesifikasi handoff, bukan hasil audit atau loader yang sudah tersedia.

| Field batch | Bentuk/tipe | Makna |
|---|---|---|
| noisy | float32 `[B,32000]` | Mono16kHz, finite, gain sudah didokumentasi |
| clean | float32 `[B,32000]` | Target aligned, crop start/end dan gain sama |
| num_samples | int64 `[B]`, semuanya32000 saat training awal | Jangan menghitung padding sebagai ucapan valid |
| sample_id / utterance_id | daftar B ID opaque | Telusur ke manifest, bukan path publik |
| speaker_id / source_id / split | metadata B item | Speaker-aware separation; lineage sumber dan turunan |
| crop_start / gain / mixing_id | metadata B item | Reproduksi crop, inverse gain, dan campuran bila sintetis |

Waveform memiliki headroom: bila peak pasangan melebihi0,99 terapkan faktor penurun yang sama ke clean/noisy dan rekam; jangan menaikkan setiap klip ke peak maksimum. Tidak melakukan normalisasi tiap sisi sendiri. STFT tidak disediakan/cached secara default oleh A2, agar preprocessing hanya satu implementasi milik adaptor model A3. Float waveform bukan PCM integer atau mel image. Alignment harus pada tingkat sampel dan diverifikasi, bukan sekadar panjang sama.

Manifest minimal: sample/utterance/speaker/source IDs, dataset version, split, private storage reference, checksum, izin/lisensi/provenance, sample rate/channel asli dan setelah proses, original/valid length, crop start, gain, exclusion reason. Untuk mixing tambahkan noise_source_id, offset, SNR, seed dan mixing version. Paths/consent pribadi tidak dipublikasikan; ringkasan audit anonim dapat masuk Git.

Fallback mixing jika komponen sah tersedia: split speaker/utterance dan source noise dahulu, lalu y=x+a*n dengan a=RMS(x)/(RMS(n)*10^(SNR/20)); RMS hanya wilayah valid dan kebijakan silence/epsilon eksplisit. Starting SNR train uniform−5..20dB dan held-out fixed0/5/10/15dB adalah usulan untuk disepakati sesudah inventory, bukan label asli dataset. Noise senyap di-resample atau ditolak dengan log, bukan dibagi nol. Common gain mencegah clipping kedua target/input. Noise pendek boleh ditile hanya dalam source/split sama dengan kebijakan seam tercatat. Validation/test mix dibuat sekali dan manifest dibekukan; augmentation tambahan hanya train.

Split harus menahan seluruh speaker dan seluruh turunan utterance. Jika speaker ID tidak tersedia, A2 melaporkan gap kepada A1; source grouping dapat didokumentasikan sebagai batasan tetapi **belum memenuhi speaker-aware acceptance** tanpa bukti tambahan atau pengecualian dosen yang eksplisit. Speaker tunggal/tidak cukup kelompok tidak boleh diklaim mendukung evaluasi speaker-disjoint. Jumlah/rasio split baru ditetapkan setelah inventory. Tidak random-split crop; audit hash dan parent IDs, termasuk noise, lintas split.

Handoff A2: laporan dataset/licence/shape/alignment, manifest freeze + hash, jumlah speaker/utterance/durasi tiap split dan exclusions, synthetic mixing decision, contoh batch contract setelah implementasi diizinkan. A1/A3 review sebelum training formal; tidak ada download atau implementasi pada task Member1.


