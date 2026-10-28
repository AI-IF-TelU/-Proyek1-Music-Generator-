# Model Proposal Nirava MIDI

Stage1, proposal belum disetujui. Model utama **nirava-midi-lstm-v1**: embedding64 → dua sel LSTM manual hidden128 → logits133, next-token CE, semua weights baru. Output token `nirava-midi-step-v1` direkonstruksi menjadi MIDI monofonik; tidak memakai pretrained, cGAN, STFT atau speech corpus.

Sumber tunggal: [ML_ARCHITECTURE](ML_ARCHITECTURE.md), [MIDI_TOKENIZATION](MIDI_TOKENIZATION.md), [DATA_CONTRACT](DATA_CONTRACT.md), [TRAINING_CONTRACT](TRAINING_CONTRACT.md). [Approval](LECTURER_APPROVAL.md) dan [gate](STAGE1_VALIDATION.md) masih terbuka. LSTM ringan adalah hipotesis desain; runtime/memory/kualitas belum diukur. Alternatif event token/GRU/Transformer memerlukan scope/budget baru, bukan pekerjaan yang sudah dijalankan.
