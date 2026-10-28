> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# Proposal model Nirava

TASK 01, 28 Oktober 2026. **Stage 1, GO tertunda; belum ada implementasi, training atau persetujuan dosen.**

Model utama yang diusulkan adalah **nirava-stft-cgan-v1**, conditional GAN STFT kompleks dengan PyTorch dasar, dirancang tim dan dilatih dari inisialisasi acak. Input noisy–clean mono 16 kHz, segmen awal 2 detik; G U-Net residual real–imaginer dan latent Gaussian, D patch kondisional, inverse iSTFT tanpa pretrained vocoder. DeepFilterNet hanya pembanding opsional berlabel, tidak memenuhi deliverable utama dari nol.

## Sumber spesifikasi

- [ML_ARCHITECTURE.md](ML_ARCHITECTURE.md): audit rubrik/from scratch, jaringan G/D, tabel shape, transform, reconstruction, trade-off dan asumsi hardware/data.
- [DATA_CONTRACT.md](DATA_CONTRACT.md): antarmuka Member 2, pasangan aligned, speaker split, lineage dan mixing fallback.
- [TRAINING_CONTRACT.md](TRAINING_CONTRACT.md): antarmuka Member 3, loss/loop, config/checkpoint, eksperimen, metrik dan reproducibility.
- [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md): kandidat Kaggle pengguna dan audit yang belum selesai.
- [LECTURER_APPROVAL.md](LECTURER_APPROVAL.md): proposal singkat dan konfirmasi dosen yang belum diterima.

Detail Member 1 terdahulu dipindahkan ke tiga kontrak di atas pada TASK 01; ini penataan sumber dokumentasi, bukan arsitektur baru yang telah diuji. Tidak menyalin implementasi eksternal. Alasan dan prompt dicatat di [LLM_INTERACTION_LOG.md](LLM_INTERACTION_LOG.md). Versi kontrak tetap v1 karena antarmuka numerik tidak berubah. Perubahan teknis berikutnya perlu review A1/A2/A3 dan versioning.
