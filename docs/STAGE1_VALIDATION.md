# Stage 1 — Strategic validation (draft)

## Domain dan status
AI/ML × speech enhancement. **Verdict: PIVOT TERARAH; GO tertunda.** Ini bukan laporan hasil riset kompetisi.

TASK 01: spesifikasi aktif dipisah ke [ML_ARCHITECTURE.md](ML_ARCHITECTURE.md), [DATA_CONTRACT.md](DATA_CONTRACT.md) dan [TRAINING_CONTRACT.md](TRAINING_CONTRACT.md). Model utama adalah cGAN dari nol; DeepFilterNet hanya baseline opsional. Pemisahan dokumen tidak memenuhi bukti pilot, validasi dataset/hardware atau persetujuan dosen. Seluruh blocker B1–B10 beserta pengecualian B7 tetap mengikuti bukti, bukan ketersediaan spesifikasi.

Konfirmasi khusus yang masih kosong: penerimaan STFT speech cGAN di luar contoh dosen, batas PyTorch dasar, latent/generative objective, pasangan/speaker metadata dan mixing dataset Kaggle, loss/sweep/metrik, format log serta perangkat/budget. Lihat [checklist dosen](LECTURER_APPROVAL.md). Jangan mulai Stage2 atau pilot atas dasar TASK01.

## Hipotesis produk
- Target awal: mahasiswa dan pembuat konten yang merekam percakapan di lingkungan berisik.
- Pain: ucapan sulit dipahami akibat kebisingan latar.
- Angle: fokus pada intelligibility dan pelestarian karakter suara, bukan klaim menghapus seluruh noise.
- Problem question: Bagaimana membersihkan noise tanpa merusak informasi ucapan?
- Nama kerja: Nirava. Nama ini telah digunakan pihak lain; belum ada pemeriksaan merek, domain, atau ketersediaan repository secara menyeluruh.

## ChatGPT test
Aplikasi memproses audio sungguhan; hasil tidak dapat digantikan dengan satu jawaban teks. Lulus secara konseptual, tetap perlu demo.

## Six winning-pattern checks
1. Failure mode: noise berkurang tetapi konsonan/ucapan ikut rusak — perlu diuji.
2. Stakes: rekaman penting menjadi sulit dipahami; hindari klaim bencana tanpa bukti.
3. Side-by-side: satu layar, audio original vs enhanced, playback tersinkron.
4. Framing: noise reduction vs speech preservation.
5. Judging proof: hasil audio nyata + metrik evaluasi + batasan.
6. Naming: nama harus membantu orang menebak manfaat; lakukan uji pengguna.

## Demo concept
Unggah klip noisy berizin → proses → dengarkan A/B dengan posisi playhead sama → unduh. Wow moment = peningkatan keterdengaran yang bisa diverifikasi, bukan animasi kosmetik.

## Nine-lens provisional scoring (1–10; judgement, bukan data)
Pain 8; differentiation 4; feasibility 7; judge appeal 7; scalability 6; winning chance 5; uniqueness 4; wow 8; ChatGPT test 8.

## Blocking questions sebelum GO
- Panduan resmi sudah dibaca dari DOCX pengguna pada 28 Oktober 2026: model dari nol, empat anggota, log LLM dan training wajib. Speech enhancement di luar contoh memerlukan konsultasi dosen (§3); belum ada persetujuan.
- Apakah dosen menerima kompleksitas cGAN dan batas operasi pustaka dasar pada [proposal](MODEL_PROPOSAL.md)?
- Tenggat, identitas empat anggota, GPU dan plafon komputasi/deployment?
- Apakah isi/lisensi mirror Kaggle sudah diverifikasi sesuai [checklist](DATASET_REQUIREMENTS.md)?
- Contoh pemenang terdahulu (jika benar-benar hackathon)?
- Apakah audio pengguna boleh diproses di server, dan berapa retensinya?

## Validasi eksternal yang masih harus dikerjakan
Riset 3–5 kompetitor relevan, 2–3 case study pemenang pada domain serupa jika ada kompetisi, tes 3–5 sampel noisy, cek lisensi model, evaluasi keterbacaan nama.

Klarifikasi Member1: panduan dosen menjadi prioritas. Kompetitor, pemenang dan scoring/desain lama adalah pendukung produk, bukan tuntutan rubrik atau blocker akademik mandiri. Bukti pilot, lisensi, penerimaan model dari nol, sumber daya, log dan izin pengguna tetap diperlukan. Proposal aktif `nirava-stft-cgan-v1` memakai STFT kompleks/2detik, belum diimplementasikan atau disetujui.

## Gate GO
GO hanya bila rubrik cocok, proposal diterima dosen, demo realistis, target pengguna jelas dan sumber daya memadai. Model generatif dari nol adalah kebutuhan terkonfirmasi. Lengkapi [checklist dosen](LECTURER_APPROVAL.md), catat verdict GO dan persetujuan eksplisit pengguna atas demo concept sebelum Stage 2. Proposal ini tidak membuka gate; training-first setelah gate mengikuti [DEVELOPMENT.md](DEVELOPMENT.md). Bukti pilot sebelum GO memerlukan izin terbatas tersendiri; tidak boleh mengimplementasikan model demi memenuhi gate tanpa izin tersebut.

## Checklist closure TASK 00B

Kotak kosong berarti bukti belum tersedia, bukan kegagalan eksperimen. Dokumen rencana tidak mencentang bukti aktual.

- [ ] **B1 — penerimaan akademik:** keputusan dosen tertulis menerima speech enhancement cGAN, kompleksitas dan kebaruan kategori, batas from scratch/pustaka, eksperimen/metrik dan format log. Pemilik A1; bukti di [LECTURER_APPROVAL.md](LECTURER_APPROVAL.md).
- [ ] **B2 — data:** versi/provenance/lisensi mirror Kaggle dan sumber asal terverifikasi; kesiapan pasangan dan rencana split speaker terdokumentasi. Checklist pemeriksaan archive baru dijalankan bila akses/unduh diizinkan. Pemilik A2.
- [ ] **B3 — sumber daya dan tim:** empat nama/NIM beserta komitmen peran, tenggat dan milestone, akses GPU/CPU, RAM/VRAM/disk, kuota/jam komputasi dan biaya/host disepakati. Pemilik A1–A4.
- [ ] **B4 — rekaman pilot:** inventaris 3–5 rekaman berizin, consent/lisensi, bahasa/noise/durasi/sample rate dan clean reference bila ada; file disimpan privat, tidak di Git. Pemilik A2/A4.
- [ ] **B5 — kebijakan gate pilot:** putuskan konflik kebutuhan bukti empiris pra-GO dengan larangan implementasi pra-GO. Izin pengguna harus menyebut pilot offline terbatas, pekerjaan yang diizinkan dan stop condition; ini belum diberikan. Approval dosen saja bukan otorisasi coding. Pemilik pengguna, dikoordinasikan A1.
- [ ] **B6 — bukti kelayakan:** setelah izin pilot, hasil nyata model utama dari nol pada 3–5 rekaman menurut [EVALUATION.md](EVALUATION.md), runtime/memori pada host target, versi model dan catatan kegagalan. DeepFilterNet tidak menggantikan bukti model utama. Pemilik A3/A4.
- [ ] **B7 — pendukung produk, bukan blocker akademik mandiri:** ringkasan kebutuhan pengguna, diferensiasi, batas klaim dan demo A/B; riset kompetitor/pemenang hanya jika relevan dan dipilih tim. Ketidakadaan studi kompetisi tidak menunda kelayakan akademik model yang telah memenuhi bukti resmi. Pemilik A1/A4; catat tidak berlaku bila konteks tidak sesuai.
- [ ] **B8 — kontrak operasi:** tim menyetujui format/sample rate/channel yang didukung, limit upload/durasi, host dan concurrency, pemrosesan server, retensi 24 jam/tombstone dan consent audio. Angka blueprint masih target. Pemilik A1/A2/A4.
- [ ] **B9 — keterlacakan:** ekspor/link chat asli, keputusan prompt/desain, log error bila ada, analisis tim, reviewer dan bukti kontribusi; jangan membuat error fiktif. Pemilik semua anggota; A4 kompilasi.
- [ ] **B10 — keputusan akhir:** review paket bukti, verdict GO bertanggal dengan rujukan B1–B9, serta persetujuan eksplisit pengguna atas demo concept dan dimulainya Stage 2. Belum tersedia.

Nama Nirava tetap dipakai. Pemeriksaan merek/domain dan lisensi font adalah risiko sebelum publikasi komersial/desain final, bukan bukti kualitas model; tidak otomatis menghalangi pilot akademik privat. GPU profiling dan model formal penuh tetap milestone training, bukan hasil yang diklaim saat closure.

## Bukti persis untuk GO dan penilaian kesiapan

Paket closure harus berisi keputusan dosen; checklist data dengan rujukan lisensi/versi; matriks anggota dan anggaran host/jadwal; manifest rekaman berizin; izin pilot; tabel hasil aktual dengan config/seed/checkpoint hash, metrik/listening, log runtime/memori dan kegagalan; ringkasan validasi produk; keputusan batas operasi/privasi; ekspor LLM; dan keputusan pengguna. Semua klaim harus menunjuk bukti yang dapat diperiksa, bukan hanya checkbox.

Konflik urutan tidak diselesaikan dengan menghapus bukti empiris: default konservatif tetap B6 sebelum GO melalui izin pilot B5 yang eksplisit. Jika pengguna dan dosen memilih gate berbasis rencana dengan validasi empiris setelah GO, perubahan kriteria serta risiko harus disetujui dan dicatat dahulu; task dokumentasi ini tidak mengubahnya secara sepihak. Pilot bukan izin scaffold Next.js/FastAPI atau pengembangan database.

**Readiness: belum GO.** Rubrik telah diketahui dan proposal lengkap secara dokumentasi; B1–B10 belum dibuktikan. Tidak ada training/pilot/hasil pada task ini. Jangan menghitung persentase kesiapan atau menyimpulkan target tercapai dari daftar dokumen.

## Scope MVP yang direkomendasikan

Tetap tiga fitur: upload WAV/MP3 tervalidasi → enhancement satu job dengan status/error jujur → A/B tersinkron dan download WAV. Next.js hanya presentasi/polling/fetch token; FastAPI melakukan validasi, lifecycle, inference dan cleanup; PostgreSQL metadata; audio di storage privat sementara. Satu API process dan antrean lokal berbatas cukup sebagai rancangan demo satu host, dengan profiling sebagai syarat kapasitas. Stack ini layak secara arsitektural; pencapaian jadwal dan performa belum terbukti tanpa B3/B6. Training offline tetap deliverable akademik utama.

Tidak menambah akun, billing, dashboard admin, Redis, Celery, streaming, batch atau Three.js. Target 25 MB/120 detik dan retensi tetap usulan, bukan jaminan. Jika kapasitas tidak cukup, usulkan pengurangan limit/durasi atau demo host lokal untuk disetujui; tidak mengganti model utama dengan pretrained secara diam-diam.

## Task Codex berikutnya yang diusulkan

**TASK 00D — Evidence Intake and Pilot Authorization Review.** Masukkan jawaban dosen, identitas/perangkat/jadwal tim, bukti lisensi/version Kaggle dan metadata izin rekaman ke checklist yang sudah ada. Susun paket pilot offline konkret dengan host, batas komputasi, operasi yang diminta dan kriteria evaluasi; catat keputusan pengguna sebelum eksekusi. Keluaran awal hanya dokumentasi dan daftar bukti kurang. Tidak mengimplementasikan model, menginstal library, mengunduh audio, mengubah skema atau membangun aplikasi tanpa otorisasi lanjutan. Jika bukti/izin belum tersedia, laporkan tetap Stage 1, bukan otomatis memulai pilot.
