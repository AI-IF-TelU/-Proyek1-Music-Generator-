> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# ML Architecture Nirava

Versi kontrak: **nirava-stft-cgan-v1**, 28 Oktober 2026. Status: **Stage 1, proposal Member 1 untuk review dosen; belum diimplementasikan atau disetujui**. Menggantikan rancangan Conv1D waveform 16.384 sampel sebelumnya, bukan eksperimen yang telah dijalankan.

## Audit terhadap panduan dosen

Panduan resmi dibaca dari DOCX Downloads pengguna, bukan ditemukan di repository. §1 mensyaratkan Vibe Coding, larangan menyalin blok tutorial/proyek eksternal, ekspor/share link LLM dan debugging yang dianalisis tim. §2 memberi empat contoh job desk; §3 meminta konsultasi arsitektur di luar contoh dan kategori 10 tahun terakhir. Speech enhancement STFT tidak otomatis diterima hanya karena cGAN/Pix2Pix dicontohkan. §4: orisinalitas 30%, log 25%, model/training 25%, kerja sama 20%. Prioritas akademik ini mengungguli kriteria kompetisi/desain lama.

| Gap awal | Keputusan arsitektur | Bukti yang masih dibutuhkan |
|---|---|---|
| Pretrained enhancement tidak menunjukkan desain/training tim | G/D dirancang tim dengan operasi dasar PyTorch, seluruh weights baru dari inisialisasi acak | Review kode/orisinalitas dan run aktual setelah izin |
| Training pernah di luar scope produk | Training offline wajib, model dari nol sebagai deliverable utama | Loop/loss/config/kurva/checkpoint dan evaluasi nyata |
| Generatif belum terdefinisi | Conditional adversarial learning G(Y,z), latent Gaussian dan D pasangan | Persetujuan definisi dosen, ablation dan audit latent |
| Kontrak shape/preprocessing belum rinci | STFT kompleks, 2 detik, shape dan inverse eksplisit | Tes round-trip/shape/gradient setelah gate |
| Bukti LLM/tim belum lengkap | Handoff A2/A3, catatan keputusan A1 dan ekspor asli oleh A4 | Log/commit/review tiap anggota, bukan template saja |

Gunakan `torch.nn` Conv2d, GroupNorm, aktivasi, tensor ops, STFT/iSTFT, autograd dan optimizer dasar sebagai usulan batas pustaka yang perlu konfirmasi dosen. Tim menulis susunan jaringan, forward pass, loop, loss dan eksperimen melalui prompt terdokumentasi. Tidak memakai pretrained encoder, vocoder, teacher, jaringan perceptual, atau paket generator siap pakai. Melanjutkan checkpoint tim sendiri boleh diusulkan sebagai tuning, bukan memakai weights pihak lain.

## Pilihan model dan representasi

Usulan: cGAN STFT kompleks kecil dengan skip connections, keluaran residual real–imaginer, discriminator patch kondisional. Referensi konseptual [SEGAN 2017](https://arxiv.org/abs/1703.09452) mendukung adversarial speech enhancement; desain STFT di sini adalah rancangan tim, bukan reproduksi SEGAN atau salinan implementasinya. Usia kategori dan tingkat kompleksitas tetap diperiksa dosen.

Notasi: y noisy, x clean sejajar, batch B. Kedua waveform float32 `[B,32000]`, mono 16 kHz, tepat 2 detik untuk training awal. Tidak menghitung STFT di Member 2: Member 3/adaptor model menjalankan transform yang sama, dikunci dalam config dan checkpoint.

### STFT dan bentuk input

Parameter: n_fft=512, win_length=512, hop_length=128, periodic Hann eksplisit, center=true, pad_mode=constant (zero), normalized=false, onesided=true, return_complex=true. Tidak ada log-magnitude sebagai input utama atau normalisasi berdasarkan test. Frame F=512/2+1=257, T=floor(32000/128)+1=251. Hasil complex64 `[B,257,251]`. Bagi real dan imaginary dengan sqrt(512), stack channel menjadi `[B,2,257,251]`; clean ditransform identik. Penskalaan tetap ini bukan standardisasi statistik dataset.

Zero-pad kanan pada frekuensi sebanyak 15 bin dan waktu sebanyak 5 frame: `[B,2,272,256]`. Ini padding jaringan agar empat downsampling tepat, bukan bin fisik tambahan. Crop kembali ke 257×251 sebelum inverse/loss/D. Tidak membuang Nyquist atau menambah frekuensi palsu pada waveform.

Rujukan API dasar: [PyTorch STFT](https://docs.pytorch.org/docs/stable/generated/torch.functional.stft.html) dan [iSTFT](https://docs.pytorch.org/docs/stable/generated/torch.istft.html). Gunakan window/parameter yang cocok dan length eksplisit; NOLA serta round-trip harus diuji. Versi PyTorch aktual belum dipilih/diinstal.

### Generator G

Encoder Conv2d kernel4 stride2 padding1; aktivasi LeakyReLU(0.2). E1 tanpa norm; E2–E4 GroupNorm(4 groups), bukan BatchNorm sehingga batch kecil tidak bergantung running statistics. Decoder nearest-neighbor upsample ke ukuran skip eksplisit, concatenate, Conv2d kernel3 stride1 padding1 + GroupNorm(4) + ReLU. Tanpa dropout pada v1. Semuanya random initialized; head normal kecil std=1e-3, bias nol sebagai inisialisasi yang dicatat, bukan weights terlatih.

| Tahap | Kanal masuk → keluar | Bentuk keluaran `[B,C,F,T]` |
|---|---|---|
| Input jaringan | 2 | B,2,272,256 |
| E1 | 2→16 | B,16,136,128 |
| E2 | 16→32 | B,32,68,64 |
| E3 | 32→64 | B,64,34,32 |
| E4 | 64→128 | B,128,17,16 |
| Latent | z Gaussian independen | B,8,17,16 |
| Bottleneck | concat E4/z 136→128, Conv1x1 + GN4 + ReLU | B,128,17,16 |
| U1 | up ke34×32, concat E3:192→64 | B,64,34,32 |
| U2 | up ke68×64, concat E2:96→32 | B,32,68,64 |
| U3 | up ke136×128, concat E1:48→16 | B,16,136,128 |
| U4 | up ke272×256, concat input:18→16 | B,16,272,256 |
| Head | Conv1x1 16→2, linear | B,2,272,256 |
| Crop/residual | crop lalu tambahkan input RI yang belum dipad | B,2,257,251 |

Output normalized RI = RI(Y)/sqrt(512) + residual. Tidak memakai sigmoid magnitude mask; output linear dapat memperbaiki komponen fase, tetapi berisiko amplitude overshoot dan perlu pengawasan clipping. z sampled per item setiap training step; validation memakai seed tetap per utterance/chunk. Uji sensitivitas beberapa z pada noisy yang sama tanpa memilih hasil terbaik. Model bisa mengabaikan z; tidak menjanjikan diversity atau perubahan kata.

### Rekonstruksi dan konsistensi spektrum

Kalikan kembali sqrt(512), bentuk kompleks, set bagian imaginary DC dan Nyquist nol untuk real waveform. iSTFT dengan Hann/FFT/hop/center/normalized/onesided sama, return_complex=false dan length=32000 menghasilkan `[B,32000]`. Tidak menggunakan fase noisy sebagai fallback; fase berasal dari estimasi kompleks. STFT arbitrary bisa tidak konsisten: untuk D dan complex loss gunakan STFT ulang waveform hasil iSTFT (kembali diskalakan sqrt(512)), sehingga D melihat representasi audio yang benar-benar dapat direkonstruksi. Jalur tersebut harus differentiable ke G; tidak detach saat update G.

Offline inference utterance penuh: chunk 32000, stride16000 (overlap50%), pad 16000 kiri/kanan lalu pad tambahan kanan sampai grid tercakup. Inverse tiap chunk, weighted overlap-add memakai periodic Hann panjang32000, bagi jumlah bobot dengan epsilon, lalu trim sesuai panjang asli. Padding konteks menjaga bobot endpoint nonzero pada wilayah hasil. Window chunk ini terpisah dari Hann STFT512. Bekukan grid/z seed/gain policy, periksa continuity dan alignment; model noncausal, tidak menjanjikan live streaming. Uji utterance pendek, panjang tak bulat dan silence sebelum memilih batas API. Tidak ada automatic clipping/loudness enhancement tersembunyi untuk mempercantik skor.

### Discriminator D

Condition Y RI dan kandidat clean RI masing-masing `[B,2,257,251]` setelah consistency projection; concatenate `[B,4,257,251]`. Noisy dan real target melalui scaling yang sama; target tidak menerima padding G. D tidak menerima z/speaker label.

| Tahap | Operasi | Bentuk |
|---|---|---|
| D1 | Conv4 s2 p1 4→16, LeakyReLU | B,16,128,125 |
| D2 | Conv4 s2 p1 16→32, GN4, LeakyReLU | B,32,64,62 |
| D3 | Conv4 s2 p1 32→64, GN4, LeakyReLU | B,64,32,31 |
| Logit | Conv3 s1 p1 64→1, linear | B,1,32,31 |

Tidak ada sigmoid dalam D; BCEWithLogits menggabungkannya secara stabil. Rata-rata BCE pada patch/item/batch. D hanya training; deployment memuat G + preprocessing/reconstruction config.

## Objective dan training

Loss yang diusulkan: adversarial BCEWithLogits + L1 RI kompleks + L1 waveform + multi-resolution STFT. Bobot awal G: (1,10,100,1). Rumus, reduction, konfigurasi eksperimen, checkpoint, evaluasi dan reproduksibilitas menjadi sumber tunggal pada [TRAINING_CONTRACT.md](TRAINING_CONTRACT.md). Ini usulan belum diuji, bukan klaim hasil.

## Alternatif minimal diffusion dan trade-off

Alternatif konseptual: epsilon-predictor kecil dengan timestep embedding dan conditioning noisy, seluruh bobot acak; forward x_t=sqrt(alpha_bar_t)*x+sqrt(1-alpha_bar_t)*epsilon dan MSE noise prediction, reverse sampling konsisten dari Gaussian. Dasar [DDPM](https://arxiv.org/abs/2006.11239) dan [conditional speech diffusion](https://arxiv.org/abs/2202.05256); bukan implementasi atau reproduksi kedua paper.

| Pilihan | Kelebihan rancangan | Biaya/risiko |
|---|---|---|
| cGAN STFT kompleks v1 | Satu forward G/chunk, fase dapat diprediksi, inverse tanpa pretrained vocoder | Dua jaringan/instabilitas GAN, STFT inconsistency, latent diabaikan, kompleksitas rekonstruksi |
| cGAN magnitude + noisy phase | Output lebih sederhana | Fase tetap terkontaminasi; bukan opsi utama v1 |
| cGAN waveform terdahulu | Tidak perlu inverse spektral | Perlu pembelajaran struktur gelombang; kontrak 1,024 detik digantikan v1 |
| DDPM minimal | Objective satu predictor dan sampling generatif eksplisit | Banyak forward, noise schedule/conditioning, latency dan komputasi belum terbukti |

cGAN diprioritaskan karena single-pass inference dan kesesuaian eksperimen dua jaringan, bukan klaim mutu lebih unggul. [DeepFilterNet](https://arxiv.org/abs/2110.05588) memprediksi gain/filter untuk enhancement; output audio tidak otomatis memenuhi definisi generatif ketat. Integrasi pretrained atau retraining rancangan pihak lain tidak membuktikan desain generatif mandiri. Hanya baseline opsional, tidak fallback tersembunyi.

## Asumsi belum terverifikasi dan handoff

- Hardware: GPU/CUDA, RAM/VRAM/disk, dukungan complex autograd/STFT, wall-time budget dan host inference belum tersedia. Jumlah parameter, peak memory, RTF dan kualitas belum dihitung secara runtime. Label ringan adalah tujuan, bukan bukti.
- Dataset aktif tetap Kaggle speech-noise-dataset; lisensi, versi, ukuran, clean target, bahasa, speaker IDs dan noise lineage belum diverifikasi. Speaker-aware adalah syarat; source-only grouping tidak boleh diberi label speaker-disjoint.
- A2 menyerahkan audit dan manifest/kontrak [DATA_CONTRACT.md](DATA_CONTRACT.md) dan audit [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md); jika speaker/target hilang, eskalasikan sebelum training formal. A3 mereview objective/shape, mengisi config/budget dan acceptance checklist sebelum implementasi; A1 review perubahan interface. A4 menyimpan prompt asli, alasan keputusan, ekspor dan hasil verifikasi.
- Dosen harus menerima adaptasi STFT speech cGAN, batas PyTorch dasar dan kelengkapan eksperimen/log. [LECTURER_APPROVAL.md](LECTURER_APPROVAL.md) belum ditandatangani. Stage 1/pilot gate tetap, tidak ada kode training/frontend/backend pada task ini.


## Antarmuka model untuk Member 3

Spesifikasi signature berikut adalah kontrak konseptual, bukan kode yang sudah tersedia:

| Operasi | Input | Output / kewajiban |
|---|---|---|
| encode_waveform | float32 `[B,32000]`, device yang dipilih | RI normalized `[B,2,257,251]`, metadata transform; tidak menambah channel batch secara ambigu |
| G.forward | padded RI `[B,2,272,256]`, z float32 `[B,8,17,16]` pada device sama | residual RI `[B,2,272,256]`; caller crop/add input sebelum inverse |
| reconstruct | estimated RI `[B,2,257,251]` | waveform float32 `[B,32000]`, DC/Nyquist dan iSTFT length eksplisit |
| project_consistent | waveform hasil rekonstruksi | RI normalized `[B,2,257,251]` untuk D/loss |
| D.forward | concat noisy/candidate RI `[B,4,257,251]` | logits float32 `[B,1,32,31]`, bukan probabilitas |
| enhance_utterance | waveform mono16kHz `[L]`, L>0, config + seed | waveform `[L]` melalui chunk/overlap-add; resampling/decoder di luar G |

Caller mengatur device, input finite, dtype dan valid length; unsupported shape/config menghasilkan kegagalan eksplisit, bukan crop/resample diam-diam. z harus disuplai eksplisit saat training/validation agar RNG bisa direproduksi, bukan dibuat di dalam forward tanpa kendali. Untuk utterance panjang, seed berasal dari run seed + ID utterance + indeks chunk dengan pemetaan stabil yang dicatat; jangan memakai hash bawaan bahasa yang berubah per proses.

Inisialisasi usulan: Conv hidden Kaiming sesuai aktivasi, bias nol; GroupNorm scale1/bias0; head normal std1e-3/bias0. Normalization constants bukan pretrained weights. Tensor layout channel-first, G/D dan window berada pada device sama. Trainer tidak boleh memanggil Next.js, FastAPI atau PostgreSQL untuk mini-batch.

## Pertanyaan approval khusus TASK 01

- [ ] Dosen menerima speech STFT cGAN dan tingkat kompleksitas sebagai adaptasi di luar contoh, dengan definisi generatif yang dinyatakan.
- [ ] Operasi dasar PyTorch dan STFT/iSTFT diperbolehkan; seluruh desain G/D, objective dan training dibuat tim melalui LLM, tanpa pretrained utama.
- [ ] Kontrak input2detik, target paired, pemisahan speaker/noise dan mixing fallback diterima.
- [ ] Jika metadata speaker atau clean target tidak ada, perubahan sumber/pengecualian diputuskan sebelum training; source split tidak dilabeli speaker-disjoint.
- [ ] Loss, ablation, sweep, metrik, budget hardware dan format bukti log/kontribusi disetujui.

Checklist keputusan terpusat tetap [LECTURER_APPROVAL.md](LECTURER_APPROVAL.md); seluruh kotak di atas belum terverifikasi. Kriteria gate tidak berubah. Memisahkan kontrak bukan klaim bahwa desain sudah layak secara empiris.
