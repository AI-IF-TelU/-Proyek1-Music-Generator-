"""Unit tests untuk arsitektur nirava_midi_lstm.py (kontrak nirava-midi-lstm-v1)."""

import os
import sys
import unittest
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import nirava_midi_lstm as ml


class NiravaModelTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.model = ml.create_model()

    def test_parameter_count_and_constants(self):
        total_params = self.model.count_parameters()
        # Perhitungan eksak:
        # Embedding: 133 * 64 = 8,512
        # Layer 1: (64*512) + (128*512) + 512 = 98,816
        # Layer 2: (128*512) + (128*512) + 512 = 131,584
        # Head: (128*133) + 133 = 17,157
        # Total = 256,069
        self.assertEqual(total_params, 256069)
        self.assertEqual(self.model.vocab_size, 133)
        self.assertEqual(self.model.embedding_dim, 64)
        self.assertEqual(self.model.hidden_dim, 128)
        self.assertEqual(self.model.num_layers, 2)

    def test_forget_gate_bias_initialization(self):
        # Gerbang f berada pada rentang [128 : 256]
        bias1 = self.model.cell_layer1.w_ih.bias
        bias2 = self.model.cell_layer2.w_ih.bias
        # Pastikan f_gate bias = 1.0
        self.assertTrue(torch.allclose(bias1[128:256], torch.ones(128)))
        self.assertTrue(torch.allclose(bias2[128:256], torch.ones(128)))
        # Pastikan i, g, o bias = 0.0
        self.assertTrue(torch.allclose(bias1[:128], torch.zeros(128)))
        self.assertTrue(torch.allclose(bias1[256:], torch.zeros(256)))

    def test_forward_shapes_and_types(self):
        B, T = 4, 128
        dummy_inputs = torch.randint(0, ml.VOCAB_SIZE, (B, T), dtype=torch.int64)

        logits, (h_last, c_last) = self.model(dummy_inputs)

        self.assertEqual(logits.shape, (B, T, ml.VOCAB_SIZE))
        self.assertEqual(logits.dtype, torch.float32)
        self.assertEqual(h_last.shape, (2, B, 128))
        self.assertEqual(c_last.shape, (2, B, 128))
        self.assertEqual(h_last.dtype, torch.float32)
        self.assertEqual(c_last.dtype, torch.float32)

    def test_step_consistency_with_forward(self):
        """Verifikasi bahwa recurrent state step-by-step identik dengan batch forward."""
        B, T = 2, 8
        dummy_inputs = torch.randint(0, ml.VOCAB_SIZE, (B, T), dtype=torch.int64)

        # 1. Batch forward
        logits_batch, (h_fwd, c_fwd) = self.model(dummy_inputs)

        # 2. Step-by-step
        h, c = self.model.init_hidden(B)
        step_logits_list = []
        for t in range(T):
            token_t = dummy_inputs[:, t]
            step_logits, (h, c) = self.model.step(token_t, (h, c))
            step_logits_list.append(step_logits)

        logits_steps = torch.stack(step_logits_list, dim=1)

        # Harus identik (toleransi numerik float32)
        self.assertTrue(torch.allclose(logits_batch, logits_steps, atol=1e-5))
        self.assertTrue(torch.allclose(h_fwd, h, atol=1e-5))
        self.assertTrue(torch.allclose(c_fwd, c, atol=1e-5))

    def test_gradient_flow_and_no_nan(self):
        B, T = 2, 16
        inputs = torch.randint(0, ml.VOCAB_SIZE, (B, T), dtype=torch.int64)
        targets = torch.randint(0, ml.VOCAB_SIZE, (B, T), dtype=torch.int64)

        logits, _ = self.model(inputs)
        loss = torch.nn.functional.cross_entropy(logits.view(-1, ml.VOCAB_SIZE), targets.view(-1))
        loss.backward()

        for name, param in self.model.named_parameters():
            self.assertIsNotNone(param.grad, f"Gradient tidak mengalir ke {name}")
            self.assertFalse(torch.isnan(param.grad).any(), f"NaN ditemukan di gradient {name}")
            self.assertFalse(torch.isinf(param.grad).any(), f"Inf ditemukan di gradient {name}")


if __name__ == "__main__":
    unittest.main()
