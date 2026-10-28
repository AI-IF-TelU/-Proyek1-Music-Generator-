# API Spec Nirava MIDI draft

Kontrak target menggantikan endpoint enhancement, belum implementasi. Base `/api/v1`, error JSON {code,message}, request schema menolak extra fields. Next.js hanya mengakses FastAPI. MVP tanpa upload file/prefix MIDI atau prompt teks.

## Endpoint yang diusulkan

- GET /health →200 status ok tanpa secrets.
- POST /generations: JSON {bars:8,seed:42,temperature:1.0}; bars enum4/8/16, seed integer0..2147483647, temperature finite0.5..1.5. Nilai default dinyatakan pada UI/backend sama, top-k20 server fixed.202 {job_id,job_token,status:pending}.400 malformed JSON,413 JSON body melebihi batas target8KiB,422 nilai/schema salah,429 queue penuh dengan Retry-After. Jangan retry POST otomatis tanpa idempotency.
- GET /generations/{job_id}: X-Job-Token,200 {job_id,status,expires_at,model_version,tokenizer_version,bars,seed,temperature,step_count,note_count,termination_reason,processing_seconds,error}. Nilai hasil null hingga tersedia. processing_seconds durasi terukur, bukan persentase. Status pending/processing/completed/failed/expired.
- GET /generations/{job_id}/midi: token, completed saja, stream output .mid dengan Content-Type audio/midi dan Content-Disposition nama server aman. Status409 sebelum completed/failed. Tidak mengekspos path. Frontend fetch berheader lalu object URL untuk download.
- DELETE /generations/{job_id}: token,204 mencabut akses/menandai expired dan menjadwalkan cleanup, bukan bukti bytes sudah hilang. Idempotent pada tombstone berizin.

## Lifecycle dan keamanan

Token32byte random baru saat POST, dikembalikan sekali, hanya di memori browser dan hash database; constant-time comparison. Semua respons job Cache-Control:no-store; header token dan create body disunting dari log. Unknown job atau token salah/hilang404 identik, expired terotorisasi410 sampai tombstone purged lalu404. Invalid UUID422, DELETE tombstone204. DELETE/expiry atomik mengalahkan publish; worker membuang late output.

CORS origin allowlist, GET/POST/DELETE/OPTIONS, headers X-Job-Token/Content-Type; expose Content-Disposition/Retry-After. JSON size limit proxy/API, request rate limit, queue/time/token cap, finite numeric checks, safe path server, tidak mengeksekusi metadata MIDI sebagai instruksi. Semua export parse ulang sebelum completed. Batas maksimum256step, event/file/time absolut diverifikasi saat profiling; tidak memakai angka ukuran WAV lama.

Polling awal2detik, backoff429/network, berhenti terminal. Retensi24jam dan tombstone1jam setelah expires_at masih usulan kebijakan. Detail storage/security pada ARCHITECTURE. Tidak ada route enhancement atau audio download sebagai API aktif.
