"""Unit tests untuk engine training nirava_midi_train.py."""

import math
import os
import sys
import unittest
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import nirava_midi_lstm as ml
import nirava_midi_tokenizer as tk
import nirava_midi_torch as nt
import nirava_midi_train as tr

TOKENS_PATH = os.path.join(os.path.dirname(__file__), "..", "processed", "tokens_v1.jsonl")


class TrainingEngineTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)

    def test_perplexity_calculation(self):
        self.assertAlmostEqual(tr.calculate_perplexity(0.0), 1.0)
        # Uniform distribution over 133 tokens gives NLL = ln(133) ≈ 4.8903 -> PPL = 133
        self.assertAlmostEqual(tr.calculate_perplexity(math.log(133)), 133.0, places=4)
        # Proteksi overflow
        self.assertEqual(tr.calculate_perplexity(100.0), float("inf"))

    def test_loss_mask_strictly_ignores_pad(self):
        B, T, V = 2, 8, ml.VOCAB_SIZE
        logits = torch.randn(B, T, V, requires_grad=True)
        targets = torch.randint(1, V, (B, T), dtype=torch.int64)

        # Buat setengah sequence di-pad
        loss_mask = torch.ones(B, T, dtype=torch.bool)
        loss_mask[:, 4:] = False
        targets[:, 4:] = tk.PAD

        loss1, n1 = tr.compute_masked_loss(logits, targets, loss_mask)
        loss1.backward()
        grad1 = logits.grad.clone()

        # Ubah nilai token pada posisi PAD (tetapi mask tetap False)
        logits.grad.zero_()
        targets_tampered = targets.clone()
        targets_tampered[:, 4:] = 99  # ubah token non-valid

        loss2, n2 = tr.compute_masked_loss(logits, targets_tampered, loss_mask)
        loss2.backward()
        grad2 = logits.grad.clone()

        # Nilai loss dan gradien harus 100% identik
        self.assertEqual(n1, 8)
        self.assertEqual(n2, 8)
        self.assertAlmostEqual(loss1.item(), loss2.item(), places=5)
        self.assertTrue(torch.allclose(grad1, grad2))
        # Gradien pada posisi PAD harus tepat nol
        self.assertTrue(torch.all(grad1[:, 4:, :] == 0.0))

    def test_early_stopping_logic(self):
        es = tr.EarlyStopping(patience=3, min_delta=0.01)

        # Epoch 1: Loss 4.0 -> best
        self.assertFalse(es(4.0))
        self.assertTrue(es.is_best)
        self.assertEqual(es.counter, 0)

        # Epoch 2: Loss 3.5 -> improvement -> best
        self.assertFalse(es(3.5))
        self.assertTrue(es.is_best)
        self.assertEqual(es.counter, 0)

        # Epoch 3: Loss 3.55 -> no improvement (patience counter = 1)
        self.assertFalse(es(3.55))
        self.assertFalse(es.is_best)
        self.assertEqual(es.counter, 1)

        # Epoch 4: Loss 3.52 -> no improvement (patience counter = 2)
        self.assertFalse(es(3.52))
        self.assertEqual(es.counter, 2)

        # Epoch 5: Loss 3.58 -> no improvement (patience counter = 3 -> STOP)
        triggered = es(3.58)
        self.assertTrue(triggered)
        self.assertEqual(es.counter, 3)

    def test_train_and_eval_single_epoch(self):
        model = ml.create_model()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
        device = torch.device("cpu")

        train_loader = nt.TorchMidiLoader(TOKENS_PATH, "train", batch_size=4, shuffle=True, seed=42)
        val_loader = nt.TorchMidiLoader(TOKENS_PATH, "validation", batch_size=4, shuffle=False)

        train_metrics = tr.train_one_epoch(model, train_loader, optimizer, device, clip_norm=1.0)
        self.assertIn("loss", train_metrics)
        self.assertIn("nll", train_metrics)
        self.assertIn("perplexity", train_metrics)
        self.assertGreater(train_metrics["tokens"], 0)
        self.assertGreater(train_metrics["batches"], 0)
        self.assertFalse(math.isnan(train_metrics["loss"]))

        val_metrics = tr.evaluate(model, val_loader, device)
        self.assertIn("nll", val_metrics)
        self.assertIn("perplexity", val_metrics)
        self.assertGreater(val_metrics["tokens"], 0)
        self.assertFalse(math.isnan(val_metrics["nll"]))

    def test_overfit_mini_corpus_sanity_check(self):
        """Sanity check: buktikan model mampu meng-overfit sequence kecil sampai loss turun tajam."""
        torch.manual_seed(123)
        # Model kecil untuk overfit test cepat
        model = ml.NiravaLSTMLanguageModel(embedding_dim=32, hidden_dim=64)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.015)

        # 1 piece sintetis 16 langkah
        inputs = torch.tensor([[tk.BOS, tk.note_token(60), tk.HOLD, tk.note_token(64),
                                tk.HOLD, tk.note_token(67), tk.REST, tk.EOS]], dtype=torch.int64)
        targets = torch.tensor([[tk.note_token(60), tk.HOLD, tk.note_token(64), tk.HOLD,
                                 tk.note_token(67), tk.REST, tk.EOS, tk.PAD]], dtype=torch.int64)
        mask = torch.tensor([[True, True, True, True, True, True, True, False]], dtype=torch.bool)

        initial_loss = None
        for step in range(100):
            optimizer.zero_grad()
            logits, _ = model(inputs)
            loss, n_valid = tr.compute_masked_loss(logits, targets, mask)
            loss_norm = loss / n_valid
            if step == 0:
                initial_loss = loss_norm.item()
            loss_norm.backward()
            optimizer.step()

        final_loss = loss_norm.item()
        # Loss awal di sekitar ln(133) ≈ 4.8, harus turun di bawah 0.3
        self.assertGreater(initial_loss, 3.5)
        self.assertLess(final_loss, 0.3, f"Model gagal overfit: final_loss={final_loss}")


if __name__ == "__main__":
    unittest.main()
