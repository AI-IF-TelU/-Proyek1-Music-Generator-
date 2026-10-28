# Dataset Requirements Nirava MIDI

**Belum ada dataset MIDI yang dipilih, diunduh atau diverifikasi.** Speech Noise Dataset Kaggle dan Valentini dibatalkan untuk produk aktif karena domainnya speech, bukan MIDI. Riwayat tersedia pada [arsip speech](archive/speech-blueprint/docs/DATASET_REQUIREMENTS.md).

A2 mencari kandidat MIDI kecil yang memiliki hak training/penelitian dan melodi monofonik memadai; nama dataset atau ukuran jangan diasumsikan. Pilih berdasarkan lisensi komposisi dan arrangement/file, provenance, work grouping dan kualitas, bukan hanya jumlah unduhan. Publik tersedia tidak berarti izin redistribusi atau output bebas hak cipta. Tidak memerlukan paired audio, sample rate, speech speaker ID atau synthetic noise mixing.

## Checklist untuk proposal dataset

- [ ] URL/version/attribution, syarat penggunaan/training/redistribusi MIDI dan status hak komposisi/arrangement.
- [ ] Ukuran download/extract/token cache/checkpoint, file/work/composer count dan budget disk/bandwidth.
- [ ] Inventory PPQ, SMF type, instrument/meter/tempo, monophony, pedal/bend dan parse failures sesuai tokenization v1.
- [ ] Exclusions/quantization loss serta kecukupan melodi setelah filter, bukan menghitung semua file sebagai usable.
- [ ] Exact/near duplicate dan karya/arrangement family; work-disjoint split serta transposition lineage.
- [ ] Manifest/hash, fixed vocabulary/tokenizer, train-only augmentation dan test freeze.
- [ ] Fixture round-trip canonical dan batch/shift/mask untuk A1/A3 setelah implementasi diizinkan.

Handoff memakai [DATA_CONTRACT](DATA_CONTRACT.md); semua kotak terbuka. Tanpa corpus sah/cukup, jangan mulai training atau mengganti dengan pretrained.
