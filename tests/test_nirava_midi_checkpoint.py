"""Unit tests untuk sistem checkpointing nirava_midi_checkpoint.py."""

import os
import shutil
import sys
import tempfile
import unittest
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import nirava_midi_checkpoint as ck
import nirava_midi_lstm as ml
import nirava_midi_tokenizer as tk


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        ck.set_seed(42)
        self.temp_dir = tempfile.mkdtemp()
        self.ckpt_path = os.path.join(self.temp_dir, "test_checkpoint.pt")
        self.export_path = os.path.join(self.temp_dir, "test_export.pt")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_load_resume(self):
        model1 = ml.create_model()
        opt1 = torch.optim.Adam(model1.parameters(), lr=1e-3)

        # Lakukan satu step buatan agar optimizer state terisi
        dummy_in = torch.randint(0, ml.VOCAB_SIZE, (2, 8))
        logits, _ = model1(dummy_in)
        loss = logits.sum()
        loss.backward()
        opt1.step()

        sha256 = ck.save_checkpoint(
            filepath=self.ckpt_path,
            model=model1,
            optimizer=opt1,
            epoch=5,
            global_step=120,
            tokens_seen=15360,
            best_val_nll=2.45,
            patience_counter=2,
            config={"lr": 1e-3, "hidden_dim": 128},
        )
        self.assertEqual(len(sha256), 64)

        # Muat ke model & optimizer baru
        model2 = ml.create_model()
        opt2 = torch.optim.Adam(model2.parameters(), lr=1e-3)

        meta = ck.load_checkpoint(self.ckpt_path, model=model2, optimizer=opt2)

        self.assertEqual(meta["epoch"], 5)
        self.assertEqual(meta["global_step"], 120)
        self.assertEqual(meta["tokens_seen"], 15360)
        self.assertAlmostEqual(meta["best_val_nll"], 2.45)
        self.assertEqual(meta["patience_counter"], 2)

        # Pastikan seluruh bobot model1 dan model2 identik
        for p1, p2 in zip(model1.parameters(), model2.parameters()):
            self.assertTrue(torch.equal(p1, p2))

        # Pastikan output model1 dan model2 identik
        logits1, _ = model1(dummy_in)
        logits2, _ = model2(dummy_in)
        self.assertTrue(torch.allclose(logits1, logits2))

    def test_export_inference_model_no_optimizer(self):
        model = ml.create_model()
        ck.export_inference_model(self.export_path, model)

        loaded_dict = torch.load(self.export_path, weights_only=False)
        self.assertNotIn("optimizer_state_dict", loaded_dict)
        self.assertIn("model_state_dict", loaded_dict)
        self.assertEqual(loaded_dict["format_version"], ck.CHECKPOINT_FORMAT_VERSION)

    def test_validation_rejects_corrupted_format(self):
        model = ml.create_model()
        ck.save_checkpoint(self.ckpt_path, model)

        # Rusak metadata format_version
        data = torch.load(self.ckpt_path, weights_only=False)
        data["format_version"] = "invalid-v999"
        torch.save(data, self.ckpt_path)

        with self.assertRaises(ValueError) as ctx:
            ck.load_checkpoint(self.ckpt_path)
        self.assertIn("tidak kompatibel", str(ctx.exception))

    def test_validation_rejects_tokenizer_hash_mismatch(self):
        model = ml.create_model()
        ck.save_checkpoint(self.ckpt_path, model)

        # Rusak tokenizer_hash
        data = torch.load(self.ckpt_path, weights_only=False)
        data["tokenizer_hash"] = "fake_hash_12345"
        torch.save(data, self.ckpt_path)

        with self.assertRaises(ValueError) as ctx:
            ck.load_checkpoint(self.ckpt_path)
        self.assertIn("Tokenizer hash mismatch", str(ctx.exception))

    def test_seed_determinism(self):
        ck.set_seed(12345)
        t1 = torch.randn(10)
        ck.set_seed(12345)
        t2 = torch.randn(10)
        self.assertTrue(torch.equal(t1, t2))


if __name__ == "__main__":
    unittest.main()
