"""Windowing dan batching nirava-midi-data-v1 (stdlib, tanpa torch).

Kontrak (docs/DATA_CONTRACT.md): x=s[start:start+128], y=s[start+1:start+129],
stride 128, window tidak melintasi piece, right-PAD ke 128. Output berupa list
Python int; Member 3 membungkusnya dengan torch.tensor(dtype=int64/bool).
"""

import json
import random

import nirava_midi_tokenizer as tk

WINDOW = 128
STRIDE = 128


def make_windows(tokens, piece_id, work_group_id, split, parent_hash="",
                 window=WINDOW, stride=STRIDE):
    """Satu piece kanonik [BOS,...,EOS] -> daftar window dict."""
    if len(tokens) < 3 or tokens[0] != tk.BOS or tokens[-1] != tk.EOS:
        raise ValueError(f"{piece_id}: sequence bukan [BOS..EOS]")
    if tokens.count(tk.EOS) != 1 or tokens.count(tk.BOS) != 1:
        raise ValueError(f"{piece_id}: BOS/EOS harus tepat sekali")
    if any(not 0 <= t < tk.VOCAB_SIZE for t in tokens):
        raise ValueError(f"{piece_id}: token di luar vocabulary")
    n_targets = len(tokens) - 1  # posisi target 1..len-1
    out = []
    for start in range(0, n_targets, stride):
        x = tokens[start:start + window]
        y = tokens[start + 1:start + window + 1]
        length = min(len(y), window)
        x = x[:length]
        y = y[:length]
        pad = window - length
        out.append({
            "input_ids": x + [tk.PAD] * pad,
            "target_ids": y + [tk.PAD] * pad,
            "loss_mask": [True] * length + [False] * pad,
            "length": length,
            "piece_id": piece_id,
            "work_group_id": work_group_id,
            "split": split,
            "window_start": start,
            "parent_hash": parent_hash,
        })
    return out


def collate(windows):
    """Gabung window menjadi batch kolom [B,128]."""
    if not windows:
        raise ValueError("batch kosong")
    return {
        "input_ids": [w["input_ids"] for w in windows],
        "target_ids": [w["target_ids"] for w in windows],
        "loss_mask": [w["loss_mask"] for w in windows],
        "lengths": [w["length"] for w in windows],
        "piece_id": [w["piece_id"] for w in windows],
        "work_group_id": [w["work_group_id"] for w in windows],
        "split": [w["split"] for w in windows],
        "window_start": [w["window_start"] for w in windows],
        "parent_hash": [w["parent_hash"] for w in windows],
    }


class MidiWindowDataset:
    """Dataset window dari processed/tokens JSONL untuk satu split."""

    def __init__(self, tokens_jsonl, split):
        self.split = split
        self.windows = []
        with open(tokens_jsonl, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                if rec["split"] != split:
                    continue
                self.windows += make_windows(
                    rec["tokens"], rec["piece_id"], rec["work_group_id"],
                    rec["split"], rec.get("tokens_sha256", ""))

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, i):
        return self.windows[i]

    def batches(self, batch_size, shuffle=False, seed=0, drop_last=False):
        """Shuffle hanya bila diminta (train); val/test urutan tetap."""
        order = list(range(len(self.windows)))
        if shuffle:
            random.Random(seed).shuffle(order)
        for i in range(0, len(order), batch_size):
            chunk = order[i:i + batch_size]
            if drop_last and len(chunk) < batch_size:
                break
            yield collate([self.windows[j] for j in chunk])

