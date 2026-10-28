# MIDI tokenization Nirava

Versi **nirava-midi-step-v1**, usulan Stage 1. Sumber data MIDI simbolik, bukan byte-level model atau waveform. [MIDI Association](https://midi.org/standard-midi-files) menjelaskan SMF sebagai pertukaran data MIDI bertimestamp; token berikut adalah format tim, bukan standar encoding MIDI.

## Grid dan vocabulary tetap

Monofonik, satu pitched instrument, 4/4, empat langkah per quarter note (16 langkah/bar). Pitch penuh0..127; velocity tidak diprediksi, export80. Vocabulary **V=133**:

| ID | Token | Arti |
|---|---|---|
| 0 | PAD | Padding batch, bukan event musik |
| 1 | BOS | Awal piece, bukan satu langkah waktu |
| 2 | EOS | Akhir piece, bukan satu langkah waktu |
| 3 | REST | Tutup nada aktif dan majukan satu langkah diam |
| 4 | HOLD | Pertahankan nada aktif satu langkah; invalid bila tidak ada nada aktif |
| 5+p | NOTE_p, p0..127 | Tutup nada aktif lalu mulai pitch p selama satu langkah |

NOTE_p yang diikuti NOTE_p mengartikulasikan ulang nada yang sama; HOLD memperpanjang note sebelumnya. BOS tidak boleh muncul di tengah, PAD tidak boleh digenerate. [Daftar pesan MIDI resmi](https://midi.org/expanded-midi-1-0-messages-list) menjadi rujukan note number dan note-on/off; tidak menyalin parser/implementasi pihak lain.

## Parsing dan canonicalization yang diusulkan

A2 memeriksa header/type/timebase dan batas file/event. Terima SMF type0/1 dengan PPQ positif dan tepat satu pitched part yang dinyatakan monofonik; merge absolute event time secara deterministik hanya untuk part itu. Tolak type2, SMPTE division, drum-only, beberapa pitched part tanpa kurasi eksplisit, polyphony, unmatched on/off, pedal/sustain atau pitch-bend aktif, dan meter selain4/4/perubahan meter. Normalize note-on velocity0 sebagai note-off. Pembatasan ini adalah scope v1, bukan penilaian seluruh MIDI.

Ubah onset/end menjadi quarter-note units dari PPQ, lalu grid index=floor(4*q+0.5). End harus > onset: bila quantization meruntuhkan durasi, usulkan minimum1step dan catat perubahan. Jika setelah quantization muncul overlap, tolak dengan alasan; jangan diam-diam memilih highest note atau chord reduction. Susun note-off sebelum note-on pada timestamp sama. Audit dampak quantization dan jumlah yang dikecualikan.

Tempo sumber dicatat; onset dalam beat/quarter tidak memakai detik. Tempo map tidak dimodelkan dan rendering export dinormalisasi120BPM; time signature diasumsikan4/4 hanya jika eksplisit atau default MIDI dengan provenance tercatat. Instrumen dan velocity asli disimpan sebagai metadata audit tetapi output memakai piano/80. Trim leading silence ke onset pertama, akhir sampai last note-off, pad REST hingga bar lengkap; simpan offset asli dan padding. Empty piece ditolak.

Piece canonical adalah [BOS, step1,...,stepN, EOS], N kelipatan16. Tidak menyisipkan BOS/EOS per training crop. Tokenisasi dapat lossy terhadap timing/tempo/velocity; round-trip diuji terhadap **melodi canonical**, bukan byte-for-byte MIDI sumber.

## Export dan sampling grammar

Decoder memelihara clock step dan satu active note. Emit note-off sebelum pergantian NOTE atau REST; tutup active note pada EOS/stop. SMF type0, satu track, channel0, program0, PPQ480, tiap langkah120ticks, tempo500000microseconds/quarter dan time signature4/4, end-of-track eksplisit. Export mencakup leading/trailing canonical rests; tidak ada hanging note. Parse ulang output untuk memverifikasi event/timing.

Default target8bar=128step, opsi4/16bar. Selama langkah < target, mask PAD/BOS/EOS dan mask HOLD bila inactive; NOTE/REST diizinkan. Pada target, berhenti dan tambahkan EOS secara deterministik, tutup note; laporkan **length_cap** bukan klaim EOS dipelajari. Untuk evaluasi kemampuan akhir alami, mode terpisah mengizinkan EOS setelah minimum1bar dan mencatat early/learned EOS vs forced cap; jangan mencampur metrik kedua mode. Temperature positif0.5..1.5 (default1), top-k20 setelah grammar mask (clamp ke jumlah token sah), seed tersimpan. Tidak menerima text/style conditioning di v1.

Catat probabilitas token sebelum mask, invalid-mass serta jumlah intervensi; file valid karena grammar bukan bukti semua sequence mentah model valid. Jika tidak ada kandidat finite atau output kosong/silent, laporkan failure; jangan regenerate diam-diam sampai terdengar baik. Ekspor bukan jaminan musik bebas plagiasi.

## Trade-off

Step tokens menghasilkan vocabulary kecil dan grammar sederhana, cocok untuk eksperimen awal. Mereka membatasi ritme pada grid, ekspresi dan polyphony. Event NOTE_ON/OFF/TIME_SHIFT memungkinkan ekspresi lebih luas tetapi grammar, panjang sequence dan pairing lebih rumit. V1 memilih grid monofonik secara eksplisit; perlu persetujuan cakupan dosen sebelum implementasi.
