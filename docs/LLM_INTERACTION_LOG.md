# Log LLM Nirava MIDI pivot

## Sesi TASK 01 Pivot Nirava to MIDI String Generator

Tanggal28Oktober2026; role ML Architecture Advisor/Member1. Pengguna menyatakan penugasan resmi: “Generative Audio (MIDI String Generator): Model mengenerate rangkaian nada musik tanpa pemrosesan berkas biner .wav yang berat.” Bukti konteks ini berasal dari pengguna, bukan approval arsitektur. Panduan DOCX dari sesi sebelumnya mendasari rubrik; tidak mengklaim konsultasi baru dengan dosen.

### Prompt dan batas pengguna

Instruksi utama TASK01 yang menjadi dasar perubahan:

> 1. Review all existing Nirava Markdown documentation.
> 2. Identify outdated Speech Denoising requirements.
> 3. Update the project scope to MIDI String Generation.
> 4. Propose a lightweight LSTM architecture and token representation.
> 5. Define a dataset interface for Member 2.
> 6. Define a training interface for Member 3.
> 7. Update the roadmap and four-member task responsibilities.
> 8. Ensure the design meets the lecturer's from-scratch and Vibe Coding requirements.
> 9. Document architecture decisions and technical trade-offs.

Konteks: Nirava MIDI Music Generator, autoregressive MIDI, LSTM PyTorch dari nol, data MIDI/output.mid, stack Next.js/FastAPI/PostgreSQL. Batas: dokumentasi saja, tanpa kode/download/copy implementation/pretrained, jangan hapus dokumen lama tanpa review, jangan ubah main/branch anggota lain atau commit/push/merge otomatis, jangan klaim performa tanpa eksperimen. Expected deliverables: PRD/blueprint/token/input-output/training/evaluasi/AGENTS dan handoff A2/A3/A4. Prompt utuh serta semua respons/tool results harus diekspor A4; kutipan/ringkasan ini bukan bukti chat lengkap.

### Keputusan dan alasan

- Branch main awal bersih; beralih ke dev/member-1-architecture sebelum menulis. Tidak memperbarui refs main/anggota lain.
- Simpan seluruh19 Markdown lama dengan hierarki dan banner arsip; ganti dokumen aktif agar kontrak speech tidak dijalankan setelah pivot.
- Grid monofonik16step/bar, token NOTE0..127/HOLD/REST plus PAD/BOS/EOS, V133. Lebih sederhana dari event MIDI umum tetapi tidak memodelkan chord/dynamics/rubato. Konfirmasi dosen diperlukan.
- Usulkan dua sel LSTM manual hidden128, embedding64 dan head133, CE next-token; operasi dasar PyTorch/autograd, semua weights baru. Dokumentasi resmi LSTM hanya konsep/API, tidak menyalin kode proyek. Usia keluarga LSTM berkonflik potensial dengan syarat kategori10tahun; eskalasi untuk konsultasi, bukan mengklaim disetujui.
- Split karya/arrangement sebelum window; dataset MIDI belum dipilih. Speech Kaggle tidak dipindahkan menjadi corpus MIDI. Lisensi komposisi dan arrangement harus diverifikasi.
- Grammar mask dicatat terpisah dari kemampuan raw model; fixed-length cap/forced EOS tidak disebut learned termination. NLL/perplexity serta listening/memorization dan biaya compute belum diukur.
- API/schema/design juga diubah sebagai proposal dokumentasi agar tidak memandu implementasi upload/denoising lama; tidak ada migrasi/fitur dibuat.

### Verifikasi dan handoff

Cek diff/whitespace, file links, archive preservation, V=5+128, input[B,128]/logits[B,128,133], branch refs dan istilah domain lama. Tidak ada error training/model karena belum implementasi. A2 review sumber/hak data dan tokenizer, A3 review gates/CE/config/budget, A4 compile ekspor sesi dan reasoning kelompok. Semua approval/bukti runtime tetap pending. Tidak ada hasil eksperimen atau benchmark dibuat.

## Riwayat sebelum pivot — bukan persyaratan aktif

Bagian berikut dipertahankan lengkap sebagai jejak sesi speech. Instruksi/model/dataset di dalamnya telah digantikan dokumentasi MIDI aktif; jangan menganggapnya scope implementasi saat ini.

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

## Pemilihan Nottingham MIDI melody

28 Oktober 2026: pengguna menetapkan https://github.com/jukedeck/nottingham-dataset/tree/master/MIDI/melody. Metadata folder dan README upstream ditinjau, repository mencantumkan GPLv3 serta asal ABC Nottingham Music Database. Tidak ada MIDI diunduh/diparse atau source implementasi disalin. Sumber dipilih tetapi SHA/hak komposisi-arrangement, inventory dan kecocokan4/4/grid belum dibuktikan. Keputusan: gunakan folder melody saja, audit work groups sebelum split, jangan mengasumsikan monophony/meter dari nama folder. DATASET_REQUIREMENTS, DATA_CONTRACT, README dan dokumen status terkait diselaraskan; riwayat sebelumnya tetap sebagai catatan waktu, bukan status dataset saat ini. Ekspor chat asli perlu dilampirkan A4; tidak ada training/error model/approval baru.

---

## Sesi Member 2 — Data Pipeline & Preprocessing

- **ID sesi:** `944b335b-5dc1-49b7-9075-2d022e955ec5`
- **Tanggal:** 28 Oktober 2026
- **Anggota:** Member 2 (Data Pipeline & Preprocessing Engineer)
- **Target modul:** Dataset audit, tokenizer (`nirava-midi-step-v1`), grouping, split, windowing, DataLoader, torch adapter, augmentasi
- **Model/provider LLM:** Google Antigravity
- **Tautan ekspor chat:** [`docs/llm_chat_export_member2.md`](llm_chat_export_member2.md) (846 baris, kronologi lengkap 173+ langkah)

### Prompt dan alasan desain

Prompt utama: pengguna menyatakan perannya sebagai Anggota 2 dan menanyakan apa saja yang harus dikerjakan. Konteks proyek sudah dipivot ke MIDI String Generator oleh Member 1. Arsitektur aktif: LSTM autoregressive, kontrak `nirava-midi-step-v1` (V=133, grid 16 step/bar, token NOTE 0–127 + HOLD + REST + PAD + BOS + EOS), input shape `int64[B,128]`.

Instruksi yang diterima dan dilaksanakan (setelah izin pilot eksplisit dari pengguna):

1. **Audit dataset Nottingham melody** — inventarisasi 1034 file MIDI, filter 4/4 + monophonic + dedup SHA256 → 515 usable
2. **Tokenizer pure-stdlib** — SMF binary parser, grid quantizer 16 step/bar, encoder/decoder/exporter tanpa dependensi eksternal (mido/pretty_midi)
3. **Grouping & split work-disjoint** — fingerprint invarian transposisi (interval+duration+gap n-gram), Jaccard similarity, union-find, split 80/10/10 seed 20261028
4. **Windowing & DataLoader** — sliding window 128 step, shift 64, PAD/mask, BOS/EOS boundary
5. **Torch adapter** — `TorchMidiLoader` menghasilkan `{input_ids: int64[B,128], target_ids: int64[B,128], loss_mask: bool[B,128], lengths: int64[B]}`
6. **Augmentasi transpose** — ±5/+6 semitone (11 offset) train-only, pitch clamped 0..127

Keputusan desain yang diterima:
- Grid monofonik 16 step/bar sesuai `MIDI_TOKENIZATION.md`; triplet/swing di-quantize ke nearest grid (mean error 0.005 step/file)
- V=133 token sesuai kontrak; tidak mengubah token IDs
- Split berbasis work group (bukan random file) untuk mencegah leakage melodi serupa
- Augmentasi hanya transposisi (tanpa tempo/velocity karena token step tidak menyimpan informasi tersebut)
- Tokenizer pure stdlib karena mido/pretty_midi tidak tersedia di lingkungan awal; keputusan ini juga mengurangi dependensi

Keputusan yang ditolak/dimodifikasi:
- Awalnya LLM mengusulkan menggunakan existing scripts (`audit_dataset.py`, `preprocess_midi.py` berbasis pretty_midi); ditolak karena dependensi tidak tersedia dan tokenizer perlu sesuai kontrak baru

### Error dan debugging

**Error 1 — Pitch-bend false rejection (KRITIS)**

- **Perintah:** `python src/run_tokenizer_audit.py`
- **Expected:** 533 file 4/4 berhasil di-encode
- **Actual:** 0/533 berhasil; semua ditolak dengan alasan `pedal_or_pitch_bend`
- **Environment:** Python 3.12.14, Windows 11, Nottingham MIDI melody dataset
- **Root cause:** Event MIDI `0xE0 0x00 0x40` (pitch-bend value 8192 = netral) ada di setiap file Nottingham pada tick 0. Parser mendeteksi keberadaan event pitch-bend tanpa memeriksa apakah nilainya netral. Demikian juga pedal CC64 value <64 (off) dianggap aktif.
- **Prompt perbaikan:** "Semua file ditolak karena pitch bend, padahal ini neutral bend. Perlu perbaiki filter agar bend value 8192 dan pedal CC64 off diterima."
- **Solusi:** Modifikasi `_parse_smf()` di `nirava_midi_tokenizer.py`: pitch-bend diterima jika `value == 8192`, pedal CC64 diterima jika `value < 64`. Ditambah 3 unit test baru.
- **Verifikasi:** Re-run audit → 519/533 berhasil encode (14 ditolak karena overlap after quantization, bukan pitch-bend). 519/519 round-trip identical.

**Error 2 — Python tidak ditemukan**

- **Perintah:** `python --version`
- **Expected:** Python 3.x
- **Actual:** Windows Store alias, bukan Python asli
- **Solusi:** Ditemukan runtime Python 3.12.14 di `C:\Users\Haikal\.cache\codex-runtimes\...`; kemudian di-install Python 3.12.10 via `winget install --id Python.Python.3.12 --scope user` dan venv di `D:\nirava-venv`

**Error 3 — PowerShell escaping**

- **Perintah:** `python -c "..."` dengan f-string mengandung escaped quotes
- **Actual:** SyntaxError karena PowerShell memakan backslash-quote
- **Solusi:** Tulis script ke file `.py` kemudian jalankan, bukan inline `-c`

### Verifikasi aktual

**Perintah tes utama:**
```powershell
$env:PYTHONPATH="c:\Users\Haikal\Downloads\-Proyek1-AI-Voice-Cleaner-\src"
cd "c:\Users\Haikal\Downloads\-Proyek1-AI-Voice-Cleaner-"
& D:\nirava-venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Hasil:** 34 tests passed (0 failures, 0 errors)
- `test_nirava_midi_tokenizer.py`: 17 tests — round-trip, token range, boundary, PAD, BOS/EOS, degenerate, export MIDI
- `test_nirava_midi_data.py`: 11 tests — window shift, PAD mask, BOS/EOS boundary, grouping, split determinism
- `test_nirava_midi_torch.py`: 6 tests — dtype int64/bool, shape [B,128], shift, mask, real data split, group leak check

**Metrik tokenizer audit (519 file):**
- Round-trip: 519/519 identical (100%)
- Total steps: 288,368
- Mean quantization error: 0.005 step/file
- Max quantization error: 0.336 step
- Tokenizer hash SHA256: `21c0930ebf49f212455600a011be2b14cd066793619b2d47c5d972495a6a9bba`

**Metrik split:**
- 517 file (2 exact dedup removed), 494 work groups
- Train: 414 / Val: 52 / Test: 51
- Leakage cross-split: 0 groups, 0 identical token sequences
- Independent leak check: max val→train Jaccard 0.239, max test→train 0.070

**Metrik windowing (tanpa augmentasi):**
- Train: 2,197 windows / Val: 269 / Test: 277

**Metrik augmentasi:**
- Train augmented: 414 orig + 4,554 transposed = 4,968 pieces → 26,364 windows
- Val/Test: unchanged (52/51 pieces, 269/277 windows)

**Keterbatasan:**
- Dataset bias: 79.4% reels, semua jigs/waltzes/slip jigs hilang karena filter 4/4
- ~26K windows masih kecil untuk LSTM; risiko memorization
- 2 file validasi dengan similarity 0.15–0.25 ke train belum di-review manual
- SHA upstream commit di-pin via GitHub API (`0992bb6cd864f6d4b90d6663e08c0ef53ffaa08f`) tetapi hash per-file lokal vs fresh clone belum dibandingkan
- Hak komposisi/arrangement Nottingham belum diverifikasi bersama tim/dosen

**Commit/diff:** Belum di-commit. Branch yang direncanakan: `dev/member-2-data`.

### File yang dihasilkan

| File | Deskripsi |
|------|-----------|
| `src/nirava_midi_tokenizer.py` | Tokenizer pure-stdlib, kontrak `nirava-midi-step-v1` |
| `src/nirava_midi_grouping.py` | Fingerprint invarian transposisi + Jaccard + union-find |
| `src/build_splits.py` | Work-disjoint split 80/10/10 |
| `src/nirava_midi_data.py` | Windowing, collate, MidiWindowDataset |
| `src/nirava_midi_torch.py` | Torch adapter: `to_tensors`, `validate_batch`, `TorchMidiLoader` |
| `src/augment_transpose.py` | Augmentasi transpose ±5/+6 train-only |
| `src/run_tokenizer_audit.py` | Audit tokenizer pada seluruh dataset |
| `tests/test_nirava_midi_tokenizer.py` | 17 unit tests tokenizer |
| `tests/test_nirava_midi_data.py` | 11 unit tests windowing/DataLoader |
| `tests/test_nirava_midi_torch.py` | 6 unit tests torch adapter |
| `reports/DATASET_AUDIT_REPORT.md` | Laporan audit lengkap (15 seksi) |
| `reports/tokenizer_audit.csv` | Hasil audit per file |
| `reports/tokenizer_audit_summary.txt` | Ringkasan statistik tokenizer |
| `reports/split_manifest.csv` | Manifest split train/val/test |
| `reports/work_groups.csv` | Daftar work groups |
| `reports/split_exclusions.csv` | File yang dieksklusi dari split |
| `reports/split_summary.txt` | Ringkasan statistik split |
| `reports/dataset_exclusions.csv` | File yang dieksklusi dari dataset |
| `reports/dataset_usable.csv` | File yang lolos filter |
| `processed/tokens_v1.jsonl` | Token sequences (tidak di-commit) |
| `processed/tokens_v1_aug.jsonl` | Token sequences + augmentasi (tidak di-commit) |
| `requirements.txt` | Dependensi proyek |
| `docs/llm_chat_export_member2.md` | Ekspor kronologi chat lengkap |

### Handoff ke Member 3

Interface yang disediakan untuk Member 3 (Training Engineer):
```python
from nirava_midi_torch import TorchMidiLoader

loader = TorchMidiLoader(
    tokens_path="processed/tokens_v1_aug.jsonl",
    split="train",       # "train" | "val" | "test"
    batch_size=32,
    window_len=128,
    window_shift=64,
    shuffle=True
)
for batch in loader:
    # batch["input_ids"]  : int64 [B, 128]
    # batch["target_ids"] : int64 [B, 128]  (input shifted right by 1)
    # batch["loss_mask"]  : bool  [B, 128]
    # batch["lengths"]    : int64 [B]
    pass
```
- Tokenizer hash: `21c0930ebf49f212455600a011be2b14cd066793619b2d47c5d972495a6a9bba`
- V = 133, PAD = 0, BOS = 1, EOS = 2, NOTE_0..NOTE_127 = 3..130, HOLD = 131, REST = 132
- Environment: Python 3.12.10, torch 2.15.0+cpu, venv di `D:\nirava-venv`
- torch CUDA belum di-install; jika training memerlukan GPU (RTX 5060 8GB, driver 616.92), Member 3 perlu `pip install torch --index-url https://download.pytorch.org/whl/cu126`

### Isu tersisa

1. Hak komposisi/arrangement Nottingham — perlu diverifikasi bersama tim/dosen
2. 2 file validasi dengan similarity 0.15–0.25 ke train — perlu review manual
3. Dataset bias 79.4% reels — didokumentasikan tetapi belum dimitigasi
4. Git commit dan PR belum dibuat
5. Stage 1 GO masih pending — tidak ada training/implementasi model
