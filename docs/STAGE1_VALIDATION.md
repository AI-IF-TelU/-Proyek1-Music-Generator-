# Stage 1 Nirava MIDI validation

**Verdict: PIVOT MIDI / GO tertunda.** Penugasan domain MIDI String Generator diberikan pengguna pada28Oktober2026; bukan approval arsitektur, data atau implementasi. Blueprint speech serta blocker speechnya dipertahankan di [arsip](archive/speech-blueprint/docs/STAGE1_VALIDATION.md), tidak menjadi gate aktif.

## Blocker aktif dan bukti

- [ ] A1: konfirmasi dosen atas LSTM manual, tingkat kompleksitas, batas operasi PyTorch dan kecocokan kriteria usia10tahun dengan keluarga LSTM lama. Jangan mengklaim kategori baru.
- [ ] A2: kandidat MIDI legal dan cukup monofonik, ukuran/hak komposisi+arrangement, work duplicate groups, split/quantization dan tokenizer audit. Nottingham MIDI/melody telah dipilih pengguna; belum diunduh atau diaudit. SHA upstream, lisensi/hak data, meter/grid dan kecukupan subset4/4 masih perlu diverifikasi.
- [ ] A1/A2/A3: review kontrak tokenizer133, state/logits, target shift/PAD, export dan limitation fixed tempo/velocity/grid.
- [ ] Tim: nama/NIM4anggota, hardware RAM/VRAM/disk, budget training/time, tenggat dan host inference.
- [ ] A4/semua: ekspor/link chat nyata, kontribusi/review dan error+solusi bila ada; template bukan bukti lengkap.
- [ ] Dosen/tim: setujui rencana ablation, NLL/perplexity, grammar/export, sampling/listening/memorization dan profiling tanpa hasil rekaan.
- [ ] Pengguna: setujui demo concept parameter→generate→note-grid/download, privacy/retention dan gate implementasi.
- [ ] Keputusan GO bertanggal, menautkan bukti di atas dan persetujuan eksplisit pengguna sebelum Stage2; belum tersedia.

## Urutan bukti tanpa deadlock

Gate saat ini tidak mengizinkan kode/training. Jika diperlukan bukti pilot sebelum GO, pengguna harus memberi izin offline terbatas dengan budget/stop condition; pilot tidak otomatis membuka pengembangan aplikasi. Kebutuhan pilot empiris pra-GO versus feasibility berbasis rencana harus dikonfirmasi dengan dosen/pengguna, bukan diam-diam diputuskan oleh task dokumentasi. Setelah izin, training/evaluasi nyata mengikuti roadmap, tidak mengubah rencana menjadi hasil.

Kriteria speech lama (3–5 noisy recordings, STOI/PESQ, sample rate, cGAN/pairing, legalitas Kaggle speech) tidak lagi berlaku. Riset kompetitor/pemenang/design heuristic bukan syarat rubrik resmi. Domain MIDI kini sesuai contoh yang diberikan pengguna, namun penerimaan model/kompleksitas tetap terbuka. Nama Nirava tetap; tagline speech dihentikan, pemeriksaan merek belum dilakukan.

Next task: review proposal MIDI bersama dosen dan intake bukti dataset/hardware oleh A2/A3/A4. Tidak download/install/model implementation pada task berikutnya tanpa otorisasi yang sesuai.
