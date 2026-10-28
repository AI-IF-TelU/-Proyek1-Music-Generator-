# Data Contract Nirava MIDI

Versi **nirava-midi-data-v1**, pemilik A2, review A1/A3. Stage1, belum download/implementasi. Input berupa MIDI berizin; tidak memakai dataset Speech Noise atau pasangan noisy-clean.

## Pipeline

Audit sumber/lisensi → parse aman dan inventory → deduplicate file serta canonical event sequence → kelompokkan work/composition/arrangement family → split train/validation/test → canonicalize/tokenize → window per piece → batch. Aturan parse/filter/quantization dan ID tetap pada [MIDI_TOKENIZATION.md](MIDI_TOKENIZATION.md). Jangan concat pieces tanpa boundary atau split window sebelum mengelompokkan karya.

Target rasio80/10/10 per work group bila inventory cukup; jumlah karya/composer/durasi/token tiap split dicatat, bukan memaksa split dari corpus terlalu kecil. Arrangement/transposition/duplikat near-identical dari karya sama harus satu split. Composer-disjoint optional sebagai evaluasi generalisasi terpisah, bukan klaim otomatis. Hash file saja tidak mendeteksi arrangement. Semua augmentasi train-only setelah split; transposition opsional hanya jika pitch tetap0..127 dan parent lineage tercatat. Validation/test tidak diacak ulang/ditranspose saat model selection.

Canonical stream [BOS,steps,EOS]. Bentuk window x=s[start:start+128], y=s[start+1:start+129], stride128, sehingga tiap target posisi piece diliput sekali; terakhir right-PAD ke128. BOS hanya start0, EOS sekali; setelah EOS tidak ada target valid. Window tidak melintasi piece, state training reset tiap window. HOLD awal window sah karena crop dari piece, bukan berarti boleh start generation dengan HOLD. Jangan menyisipkan BOS palsu pada crop.

| Field | Bentuk/ketentuan |
|---|---|
| input_ids / target_ids | int64[B,128], IDs0..132 |
| loss_mask | bool[B,128], true untuk target non-PAD termasuk EOS |
| lengths | int64[B], jumlah target valid1..128 |
| piece_id/work_group_id/split | metadata B item, trace ke manifest |
| window_start/parent_hash | offset token dan provenance |

A2 menyerahkan token ID canonical, bukan embeddings/one-hot atau MIDI bytes sebagai input model. Vocabulary fixed133 tidak dipelajari dari test. Train/validation/test terpisah storage manifest; tokenizer ID/version/hash sama. A3 wajib menolak mismatch, sequence kosong atau target shift salah.

## Manifest dan acceptance

Manifest: source URL/version/attribution/license, file SHA256, opaque piece/work/composer IDs bila tersedia, arrangement/duplicate group, SMF format/PPQ/instruments/polyphony/meter/tempo, filter/quantization decisions, note count/length, tokens hash/tokenizer version, split dan exclusion reason. File copyrighted/private tidak di Git. Laporkan exclusions dan bias monophonic filtering; jangan menyebut dataset representatif tanpa audit.

A2 perlu membuktikan parse→canonical tokens→export→parse ekuivalen onset/pitch/duration canonical, split leakage nol yang terdeteksi, token grammar benar dan target shifting/mask benar. Ini tes yang direncanakan setelah izin, belum lulus. Bila corpus legal/monofonik tidak cukup, hentikan dan konsultasi scope/data; jangan membuat metadata atau approval palsu.

## Sumber Nottingham yang dipilih pengguna

Folder aktif hanya [jukedeck/nottingham-dataset/MIDI/melody](https://github.com/jukedeck/nottingham-dataset/tree/master/MIDI/melody). Pin upstream commit dalam manifest sebelum ingest; data belum diunduh. A2 menambahkan upstream relative path, revision dan work/tune grouping evidence pada metadata, serta memisahkan alasan reject meter/polyphony/quantization.

Kontrak tensor/vocabulary tetap v1. Folder melody tidak membuktikan semua file memenuhi monophony4/4/grid; A2 melaporkan retained count/durasi dan distribusi meter. Revisi kontrak jika data tidak cukup harus direview A1/A3/dosen, bukan relabel meter diam-diam. Rujukan audit/lisensi dan checklist ada pada [DATASET_REQUIREMENTS](DATASET_REQUIREMENTS.md).
