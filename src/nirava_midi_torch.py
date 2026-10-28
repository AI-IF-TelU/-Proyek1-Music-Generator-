"""Adaptor torch untuk nirava_midi_data (kontrak nirava-midi-data-v1).

Mengubah batch list Python menjadi tensor:
input_ids/target_ids int64[B,128], loss_mask bool[B,128], lengths int64[B].
Metadata (piece_id dst.) tetap list Python.
"""

import torch

import nirava_midi_data as nd
import nirava_midi_tokenizer as tk

TENSOR_KEYS = {
    "input_ids": torch.int64,
    "target_ids": torch.int64,
    "loss_mask": torch.bool,
    "lengths": torch.int64,
}


def to_tensors(batch):
    """Konversi satu batch hasil nd.collate dan validasi kontrak."""
    out = dict(batch)
    for key, dtype in TENSOR_KEYS.items():
        out[key] = torch.tensor(batch[key], dtype=dtype)
    validate_batch(out)
    return out


def validate_batch(b):
    """A3 wajib menolak batch yang melanggar kontrak; cek di sini juga."""
    x, y, m, n = b["input_ids"], b["target_ids"], b["loss_mask"], b["lengths"]
    if x.shape != y.shape or x.shape != m.shape or x.dim() != 2:
        raise ValueError(f"shape tidak konsisten: {x.shape} {y.shape} {m.shape}")
    if x.shape[1] != nd.WINDOW:
        raise ValueError(f"panjang window {x.shape[1]} != {nd.WINDOW}")
    if n.shape != (x.shape[0],):
        raise ValueError("lengths harus [B]")
    if int(x.min()) < 0 or int(x.max()) >= tk.VOCAB_SIZE \
            or int(y.min()) < 0 or int(y.max()) >= tk.VOCAB_SIZE:
        raise ValueError("token di luar 0..132")
    if int(n.min()) < 1 or int(n.max()) > nd.WINDOW:
        raise ValueError("lengths di luar 1..128")
    if not torch.equal(m.sum(dim=1), n):
        raise ValueError("loss_mask tidak cocok dengan lengths")
    if bool((y[~m] != tk.PAD).any()) or bool((x[~m] != tk.PAD).any()):
        raise ValueError("posisi non-valid harus PAD")
    if bool((y[m] == tk.PAD).any()):
        raise ValueError("target valid tidak boleh PAD")


class TorchMidiLoader:
    """Iterator batch tensor di atas MidiWindowDataset."""

    def __init__(self, tokens_jsonl, split, batch_size, shuffle=False,
                 seed=0, drop_last=False):
        self.dataset = nd.MidiWindowDataset(tokens_jsonl, split)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.seed = seed
        self.drop_last = drop_last
        self.epoch = 0

    def __len__(self):
        n = len(self.dataset)
        return n // self.batch_size if self.drop_last \
            else -(-n // self.batch_size)

    def __iter__(self):
        # seed berbeda tiap epoch agar urutan train berubah tapi reproducible
        seed = self.seed + self.epoch
        self.epoch += 1
        for batch in self.dataset.batches(
                self.batch_size, self.shuffle, seed, self.drop_last):
            yield to_tensors(batch)

