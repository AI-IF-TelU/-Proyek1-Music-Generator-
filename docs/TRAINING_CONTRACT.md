# Training Contract Nirava MIDI

Versi **nirava-midi-training-v1** dan format **nirava-midi-checkpoint-v1**. Pemilik A3, review A1/A2. Stage1, rencana bukan implementasi. Model [ML_ARCHITECTURE](ML_ARCHITECTURE.md), tokenizer [MIDI_TOKENIZATION](MIDI_TOKENIZATION.md), data [DATA_CONTRACT](DATA_CONTRACT.md).

## Objective dan loop

Teacher-forced next-token cross entropy pada logits[B,T,133] dan targets[B,T], ignore PAD0. NLL=sum CE valid / jumlah target valid termasuk EOS. Tidak menghitung BOS sebagai target; model tetap boleh memberi logit untuk seluruh vocabulary saat evaluasi raw NLL. Tidak grammar-mask logits untuk mempercantik perplexity. Perplexity=exp(mean NLL), laporkan overflow bila terjadi, aggregation berbobot jumlah token bukan mean batch/perplexity.

Usulan awal: embedding64, dua LSTM hidden128, T128, batch16, Adam LR1e-3 betas(0.9,0.999), float32, grad norm clipping1, dropout0, max50epoch, validation tiap epoch, patience8 atas validation NLL. Max updates dan wall-time harus diisi setelah data/hardware diketahui. Semua bobot baru; bukan tuning pretrained. CPU dapat menjadi target eksperimen awal tetapi feasibility belum diukur.

Loop: shuffle train windows per seed, reset h/c, embedding/recurrence/head, masked CE, zero_grad, backward, clip dan optimizer.step; log raw loss/grad norm/LR/token count. Validation eval/no_grad dengan data tetap dan raw CE; pilih best minimum validation token-NLL, tie model lebih kecil/runtime. Test dibuka sesudah config/checkpoint beku. Inference autoregresif terpisah dengan state carry dan grammar; tidak mengevaluasi sampling memakai teacher-forced accuracy saja.

R0 baseline unigram train-only smoothed probabilities; R1 LSTM usulan; R2 LR3e-4; R3 hidden64; R4 T64; R5 sampling temperature0.8/1/1.2 pada checkpoint sama (bukan retraining). Satu faktor berubah, data/tokenizer sama dan budget exposure/update dicatat. T64 mengubah konteks/window count sehingga laporkan perbedaan; jangan mengklaim fair compute tanpa normalisasi. Ulang seed jika budget tersedia; run gagal tetap dilaporkan.

## Config, checkpoint dan reproducibility

Resolved config memuat run/source commit + dirty patch hash, architecture/tokenizer/data/training versions, vocabulary133 dan ID map hash, dataset/manifest/split hashes, window/stride, init/optimizer/clipping, hyperparameters, seeds, precision/device/software/OS, budget/cadence, model selection serta sampling mode/temp/top-k/cap. Pin versi environment dan parser setelah disetujui, tanpa instalasi pada task ini.

Mapping checkpoint: format_version, model_state, optimizer_state, scheduler/scaler_state bila dipakai, epoch/global_step, tokens_seen, RNG Python/NumPy bila ada/torchCPU/CUDA, DataLoader/sampler state, resolved_config/hash, vocabulary/tokenizer hash, manifest/source hash, best_val_nll dan patience state. Save last/best di luar Git, checksum SHA256. Resume default batas epoch; mid-epoch hanya bila state sampler/worker diuji. State h/c tidak diteruskan antar training window. Ekspor inference model/config/tokenizer map/hash tanpa optimizer; loading checkpoint pihak tak tepercaya dilarang.

Seed init/shuffle/augmentation/worker/generation, dokumentasikan deterministic flags dan batas reproducibility lintas device/version. Sampling seed tidak menjamin byte-identical lintas library; bandingkan event canonical dan catat environment. Simpan token-level metric history, kurva train/val NLL/perplexity, failure log, actual time/memory dan source snapshot. Tidak ada skor dibuat pada task ini.

## Acceptance dan handoff

Setelah izin: shape dan shift/mask, CE pada PAD, finite gradient, overfit corpus kecil, reset/carry state, save/resume, vocabulary mismatch, grammar/export dan cap termination tests. Audit sequence raw serta post-mask; score listening/memorization mengikuti [EVALUATION](EVALUATION.md). Hentikan NaN/OOM/budget habis dan catat; jangan menyembunyikan retries. A2 menyerahkan manifest/tokenizer fixtures, A1 review gates/shape, A3 mengisi budget/run, A4 menyimpan prompt/error/analisis/hasil. Bukan izin mulai training.
