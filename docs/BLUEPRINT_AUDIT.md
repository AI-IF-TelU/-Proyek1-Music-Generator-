# Blueprint Audit Nirava MIDI Pivot

28 Oktober2026, dokumentasi saja, branch dev/member-1-architecture. Stage1 **PIVOT MIDI / GO tertunda**. Penugasan MIDI String Generator disampaikan pengguna; LSTM dan scope belum dinyatakan disetujui dosen.

## Temuan domain lama dan tindakan

| Rancangan speech yang usang | Pengganti MIDI aktif |
|---|---|
| Speech restoration/Keep the voice. Lose the noise. | Nirava MIDI Music Generator, tagline speech dihentikan |
| DeepFilterNet/cGAN/STFT/iSTFT, paired mono16kHz/2detik | Random-init autoregressive LSTM, vocabulary133 step tokens |
| Kaggle Speech Noise/Valentini, clean-noisy mixing, speaker split | Dataset MIDI belum dipilih, legalitas komposisi/arrangement dan work split |
| Upload WAV/MP3, enhancement/A-B/download WAV | Parameter generation/status/note-grid/download .mid |
| STOI/PESQ/SI-SDR/phoneme preservation | Raw NLL/perplexity, grammar/export, musikalitas, repetition/memorization |
| Enhancement API/table/audio keys/sample-rate metadata | Proposal generation API/metadata/MIDI storage, belum migrasi |
| Data pipeline dan training dua optimizer G/D | Canonical tokenizer/windows dan next-token CE LSTM |

## Preservation untuk review

Seluruh19 Markdown sebelum pivot (README, AGENTS dan18 docs) disalin ke [archive/speech-blueprint](archive/speech-blueprint/README.md), hierarki root/docs dipertahankan dan tiap berkas ditandai arsip. Isi lama tetap tersedia; tidak menghapus berkas tanpa review. Arsip bukan kontrak aktif atau otorisasi coding. Log interaksi aktif mempertahankan riwayat dan menambahkan sesi pivot. Git history tetap utuh; tidak commit/push/merge dalam task ini.

Dokumen aktif diperbarui: AGENTS/README, PRD, STAGE1_VALIDATION, ARCHITECTURE, ML_ARCHITECTURE, DATA_CONTRACT, TRAINING_CONTRACT, DATASET_REQUIREMENTS, EVALUATION, DEVELOPMENT, TEAM_RESPONSIBILITIES, LECTURER_APPROVAL, MODEL_PROPOSAL, DESIGN_SYSTEM, API_SPEC, DATABASE_SCHEMA, audit ini dan LLM_INTERACTION_LOG. MIDI_TOKENIZATION ditambahkan. Perubahan API/skema hanya spesifikasi pengganti, tanpa endpoint, database atau migrasi aktual.

## Kesesuaian panduan dan keputusan

Model/embedding/gates/training dari nol menggunakan operasi dasar PyTorch, LLM prompts dan review tim. Dilarang menyalin source eksternal. Empat peran tetap sesuai job desk. Rubrik terdahulu30%orisinalitas,25%log,25%model/training,20%tim menjadi fokus; referensi hackathon tidak menggantikan bukti. Belum ada nilai yang dicapai. Penugasan MIDI yang diberikan pengguna mengatasi mismatch domain, bukan usia kategori atau kecukupan LSTM; perlu konfirmasi dosen.

Trade-off: token grid monofonik memudahkan decode tetapi membuang polyphony/dynamics/rubato. Manual LSTM memberi bukti desain namun lambat dan konteks terbatas. Fixed-length grammar membantu export tetapi tidak membuktikan learned EOS; log raw invalid probability dan forced termination. Dataset kecil berisiko memorization/hak cipta; ekspor valid bukan lisensi orisinalitas.

## Risiko dan verifikasi

Corpus/lisensi/ukuran/monophony, duplicate families, perangkat/budget, penerimaan LSTM lama dan kompleksitas, kualitas ritme/variasi, error parsing/quantization, privacy/retention serta approval/demo masih terbuka. Tidak ada download/install/model/training/fitur atau hasil empiris. Pemeriksaan task meliputi link lokal, preservasi arsip, vocabulary/shape aritmetika, diff/whitespace, branch refs dan pencarian istilah speech tersisa sebagai referensi historis. Runtime/parse/round-trip/loss/gradient belum diuji dan tidak dinyatakan lulus.

## Pembaruan setelah pivot: sumber MIDI dipilih

28 Oktober 2026: pengguna memilih Nottingham `jukedeck/nottingham-dataset`, folder MIDI/melody. Pernyataan dataset belum dipilih pada tabel pivot di atas adalah status historis saat pivot, bukan status terkini. Sumber sudah dipilih, audit isi/lisensi/work-split/grid dan pin SHA masih pending; lihat DATASET_REQUIREMENTS. Tidak mengubah kontrak model/token atau status Stage1, tidak download/implementasi/commit/push pada pembaruan sumber ini.
