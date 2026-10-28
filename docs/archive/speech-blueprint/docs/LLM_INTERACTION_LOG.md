> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# Log interaksi LLM

## TASK 01 — Nirava From-Scratch ML Architecture

Tanggal: 28 Oktober 2026. Peran A1; nama/NIM belum dipetakan. Branch awal main bersih, lalu beralih ke `dev/member-1-architecture` sebelum menulis file. Tidak ada perubahan pada branch lain, commit/push/merge. Panduan dosen dibaca ulang read-only dari DOCX Downloads pengguna; tidak ditemukan sebagai berkas repository. Ekspor/link chat asli sesi ini belum dilampirkan; A4 harus menyertakannya. Catatan berikut adalah ringkasan dengan kutipan instruksi, bukan klaim ekspor percakapan lengkap.

### Prompt dan batas pengguna

Judul asli: TASK 01 — Nirava From-Scratch ML Architecture. Role: Senior Machine Learning Architect & Vibe Coding Advisor. Konteks empat anggota, LLM-guided from scratch, stack Next.js/TypeScript–FastAPI/Python–PostgreSQL/PyTorch dan kandidat Kaggle Speech Noise Dataset. Instruksi teknis asli:

> 4. Replace the pretrained DeepFilterNet approach as the primary model proposal.
> 5. Design a lightweight Conditional GAN for speech denoising, built from scratch.
> 6. Explain the Generator, Discriminator, STFT representation, tensor shapes, reconstruction strategy, and proposed loss functions.
> 7. Define a clear data contract for Member 2: Mono audio at 16 kHz; Aligned noisy-clean pairs; Initial 2-second segments; Train/validation/test separation; Synthetic noise mixing fallback.
> 8. Define the model and training interface for Member 3.
> 9. Specify evaluation metrics, checkpoint format, and reproducibility requirements.
> 10. Document technical trade-offs, hardware assumptions, and questions requiring lecturer approval.

Instruksi awal1–3: cek branch sebelum perubahan, baca AGENTS/README/docs relevan dan ikuti panduan resmi. Deliverable yang diminta: ML_ARCHITECTURE, DATA_CONTRACT, TRAINING_CONTRACT, STAGE1_VALIDATION, ARCHITECTURE, DEVELOPMENT, AGENTS serta rekaman prompt/keputusan. Batas: dokumentasi saja, tanpa implementasi/training/download/fitur/dependency/pretrained utama/approval asumsi, tanpa perubahan main/branch anggota lain dan tanpa commit/push/merge otomatis. Prompt utuh termasuk expected output tetap pada percakapan asli untuk diekspor A4.

### Keputusan dan alasan

1. Pertahankan desain `nirava-stft-cgan-v1` yang sudah menggantikan DeepFilterNet sebagai utama; jangan memulai ulang desain atau mengklaim pretrained memenuhi rubrik. Panduan dosen tetap prioritas dan seluruh bobot utama baru.
2. Pindahkan detail model dari MODEL_PROPOSAL ke ML_ARCHITECTURE, bagian objective/loop/config/checkpoint ke TRAINING_CONTRACT, dan kontrak A2 dari DATASET_REQUIREMENTS ke DATA_CONTRACT. Dokumen lama tetap sebagai ringkasan/audit dengan tautan, untuk mencegah dua sumber yang menyimpang. Antarmuka numerik tidak berubah; versi v1 dipertahankan.
3. Pertahankan segmen32000/STFT257×251/pad272×256, latent dan residual RI/iSTFT. Tambahkan signature konseptual untuk G residual, D logit, transform/inverse serta utterance inference agar tanggung jawab caller jelas. Tidak ada implementasi signature.
4. Perjelas format checkpoint mapping/version, source snapshot ketika dirty, seed worker/latent stabil, lingkungan/determinism dan batas resume epoch. Ini acceptance rencana, bukan bukti reproducibility runtime.
5. Dataset/ukuran/lisensi/speaker/clean target dan hardware tetap unknown. Mixing fallback bersyarat; source grouping bukan bukti speaker-disjoint. Tidak memasukkan angka hasil/approval palsu.

### Verifikasi dan handoff

Review dimensi STFT/convolution memakai aritmetika, link lokal dan git diff/whitespace serta daftar file Markdown; bukan PyTorch tests. API dasar STFT/iSTFT diperiksa lewat dokumentasi resmi, tidak menyalin kode proyek luar. Tidak ada error training karena model belum dibuat. A2 diminta review audit/manifest/data contract, A3 review tensor/objective/config/budget, A4 menyertakan percakapan asli, alasan kelompok dan bukti verifikasi. Runtime, round-trip, gradient, kualitas, RAM/VRAM dan persetujuan dosen belum diverifikasi. Rekomendasi berikutnya TASK02 review bukti data/hardware/approval, bukan otomatis implementasi.

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
