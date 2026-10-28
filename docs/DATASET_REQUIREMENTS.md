# Dataset Requirements Nirava MIDI

## Pilihan aktif

Pengguna memilih [Nottingham Dataset — MIDI/melody](https://github.com/jukedeck/nottingham-dataset/tree/master/MIDI/melody), repository `jukedeck/nottingham-dataset`, branch upstream `master`, pada 28 Oktober 2026. Scope data hanya berkas MIDI di folder itu; tidak otomatis memasukkan chord/accompaniment, folder lain, atau implementasi upstream. Belum ada dataset yang diunduh, diparse atau dipakai training. Speech Noise/Valentini tidak digunakan; riwayatnya ada pada [arsip speech](archive/speech-blueprint/docs/DATASET_REQUIREMENTS.md).

## Informasi sumber yang telah dibaca

[README upstream](https://github.com/jukedeck/nottingham-dataset/blob/master/README.md) menyatakan asal ABC dari Nottingham Music Database serta proses cleaning dan konversi MIDI. [Lisensi repository](https://github.com/jukedeck/nottingham-dataset/blob/master/LICENSE.md) dicantumkan sebagai GPLv3. Catatan cleaning merupakan provenance data; bukan alasan menyalin source implementasi atau menganggap isi MIDI tanpa kesalahan.

Pilihan sumber dan pembacaan metadata berbeda dari audit hak komposisi/arrangement, atribusi dan kebijakan penggunaan/redistribusi tim yang masih perlu diperiksa. Jangan menyatakan semua melodi public domain, semua penggunaan diperbolehkan, atau output bebas hak cipta hanya karena label lisensi repository.

## Kecocokan dan risiko

Folder melody selaras dengan tujuan model simbolik monofonik, namun monophony, meter, tuplets, event, PPQ, parse validity dan jumlah usable belum dibuktikan dengan inspeksi file. UI GitHub memotong listing direktori; jumlah file final harus diperoleh dari inventory pada revision yang dipin, bukan menghitung tampilan halaman.

Kontrak `nirava-midi-step-v1` tetap 4/4 dan grid16step/bar. A2 harus melaporkan sebaran meter dan quantization error serta jumlah/durasi karya yang tersisa setelah filter. Jangan mengganti label3/4 atau6/8 menjadi4/4, memotong tuplet diam-diam, atau mengklaim seluruh Nottingham diterima. Jika subset terlalu kecil/ritme rusak, konsultasikan revisi tokenizer/cakupan dengan A1/A3/dosen sebelum training; tidak mengubah kontrak sepihak.

File/versi/aransemen karya sama atau melodi transposisi harus berada pada split yang sama. Filename bukan bukti work identity dan hash byte tidak mendeteksi kesamaan musikal. Pengelompokan memanfaatkan metadata/tune identity bila tersedia ditambah similarity canonical, dengan unknowns dilaporkan. Split80/10/10 tetap target setelah inventory, bukan split resmi Nottingham yang sudah dibuktikan.

## Checklist Member 2

- [x] Sumber dan folder dipilih pengguna; URL serta README upstream ditinjau.
- [x] Pin commit SHA upstream dan tanggal akses: `0992bb6cd864f6d4b90d6663e08c0ef53ffaa08f` (commit 2017-03-03), diakses 28 Oktober 2026 via GitHub API. Manifest paths/hash ada di `reports/midi_manifest.csv`. Catatan: salinan lokal berasal dari ZIP, jadi kesamaan isi dengan SHA ini belum diverifikasi byte per byte. Bukti lisensi/atribusi masih perlu dilengkapi.
- [ ] Review hak komposisi/arrangement dan syarat training/redistribusi bersama tim/dosen, bukan sekadar label repository.
- [x] Inventory ukuran download/extract/cache, file/work/token count dan budget disk: 1034 file MIDI mentah (869 KB), 519 file ter-encode (288.368 steps / 289.406 tokens), 517 karya unik pada split final (414 train / 52 val / 51 test), 494 work groups, 2.753 windows tanpa augmentasi / 26.364 windows dengan train-only transposisi.
- [x] Audit PPQ/SMF type, pitched part/monophony, meter/tempo, pedal/bend, note pairing, parse failures dan aturan filter v1: Selesai penuh. SMF type 1 (100%), PPQ 1024 (100%), single pitched part (100%). Pitch-bend netral (8192) dan pedal off (<64) diterima; bend/pedal aktif ditolak. 501 ditolak non-4/4, 14 ditolak overlap grid. Detail di `reports/DATASET_AUDIT_REPORT.md` dan `reports/tokenizer_audit.csv`.
- [x] Ukur exclusions/quantization loss, tuplets dan kecukupan subset4/4; dokumentasikan distribusi yang hilang dan bias: Selesai. Mean quantization error 0.0051 langkah/file, max error 0.3359 langkah. 105 file memiliki event off-grid (>0.25 langkah; triplet/swing) yang dipetakan ke grid terdekat. Bias terdokumentasi: 79.4% reels, jigs/waltzes/slip jigs hilang (0% retained). Rekonsiliasi 515 (audit awal) vs 517 (split final) selesai didokumentasikan.
- [x] Audit exact/near duplicates, work/arrangement/transposition groups sebelum split dan sebelum windowing. Selesai: 494 work group (22 multi-file) via fingerprint interval invarian transposisi + Jaccard ≥0.25 + union-find. 2 exact duplicates dibuang. Detail di `reports/work_groups.csv`.
- [x] Bekukan work-disjoint split, manifest/hash dan tokenizer version; train-only augmentation, validation/test tidak dipakai tuning. Selesai: split 414/52/51 (80/10/10), seed 20261028, leakage 0 (diverifikasi terpisah). Augmentasi transposisi train-only ±5/+6. Manifest di `reports/split_manifest.csv`, tokenizer hash `21c0930e...`.
- [x] Uji canonical round-trip serta target shift/PAD/mask setelah implementasi diizinkan, kemudian handoff [DATA_CONTRACT](DATA_CONTRACT.md). Round-trip 519/519 lulus. Shift/PAD/mask diuji unit (34 tes lulus termasuk tes torch `int64[B,128]`). Handoff belum dilakukan secara formal kepada A3.

Semua bukti runtime/data tetap pending. Pemilihan dataset tidak membuka Stage2 atau memberi izin download/install/training; approval arsitektur dan gate [STAGE1_VALIDATION](STAGE1_VALIDATION.md) tetap berlaku.
