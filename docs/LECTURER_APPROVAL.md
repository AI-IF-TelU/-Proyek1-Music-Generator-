# Lecturer Approval Nirava MIDI

Usulan: **Nirava — MIDI Music Generator**, next-token autoregressive melodi monofonik. Vocabulary133 NOTE/HOLD/REST + special tokens pada grid16step/bar. Embedding64, dua sel LSTM manual hidden128, linear head133, CE next-token. Semua weights baru melalui LLM-guided development. Output MIDI piano satu track via decoder tim tanpa waveform processing. Next.js/FastAPI/PostgreSQL tetap.

Penugasan Generative Audio & Sequence/MIDI String Generator diberikan pengguna. Panduan terdahulu menekankan model dari nol, log, orisinalitas dan empat peran; penugasan domain tidak mengesahkan spesifikasi berikut.

- [ ] LSTM manual dengan PyTorch Linear/tensor/autograd memenuhi from scratch dan tingkat kompleksitas.
- [ ] Penggunaan keluarga LSTM lama diterima atau syarat kategori10tahun perlu penyesuaian; belum ada keputusan.
- [ ] Monofonik, fixed4/4/120BPM/velocity80, NOTE/HOLD/REST dan quantization lossy memenuhi tugas.
- [ ] Dataset MIDI beserta hak komposisi/arrangement, filtering dan work-disjoint split diterima; Nottingham MIDI/melody telah dipilih, tetapi audit hak data, work grouping dan subset sesuai tokenizer belum selesai.
- [ ] CE/NLL/perplexity, ablation/sweep, sampling/raw validity versus grammar, listening dan memorization audit memadai.
- [ ] Bentuk ekspor/link LLM, error analysis, kontribusi4anggota dan bukti training memadai.
- [ ] Hardware/time budget/tenggat dan urutan pilot/GO diputuskan tanpa izin coding tersirat.

Detail [model](ML_ARCHITECTURE.md), [token](MIDI_TOKENIZATION.md), [data](DATA_CONTRACT.md), [training](TRAINING_CONTRACT.md), [evaluasi](EVALUATION.md). Tanggal/nama dosen/keputusan/bukti konsultasi: belum ada. Tidak menghubungi dosen pada task ini; persetujuan pengguna atas demo concept dan verdict GO tetap terpisah.
