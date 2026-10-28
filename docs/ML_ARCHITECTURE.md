# ML Architecture Nirava MIDI LSTM

Kontrak **nirava-midi-lstm-v1**, Stage1 proposal 28 Oktober2026. Domain MIDI String Generator ditetapkan pengguna sebagai penugasan dosen. Itu tidak berarti arsitektur/hyperparameter ini telah disetujui. Model mempelajari p(token_t | prefix) dari MIDI canonical [MIDI_TOKENIZATION.md](MIDI_TOKENIZATION.md); tidak ada GAN, STFT, audio decoder atau pretrained utama.

## LSTM dari nol

Embedding learned V133→E64; dua lapis sel LSTM unidirectional hidden128, linear head128→133. Sel diusulkan ditulis tim dengan operasi Linear/tensor PyTorch/autograd: a_t=W_x*x_t+W_h*h_prev+b, pecah menjadi i,f,g,o; i/f/o=sigmoid, g=tanh; c_t=f*c_prev+i*g; h_t=o*tanh(c_t). W_x berbentuk[512,input_dim], W_h[512,128], bias[512]. Lapisan1 menerima64, lapisan2 menerima128. Initial h/c nol per window/piece, bukan state dari piece lain. Tidak bidirectional karena inference tidak melihat masa depan.

Semua embedding/weights diinisialisasi baru (usulan uniform/normal kecil, forget bias1, bias lain0), seed dan metode dikunci config. Tim menulis recurrence/stack/forward/sampling sendiri melalui prompt beralasan. nn.LSTM boleh dibandingkan untuk cek API hanya bila dosen mengizinkan, bukan primary implementasi otomatis. [Dokumentasi PyTorch LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html) rujukan fungsi dasar dan persamaan, bukan sumber kode proyek. Tidak memakai pretrained embeddings atau model music siap pakai.

| Interface | Bentuk/tipe |
|---|---|
| tokens input / targets | int64[B,T], T awal128 |
| embedding | float32[B,T,64] |
| h0,c0 dan state keluaran | masing-masing float32[2,B,128] |
| recurrent output | float32[B,T,128] |
| logits | float32[B,T,133], tanpa softmax saat CE |
| generate_step | token int64[B,1], state[2,B,128] → logits[B,1,133], state baru |

Batch contract [DATA_CONTRACT.md](DATA_CONTRACT.md); objective, checkpoint dan eksperimen [TRAINING_CONTRACT.md](TRAINING_CONTRACT.md). Ganti state hanya pada sampel valid; right PAD tidak memengaruhi loss dan state terakhir valid dipilih bila diperlukan. Training window di-reset; generation state dibawa antar token dalam satu piece. Teacher forcing membedakan training dengan sampling bebas, sehingga exposure bias harus dievaluasi.

## Sampling dan reconstruction

Mulai BOS, state nol, sample autoregresif memakai grammar/temp/top-k/seed, hentikan sesuai mode/cap. Token musik di-decode ke event dengan note-off dan tick yang valid, lalu serialize SMF .mid dan parse ulang; detail tunggal ada di MIDI_TOKENIZATION. Tidak menyintesis WAV; piano-roll/DAW playback bukan ML inference. Fixed-length default memakai forced EOS yang diberi label, bukan mengklaim model belajar struktur lagu lengkap.

## Trade-off dan pertanyaan

Manual LSTM menunjukkan pemahaman recurrence tetapi loop Python mungkin lambat; dua layer128 adalah target kecil yang belum diprofil. GRU lebih sederhana namun bukan pilihan yang diminta; Transformer memperluas konteks dengan biaya/kompleksitas lebih besar; tidak perlu keduanya untuk MVP. Grid monofonik kehilangan chord, dynamics dan rubato. Hidden state kecil berisiko repetisi/kurang struktur; data kecil berisiko memorization.

LSTM berasal dari keluarga lama; kecocokan dengan kriteria kategori10tahun terakhir pada panduan terdahulu belum jelas. Minta dosen menerima LSTM sebagai baseline tugas MIDI dan menetapkan kompleksitas yang diharapkan; jangan mengklaim LSTM arsitektur baru. Penugasan domain dari pengguna adalah fakta konteks, approval model belum ada.

Hardware belum diketahui: CPU/GPU, RAM/VRAM, OS/Python/PyTorch, jam training dan tenggat. Jangan mengklaim muat/cepat dari ukuran hidden saja. Benchmark parameter/time/token/peak memory setelah izin. Dataset MIDI, jumlah works/composer, lisensi dan proporsi monofonik belum tersedia. [Approval](LECTURER_APPROVAL.md), [gate](STAGE1_VALIDATION.md) tetap terbuka.
