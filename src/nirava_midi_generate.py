"""Modul autoregressive sampling dan ekspor MIDI untuk nirava-midi-lstm-v1.

Mengikuti docs/ML_ARCHITECTURE.md dan docs/MIDI_TOKENIZATION.md:
- Autoregressive step-by-step inference dimulai dari BOS
- Grammar constraints:
  - PAD (0) dan BOS (1) tidak pernah di-sample saat generasi
  - HOLD (4) hanya diizinkan jika sedang ada nada aktif
- Kontrol sampling: temperature scaling (tau) dan top-k filtering
- Terminasi: token EOS (2) atau batas panjang bar (length_cap)
- Alignment ke batas birama (kelipatan 16 langkah) sebelum EOS
- Ekspor SMF Type 0 (120 BPM, PPQ 480, velocity 80) via export_smf
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import torch
import torch.nn.functional as F

import nirava_midi_lstm as ml
import nirava_midi_tokenizer as tk


def apply_grammar_mask(logits: torch.Tensor, note_is_active: bool) -> torch.Tensor:
    """Masking logit token yang melanggar aturan grammar musik monofonik.

    Aturan:
    1. PAD (0) dan BOS (1) tidak boleh di-generate.
    2. HOLD (4) hanya valid jika ada nada aktif sebelumnya.
    """
    masked = logits.clone()
    masked[tk.PAD] = -float("inf")
    masked[tk.BOS] = -float("inf")

    if not note_is_active:
        masked[tk.HOLD] = -float("inf")

    return masked


def apply_top_k(logits: torch.Tensor, k: Optional[int] = None) -> torch.Tensor:
    """Filter logits untuk mempertahankan hanya k nilai teratas."""
    if k is None or k <= 0 or k >= logits.size(-1):
        return logits
    val, _ = torch.topk(logits, k)
    min_val = val[-1]
    return torch.where(logits < min_val, torch.tensor(-float("inf"), device=logits.device), logits)


def generate_melody(
    model: ml.NiravaLSTMLanguageModel,
    max_bars: int = 8,
    temperature: float = 1.0,
    top_k: Optional[int] = 20,
    seed: Optional[int] = None,
    prompt_tokens: Optional[List[int]] = None,
    device: Optional[torch.device] = None,
) -> Dict[str, Any]:
    """Lakukan autoregressive generation untuk menghasilkan melodi musik monofonik.

    Args:
        model: model NiravaLSTMLanguageModel terlatih
        max_bars: panjang maksimum dalam birama (misal 4, 8, atau 16 bar)
        temperature: parameter temperatur sampling (default 1.0, >0)
        top_k: batasi ke k kandidat token teratas (opsional)
        seed: random seed opsional untuk determinisme
        prompt_tokens: token prefix (default [BOS])
        device: torch device

    Returns:
        dict berisi: tokens, bars, steps, note_count, termination_reason, midi_bytes
    """
    if seed is not None:
        torch.manual_seed(seed)

    if device is None:
        device = next(model.parameters()).device

    model.eval()
    temperature = max(1e-4, float(temperature))
    max_steps = max_bars * tk.STEPS_PER_BAR

    # Inisialisasi prompt
    if prompt_tokens is None or len(prompt_tokens) == 0:
        prompt_tokens = [tk.BOS]

    tokens = list(prompt_tokens)
    note_is_active = False

    # Warm-up hidden state dengan prompt tokens
    h, c = model.init_hidden(batch_size=1, device=device)
    last_logits = None

    with torch.no_grad():
        for tok in tokens:
            tok_tensor = torch.tensor([tok], dtype=torch.int64, device=device)
            last_logits, (h, c) = model.step(tok_tensor, (h, c))
            if tk.is_note(tok):
                note_is_active = True
            elif tok == tk.REST:
                note_is_active = False

        termination_reason = "length_cap"

        # Autoregressive sampling loop
        while len(tokens) - 1 < max_steps:
            logits_step = last_logits[0]  # [vocab_size]

            # 1. Grammar mask
            logits_step = apply_grammar_mask(logits_step, note_is_active)

            # 2. Temperature scaling
            scaled_logits = logits_step / temperature

            # 3. Top-k filtering
            filtered_logits = apply_top_k(scaled_logits, top_k)

            # 4. Softmax probability
            probs = F.softmax(filtered_logits, dim=-1)

            # 5. Multinomial sampling
            sampled_token = int(torch.multinomial(probs, num_samples=1).item())

            # Cek penghentian alami (EOS)
            if sampled_token == tk.EOS:
                # Pastikan panjang langkah sebelum EOS merupakan kelipatan 16
                steps_so_far = len(tokens) - 1
                rem = steps_so_far % tk.STEPS_PER_BAR
                if rem > 0:
                    pad_len = tk.STEPS_PER_BAR - rem
                    tokens.extend([tk.REST] * pad_len)
                tokens.append(tk.EOS)
                termination_reason = "eos"
                break

            tokens.append(sampled_token)

            # Update status nada aktif
            if tk.is_note(sampled_token):
                note_is_active = True
            elif sampled_token == tk.REST:
                note_is_active = False

            # Forward step berikutnya
            tok_tensor = torch.tensor([sampled_token], dtype=torch.int64, device=device)
            last_logits, (h, c) = model.step(tok_tensor, (h, c))

        # Jika mencapai max_steps tanpa EOS alami
        if tokens[-1] != tk.EOS:
            steps_so_far = len(tokens) - 1
            rem = steps_so_far % tk.STEPS_PER_BAR
            if rem > 0:
                pad_len = tk.STEPS_PER_BAR - rem
                tokens.extend([tk.REST] * pad_len)
            tokens.append(tk.EOS)
            termination_reason = "length_cap"

    # Decode ke berkas MIDI standar
    midi_bytes = tk.export_smf(tokens)
    notes = tk.decode_tokens(tokens)
    total_steps = len(tokens) - 2

    return {
        "tokens": tokens,
        "bars": total_steps // tk.STEPS_PER_BAR,
        "steps": total_steps,
        "note_count": len(notes),
        "termination_reason": termination_reason,
        "midi_bytes": midi_bytes,
    }


def save_midi(midi_bytes: bytes, filepath: str) -> str:
    """Simpan berkas MIDI ke disk."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(midi_bytes)
    return str(path)
