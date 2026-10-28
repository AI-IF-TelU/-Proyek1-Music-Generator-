# Roadmap training-first dan gate

Status 28 Oktober 2026: **Stage 1, GO tertunda**. Ini rencana, bukan pekerjaan yang telah dilakukan. Jadwal ditetapkan setelah hardware dan tenggat diketahui.

## M0 Stage 1 dokumentasi dan konsultasi

Handoff Member 1: spesifikasi `nirava-stft-cgan-v1` (RI-STFT cGAN, segmen2detik) menggantikan proposal waveform awal. A2 review data contract/shape dan bukti speaker/pairing; A3 review loss/config/checkpoint/rekonstruksi; A4 mengarsipkan prompt dan keputusan. Handoff dokumentasi bukan izin training. Panduan akademik dosen prioritas; riset kompetitor/referensi visual adalah pendukung produk, bukan pengganti syarat akademik atau blocker akademik mandiri.

- [x] Baca seluruh Markdown awal dan panduan dosen; petakan rubrik 30/25/25/20.
- [x] Usulkan cGAN dari nol, alternatif diffusion, dataset Kaggle dan empat job desk.
- [ ] Dosen menerima domain speech enhancement, kompleksitas dan batas from scratch.
- [ ] Verifikasi metadata/lisensi sumber dataset, akses GPU, plafon komputasi, jadwal dan identitas anggota.
- [ ] Selesaikan validasi target/kompetitor dan kebijakan audio/retensi yang relevan.
- [ ] Catat verdict Stage 1 GO dan persetujuan eksplisit pengguna atas demo concept.

TASK 00B/00C tidak mengizinkan model, instalasi, download data atau scaffold. Kebutuhan bukti empiris pra-GO tidak mengizinkan coding diam-diam. [Checklist closure B1–B10](STAGE1_VALIDATION.md) mencatat konflik gate ini: pilot offline sebelum GO memerlukan izin pengguna yang terbatas dan eksplisit. Saat ini izin tersebut belum ada. Kriteria dan prosedur pilot terdapat pada [EVALUATION.md](EVALUATION.md); hasil aktual tidak boleh digantikan proposal.

Task berikutnya yang diusulkan adalah **TASK 00D — Evidence Intake and Pilot Authorization Review**, dengan keluaran awal dokumentasi/bukti, bukan implementasi. Blueprint model, dataset dan tim yang ada dipakai kembali; jangan membuat ulang proyek.

## M1 Data setelah GO

A2 memverifikasi dataset aktif speech-noise-dataset, lisensi, archive hash, struktur paired atau clean speech + noise, split speaker/source/noise dan preprocessing; A1 menetapkan shape/forward/loss, A4 menyiapkan ekspor chat. Mixing terkontrol hanya direncanakan jika komponen sah tersedia. Keluaran: checklist dataset selesai, manifest, data tests dan baseline noisy reproduksibel. Tahan training formal jika clean target, pairing atau leakage belum beres. Jangan memakai asumsi speaker/test split Valentini pada dataset baru.

## M2 Training minimum

A1/A3 setelah izin membangun G/D STFT kompleks sesuai MODEL_PROPOSAL, inverse differentiable/consistency projection, loss, loop dan checkpoint/resume melalui prompt terdokumentasi. Uji shape32000→257×251→272×256, round-trip STFT/iSTFT, gradient G/D, silence/padding, finite loss, subset overfit, overlap-add dan resume. Profil parameter/RAM/VRAM/batch-time untuk config batch4 usulan sebelum menyetujui sweep. Keluaran: training aktual dengan kurva dan failure log, belum klaim kualitas.

## M3 Eksperimen dan evaluasi

A3 menjalankan eksperimen [MODEL_PROPOSAL](MODEL_PROPOSAL.md); A2 menjaga split dan A4 mengaudit log/config. Pilih checkpoint pada validation sesuai [EVALUATION](EVALUATION.md), bekukan keputusan sebelum test. Keluaran: ablation, tabel termasuk run gagal, hasil held-out, profiling dan batasan. Jika fidelity/biaya gagal, konsultasikan pivot; pretrained tidak menggantikan deliverable dari nol.

## M4 Integrasi setelah bukti model

Konfirmasi kelayakan model/demo sebelum scaffold produk. AMATI 5–8 referensi, TIRU pola 2–3 tanpa menyalin, MODIFIKASI UI; lalu Next.js, FastAPI, PostgreSQL/Alembic, adaptor checkpoint, upload dan secure job lifecycle, A/B sepadan, download dan cleanup. Tidak menambah Redis/Celery tanpa kebutuhan terbukti. Jalankan tes API/audio, lint/typecheck relevan dan QA aksesibilitas.

## M5 Pengumpulan

Demo nyata, laporan/grafik eksperimen, ekspor log LLM aktif, bukti commit/log tiap anggota, audit lisensi, reproduksi terpilih dan persiapan presentasi individu. Deployment bila diperlukan dan diotorisasi.

## Definition of done

Model utama dilatih tim dari nol; loop/loss/tuning terdokumentasi; metrik dapat dilacak ke split/config/checkpoint; log LLM kronologis termasuk debugging nyata; empat peran memiliki bukti dan penguasaan materi. Produk memenuhi kontrak keamanan/error/cleanup/A-B. Tidak ada hasil fiktif, secrets, audio pribadi atau weights dalam Git. Nama anggota, tenggat, GPU dan approval belum tersedia. Ownership: [TEAM_RESPONSIBILITIES.md](TEAM_RESPONSIBILITIES.md).
