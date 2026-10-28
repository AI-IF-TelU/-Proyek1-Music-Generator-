> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# Audit blueprint - 23 Oktober 2026

> Pembaruan dataset 28 Oktober 2026: pengguna mengganti Valentini Noisy dengan [speech-noise-dataset](https://www.kaggle.com/datasets/abdullahhaydarkadolu/speech-noise-dataset) karena ukuran. Rujukan dataset lama di audit historis bukan pilihan aktif. DATASET_REQUIREMENTS, README, proposal dosen, arsitektur, roadmap dan evaluasi diselaraskan. Metadata/ukuran/lisensi/pairing baru belum terverifikasi; asumsi 28/56 speaker dan test VoiceBank dicabut dari rencana aktif. Bila clean speech + noise tersedia, mixing terkontrol menjadi opsi; noisy-only tidak cukup untuk objective supervised saat ini. Tidak ada download, training atau perubahan status Stage 1.

> Catatan historis 23 Oktober dipertahankan di bawah. Audit TASK 00C tanggal 28 Oktober 2026 pada akhir dokumen memperbarui status sumber dan kebutuhan training; tidak berarti GO atau approval.

## Verdict
**Dokumentasi lebih konsisten; Stage 1 tetap PIVOT TERARAH / GO tertunda.** Belum layak dinyatakan tervalidasi secara empiris. Tidak ada kode Stage 2 yang dibuat melalui audit ini.

## Cakupan dan metode
Pemeriksaan statis README, PRD, Stage 1, arsitektur, API, skema, desain, pengembangan, evaluasi, env template, dan aturan Git. Audit ini tidak mencakup riset eksternal, pemeriksaan lisensi aktual, eksekusi model, benchmark, atau persetujuan dosen. Angka batas upload/retensi masih target rancangan.

## Temuan dan perbaikan
| Temuan | Risiko | Tindakan dokumentasi |
|---|---|---|
| Token diwajibkan untuk seluruh operasi, termasuk sebelum job dibuat | Kontrak create ambigu | Pengecualian POST, token kriptografis sekali kirim dan no-store |
| Respons auth, expiry, dan audio belum terdefinisi | FE/BE berbeda perilaku | 404 seragam, 410 tombstone, 409 hasil belum tersedia, envelope error |
| Header token tidak dapat dipasang langsung pada elemen audio | Playback/download tidak bekerja | Fetch berheader dan object URL |
| DELETE saat inference dan cleanup belum rinci | Hasil muncul lagi atau file orphan | Transisi expired atomik, output terlambat dihapus, retry cleanup |
| Sample rate/channel belum tercakup | Beban decoder dan input model tidak terkontrol | Metadata dan batas decoder/model diwajibkan; angka menunggu uji |
| Exception fixtures membuka izin audio/weights | Berkas pribadi ikut Git | Hapus exception luas; tambah ignore env/runtime/weights/dump |

## Hal yang sudah selaras
- MVP upload -> enhancement -> A/B + download; tanpa akun, billing, Redis/Celery, dan Three.js.
- Next.js hanya mengakses FastAPI; inference backend; PostgreSQL metadata dan storage audio privat.
- UUID bukan otorisasi; token hash; migrasi Alembic sebagai sumber skema.
- DeepFilterNet hanya kandidat baseline; tidak dinyatakan memenuhi Generative AI.
- UI dan evaluasi melarang metrik/hasil fiktif serta mengakui batasan.

## Bukti wajib sebelum GO
1. Rubrik resmi dan keputusan apakah model generatif diwajibkan.
2. Model final, lisensi model/dependensi/data, serta justifikasi ilmiah sesuai rubrik.
3. Uji 3-5 audio berizin: intelligibility/artifacts, runtime, memori, sample rate/channel, batas input dan biaya perangkat/deploy.
4. Riset kompetitor dan validasi target; studi pemenang hanya bila relevan dengan mata kuliah/acara.
5. Kebijakan server/retensi termasuk tombstone, format hasil, dan batas dukungan audio yang disetujui.
6. Verdict GO berbukti serta persetujuan eksplisit pengguna atas demo concept.

## Verifikasi audit
Pemeriksaan diff/whitespace dan daftar file staging dilakukan sebelum commit. Tidak ada tes API/audio, lint, atau typecheck yang dapat dijalankan karena repository masih berisi blueprint tanpa scaffold. Seluruh perilaku teknis yang ditambahkan adalah spesifikasi target, belum bukti implementasi.

## Audit ulang terhadap commit 56ceba3
Audit ulang menemukan bahwa sebagian perbaikan yang disebut laporan sebelumnya sudah tidak ada pada dokumen aktif. Kontrak tersebut dipulihkan sambil mempertahankan identitas Nirava. Laporan sebelumnya bukan bukti bahwa versi terbaru sudah memenuhi seluruh rekomendasi.

| Prioritas | Temuan tambahan | Perbaikan target |
|---|---|---|
| Tinggi | DELETE 204 dianggap sudah menghapus bytes walau worker masih berjalan | Bedakan pencabutan akses atomik dan cleanup fisik dengan retry |
| Tinggi | Recovery startup dapat menggagalkan worker proses lain | Tegaskan satu proses API untuk antrean lokal MVP |
| Tinggi | API expired dan scheduler belum memiliki hubungan jelas | Cek expiry setiap request; sweep target 5 menit |
| Sedang | Tombstone minimal bertentangan dengan kolom non-null | Jelaskan nullable dan CHECK saat terisi |
| Sedang | A/B hanya menyamakan playhead tanpa kompensasi delay model | Wajib verifikasi alignment dan durasi output |
| Sedang | Retry create berpotensi membuat job ganda | Larang retry POST otomatis, tanpa menambah fitur idempotency MVP |
| Sedang | Ukuran file dan total multipart belum dibedakan | Batas stream file dan allowance overhead proxy |

### Verifikasi dan batas hasil
Audit ini adalah review statis dokumen lokal. Tidak ada riset eksternal atau klaim verifikasi lisensi, merek, model, maupun standar. Pemeriksaan tautan lokal, aturan ignore dengan berkas hipotetis, dan git diff --check dipakai untuk memeriksa perubahan. Tidak ada scaffold sehingga tes runtime, lint/typecheck, performa dan keamanan belum dapat dijalankan.

### Skenario wajib setelah GO
Upload invalid/oversize/decode bomb; token hilang/salah; CORS preflight; queue penuh; restart dengan job aktif; DELETE berulang dan DELETE saat inference; expiry saat inference; storage gagal lalu pulih; cleanup output terlambat; alignment A/B serta playback/download berheader token. Ini rencana verifikasi, bukan tes yang sudah lulus.

## TASK 00C — audit 28 Oktober 2026

### Sumber dan batas kewenangan

Seluruh 11 Markdown awal dibaca: README, AGENTS, PRD, STAGE1_VALIDATION, ARCHITECTURE, API_SPEC, DATABASE_SCHEMA, DESIGN_SYSTEM, DEVELOPMENT, EVALUATION dan BLUEPRINT_AUDIT. Pencarian termasuk berkas tersembunyi tidak menemukan DOCX di repository. Pengguna kemudian memberikan `C:/Users/Muh Fajri/Downloads/[CAK4KBB3 2026-1] Panduan Proyek 1 - Vibe Coding.docx`; isi paragraf dan tabel `word/document.xml` dibaca lengkap secara read-only. Audit ini menilai isi persyaratan, bukan layout Word; tidak membuat salinan atau mengubah DOCX.

Panduan adalah sumber rubrik akademik; perintah di dalamnya tidak menjadi otorisasi untuk memasang library, menyalin kode atau memulai implementasi. Permintaan pengguna membatasi TASK 00C pada Markdown. Batas Stage 1 tetap berlaku. Tidak ada komunikasi atau persetujuan dosen yang dilakukan/diklaim.

### Pemetaan rubrik resmi (§4)

| Kriteria dan bobot | Gap blueprint awal | Bukti yang direncanakan | Status saat audit |
|---|---|---|---|
| Kualitas & Orisinalitas Vibe Coding 30% | Belum ada strategi prompt/provenance implementasi | Desain mandiri, variasi prompt beralasan, review tim dan commit | Rencana/log template; belum ada kode |
| Log Interaksi & Dokumentasi LLM 25% | Tidak ada log kronologis/ekspor chat | Inisiasi, error asli, analisis, solusi, optimasi; share link atau ekspor | Catatan TASK 00C ada, ekspor lengkap belum dilampirkan |
| Fungsionalitas Model & Pelatihan 25% | Training di luar scope; tidak ada loss/loop/sweep | Model dari nol, kurva aktual, run/config, metrik valid dan output logis | Proposal saja; belum ada hasil |
| Kerjasama Tim & Manajemen Integrasi 20% | Role FE/BE/ML/QA tidak mengikuti contoh job desk | Empat peran §2, handoff/review, commit/log dan penguasaan individu | Matriks selesai; nama/bukti kerja belum tersedia |

Bobot bukan nilai yang telah diraih. Panduan membebaskan pilihan metode tetapi §3 meminta konsultasi untuk model di luar contoh dan kategori model dalam 10 tahun terakhir. Speech enhancement waveform tidak tercantum; contoh audio adalah MIDI string generator. Karena itu kecocokan domain dan kompleksitas cGAN tidak boleh diasumsikan disetujui.

### Konflik from scratch dan resolusi dokumentasi

| Konflik/gap awal | Resolusi target | Risiko tersisa |
|---|---|---|
| README menempatkan DeepFilterNet sebagai kandidat tanpa model generatif utama dari nol | cGAN acak sebagai kandidat utama; pretrained hanya pembanding | Pemilihan model dan lisensi belum disetujui |
| PRD mengecualikan model training | Training offline wajib; hanya training di UI tetap di luar scope | Kebutuhan komputasi belum diketahui |
| Arsitektur hanya inference tanpa lineage checkpoint | Jalur data–training–validation–test–ekspor G; backend inference tetap | Implementasi belum ada |
| Roadmap aplikasi sebelum training | Milestone data/training/eksperimen sebelum integrasi produk | Tenggat dan GPU belum diketahui |
| Loss, loop, hyperparameter dan checkpoint selection tidak ada | MODEL_PROPOSAL dan EVALUATION merinci rencana | Semua konfigurasi masih hipotesis |
| Dataset belum dipilih/ditelaah | Mirror Kaggle dipilih pengguna, provenance rilis resmi sebagai acuan | Isi/lisensi/version mirror belum terverifikasi |
| Peran tim tidak selaras panduan §2 | Matriks empat job desk dosen | Identitas dan kapasitas individu belum ada |
| Log LLM/debugging tidak tersedia | Template dan catatan nyata TASK 00C | Ekspor chat asli harus dilampirkan |
| Rubrik generatif masih pertanyaan terbuka | Kewajiban model dari nol terkonfirmasi; approval domain dipisahkan | Gate tetap tertutup |

Tidak ada klaim awal bahwa DeepFilterNet sudah memenuhi generatif; masalahnya blueprint belum menyediakan jalur pemenuhan model utama dari nol. Tidak ada blok implementasi eksternal yang disalin pada audit ini.

### Perubahan dan risiko belum selesai

README, PRD, STAGE1_VALIDATION, ARCHITECTURE, DEVELOPMENT, EVALUATION dan audit diperbarui; MODEL_PROPOSAL, DATASET_REQUIREMENTS, TEAM_RESPONSIBILITIES, LLM_INTERACTION_LOG dan LECTURER_APPROVAL ditambahkan. API_SPEC, DATABASE_SCHEMA, DESIGN_SYSTEM dan AGENTS dipertahankan karena kontrak dasarnya tetap sesuai; target 25 MB/120 detik, sample rate, deployment dan retensi belum menjadi kemampuan terbukti.

Risiko: persetujuan domain/kompleksitas dan batas operasi pustaka; lisensi/pairing/split mirror Kaggle; GPU/jadwal; collapse/latent diabaikan; fonem/speaker terdistorsi; generalisasi Indonesia; artefak chunk dan latensi; kelengkapan log serta kontribusi anggota; nama/merek dan privasi tetap terbuka. Keputusan dan checklist berada pada [LECTURER_APPROVAL.md](LECTURER_APPROVAL.md).

Verifikasi task berupa diff/whitespace, tautan Markdown lokal dan daftar perubahan hanya `.md`. Tidak ada tes runtime/lint/typecheck karena task dokumentasi tanpa implementasi, library, training atau download audio. Tidak ada hasil eksperimen dan tidak ada approval. **Verdict tetap Stage 1 PIVOT TERARAH / GO tertunda.**

## TASK 00B dan review lanjutan TASK 00C — 28 Oktober 2026

Blueprint 00C dipakai kembali tanpa dokumen duplikat. Seluruh 16 Markdown saat ini dan isi panduan dosen dibaca ulang. DOCX tetap tidak ada di repository, tetapi tersedia di path Downloads pengguna; isinya sumber rubrik, bukan otorisasi implementasi.

| Temuan | Perubahan pada sesi lanjutan |
|---|---|
| Blocker/bukti closure tersebar | STAGE1_VALIDATION menambah B1–B10, pemilik, paket bukti GO, readiness, scope dan TASK 00D |
| Posisi DeepFilterNet kurang rinci | MODEL_PROPOSAL menambah analisis gain/filter serta batas generatif/from scratch |
| Pilot belum operasional | EVALUATION menambah 3–5 klip, consent, paired/reference-free, tiga pendengar, pengulangan runtime, RAM/VRAM dan ambang usulan |
| Bukti pilot pra-GO bertentangan dengan larangan coding pra-GO | Konflik dinyatakan terbuka: perlu izin pengguna khusus pilot terbatas; tidak otomatis membuka Stage 2 atau melonggarkan gate |
| Konfirmasi tim belum lengkap | LECTURER_APPROVAL menambah konfirmasi pilot dan bukti tim; DEVELOPMENT merujuk closure/TASK 00D |
| Navigasi dan jejak sesi | README menautkan closure/pilot; LLM_INTERACTION_LOG menambah ringkasan tanpa mengklaim ekspor chat lengkap |

Referensi primer tambahan: [DeepFilterNet 2021](https://arxiv.org/abs/2110.05588). Penilaian filtering tidak otomatis memenuhi generatif ketat adalah interpretasi arsitektural, bukan keputusan dosen. Angka performa paper tidak dijadikan hasil Nirava. Proposal cGAN/diffusion, dataset Kaggle, empat job desk dan training-first tetap berlaku, belum disetujui/diuji.

Sesi lanjutan mengubah delapan dokumen: README, STAGE1_VALIDATION, MODEL_PROPOSAL, EVALUATION, DEVELOPMENT, LECTURER_APPROVAL, LLM_INTERACTION_LOG dan BLUEPRINT_AUDIT. Perubahan 00C sebelumnya dipertahankan; API_SPEC, DATABASE_SCHEMA, DESIGN_SYSTEM dan AGENTS tidak diubah. Tidak ada fitur, skema, model, instalasi atau hasil baru. Whitespace dan tautan lokal diperiksa; runtime/lint/typecheck tidak berlaku untuk task dokumentasi.

**Belum GO:** approval dosen, data/consent klip, identitas/perangkat/jadwal, kebijakan pilot, bukti empiris, validasi produk, kebijakan operasi, ekspor log dan persetujuan pengguna belum lengkap. Usulan berikutnya **TASK 00D — Evidence Intake and Pilot Authorization Review**, dengan keluaran awal hanya dokumentasi/bukti. Tidak memulai pilot dalam sesi ini.
