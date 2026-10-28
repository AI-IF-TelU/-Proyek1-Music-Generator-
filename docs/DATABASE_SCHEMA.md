# Database Schema Nirava MIDI proposal

Dokumentasi target, **tidak ada skema database atau migrasi yang dijalankan**. Rancangan enhancement_jobs lama dipertahankan di arsip speech; tabel/kolom berikut tidak dianggap sudah ada. Saat implementasi diizinkan gunakan Alembic, bukan create_all production.

## generation_jobs usulan

UUID id PK server-generated; access_token_hash NOT NULL; status enum pending/processing/completed/failed/expired; bars INTEGER4/8/16; seed INTEGER bounded; temperature DOUBLE PRECISION finite/in range; model_version/tokenizer_version TEXT; output_storage_key TEXT nullable; step_count/note_count/output_size_bytes nullable; termination_reason nullable; processing_seconds nullable; error_code nullable; created_at/started_at/completed_at/expires_at TIMESTAMPTZ. PostgreSQL menyimpan metadata, bukan MIDI bytes, tokens corpus atau weights.

CHECK target: durations/counts nonnegative ketika terisi, size positif, expires_at>created_at. Index status/created_at dan expires_at. Source file path tidak berasal dari pengguna. Tidak ada original_filename/sample_rate/channel atau input_audio key untuk MVP tanpa upload. Version fields mendukung lineage checkpoint; token/hash/path privat tidak dicatat pada log.

## Retention target

Output24jam, expired menutup akses langsung pada request. Cleanup menghapus storage dengan retry; simpan storage key sampai deletion sukses. Tombstone id/access hash/status/expiry minimal sampai expires_at+1jam, lalu purge hanya setelah output termasuk late worker telah ditangani. Field nonminimal dapat nullable/dihapus pada tombstone sesuai kebijakan. Publish update completed atomik hanya jika status processing dan belum expired. Kebijakan privasi/retensi perlu konfirmasi; tidak ada user table MVP.
