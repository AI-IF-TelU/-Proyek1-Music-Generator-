> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# API Contract — v1 draft

Base path `/api/v1`; JSON errors `{ "code": "...", "message": "..." }`. Seluruh operasi pada job yang sudah dibuat memakai token akses rahasia pada header `X-Job-Token`, dikirim hanya ke pemilik sesi browser; tidak masuk URL atau log.

## `GET /health`
200 `{ "status": "ok" }` (jangan tampilkan secrets atau detail infrastruktur).

## `POST /enhancements`
`multipart/form-data` dengan field `file`. 202:
```json
{"job_id":"uuid","job_token":"random-secret","status":"pending"}
```
Pembuatan job tidak membutuhkan `X-Job-Token`; token baru dikembalikan sekali pada respons 202. Gunakan minimal 32 byte acak kriptografis, hash di database, bandingkan secara constant-time, dan simpan token hanya di memori sesi browser. Respons 202 memakai `Cache-Control: no-store`. Token hilang berarti akses job tidak dapat dipulihkan pada MVP.

400 untuk multipart rusak, 413 untuk ukuran di atas 25 MB (25.000.000 byte), 415 untuk format selain WAV/MP3 atau codec tidak didukung, 422 untuk audio gagal didekode, kosong, durasi di atas 120 detik, atau sample rate tidak didukung. 429 untuk kapasitas antrean/konkurensi penuh, dengan `Retry-After`. Batas diperiksa sebelum menerima job; file sementara dibersihkan jika ditolak.

## `GET /enhancements/{job_id}`
Header `X-Job-Token`. 200:
```json
{"job_id":"uuid","status":"processing","duration_seconds":12.4,"processing_seconds":null,"error":null}
```
Status: `pending | processing | completed | failed | expired`.

## `GET /enhancements/{job_id}/audio?version=original|enhanced`
Header `X-Job-Token`; stream audio; enhanced hanya tersedia setelah completed. Gunakan `Cache-Control: private, no-store`; jangan ekspos path disk. Respons sukses 200 memiliki `Content-Type` sesuai encoding aktual dan `Content-Disposition` dengan nama aman. Hasil enhanced menggunakan WAV PCM; encoding/sample rate final ditetapkan setelah pemilihan model. Frontend mengambil audio dengan fetch berheader token lalu membuat object URL, karena elemen audio/link biasa tidak mengirim header khusus; revoke object URL saat selesai.

## `DELETE /enhancements/{job_id}`
Header `X-Job-Token`; cabut akses secara atomik dengan status expired dan jadwalkan penghapusan audio. Respons 204 berarti akses telah dicabut, bukan bukti penghapusan fisik selesai; cleanup yang gagal diulang. Operasi idempotent.

## Security/limits
CORS allowlist eksplisit, request size limit pada reverse proxy dan API, rate limit, MIME + magic/decoder verification, UUID opaque, token di-hash pada DB, tidak simpan token plaintext. Pembersihan file pada error dan expiry.

## Respons dan lifecycle bersama
- Job tidak ada atau token salah/hilang: 404 dengan pesan identik; jangan membocorkan keberadaan job.
- Job expired yang metadata otorisasinya masih tersedia: 410 untuk status/audio. Setelah metadata dibersihkan: 404.
- Enhanced diminta sebelum completed atau sesudah failed: 409. Parameter version tidak valid atau UUID tidak valid: 422.
- Error API, termasuk validasi framework, memakai envelope JSON di atas; respons 204 tidak memiliki body. `error` pada status adalah null atau objek `{ "code": "...", "message": "..." }` yang aman.
- Transisi normal: pending -> processing -> completed/failed; job aktif maupun terminal dapat menjadi expired saat dihapus atau melewati retensi. Retensi dihitung dari created_at.
- DELETE terotorisasi pada tombstone expired tetap 204 sampai metadata dibersihkan. Job yang sudah dibersihkan mengembalikan 404.
- Penghapusan saat inference berjalan menandai expired secara atomik; worker tidak boleh menerbitkan hasil atau mengubah expired kembali menjadi completed. Hapus output terlambat dan lakukan retry cleanup jika storage gagal.
- Polling awal setiap 2 detik, berhenti pada completed/failed/expired; backoff pada 429 atau gangguan jaringan.

## Detail integrasi yang harus diuji pada Stage 2
- Semua respons job, termasuk status dan error, memakai `Cache-Control: no-store`. Redaksi header X-Job-Token dan body respons create pada log proxy/APM wajib.
- CORS hanya origin frontend terkonfigurasi; izinkan GET, POST, DELETE, OPTIONS dan header X-Job-Token/Content-Type. Expose Content-Disposition dan Retry-After bila dibaca frontend. Jangan memakai wildcard origin.
- Batas 25.000.000 byte berlaku untuk isi file; batas request proxy harus memberi ruang overhead multipart. API membatasi stream sebelum seluruh file masuk memori. Missing file/multiple file ditolak 422.
- MVP mengambil file utuh via fetch; Range/206 belum dijanjikan. Hanya satu versi A/B bersuara pada satu waktu; frontend menyamakan posisi waktu. Backend harus mengompensasi latency/padding model agar timeline hasil sepadan dan mencatat durasi hasil.
- Status response mencantumkan expires_at (UTC ISO 8601). processing_seconds adalah waktu inference terukur setelah selesai/gagal, bukan persentase progress.
- Status job dibaca dengan expiry check pada request; jangan menunggu scheduler untuk mencabut akses. Worker hanya dapat mengklaim pending satu kali secara atomik.
- Setelah cleanup metadata selesai, DELETE ulang menjadi 404; frontend memperlakukan 404/410 sebagai akses yang sudah tidak tersedia. Jangan retry POST otomatis karena MVP belum memiliki idempotency key.
