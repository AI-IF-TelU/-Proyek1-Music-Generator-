# PRD Nirava MIDI Music Generator

**Stage 1, usulan untuk review.** Membantu mahasiswa/pemusik pemula memperoleh ide melodi pendek yang dapat diedit dalam DAW melalui MIDI, bukan menghasilkan rekaman suara.

## MVP dan alur

Pilih 4/8/16 bar, seed integer dan temperature terbatas → kirim job → tampilkan pending/processing/completed/failed/expired → periksa note grid, jumlah nada/bar, model version dan termination reason → unduh .mid. Piano-roll adalah representasi simbolik; browser playback/render audio opsional di luar MVP, bukan dependensi keberhasilan demo.

Acceptance target: output SMF type0 satu track piano, grid 4/4, 120 BPM, PPQ480, satu melodi tanpa tumpang-tindih, note-on/off seimbang; rentang pitch MIDI0..127, velocity80. Panjang bar dikonversi menjadi maksimal 64/128/256 langkah enam-belas; kebijakan EOS dan forced end dijelaskan pada MIDI_TOKENIZATION. Token invalid/repair/failure tidak disembunyikan. Belum ada output atau performa terukur.

## Akademik

Model autoregressive LSTM dari inisialisasi acak, tokenizer tim, data audit dan split work-disjoint, loop/loss/eksperimen serta metrik held-out dan log LLM wajib. Stack Next.js/TypeScript, FastAPI/Python/PyTorch, PostgreSQL dipertahankan. Penugasan MIDI dikonfirmasi pengguna; kompleksitas LSTM dan syarat usia kategori perlu review dosen.

## Batas lingkup

V1 monofonik, satu instrumen, fixed tempo/meter/velocity. Tidak menghasilkan chord/multitrack atau mempelajari ekspresi velocity, tempo dan pedal. Tidak ada speech dataset, WAV preprocessing, STFT/cGAN, A/B denoising, transkripsi atau pretrained utama. Tidak ada dataset yang dipilih/diunduh. Tidak ada akun/billing/upload pengguna atau training via UI.

## Ukuran sukses dan pertanyaan

NLL/perplexity held-out, valid export, repair/termination rate, variasi ritme/pitch, repetition/memorization, penilaian musikal pendengar, latency dan peak memory. Angka target dibekukan sebelum eksperimen, bukan hasil. Pertanyaan: hak data MIDI, cakupan monofonik, jumlah work/composer, budget hardware/tenggat, penerimaan LSTM manual, kebijakan retensi dan kontrol generation. Retensi24jam dan kapasitas host masih usulan.
