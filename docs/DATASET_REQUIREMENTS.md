# Dataset dan verifikasi Nirava

## Sumber yang dipilih

Pilihan terbaru pengguna pada 28 Oktober 2026: [Kaggle speech-noise-dataset](https://www.kaggle.com/datasets/abdullahhaydarkadolu/speech-noise-dataset), uploader pada URL `abdullahhaydarkadolu`. Menggantikan Valentini Noisy karena dataset sebelumnya dinilai terlalu besar oleh pengguna. Ukuran relatif dataset baru belum diukur; tidak mengklaim angka ukuran atau penghematan tertentu.

Halaman baru dibuka melalui alat web tetapi metadata/file tidak terbaca. Dataset belum diunduh: versi, ukuran archive/ekstraksi, jumlah file, bahasa, speaker, sample rate, struktur, lisensi dan asal komponennya **belum diverifikasi**. Jangan menganggap dataset ini mirror VoiceBank-DEMAND atau mewarisi lisensi, 28/56 speaker, 48 kHz dan test split dataset sebelumnya.

## Kecocokan dengan training berpasangan

Model utama cGAN dari nol tetap kandidat; keputusan pipeline bergantung hasil inventaris data:

- Jika tersedia noisy–clean yang benar-benar sejajar, gunakan pasangan yang diverifikasi; nama folder/basename serupa saja bukan bukti alignment.
- Jika tersedia clean speech dan noise terpisah, usulkan pembuatan noisy sintetis dari clean target melalui mixing dengan SNR, seed, gain dan source ID tercatat. Bagi sumber speech/speaker dan sumber noise sebelum mixing agar turunannya tidak bocor lintas split. Validation/test memakai campuran tetap yang dibekukan; noise baru dan rekaman riil diuji terpisah. Ini rencana kondisional, belum konfirmasi isi atau izin penggunaannya.
- Jika hanya noisy speech, noise-only, atau target clean tidak sah/tersedia, hentikan persiapan supervised training dan laporkan gap. Jangan menganggap noisy sebagai target clean atau menambahkan pretrained teacher tersembunyi.

Manfaat dataset yang lebih kecil adalah potensi pengurangan kebutuhan unduh/storage; kelayakan tersebut harus dibuktikan dengan inventory nyata. Risiko ukuran kecil: cakupan speaker/noise sempit, overfitting dan evaluasi tidak representatif. Bahasa Indonesia, rekaman ponsel, reverberation, clipping dan ucapan bertumpuk tetap perlu diperiksa; tidak diasumsikan tersedia.

## Checklist sebelum training

- [ ] Rekam dataset version, tanggal akses, sumber asal setiap komponen, URL, nama archive, ukuran unduh/ekstraksi, SHA-256 dan manifest. Bandingkan kebutuhan disk dengan budget tim sebelum download.
- [ ] Verifikasi lisensi Kaggle dan komponen speech/noise, consent, atribusi serta hak penggunaan akademik/mixing/redistribusi. Jangan commit audio atau archive.
- [ ] Inventaris jenis data (paired, clean + noise, atau tidak memadai), jumlah file/durasi, speaker/source ID dan bahasa. Putuskan rute pipeline berdasarkan bukti, bukan judul dataset.
- [ ] Decode dan periksa sample rate/channel, panjang, alignment, duplikasi, silence, NaN dan clipping. Untuk paired, pastikan satu target sah per noisy; karantina mismatch dengan alasan.
- [ ] Bila mixing diperlukan, definisikan rentang SNR, perhitungan RMS termasuk silence guard, gain bersama untuk mencegah clipping, panjang/offset noise dan seed. Catat seluruh provenance setiap pasangan. Mixing belum diimplementasikan.
- [ ] Pertahankan split resmi hanya jika tersedia dan bebas leakage. Jika tidak ada, buat manifest train/validation/test yang dibekukan sebelum training, dikelompokkan menurut speaker dan sumber rekaman; rasio/jumlah ditetapkan setelah inventory. Jangan menganggap ada test resmi. Bila speaker ID tidak tersedia, gunakan source grouping yang dapat ditelusuri dan nyatakan keterbatasan; jangan mengklaim speaker-disjoint tanpa bukti.
- [ ] Pisahkan sumber noise antar split bila membuat pasangan sintetis; audit hash/source overlap termasuk potongan rekaman dan turunannya. Test tidak dipakai untuk tuning/normalisasi.
- [ ] Resample pasangan identik ke target mono 16 kHz dengan antialiasing; verifikasi delay/panjang dan kebijakan downmix. Target model bukan fakta sample rate dataset.
- [ ] Crop training awal berpasangan 32000 sampel (2 detik). Untuk v1, gunakan segmen penuh: klip lebih pendek ditandai excluded_from_initial_training dengan jumlah/durasi dilaporkan, tidak digabung lintas penutur atau diulang agar tampak panjang. Validation/test tetap menyertakan klip pendek via padding/trim inference. Gunakan gain pasangan yang sama dan simpan skala; jangan normalisasi clean/noisy independen.
- [ ] Augmentasi acak hanya pada train; validation/test tetap beku. Campuran sintetis evaluasi dibuat sekali dari sumber held-out, bukan diacak tiap evaluasi.
- [ ] Ukur kebutuhan storage/cache/checkpoint, RAM/VRAM dan waktu training setelah izin yang sesuai. Perubahan pilihan dataset ini tidak mengotorisasi download, instalasi atau training.

Pemilik: A2; review provenance/leakage/lisensi A4 dan kontrak input A1. Seluruh checklist masih terbuka. Hasil inventory harus menentukan apakah dataset cukup untuk objective dan metrik berpasangan sebelum eksperimen formal.

## Riwayat keputusan

## Kontrak data Member 2 untuk Member 1 dan 3

Versi **nirava-data-v1**, kompatibel dengan **nirava-stft-cgan-v1**. Ini spesifikasi handoff, bukan hasil audit atau loader yang sudah tersedia.

| Field batch | Bentuk/tipe | Makna |
|---|---|---|
| noisy | float32 `[B,32000]` | Mono16kHz, finite, gain sudah didokumentasi |
| clean | float32 `[B,32000]` | Target aligned, crop start/end dan gain sama |
| num_samples | int64 `[B]`, semuanya32000 saat training awal | Jangan menghitung padding sebagai ucapan valid |
| sample_id / utterance_id | daftar B ID opaque | Telusur ke manifest, bukan path publik |
| speaker_id / source_id / split | metadata B item | Speaker-aware separation; lineage sumber dan turunan |
| crop_start / gain / mixing_id | metadata B item | Reproduksi crop, inverse gain, dan campuran bila sintetis |

Waveform memiliki headroom: bila peak pasangan melebihi0,99 terapkan faktor penurun yang sama ke clean/noisy dan rekam; jangan menaikkan setiap klip ke peak maksimum. Tidak melakukan normalisasi tiap sisi sendiri. STFT tidak disediakan/cached secara default oleh A2, agar preprocessing hanya satu implementasi milik adaptor model A3. Float waveform bukan PCM integer atau mel image. Alignment harus pada tingkat sampel dan diverifikasi, bukan sekadar panjang sama.

Manifest minimal: sample/utterance/speaker/source IDs, dataset version, split, private storage reference, checksum, izin/lisensi/provenance, sample rate/channel asli dan setelah proses, original/valid length, crop start, gain, exclusion reason. Untuk mixing tambahkan noise_source_id, offset, SNR, seed dan mixing version. Paths/consent pribadi tidak dipublikasikan; ringkasan audit anonim dapat masuk Git.

Fallback mixing jika komponen sah tersedia: split speaker/utterance dan source noise dahulu, lalu y=x+a*n dengan a=RMS(x)/(RMS(n)*10^(SNR/20)); RMS hanya wilayah valid dan kebijakan silence/epsilon eksplisit. Starting SNR train uniform−5..20dB dan held-out fixed0/5/10/15dB adalah usulan untuk disepakati sesudah inventory, bukan label asli dataset. Noise senyap di-resample atau ditolak dengan log, bukan dibagi nol. Common gain mencegah clipping kedua target/input. Noise pendek boleh ditile hanya dalam source/split sama dengan kebijakan seam tercatat. Validation/test mix dibuat sekali dan manifest dibekukan; augmentation tambahan hanya train.

Split harus menahan seluruh speaker dan seluruh turunan utterance. Jika speaker ID tidak tersedia, A2 melaporkan gap kepada A1; source grouping dapat didokumentasikan sebagai batasan tetapi **belum memenuhi speaker-aware acceptance** tanpa bukti tambahan atau pengecualian dosen yang eksplisit. Speaker tunggal/tidak cukup kelompok tidak boleh diklaim mendukung evaluasi speaker-disjoint. Jumlah/rasio split baru ditetapkan setelah inventory. Tidak random-split crop; audit hash dan parent IDs, termasuk noise, lintas split.

Handoff A2: laporan dataset/licence/shape/alignment, manifest freeze + hash, jumlah speaker/utterance/durasi tiap split dan exclusions, synthetic mixing decision, contoh batch contract setelah implementasi diizinkan. A1/A3 review sebelum training formal; tidak ada download atau implementasi pada task Member1.

## Riwayat keputusan dataset

Pilihan terdahulu [muhmagdy/valentini-noisy](https://www.kaggle.com/datasets/muhmagdy/valentini-noisy) dibatalkan karena ukuran menurut pengguna. Catatan audit/log terdahulu dipertahankan sebagai riwayat, bukan sumber aktif. Tidak ada bukti download/training dari dataset lama maupun baru. Stage 1 tetap GO tertunda.
