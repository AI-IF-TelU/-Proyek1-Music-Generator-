"""Unit tests untuk modul generation dan export MIDI nirava_midi_generate.py."""

import os
import shutil
import sys
import tempfile
import unittest
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import nirava_midi_generate as gen
import nirava_midi_lstm as ml
import nirava_midi_tokenizer as tk


class GenerationTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.model = ml.create_model()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_grammar_mask(self):
        logits = torch.zeros(ml.VOCAB_SIZE)

        # Tanpa nada aktif: PAD, BOS, HOLD harus -inf
        masked1 = gen.apply_grammar_mask(logits, note_is_active=False)
        self.assertEqual(masked1[tk.PAD].item(), -float("inf"))
        self.assertEqual(masked1[tk.BOS].item(), -float("inf"))
        self.assertEqual(masked1[tk.HOLD].item(), -float("inf"))
        self.assertEqual(masked1[tk.REST].item(), 0.0)
        self.assertEqual(masked1[tk.note_token(60)].item(), 0.0)

        # Dengan nada aktif: HOLD diperbolehkan
        masked2 = gen.apply_grammar_mask(logits, note_is_active=True)
        self.assertEqual(masked2[tk.HOLD].item(), 0.0)
        self.assertEqual(masked2[tk.PAD].item(), -float("inf"))
        self.assertEqual(masked2[tk.BOS].item(), -float("inf"))

    def test_top_k_filtering(self):
        logits = torch.arange(10, dtype=torch.float32)
        filtered = gen.apply_top_k(logits, k=3)
        # 3 nilai teratas adalah 7, 8, 9
        self.assertEqual(filtered[9].item(), 9.0)
        self.assertEqual(filtered[8].item(), 8.0)
        self.assertEqual(filtered[7].item(), 7.0)
        self.assertEqual(filtered[6].item(), -float("inf"))
        self.assertEqual(filtered[0].item(), -float("inf"))

    def test_generate_melody_valid_tokens_and_midi(self):
        res = gen.generate_melody(
            model=self.model,
            max_bars=2,
            temperature=0.8,
            top_k=10,
            seed=123,
        )

        tokens = res["tokens"]
        self.assertEqual(tokens[0], tk.BOS)
        self.assertEqual(tokens[-1], tk.EOS)
        self.assertEqual(res["bars"], 2)
        self.assertEqual(res["steps"], 32)
        self.assertIn(res["termination_reason"], ["eos", "length_cap"])

        # Decode tokens harus berhasil tanpa exception
        notes = tk.decode_tokens(tokens)
        self.assertEqual(len(notes), res["note_count"])

        # Validasi berkas MIDI
        midi_bytes = res["midi_bytes"]
        self.assertTrue(midi_bytes.startswith(b"MThd"))
        info = tk.parse_smf(midi_bytes)
        self.assertEqual(info["ppq"], tk.EXPORT_PPQ)

        # Round-trip check: parse dan encode ulang
        encoded_tokens, meta = tk.encode_smf_bytes(midi_bytes)
        self.assertEqual(encoded_tokens[0], tk.BOS)
        self.assertEqual(encoded_tokens[-1], tk.EOS)

    def test_generation_determinism_with_seed(self):
        res1 = gen.generate_melody(self.model, max_bars=4, temperature=1.0, seed=999)
        res2 = gen.generate_melody(self.model, max_bars=4, temperature=1.0, seed=999)

        self.assertEqual(res1["tokens"], res2["tokens"])
        self.assertEqual(res1["midi_bytes"], res2["midi_bytes"])

    def test_save_midi_file(self):
        res = gen.generate_melody(self.model, max_bars=2, seed=42)
        out_path = os.path.join(self.temp_dir, "output.mid")
        saved_file = gen.save_midi(res["midi_bytes"], out_path)

        self.assertTrue(os.path.exists(saved_file))
        self.assertGreater(os.path.getsize(saved_file), 50)


if __name__ == "__main__":
    unittest.main()
