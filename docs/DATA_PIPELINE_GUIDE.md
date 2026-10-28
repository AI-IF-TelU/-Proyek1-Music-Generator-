# Nirava MIDI Data Pipeline & Execution Guide

**Role:** Member 2 (Data Pipeline & Preprocessing Engineer)  
**Contract Version:** `nirava-midi-data-v1` / `nirava-midi-step-v1`  
**Target Recipient:** Member 3 (Training Engineer) & Tim Nirava

---

## 1. Persyaratan Lingkungan (Environment Requirements)

- **Python:** 3.10, 3.11, atau 3.12 (teruji pada Python 3.12.10 64-bit).
- **PyTorch:** `torch >= 2.0.0` (teruji pada `torch==2.15.0+cpu` untuk CPU dan kompatibel dengan build CUDA).
- **Dependensi Eksternal:** **Nol (Zero external MIDI libraries)**. Seluruh parser SMF binary, tokenizer, pengelompokan fingerprint, dan DataLoader ditulis murni dengan Python standard library (`struct`, `json`, `hashlib`, `random`, `pathlib`).
- **File requirements:** [`requirements.txt`](../requirements.txt)
  ```text
  torch>=2.0.0
  ```

---

## 2. Panduan Setup Lingkungan Bersih (Clean Setup)

Gunakan perintah relatif terhadap root direktori proyek (hindari path absolut):

### A. Windows (PowerShell)
```powershell
# 1. Masuk ke root direktori proyek
cd <path-to-nirava-repo>

# 2. Buat virtual environment
python -m venv .venv

# 3. Aktifkan virtual environment
.venv\Scripts\activate

# 4. Install dependensi
pip install -r requirements.txt
```

> [!TIP]
> **Opsional (Untuk Member 3 dengan GPU NVIDIA / CUDA):**  
> Jika menggunakan GPU (misalnya RTX 5060 dengan driver >= 528 / 616), pasang build PyTorch CUDA:
> ```powershell
> pip install torch --index-url https://download.pytorch.org/whl/cu126
> ```

### B. Linux / macOS (Bash / Zsh)
```bash
# 1. Masuk ke root direktori proyek
cd <path-to-nirava-repo>

# 2. Buat virtual environment
python3 -m venv .venv

# 3. Aktifkan virtual environment
source .venv/bin/activate

# 4. Install dependensi
pip install -r requirements.txt
```

---

## 3. Eksekusi Uji Coba Unit Test (34 Tests)

Seluruh komponen pipeline memiliki unit test mandiri:
- `tests/test_nirava_midi_tokenizer.py` (17 tes): parser SMF, quantizer grid, filter pitch-bend/pedal, decode grammar, round-trip 100%.
- `tests/test_nirava_midi_data.py` (11 tes): windowing stride 128, right-PAD, target shift, isolasi work-group, split deterministik.
- `tests/test_nirava_midi_torch.py` (6 tes): konversi tensor `int64[B,128]`, `bool[B,128]`, loss mask, split riil, validasi batch.

### Menjalankan Seluruh Tes:

**Windows PowerShell:**
```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
```

**Linux / macOS:**
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

**Output yang diharapkan:**
```text
Ran 34 tests in ~1.5s
OK
```

---

## 4. Reproduksi Pipeline Data dari Nol (Step-by-Step)

Jika cache token di direktori `processed/` belum ada atau ingin dibangun ulang secara deterministik:

### Langkah 1: Audit Dataset & Tokenizer
Memeriksa seluruh 1034 file MIDI di folder `data/.../MIDI/melody/`, menguji filter 4/4, monophony, dan round-trip consistency:
```bash
python src/run_tokenizer_audit.py
```
- Output: `reports/tokenizer_audit.csv`, `reports/tokenizer_audit_summary.txt`.
- Hasil terverifikasi: 519 file ter-encode, 501 ditolak non-4/4, 14 ditolak overlap grid, 519/519 lulus round-trip identik.

### Langkah 2: Work-Disjoint Grouping & Split 80/10/10
Mengekstrak fingerprint n-gram invarian transposisi, mendeteksi duplikat, mengelompokkan karya dekat (Jaccard ≥ 0.25), membagi split secara deterministik (seed: 20261028), dan menulis token kanonik:
```bash
python src/build_splits.py
```
- Output: `reports/split_manifest.csv`, `reports/work_groups.csv`, `reports/split_exclusions.csv`, `reports/split_summary.txt`, `processed/tokens_v1.jsonl`.
- Hasil terverifikasi: 517 karya unik (2 exact duplicate dibuang: `hpps25` dan `reelsm-q24`), 494 work groups, 414 train / 52 validation / 51 test.

### Langkah 3: Augmentasi Transposisi Train-Only
Meng-augmentasi **hanya** split train dengan 11 offset transposisi (±5/+6 semitone):
```bash
python src/augment_transpose.py
```
- Output: `processed/tokens_v1_aug.jsonl`.
- Hasil terverifikasi:
  - Train: 414 original + 4.554 transposed = 4.968 pieces (menghasilkan **26.364 windows**).
  - Validation: 52 pieces (269 windows, 100% untouched).
  - Test: 51 pieces (277 windows, 100% untouched).

---

## 5. Panduan Konsumsi untuk Member 3 (Training Interface)

Member 3 dapat langsung mengonsumsi batch PyTorch melalui iterator `TorchMidiLoader` di `src/nirava_midi_torch.py`:

```python
from nirava_midi_torch import TorchMidiLoader

# 1. Inisialisasi Loader untuk Split Tertentu
train_loader = TorchMidiLoader(
    tokens_jsonl="processed/tokens_v1_aug.jsonl",
    split="train",         # "train", "validation", atau "test"
    batch_size=32,
    shuffle=True,          # Otomatis True untuk train
    seed=20261028,
    drop_last=False
)

# 2. Iterasi Batch dalam Training Loop
for batch in train_loader:
    # --- Tensor Tensors ---
    x = batch["input_ids"]     # torch.int64 [B, 128], rentang token 0..132
    y = batch["target_ids"]    # torch.int64 [B, 128], shifted 1 langkah ke kanan dari x
    mask = batch["loss_mask"]  # torch.bool  [B, 128], True untuk posisi valid (termasuk EOS)
    lengths = batch["lengths"] # torch.int64 [B], jumlah token valid per sample (1..128)
    
    # --- Metadata Python List ---
    piece_ids = batch["piece_id"]         # list of str [B]
    group_ids = batch["work_group_id"]    # list of str [B]
    splits    = batch["split"]            # list of str [B]
    starts    = batch["window_start"]     # list of int [B]
    
    # --- Contoh Forward Pass & Loss Masking ---
    # logits = model(x) # expected shape: [B, 128, 133]
    # loss = criterion(logits.view(-1, 133), y.view(-1))
    # loss = (loss * mask.view(-1)).sum() / mask.sum()
```

### Spesifikasi Semantik Token (V=133):
| Token ID | Simbol | Arti Musikal |
|---|---|---|
| `0` | `PAD` | Padding akhir window (diabaikan oleh `loss_mask`) |
| `1` | `BOS` | Penanda awal komposisi (hanya muncul di window index 0 suatu piece) |
| `2` | `EOS` | Penanda akhir komposisi |
| `3` | `REST` | Satu langkah hening (1/16 bar) |
| `4` | `HOLD` | Memperpanjang nada aktif sebelumnya 1 langkah |
| `5..132` | `NOTE_0..127` | Artikulasi nada MIDI pitch `0..127` (pitch = token_id - 5) |

---

## 6. Lisensi Dataset & Atribusi

- **Repository Upstream:** [jukedeck/nottingham-dataset](https://github.com/jukedeck/nottingham-dataset)
- **Pinned Commit:** `0992bb6cd864f6d4b90d6663e08c0ef53ffaa08f` (2017-03-03)
- **Lisensi Repositori:** GNU General Public License v3.0 (GPLv3).
- **Asal Data:** Nottingham Music Database (koleksi musik folk tradisional Inggris/Irlandia/Amerika).
- **Status Hak Cipta:**
  - Melodi dasar adalah lagu tradisional (folk public domain).
  - Transkripsi dan representasi digital ABC/MIDI dirilis secara terbuka di bawah GPLv3.
  - Penggunaan pada proyek Nirava ditujukan murni untuk keperluan akademik non-komersial.
  - Review formal hak cipta/atribusi bersama dosen pembimbing tetap dijadwalkan pada evaluasi Stage 1.

