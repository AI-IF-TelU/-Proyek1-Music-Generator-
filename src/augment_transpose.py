"""Augmentasi transposisi train-only.

Membaca processed/tokens_v1.jsonl, meng-augmentasi piece di split train
dengan transposisi ±k semitone (pitch tetap 0..127), menulis hasilnya
ke processed/tokens_v1_aug.jsonl. Validation/test disalin apa adanya.

Lineage: tiap piece augmentasi mencatat parent_piece_id dan transpose_offset.
"""

import json
from pathlib import Path

import nirava_midi_tokenizer as tk

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "processed" / "tokens_v1.jsonl"
DST = ROOT / "processed" / "tokens_v1_aug.jsonl"

OFFSETS = list(range(-5, 7))  # -5..+6 semitone, total 12 versi termasuk 0


def transpose_tokens(tokens, offset):
    """Transposisi token, skip PAD/BOS/EOS/REST/HOLD. Raise jika di luar 0..127."""
    out = []
    for t in tokens:
        if tk.is_note(t):
            p = tk.token_pitch(t) + offset
            if not 0 <= p <= 127:
                return None  # tidak bisa ditransposisi sejauh ini
            out.append(tk.note_token(p))
        else:
            out.append(t)
    return out


def main():
    records = [json.loads(line) for line in SRC.read_text("utf-8").splitlines()]
    out = []

    for rec in records:
        if rec["split"] != "train":
            out.append(rec)
            continue

        # asli (offset 0) tetap ada
        out.append(rec)

        # transposisi
        for offset in OFFSETS:
            if offset == 0:
                continue
            transposed = transpose_tokens(rec["tokens"], offset)
            if transposed is None:
                continue  # pitch keluar 0..127, lewati
            out.append({
                "piece_id": f"{rec['piece_id']}_t{offset:+d}",
                "work_group_id": rec["work_group_id"],
                "split": "train",
                "tokens_sha256": "",  # bukan piece asli
                "tokens": transposed,
                "parent_piece_id": rec["piece_id"],
                "transpose_offset": offset,
            })

    DST.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n",
                   encoding="utf-8")

    train_orig = sum(1 for r in out if r["split"] == "train" and r.get("transpose_offset", 0) == 0)
    train_aug = sum(1 for r in out if r["split"] == "train" and r.get("transpose_offset", 0) != 0)
    val = sum(1 for r in out if r["split"] == "validation")
    test = sum(1 for r in out if r["split"] == "test")

    print(f"Input: {len(records)} pieces")
    print(f"Output: {len(out)} pieces -> {DST}")
    print(f"  train: {train_orig} original + {train_aug} augmented = {train_orig + train_aug}")
    print(f"  validation: {val} (tidak di-augmentasi)")
    print(f"  test: {test} (tidak di-augmentasi)")


if __name__ == "__main__":
    main()

