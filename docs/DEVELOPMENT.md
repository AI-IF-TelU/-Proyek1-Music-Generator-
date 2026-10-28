# Development Nirava MIDI roadmap

Stage1, dokumentasi saja. Semua milestone implementasi berikut bersyarat izin; tidak ada hasil training.

1. M0 review pivot: dosen menilai LSTM manual/kompleksitas/usia kategori, tokenizer dan scope monofonik; tim mengisi identitas/hardware/jadwal; A4 menyimpan percakapan asli. Verdict GO dan persetujuan demo/pilot terpisah sesuai STAGE1_VALIDATION.
2. M1 setelah izin: A2 audit corpus MIDI legal, parse/filter/dedup/work split, canonical tokenizer dan round-trip fixtures; A1/A3 review data interface. Hentikan jika data tidak cukup/hak tidak jelas.
3. M2 setelah izin: A1/A3 membangun embedding/sel LSTM/forward/loss dan shifted-token loader melalui prompt; uji shape/gradient/PAD/state reset, tiny overfit dan checkpoint/resume; profil memori/time sebelum sweep.
4. M3 A3 eksperimen terkontrol, validation selection lalu test frozen, sampling/grammar/export/listening dan memorization audit. A4 kompilasi curve/run gagal dan penjelasan kelompok.
5. M4 hanya setelah model layak: Next.js parameter/status/note-grid/download, FastAPI secure generation lifecycle/export, PostgreSQL metadata/Alembic, expiry/cleanup. Tidak membangun aplikasi untuk menutupi ketiadaan training.
6. M5 demo MIDI nyata, laporan metode/loss/eksperimen/metrik, ekspor LLM, bukti4anggota, batasan dan presentasi individu. Deployment bila diperlukan/diotorisasi.

Definition of done: model tim dilatih dari nol, corpus/split/lineage sah, file valid dan limitation transparan, log nyata dan tes relevan, tidak ada secrets/weights/copyrighted data di Git. NLL/perplexity dan sampling results belum tersedia. Stack aplikasi tetap; pipeline speech tidak dilanjutkan. Rencana detail mengikuti ML_ARCHITECTURE, DATA_CONTRACT, TRAINING_CONTRACT dan EVALUATION.

## Pembaruan sumber data

Nottingham `MIDI/melody` telah dipilih pengguna; M1 kini mengaudit sumber tersebut, bukan mencari corpus tanpa pilihan. Belum ada download/parse. Prioritaskan pin SHA, hak data, work grouping serta filter4/4/quantization sebelum menyetujui subset dan budget training. Lihat [DATASET_REQUIREMENTS](DATASET_REQUIREMENTS.md).
