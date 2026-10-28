# Log interaksi LLM

## Sesi Member 1 — finalisasi arsitektur

Tanggal28 Oktober2026; peran Member1 Prompt Engineer & LLM Navigator, nama/NIM belum tersedia. Branch `dev/member-1-architecture` dibuat dari main tanpa commit; seluruh perubahan terdahulu dipertahankan. Ringkasan ini perlu dilengkapi ekspor/link chat asli oleh Member4; bukan pengganti bukti percakapan lengkap.

### Prompt pengguna yang menjadi dasar keputusan

Judul asli: TASK MEMBER 1 — Finalize Nirava ML Architecture. Instruksi utama yang direkam:

> The official lecturer requirements take priority over the previous hackathon blueprint.
>
> 1. Audit the current ML architecture against the lecturer's from-scratch requirement.
> 2. Propose a lightweight Conditional GAN architecture for speech enhancement using PyTorch.
> 3. Define the generator and discriminator architecture, STFT representation, expected tensor shapes, output reconstruction, and proposed loss functions.
> 4. Define the data interface required from Member 2: Mono 16 kHz; Aligned noisy-clean pairs; Initial 2-second segments; Speaker-aware train/validation/test separation; Dataset audit and synthetic mixing fallback.
> 5. Define the training interface for Member 3, including checkpoints, experiment configurations, and evaluation metrics.
> 6. Identify the hardware and dataset assumptions that still require verification.
> 7. Update AGENTS.md, ARCHITECTURE.md, PRD.md, DEVELOPMENT.md, and other relevant documentation.
> 8. Prepare an architecture proposal for lecturer approval.
> 9. Record the prompt, technical decisions, and reasoning so Member 4 can maintain the required LLM interaction log.

Batas pengguna: jangan implementasi training/download data/fitur aplikasi/install dependencies, pretrained utama atau asumsi approval; hanya tanggung jawab Member1, stack tetap, tanpa commit/push. Bagian konteks dan prompt lengkap tetap ada pada percakapan asli yang belum diekspor.

### Keputusan dan alasan teknis

- `nirava-stft-cgan-v1` menggantikan Conv1D waveform1,024detik dengan RI-STFT U-Net Conv2d untuk segmen2detik. Alasan: input/output spektral eksplisit, peluang koreksi fase, inverse tanpa pretrained vocoder. Risiko: inconsistency/artefak fase dan training GAN belum terbukti.
- FFT512/hop128/Hann, center/constant pad;257×251→pad272×256 agar empat downsampling tepat. Real/imaginary dibagi sqrt512 tetap, bukan normalisasi dataset/test. iSTFT panjang eksplisit dan projection lewat STFT hasil audio menyamakan representasi D real/fake.
- Kanal16/32/64/128, GroupNorm dan latent Gaussian bottleneck mengusulkan kapasitas kecil untuk batch4. Ini tujuan resource, bukan benchmark. D patch kondisional dan BCEWithLogits dengan L1 RI/waveform/MR-STFT mengikat fidelity sekaligus adversarial objective. Latent bisa diabaikan; perlu audit sensitivitas.
- Kontrak `nirava-data-v1` memasok waveform aligned, lineage/manifest dan split speaker-aware sebelum crop/mixing. Jika ID speaker tidak diketahui, gap tidak boleh ditutup dengan klaim speaker-disjoint palsu.
- Panduan dosen diprioritaskan: heuristik kompetisi/referensi desain bukan blocker akademik mandiri. Stage1, approval domain dan izin pilot tetap berlaku.

### Hambatan tooling dan verifikasi

Pembuatan branch pertama gagal karena izin menulis Git refs; percobaan dengan akses yang sesuai berhasil. Pembacaan DOCX awal gagal karena file sedang dibuka proses lain; berhasil dibaca read-only dengan FileShare.ReadWrite, tanpa menutup aplikasi atau mengubah DOCX. Ini hambatan tooling, bukan error training/model. Tidak ada pesan error notebook yang direkayasa.

Verifikasi task hanya review statis shape/kontrak, hitung dimensi convolution, diff/whitespace dan link Markdown lokal. Round-trip PyTorch, gradient, RAM/VRAM, training dan metrik belum dijalankan. Member4 harus menyertakan output verifikasi aktual dan ekspor sesi sebelum laporan final; semua anggota tetap menganalisis keputusan, bukan menganggap jawaban LLM sebagai validasi empiris.

## Perubahan pilihan dataset 28 Oktober 2026

Pengguna mengganti Kaggle muhmagdy/valentini-noisy karena terlalu besar dengan abdullahhaydarkadolu/speech-noise-dataset. Halaman baru dibuka tetapi metadata/file tidak terbaca melalui alat web; ukuran, lisensi dan struktur belum dikonfirmasi. Dokumentasi aktif diperbarui tanpa download/instalasi/training. Pairing langsung atau mixing clean speech + noise masih bergantung inventory; tidak mengasumsikan test/speaker VoiceBank. Catatan sesi terdahulu dipertahankan sebagai riwayat. Ekspor percakapan asli tetap perlu dilampirkan.

Panduan dosen §1 dan §5 mewajibkan rekaman chat (share link aktif atau ekspor Markdown/PDF) serta log setiap pembuatan kode/debugging. Ringkasan ini bukan pengganti ekspor kronologi lengkap. Jangan merekayasa error atau sesi yang tidak terjadi; hapus rahasia/token/audio pribadi sebelum membagikan log, dengan redaksi ditandai.

## Catatan sesi TASK 00C

- Tanggal: 28 Oktober 2026; pelaksana: assistant dengan arahan pengguna, nama anggota belum dipetakan.
- Tujuan: audit blueprint, model from scratch, dan penyelarasan dengan panduan dosen; pengguna memilih Kaggle muhmagdy/valentini-noisy dan memberikan path panduan di Downloads.
- Alasan: blueprint awal mengecualikan training dan mengutamakan aplikasi, sementara proyek mensyaratkan model dari nol.
- Tindakan: membaca seluruh 11 Markdown awal, mengekstrak isi panduan DOCX termasuk tabel rubrik, membaca sumber primer model/dataset, memperbarui dokumentasi saja.
- Hasil: kandidat cGAN dan alternatif DDPM, checklist dataset, job desk empat anggota, milestone training-first dan checklist approval. Tidak ada kode model, instalasi, training, atau hasil benchmark.
- Debugging model: tidak berlaku; belum ada model/error notebook. Keterbatasan sumber: isi Kaggle tidak terbaca melalui alat web; metadata mirror belum diverifikasi.
- Bukti chat: **belum dilampirkan**; ekspor percakapan asli atau tambahkan share link sebelum pengumpulan. Catatan ini tidak mengklaim kelengkapan 25% rubrik log.

## Template setiap sesi berikutnya

- ID sesi, tanggal, anggota, target modul, model/provider LLM bila diketahui, tautan chat atau lokasi ekspor.
- Prompt asli dan alasan desain; respons LLM/rujukan ekspor, bagian diterima/ditolak serta analisis anggota.
- Error asli lengkap beserta perintah, environment, input reproduksi dan expected/actual; jika tidak ada error tulis tidak berlaku.
- Prompt perbaikan, hipotesis penyebab, solusi yang dipilih dan alasan; jangan menganggap jawaban LLM otomatis benar.
- Verifikasi aktual: perintah tes, hasil, keterbatasan, commit/diff terkait, reviewer dan isu tersisa.
- Optimasi: config/run sebelum–sesudah, metrik aktual dan alasan keputusan; bedakan usulan dengan hasil.

## Catatan sesi lanjutan TASK 00B dan review TASK 00C

- Tanggal: 28 Oktober 2026; identitas anggota tetap belum dipetakan.
- Permintaan: menyiapkan closure Stage 1 dan meninjau kembali kesesuaian blueprint dari nol tanpa menduplikasi dokumentasi atau implementasi.
- Tindakan: membaca 16 Markdown yang tersedia dan membaca ulang isi panduan DOCX dari Downloads secara read-only; menelaah sumber primer DeepFilterNet; menambah checklist B1–B10, pilot 3–5 rekaman, ambang usulan, scope dan task berikutnya pada dokumen yang ada.
- Analisis: DeepFilterNet layak sebagai baseline enhancement tetapi pretrained tidak memenuhi from scratch; prediksi gain/filter bukan otomatis generative modeling. Ada konflik urutan bukti empiris pra-GO dengan larangan coding pra-GO; izin pilot terbatas harus eksplisit dan belum tersedia.
- Hasil: rencana siap ditinjau, bukan bukti pilot/training atau approval. Tidak ada error model sehingga debugging model tidak berlaku. Ekspor/link percakapan asli sesi ini masih harus dilampirkan; ringkasan ini tidak menggantikannya.
- Verifikasi: diff/whitespace, link lokal dan review batas perubahan Markdown. Tidak menjalankan runtime/lint/typecheck untuk task dokumentasi.
