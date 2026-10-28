"""Helper untuk membuat fixture processed/tokens_v1.jsonl sintetis untuk testing.

Memungkinkan pengujian unit TorchMidiLoader dan loop training berjalan
tanpa ketergantungan pada dataset biner Nottingham yang diabaikan Git.
"""

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

import nirava_midi_tokenizer as tk


def generate_piece_tokens(base_pitch=60, n_bars=8):
    """Buat sequence nada monofonik valid: [BOS, ..., EOS]."""
    steps = []
    pitches = [base_pitch, base_pitch + 2, base_pitch + 4, base_pitch + 5,
               base_pitch + 7, base_pitch + 9, base_pitch + 11, base_pitch + 12]
    total_steps = n_bars * tk.STEPS_PER_BAR
    step = 0
    while step < total_steps:
        # Pilih note dengan durasi 2 sampai 4 step
        p = pitches[(step // 4) % len(pitches)]
        duration = min(4, total_steps - step)
        steps.append(tk.note_token(p))
        for _ in range(duration - 1):
            steps.append(tk.HOLD)
        step += duration
        # Sisipkan rest sesekali jika masih ada sisa
        if step < total_steps and step % 16 == 0:
            steps.append(tk.REST)
            step += 1

    # Pad ke kelipatan STEPS_PER_BAR jika perlu
    rem = len(steps) % tk.STEPS_PER_BAR
    if rem > 0:
        steps += [tk.REST] * (tk.STEPS_PER_BAR - rem)

    return [tk.BOS] + steps + [tk.EOS]


def create_synthetic_tokens_jsonl(output_path=None):
    if output_path is None:
        output_path = ROOT / "processed" / "tokens_v1.jsonl"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    # Train: 8 pieces
    for i in range(8):
        toks = generate_piece_tokens(base_pitch=55 + (i * 2) % 15, n_bars=10 + (i % 4))
        h = hashlib.sha256(bytes(toks)).hexdigest()
        records.append({
            "piece_id": f"train_synth_{i:03d}",
            "work_group_id": f"wg_train_{i:03d}",
            "split": "train",
            "tokens_sha256": h,
            "tokens": toks,
        })

    # Validation: 2 pieces
    for i in range(2):
        toks = generate_piece_tokens(base_pitch=62 + i * 3, n_bars=8)
        h = hashlib.sha256(bytes(toks)).hexdigest()
        records.append({
            "piece_id": f"val_synth_{i:03d}",
            "work_group_id": f"wg_val_{i:03d}",
            "split": "validation",
            "tokens_sha256": h,
            "tokens": toks,
        })

    # Test: 2 pieces
    for i in range(2):
        toks = generate_piece_tokens(base_pitch=64 + i * 4, n_bars=8)
        h = hashlib.sha256(bytes(toks)).hexdigest()
        records.append({
            "piece_id": f"test_synth_{i:03d}",
            "work_group_id": f"wg_test_{i:03d}",
            "split": "test",
            "tokens_sha256": h,
            "tokens": toks,
        })

    with output_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"Fixture sintetis berhasil dibuat: {output_path} ({len(records)} pieces)")
    return output_path


if __name__ == "__main__":
    create_synthetic_tokens_jsonl()
