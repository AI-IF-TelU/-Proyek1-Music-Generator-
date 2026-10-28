import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import nirava_midi_tokenizer as tk  # noqa: E402


def make_smf(notes, ppq=480, sig=(4, 4), fmt=0, extra=b""):
    """notes: [(on_tick, off_tick, pitch)] -> SMF mentah untuk tes."""
    events = []
    for on, off, p in notes:
        events.append((on, 1, p))
        events.append((off, 0, p))
    body = bytearray()
    if sig:
        body += b"\x00\xFF\x58\x04" + bytes([sig[0], sig[1].bit_length() - 1, 24, 8])
    body += extra
    last = 0
    for tick, kind, p in sorted(events):
        body += tk._varlen(tick - last)
        last = tick
        body += bytes([0x90 if kind else 0x80, p, 64 if kind else 0])
    body += b"\x00\xFF\x2F\x00"
    import struct
    return (b"MThd" + struct.pack(">IHHH", 6, fmt, 1, ppq)
            + b"MTrk" + struct.pack(">I", len(body)) + bytes(body))


class TokenizerTests(unittest.TestCase):
    def test_vocab_constants(self):
        self.assertEqual(tk.VOCAB_SIZE, 133)
        self.assertEqual(tk.note_token(0), 5)
        self.assertEqual(tk.note_token(127), 132)
        with self.assertRaises(ValueError):
            tk.note_token(128)

    def test_encode_basic(self):
        # satu quarter C4 (60) lalu satu quarter E4 (64) pada PPQ 480
        data = make_smf([(0, 480, 60), (480, 960, 64)])
        tokens, meta = tk.encode_smf_bytes(data)
        steps = [tk.note_token(60), tk.HOLD, tk.HOLD, tk.HOLD,
                 tk.note_token(64), tk.HOLD, tk.HOLD, tk.HOLD]
        steps += [tk.REST] * 8  # pad ke 16
        self.assertEqual(tokens, [tk.BOS] + steps + [tk.EOS])
        self.assertEqual(meta["bars"], 1)
        self.assertEqual(meta["trailing_pad_steps"], 8)

    def test_leading_silence_trimmed(self):
        data = make_smf([(960, 1440, 62)])
        tokens, meta = tk.encode_smf_bytes(data)
        self.assertEqual(meta["leading_offset_steps"], 8)
        self.assertEqual(tokens[1], tk.note_token(62))

    def test_rest_between_notes(self):
        data = make_smf([(0, 120, 60), (480, 600, 60)])
        tokens, _ = tk.encode_smf_bytes(data)
        self.assertEqual(tokens[1:6], [tk.note_token(60), tk.REST, tk.REST,
                                       tk.REST, tk.note_token(60)])

    def test_repeated_pitch_is_rearticulated(self):
        data = make_smf([(0, 120, 60), (120, 240, 60)])
        tokens, _ = tk.encode_smf_bytes(data)
        self.assertEqual(tokens[1:3], [tk.note_token(60)] * 2)

    def test_min_duration_one_step(self):
        data = make_smf([(0, 10, 60), (480, 960, 61)])
        tokens, meta = tk.encode_smf_bytes(data)
        self.assertEqual(meta["min_duration_adjusted"], 1)
        self.assertEqual(tokens[1], tk.note_token(60))
        self.assertEqual(tokens[2], tk.REST)

    def test_reject_non_44(self):
        with self.assertRaises(tk.Reject) as cm:
            tk.encode_smf_bytes(make_smf([(0, 480, 60)], sig=(6, 8)))
        self.assertEqual(cm.exception.reason, "non_4_4_meter")

    def test_reject_missing_meter(self):
        with self.assertRaises(tk.Reject) as cm:
            tk.encode_smf_bytes(make_smf([(0, 480, 60)], sig=None))
        self.assertEqual(cm.exception.reason, "meter_not_explicit")

    def test_reject_overlap(self):
        with self.assertRaises(tk.Reject) as cm:
            tk.encode_smf_bytes(make_smf([(0, 960, 60), (480, 1440, 64)]))
        self.assertEqual(cm.exception.reason, "overlap_after_quantization")

    def test_reject_pedal(self):
        pedal = b"\x00\xB0\x40\x7F"
        with self.assertRaises(tk.Reject) as cm:
            tk.encode_smf_bytes(make_smf([(0, 480, 60)], extra=pedal))
        self.assertEqual(cm.exception.reason, "pedal_or_pitch_bend")

    def test_neutral_pitch_bend_is_accepted(self):
        neutral = b"\x00\xE0\x00\x40"  # 8192, seperti pada file Nottingham
        tokens, _ = tk.encode_smf_bytes(make_smf([(0, 480, 60)], extra=neutral))
        self.assertEqual(tokens[1], tk.note_token(60))

    def test_active_pitch_bend_rejected(self):
        bent = b"\x00\xE0\x00\x50"
        with self.assertRaises(tk.Reject) as cm:
            tk.encode_smf_bytes(make_smf([(0, 480, 60)], extra=bent))
        self.assertEqual(cm.exception.reason, "pedal_or_pitch_bend")

    def test_pedal_off_accepted(self):
        pedal_off = b"\x00\xB0\x40\x00"
        tokens, _ = tk.encode_smf_bytes(make_smf([(0, 480, 60)], extra=pedal_off))
        self.assertEqual(tokens[1], tk.note_token(60))

    def test_bad_header(self):
        with self.assertRaises(tk.SmfError):
            tk.parse_smf(b"not a midi file at all")

    def test_decode_rejects_invalid_grammar(self):
        steps = [tk.HOLD] + [tk.REST] * 15
        with self.assertRaises(ValueError):
            tk.decode_tokens([tk.BOS] + steps + [tk.EOS])
        with self.assertRaises(ValueError):
            tk.decode_tokens([tk.BOS] + [tk.REST] * 15 + [tk.EOS])
        with self.assertRaises(ValueError):
            tk.decode_tokens([tk.REST] * 16)

    def test_round_trip_tokens(self):
        data = make_smf([(0, 480, 60), (480, 600, 67), (960, 1920, 55)])
        tokens, _ = tk.encode_smf_bytes(data)
        exported = tk.export_smf(tokens)
        tokens2, meta2 = tk.encode_smf_bytes(exported)
        self.assertEqual(tokens, tokens2)
        self.assertEqual(meta2["source_ppq"], 480)

    def test_export_has_no_hanging_note(self):
        tokens = [tk.BOS, tk.note_token(60)] + [tk.HOLD] * 15 + [tk.EOS]
        info = tk.parse_smf(tk.export_smf(tokens))
        self.assertEqual(info["unmatched"], 0)
        self.assertEqual(info["format"], 0)
        self.assertEqual(info["ppq"], 480)
        self.assertEqual(info["tracks"][0], [(0, 1920, 60, 0)])


if __name__ == "__main__":
    unittest.main()
