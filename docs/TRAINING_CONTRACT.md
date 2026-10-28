# Training Contract Nirava

Versi **nirava-training-v1**, TASK 01, 28 Oktober 2026. Pemilik Member 3; review Member 1 dan Member 2. Status Stage 1, usulan tanpa implementasi atau hasil. Kontrak model [ML_ARCHITECTURE.md](ML_ARCHITECTURE.md), batch [DATA_CONTRACT.md](DATA_CONTRACT.md).

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



## Format checkpoint dan keluaran run

Usulan berkas `last.pt` dan `best.pt` hanya di storage eksperimen privat, berisi mapping dengan `checkpoint_format_version=nirava-checkpoint-v1`, `architecture_id=nirava-stft-cgan-v1`, `data_contract_version=nirava-data-v1`, `training_contract_version=nirava-training-v1`, `model_g`, `model_d`, `optimizer_g`, `optimizer_d`, `epoch`, `global_step`, `rng_states`, `sampler_state`, `resolved_config`, `config_hash`, `manifest_hash`, `source_revision`, `best_metric` dan `patience_counter`. Scheduler/scaler bila dipakai wajib ikut. Bukan whole-model object dari kode eksternal. Format mapping diperiksa sebelum resume; hash berbeda memerlukan run baru atau keputusan migrasi yang dicatat. Epoch-boundary checkpoint adalah default awal; resume mid-epoch hanya dijanjikan bila posisi sampler/worker augmentation sudah direkam dan diuji.

Ringkasan run nonrahasia: resolved config, environment/lockfile reference, metric history berformat JSONL/CSV (step,epoch,split,loss components,STOI,SI-SDR,LR,elapsed,peak memory), exception/failure log, source snapshot hash dan checkpoint SHA-256. Semua grafik harus berasal dari history aktual dan memuat run/split/unit. File `.pt`, audio dan dataset tidak masuk Git. Tidak ada format/berkas run yang dibuat pada TASK 01.

## Reproduksibilitas dan acceptance Member 3

- Kunci versi Python/PyTorch/CUDA/cuDNN, OS/device, dependency lock/hash, thread/precision dan decoder/resampler. Tidak memasang atau mengasumsikan versi pada tahap ini.
- Seed RNG Python, NumPy bila dipakai, torch CPU/CUDA, DataLoader generator/worker dan mixing/crop. Validation/test memakai manifest dan latent/crop/grid tetap. Seed saja tidak menjamin determinisme lintas hardware atau versi; catat setting deterministic/benchmark, operasi nondeterministik dan trade-off kecepatannya.
- Inisialisasi/normalisasi mengikuti ML_ARCHITECTURE. Perubahan loss/preprocessing atau channel memerlukan versi/config baru, review A1/A2 dan rerun yang bisa dilacak.
- Sebelum eksperimen formal setelah izin: terima audit/manifest A2, buktikan no leakage, smoke shape/inverse/gradient, overfit subset kecil, checkpoint/resume dan profiling. Jangan menyamakan initial loss rendah karena residual passthrough dengan keberhasilan denoising.
- Setelah run: laporkan setiap kegagalan, komponen loss dan validasi, pemilihan checkpoint serta skor utterance held-out. Model selection hanya validation. Tidak mengulang tuning memakai test lalu tetap menyebutnya held-out.

## Handoff dan stop conditions

A2 menyerahkan audit/manifest/hash serta waveform sesuai DATA_CONTRACT; A1 mereview tensor/objective/rekonstruksi; A3 mengisi config dan budget terukur; A4 menyimpan prompt, error asli dan analisis tim. Hentikan run pada NaN/Inf, OOM berulang atau budget habis; simpan log/checkpoint valid terakhir bila mungkin. Mengubah batch/precision/budget dicatat sebagai konfigurasi/run baru, bukan hasil diam-diam.

TASK 01 hanya mendefinisikan kontrak: model/trainer belum dibuat. Gate Stage1 dan izin pilot pada [STAGE1_VALIDATION.md](STAGE1_VALIDATION.md) tetap berlaku. Task selanjutnya direkomendasikan review data/hardware/approval; implementasi memerlukan otorisasi tersendiri.
