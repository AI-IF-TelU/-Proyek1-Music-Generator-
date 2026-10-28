import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import nirava_midi_data as nd  # noqa: E402
import nirava_midi_grouping as gp  # noqa: E402
import nirava_midi_tokenizer as tk  # noqa: E402
import build_splits as bs  # noqa: E402


def piece(n_steps):
    steps = [tk.note_token(60 + i % 12) for i in range(n_steps)]
    return [tk.BOS] + steps + [tk.EOS]


class WindowTests(unittest.TestCase):
    def test_shift_and_shapes(self):
        toks = piece(300)  # 302 token -> 301 target
        wins = nd.make_windows(toks, "p1", "w1", "train")
        self.assertEqual(len(wins), 3)  # ceil(301/128)
        for w in wins:
            self.assertEqual(len(w["input_ids"]), 128)
            self.assertEqual(len(w["target_ids"]), 128)
            self.assertEqual(len(w["loss_mask"]), 128)
        w0 = wins[0]
        self.assertEqual(w0["input_ids"][0], tk.BOS)
        self.assertEqual(w0["target_ids"][:127], w0["input_ids"][1:128])
        self.assertEqual(w0["target_ids"][127], toks[128])

    def test_each_target_covered_once(self):
        toks = piece(300)
        wins = nd.make_windows(toks, "p1", "w1", "train")
        covered = []
        for w in wins:
            covered += w["target_ids"][:w["length"]]
        self.assertEqual(covered, toks[1:])

    def test_last_window_pad_and_mask(self):
        toks = piece(300)
        last = nd.make_windows(toks, "p1", "w1", "train")[-1]
        n = last["length"]
        self.assertEqual(n, 301 - 256)
        self.assertEqual(last["target_ids"][n - 1], tk.EOS)
        self.assertTrue(all(t == tk.PAD for t in last["target_ids"][n:]))
        self.assertTrue(all(t == tk.PAD for t in last["input_ids"][n:]))
        self.assertEqual(last["loss_mask"], [True] * n + [False] * (128 - n))

    def test_bos_only_in_first_window(self):
        wins = nd.make_windows(piece(300), "p1", "w1", "train")
        self.assertIn(tk.BOS, wins[0]["input_ids"])
        for w in wins[1:]:
            self.assertNotIn(tk.BOS, w["input_ids"])

    def test_eos_once_and_no_target_after(self):
        wins = nd.make_windows(piece(300), "p1", "w1", "train")
        eos_count = sum(w["target_ids"].count(tk.EOS) for w in wins)
        self.assertEqual(eos_count, 1)

    def test_exact_multiple_boundary(self):
        toks = piece(127)  # 129 token -> 128 target, tepat satu window
        wins = nd.make_windows(toks, "p", "w", "train")
        self.assertEqual(len(wins), 1)
        self.assertEqual(wins[0]["length"], 128)
        self.assertTrue(all(wins[0]["loss_mask"]))

    def test_invalid_sequences_rejected(self):
        with self.assertRaises(ValueError):
            nd.make_windows([tk.REST] * 20, "p", "w", "train")
        with self.assertRaises(ValueError):
            nd.make_windows([tk.BOS, tk.REST, 999, tk.EOS], "p", "w", "train")

    def test_collate_shapes(self):
        wins = nd.make_windows(piece(300), "p1", "w1", "train")
        b = nd.collate(wins)
        self.assertEqual(len(b["input_ids"]), 3)
        self.assertEqual(b["lengths"], [128, 128, 45])
        with self.assertRaises(ValueError):
            nd.collate([])


class GroupingSplitTests(unittest.TestCase):
    def test_fingerprint_transposition_invariant(self):
        a = [tk.BOS] + [tk.note_token(p) for p in (60, 62, 64, 65, 67, 69, 71, 72) * 2] + [tk.EOS]
        b = [tk.BOS] + [tk.note_token(p + 5) for p in (60, 62, 64, 65, 67, 69, 71, 72) * 2] + [tk.EOS]
        self.assertEqual(gp.fingerprint(a), gp.fingerprint(b))

    def test_union_find_groups(self):
        names = ["a", "b", "c", "d"]
        groups = gp.group_by_threshold(names, [("a", "b", 0.9), ("b", "c", 0.5)], 0.4)
        sizes = sorted(len(v) for v in groups.values())
        self.assertEqual(sizes, [1, 3])

    def test_split_never_breaks_group_and_is_deterministic(self):
        groups = {f"w{i}": [f"f{i}_{j}" for j in range(1 + i % 3)] for i in range(100)}
        sizes = {g: len(v) for g, v in groups.items()}
        s1 = bs.assign_splits(groups, sizes, seed=7)
        s2 = bs.assign_splits(groups, sizes, seed=7)
        self.assertEqual(s1, s2)
        counts = {"train": 0, "validation": 0, "test": 0}
        for g, sp in s1.items():
            counts[sp] += sizes[g]
        total = sum(counts.values())
        self.assertAlmostEqual(counts["train"] / total, 0.8, delta=0.05)
        self.assertGreater(counts["validation"], 0)
        self.assertGreater(counts["test"], 0)


if __name__ == "__main__":
    unittest.main()

