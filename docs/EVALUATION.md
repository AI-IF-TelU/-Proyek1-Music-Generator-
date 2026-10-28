# Evaluation Nirava MIDI

Rencana Stage1, belum ada hasil. Tujuan: model mempelajari distribusi melodi dan menghasilkan file MIDI yang valid, bervariasi dan layak ditinjau manusia, tanpa klaim orisinalitas mutlak.

## Evaluasi held-out

Token NLL/perplexity raw sebelum grammar mask, next-token accuracy non-PAD sebagai sekunder, token count dan breakdown NOTE/HOLD/REST/EOS. Bandingkan unigram train-only; split work-disjoint, tidak tuning test. NLL rendah bukan bukti musik bagus atau tidak menyalin.

Sampling suite tetap: contoh10seed × 4/8/16bar × temperature default1, top-k20, checkpoint sama; listening pilih subset sebelum melihat hasil (usulan5clips/seed yang ditentukan, tiga pendengar). Bandingkan juga3temperature pada seed tetap sebagai sensitivity, bukan cherry-pick. Angka suite adalah rencana yang perlu budget, belum dilakukan.

Catat raw invalid-mass/invalid next-token rate (misal HOLD inactive), post-mask/export parser validity, finite onset/duration, note-on/off balance, nonempty/non-silent rate, repair/mask count, learned EOS versus length_cap dan panjang aktual. Grammar menjamin sebagian validitas; laporkan intervensinya terpisah dari kualitas model.

Deskriptif: pitch range/class histogram, note/rest/duration diversity, note density, repeated n-gram/loop rate. Cocokkan distribusi held-out dengan keterbatasan style corpus, bukan memaksimalkan entropy. Memorization: longest matching token span dan exact/near-match melodi terhadap train setelah canonicalization serta transposition-aware check bila layak; lagu pendek/idiom umum membuat ambang ambigu. Tidak mengklaim lolos similarity berarti bebas hak cipta.

Listening blind/random order via renderer/DAW yang sama bila tersedia: coherence, rhythm, variety, perceived repetition rating1..5 dan alasan. Renderer bukan model utama, audio rendering bukan fitur MVP. Catat instrumen/tempo, peserta dan jumlah contoh; jangan menyebut penilaian kecil sebagai generalisasi populasi.

## Kelayakan dan acceptance usulan

Parser/export structural validity100% pada suite, tidak ada hanging note, cap selalu ditegakkan, failure transparan; validitas token raw dilaporkan bukan disembunyikan. Validation NLL membaik terhadap unigram dan baseline awal harus dibuktikan, tanpa ambang performa rekaan. Rating/listening dan batas repetition disepakati sebelum eksperimen setelah memahami corpus. Peak RAM/VRAM, cold model load, warm token/sec dan detik per128step di host/batch1 yang dicatat; lima ulang per seed uji terbatas, median/p95 deskriptif. Budget absolut ditetapkan tim sebelum run.

Tes setelah izin: parser limits, quantization, canonical round-trip, work leakage, shifted targets/PAD, causal inference, gradient, checkpoint/resume, invalid token masking, temperature edge, deterministic seed dan max-step termination. Tidak lagi memakai STOI/PESQ/SI-SDR, intelligibility speech atau A/B audio; rencana lama diarsipkan.
