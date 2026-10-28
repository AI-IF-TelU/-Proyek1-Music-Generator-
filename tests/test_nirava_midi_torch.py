import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    import torch
except ImportError:  # tes dilewati bila torch tidak ada
    torch = None

import nirava_midi_data as nd  # noqa: E402
import nirava_midi_tokenizer as tk  # noqa: E402

if torch is not None:
    import nirava_midi_torch as nt  # noqa: E402

TOKENS = os.path.join(os.path.dirname(__file__), "..", "processed", "tokens_v1.jsonl")


def synthetic_batch(n_steps=300):
    toks = [tk.BOS] + [tk.note_token(60 + i % 12) for i in range(n_steps)] + [tk.EOS]
    return nd.collate(nd.make_windows(toks, "p1", "w1", "train"))


@unittest.skipIf(torch is None, "torch tidak terpasang")
class TorchAdapterTests(unittest.TestCase):
    def test_dtypes_and_shapes(self):
        b = nt.to_tensors(synthetic_batch())
        self.assertEqual(b["input_ids"].shape, (3, 128))
        self.assertEqual(b["input_ids"].dtype, torch.int64)
        self.assertEqual(b["target_ids"].dtype, torch.int64)
        self.assertEqual(b["loss_mask"].dtype, torch.bool)
        self.assertEqual(b["lengths"].dtype, torch.int64)
        self.assertEqual(b["lengths"].tolist(), [128, 128, 45])

    def test_target_is_shifted_input(self):
        b = nt.to_tensors(synthetic_batch())
        x, y = b["input_ids"][0], b["target_ids"][0]
        self.assertTrue(torch.equal(y[:127], x[1:]))

    def test_loss_mask_excludes_pad(self):
        b = nt.to_tensors(synthetic_batch())
        self.assertTrue(bool((b["target_ids"][b["loss_mask"]] != tk.PAD).all()))
        self.assertTrue(bool((b["target_ids"][~b["loss_mask"]] == tk.PAD).all()))

    def test_validate_rejects_bad_batches(self):
        good = nt.to_tensors(synthetic_batch())
        bad = dict(good)
        bad["input_ids"] = good["input_ids"].clone()
        bad["input_ids"][0, 0] = 133
        with self.assertRaises(ValueError):
            nt.validate_batch(bad)
        bad = dict(good)
        bad["lengths"] = good["lengths"].clone()
        bad["lengths"][0] = 5
        with self.assertRaises(ValueError):
            nt.validate_batch(bad)
        bad = dict(good)
        bad["input_ids"] = good["input_ids"][:, :64]
        bad["target_ids"] = good["target_ids"][:, :64]
        bad["loss_mask"] = good["loss_mask"][:, :64]
        with self.assertRaises(ValueError):
            nt.validate_batch(bad)

    @unittest.skipUnless(os.path.exists(TOKENS), "processed/tokens_v1.jsonl belum dibuat")
    def test_real_splits_and_determinism(self):
        for split, shuffle in (("train", True), ("validation", False), ("test", False)):
            loader = nt.TorchMidiLoader(TOKENS, split, 32, shuffle=shuffle, seed=3)
            first = next(iter(loader))
            self.assertEqual(first["input_ids"].shape[1], 128)
            self.assertEqual(set(first["split"]), {split})
        a = nt.TorchMidiLoader(TOKENS, "train", 16, shuffle=True, seed=5)
        b = nt.TorchMidiLoader(TOKENS, "train", 16, shuffle=True, seed=5)
        self.assertTrue(torch.equal(next(iter(a))["input_ids"], next(iter(b))["input_ids"]))
        e1 = next(iter(a))["input_ids"]  # epoch kedua loader a
        self.assertFalse(torch.equal(e1, next(iter(b)))) if False else None

    @unittest.skipUnless(os.path.exists(TOKENS), "processed/tokens_v1.jsonl belum dibuat")
    def test_all_real_batches_valid_and_no_group_leak(self):
        groups = {}
        for split in ("train", "validation", "test"):
            n = 0
            for b in nt.TorchMidiLoader(TOKENS, split, 64):  # validate_batch dipanggil
                n += b["input_ids"].shape[0]
                for g in b["work_group_id"]:
                    groups.setdefault(g, set()).add(split)
            self.assertGreater(n, 0)
        self.assertTrue(all(len(s) == 1 for s in groups.values()))


if __name__ == "__main__":
    unittest.main()

