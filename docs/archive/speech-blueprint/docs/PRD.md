> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# Product Requirements Document (draft)

## Outcome
Membantu pengguna memahami rekaman ucapan yang terganggu noise tanpa menjanjikan hasil sempurna.

## Persona
Mahasiswa yang merekam diskusi/kuliah; kreator yang merekam voiceover sederhana.

## User journey
Landing langsung ke workspace → pilih sampel atau upload → validasi → progress → hasil A/B → unduh → file dihapus sesuai retensi.

## MVP acceptance criteria
- Upload WAV dan MP3 valid; format lain ditolak dengan alasan jelas.
- Batas awal: 25 MB, durasi maksimal 120 detik (konfigurasi, perlu uji performa).
- Backend mengembalikan job ID + akses token rahasia; frontend polling status.
- Hasil dapat didengarkan dengan perbandingan waktu yang sepadan.
- Jika model gagal, tampilkan pesan aman, tidak menyimpan stack trace untuk user.
- Akses audio kedaluwarsa otomatis (target 24 jam sejak pembuatan). Penghapusan fisik dilakukan cleanup berkala dengan retry; metadata otorisasi minimal sementara mengikuti kebijakan tombstone di DATABASE_SCHEMA.md, masih tunduk persetujuan kampus.
- Aplikasi nyaman pada mobile dan desktop, keyboard accessible.

## Out of scope
Login, multi-tenant enterprise, batch upload, transkripsi, training melalui antarmuka pengguna, live mic streaming, billing, social sharing.

## Deliverable akademik wajib

Member 1 mengusulkan kontrak `nirava-stft-cgan-v1`: cGAN PyTorch pada komponen real–imaginer STFT, input training awal mono 16 kHz sepanjang 32000 sampel (2 detik), pasangan noisy–clean sejajar dan split speaker-aware. Rekonstruksi memakai iSTFT tanpa pretrained vocoder. Segmen training bukan batas upload produk; input panjang ditangani chunking offline di backend sesuai konfigurasi model. Kelayakan speaker/clean target dataset aktif belum terverifikasi.

Panduan dosen menjadi prioritas atas kebutuhan hackathon lama. Bukti yang dinilai terutama orisinalitas Vibe Coding, log interaksi, model/pelatihan dan kerja sama; polish aplikasi tidak menggantikan training.

Desain dan training model generatif dari inisialisasi acak, data pipeline berpasangan, loss/loop, eksperimen hyperparameter, grafik metrik valid, serta log LLM dan debugging masuk lingkup proyek. Training dilakukan offline setelah gate disetujui, tidak melalui endpoint produk. Lihat [proposal model](MODEL_PROPOSAL.md) dan [dataset pilihan pengguna](DATASET_REQUIREMENTS.md). DeepFilterNet pretrained saja tidak memenuhi kebutuhan ini. Semua hasil masih belum diukur.

## Success measures (belum ada hasil)
Job completion rate, median processing time, hasil uji intelligibility, MOS listening panel atau proxy evaluasi dengan keterbatasan dinyatakan.

## Open decisions
Penerimaan dosen untuk speech enhancement di luar contoh, model final, lisensi/isi mirror Kaggle, GPU/tenggat, batas durasi, lokasi deploy, kebijakan retensi, dan protokol evaluasi final. Rubrik resmi sudah dibaca; persetujuan belum ada.
