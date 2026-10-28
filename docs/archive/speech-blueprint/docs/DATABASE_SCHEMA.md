> ARSIP SPEECH — digantikan pivot MIDI 28 Oktober 2026. Dipertahankan untuk review/history, bukan persyaratan aktif atau instruksi kerja. Dokumen aktif berada di root repository dan docs/.

# PostgreSQL schema — draft

## `enhancement_jobs`
| Column | Type | Constraint / meaning |
|---|---|---|
| id | UUID | PK, generated server-side |
| access_token_hash | VARCHAR(128) | NOT NULL, hash token job |
| original_filename | VARCHAR(255) | sanitized display name |
| status | VARCHAR(16) | pending/processing/completed/failed/expired |
| input_storage_key | TEXT NULL | private storage key, not public URL |
| output_storage_key | TEXT NULL | enhanced audio key |
| content_type | VARCHAR(100) | detected MIME |
| file_size_bytes | BIGINT | positive |
| duration_seconds | DOUBLE PRECISION NULL | validated duration |
| processing_seconds | DOUBLE PRECISION NULL | runtime |
| error_code | VARCHAR(64) NULL | safe error category |
| created_at | TIMESTAMPTZ | default now() |
| started_at | TIMESTAMPTZ NULL | processing start |
| completed_at | TIMESTAMPTZ NULL | completion |
| expires_at | TIMESTAMPTZ | indexed for cleanup |

Indexes: `(status, created_at)`, `(expires_at)`. Alembic migrations as source of truth.

## Retention
Target 24h, adjustable after privacy requirements. Cleanup process deletes storage objects and metadata or retains only aggregate anonymized counters with explicit policy. Prevent stale paths and orphan files.

## No user table initially
MVP tanpa akun. Job token adalah capability credential; tetap ada risiko jika token bocor. Jangan simpan audio bytes di PostgreSQL.

## Constraints dan penghapusan (target migrasi)
Tambahkan CHECK untuk enum status, file_size_bytes > 0, durasi positif jika terisi, processing_seconds >= 0 jika terisi, serta expires_at > created_at. Validasi aplikasi tetap diperlukan.

Simpan detected_sample_rate_hz (INTEGER positif) dan detected_channels (INTEGER positif) sebagai metadata validasi decoder. Batas dukungan ditentukan setelah uji model; jangan menerima nilai tak terbatas hanya karena decoder dapat membacanya.

Saat expired, storage key boleh null setelah file berhasil dihapus. Pertahankan metadata minimal (id, access_token_hash, status, expires_at) sebagai tombstone setidaknya sampai expires_at + 1 jam untuk DELETE idempotent/410, lalu hapus. Nama file dan metadata audio dibersihkan saat file dihapus. Cleanup file yang gagal harus selesai sebelum baris dihapus agar objek tidak menjadi orphan. Periode tombstone ini usulan yang masih perlu persetujuan kebijakan privasi.

Simpan output_duration_seconds (DOUBLE PRECISION positif jika terisi) untuk verifikasi timeline A/B. Update completed beserta output_storage_key hanya berhasil bila status masih processing dan belum kedaluwarsa. Jika update kalah oleh DELETE/expiry, worker menghapus output yang baru dibuat.

Kolom original_filename, content_type, file_size_bytes, duration_seconds, detected_sample_rate_hz, detected_channels dan output_duration_seconds harus nullable untuk tombstone minimal; CHECK nilai positif berlaku ketika terisi. Jangan menghapus storage key yang masih diperlukan untuk retry cleanup. Purge metadata hanya setelah semua file dan output worker terlambat telah ditangani.
