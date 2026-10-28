# Proposal arsitektur ML Nirava

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

## Objective dan kontrak training Member 3

Semua konstanta adalah starting hypotheses yang harus dibekukan sebelum eksperimen; belum optimal/terukur. Epsilon=1e-7 untuk log/rasio loss. Gunakan Y/X scaled RI dan X_hat_consistent dari waveform rekonstruksi.

- L_D = 0.5*(mean BCEWithLogits(D(Y,X),1) + mean BCEWithLogits(D(Y,stopgrad(X_hat_consistent)),0)).
- L_adv = mean BCEWithLogits(D(Y,X_hat_consistent),1).
- L_RI = mean abs perbedaan komponen real/imaginary scaled, semua bin/frame fisik.
- L_wave = mean abs(x_hat-x) pada sampel valid, sebelum quantization/clipping.
- L_MR = mean lintas resolusi [(norm_F(abs(S_hat)-abs(S_x)) / max(norm_F(abs(S_x)),epsilon)) + mean abs(log(abs(S_hat)+epsilon)-log(abs(S_x)+epsilon))]. STFT resolusi (FFT,window,hop)=(256,256,64),(512,512,128),(1024,1024,256), Hann periodic, center=true/constant, tanpa learned features. Hitung per item sebelum mean batch; catat silence policy dan jangan diam-diam menghapus silence dari evaluasi.
- L_G = 1*L_adv + 10*L_RI + 100*L_wave + 1*L_MR. Simpan raw dan weighted components. Tidak memakai loss SI-SDR pada v1 karena silence/scale ambiguity; tetap metrik evaluasi dengan kebijakan validitas jelas.

Urutan per batch: A2 waveform→STFT, sample z, forward G→iSTFT→STFT konsisten; update D dengan fake detached; update G dengan D frozen tetapi gradien terhadap input fake tetap aktif. Fresh forward D setelah update D untuk loss G; jangan reuse graph D yang parameternya telah berubah. Zero-grad setiap optimizer, ratio satu update D : satu G, tidak memakai adversarial gradient ke target/data. Validation eval/no_grad dan z tetap, tanpa update weights. Pemeriksaan shape/grad dan overfit subset kecil baru setelah gate/izin pilot.

### Config eksperimen dan checkpoint

Config minimal: architecture_id, data_contract_version, run_id, source_commit, seed, dataset_version/manifest_hash, split IDs, sample_rate/segment_samples, semua parameter STFT/scaling/padding, kanal/norm/latent, reconstruction/chunk grid, optimizer G/D, LR/betas, batch/accumulation, epochs/max_updates, loss weights/resolusi/epsilon, precision/device, validation cadence, checkpoint metric/patience dan budget GPU-hour. Simpan resolved config dengan hash; source commit saja tidak cukup bila workspace dirty, rekam patch/hash dan jangan menyebut run reproduksibel tanpa snapshot source.

Starting config: Adam G/D LR2e-4, betas(0.5,0.999), batch4, accumulation1, float32, max50 epoch dengan plafon update/waktu yang ditetapkan setelah inventory/profiling, validation tiap epoch, patience8 pada mean validation STOI. Catat item count/update/epoch untuk perbandingan setara. GPU tipe/VRAM belum diketahui; batch4 bukan klaim akan muat. AMP/scheduler/gradient clipping belum default; jika dipakai ubah config/eksperimen dan verifikasi STFT complex precision serta grad finite.

Checkpoint last/best: G/D state_dict, optimizer states, epoch/global_step, RNG Python/NumPy bila digunakan/torch CPU/CUDA, sampler state atau rencana shuffle, scaler/scheduler bila ada, resolved config/hash, manifest hash, architecture/data-contract version, best score/patience state. Simpan di luar Git; hash untuk lineage. Resume hanya jika config/manifest kompatibel. Ekspor inference terpisah hanya G/config/hash, tidak optimizer/D. Jangan memuat pickle/checkpoint pihak tak tepercaya.

| Run terencana | Perubahan dari v1 | Pertanyaan |
|---|---|---|
| R0 | lambda_adv=0, tidak training D | Apakah adversarial menambah manfaat? Bukan model generatif final |
| R1 | v1 | Referensi |
| R2 | LR G/D1e-4 | Stabilitas |
| R3 | batch2 | Budget/sensitivitas; laporkan update dan contoh terpapar |
| R4 | lambda_wave50 | Fidelity vs adversarial |
| R5 | lambda_MR0 | Kontribusi multi-resolution loss |

Satu faktor berubah, split sama; bekukan budget update dan laporkan paparan contoh yang berbeda akibat batch. Replikasi kandidat terbaik pada tiga seed bila budget memungkinkan; jika satu seed, nyatakan batasan. Tidak wajib menjalankan diffusion hanya untuk pembanding. Tetapkan kriteria stop NaN/OOM, solusi/log dan rerun ID; jangan menyembunyikan run gagal.

### Evaluasi dan acceptance handoff

Pilih best checkpoint menurut mean validation STOI, tie SI-SDR lalu biaya inference; artefak berat pada validation menjadi veto tertulis. Early stopping tidak memakai test. Setelah freeze checkpoint/config, evaluasi semua utterance test valid; noisy baseline wajib, reconstruction-only ablation dan pretrained optional berlabel terpisah. STOI/SI-SDR/delta terhadap noisy, PESQ hanya jika tooling/lisensi sesuai, listening intelligibility/artefak/fonem/speaker, RTF dan peak RAM/VRAM. [EVALUATION.md](EVALUATION.md) tetap sumber protokol pilot/ambang usulan, bukan hasil. Gunakan per-utterance aggregation dan lengkapi failure log. Speech/noise sintetis test tidak diacak ulang tiap epoch.

Tes yang disyaratkan nanti: 32000→257×251→272×256 dan semua tabel shape; STFT round-trip max abs error awal ≤1e-5 float32 pada waveform bounded (konfirmasi device/toleransi); iSTFT length; DC/Nyquist; finite zero/silence loss; D detach dan G gradient lewat inverse/projection; checkpoint/resume; split leakage; padding/overlap-add continuity; reconstruction duration dan alignment. Ini acceptance spesifikasi, belum tes yang lulus.

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
- A2 menyerahkan audit dan manifest/kontrak [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md); jika speaker/target hilang, eskalasikan sebelum training formal. A3 mereview objective/shape, mengisi config/budget dan acceptance checklist sebelum implementasi; A1 review perubahan interface. A4 menyimpan prompt asli, alasan keputusan, ekspor dan hasil verifikasi.
- Dosen harus menerima adaptasi STFT speech cGAN, batas PyTorch dasar dan kelengkapan eksperimen/log. [LECTURER_APPROVAL.md](LECTURER_APPROVAL.md) belum ditandatangani. Stage 1/pilot gate tetap, tidak ada kode training/frontend/backend pada task ini.
