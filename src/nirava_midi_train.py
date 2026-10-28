"""Engine pelatihan dan custom loss untuk nirava-midi-training-v1.

Mengikuti docs/TRAINING_CONTRACT.md:
- Teacher-forced cross-entropy next-token prediction pada logits [B, T, 133] dan target [B, T]
- Mengabaikan token PAD (token 0) via loss_mask
- Agregasi token-weighted NLL = sum(CE valid) / total(token valid)
- Perplexity = exp(mean NLL) dengan proteksi overflow
- Optimizer: Adam (lr 1e-3, betas (0.9, 0.999))
- Gradient norm clipping: max_norm = 1.0
- Evaluasi deterministik no_grad
- Early stopping berbasis validation NLL (default patience = 8)
"""

import math
from typing import Dict, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F

import nirava_midi_tokenizer as tk


def compute_masked_loss(
    logits: torch.Tensor,
    targets: torch.Tensor,
    loss_mask: torch.Tensor,
) -> Tuple[torch.Tensor, int]:
    """Hitung total cross entropy loss hanya pada token valid (non-PAD).

    Args:
        logits: float32 tensor [B, T, V]
        targets: int64 tensor [B, T]
        loss_mask: bool tensor [B, T]

    Returns:
        total_loss: scalar sum cross-entropy loss untuk seluruh token valid
        n_valid: jumlah token target valid (int)
    """
    n_valid = int(loss_mask.sum().item())
    if n_valid == 0:
        return torch.tensor(0.0, device=logits.device, requires_grad=True), 0

    valid_logits = logits[loss_mask]    # [n_valid, V]
    valid_targets = targets[loss_mask]  # [n_valid]

    # reduction='sum' agar kita bisa mengakumulasi total NLL berbobot jumlah token
    total_loss = F.cross_entropy(valid_logits, valid_targets, reduction="sum")
    return total_loss, n_valid


def calculate_perplexity(mean_nll: float) -> float:
    """Hitung perplexity = exp(mean_nll) dengan proteksi overflow."""
    if mean_nll > 85.0:  # batas aman eksponensial float64
        return float("inf")
    return math.exp(mean_nll)


def train_one_epoch(
    model: nn.Module,
    data_loader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    clip_norm: float = 1.0,
) -> Dict[str, float]:
    """Latih model untuk satu epoch penuh.

    Setiap window training me-reset recurrent state (h, c) sesuai kontrak.
    """
    model.train()
    total_loss = 0.0
    total_tokens = 0
    total_grad_norm = 0.0
    num_batches = 0

    for batch in data_loader:
        input_ids = batch["input_ids"].to(device)
        target_ids = batch["target_ids"].to(device)
        loss_mask = batch["loss_mask"].to(device)

        optimizer.zero_grad()

        # State di-reset per window (state=None menghasilkan h0=0, c0=0)
        logits, _ = model(input_ids, state=None)

        batch_loss, n_valid = compute_masked_loss(logits, target_ids, loss_mask)
        if n_valid == 0:
            continue

        # Normalisasi loss per batch untuk gradien backward
        loss_for_backward = batch_loss / n_valid
        loss_for_backward.backward()

        # Gradient norm clipping
        grad_norm = nn.utils.clip_grad_norm_(model.parameters(), max_norm=clip_norm)

        optimizer.step()

        total_loss += batch_loss.item()
        total_tokens += n_valid
        total_grad_norm += float(grad_norm.item() if torch.is_tensor(grad_norm) else grad_norm)
        num_batches += 1

    mean_nll = total_loss / max(1, total_tokens)
    ppl = calculate_perplexity(mean_nll)
    avg_grad_norm = total_grad_norm / max(1, num_batches)

    return {
        "loss": mean_nll,
        "nll": mean_nll,
        "perplexity": ppl,
        "tokens": total_tokens,
        "avg_grad_norm": avg_grad_norm,
        "batches": num_batches,
    }


def evaluate(
    model: nn.Module,
    data_loader,
    device: torch.device,
) -> Dict[str, float]:
    """Evaluasi model pada validation/test set secara deterministik."""
    model.eval()
    total_loss = 0.0
    total_tokens = 0
    num_batches = 0

    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch["input_ids"].to(device)
            target_ids = batch["target_ids"].to(device)
            loss_mask = batch["loss_mask"].to(device)

            logits, _ = model(input_ids, state=None)

            batch_loss, n_valid = compute_masked_loss(logits, target_ids, loss_mask)
            total_loss += batch_loss.item()
            total_tokens += n_valid
            num_batches += 1

    mean_nll = total_loss / max(1, total_tokens)
    ppl = calculate_perplexity(mean_nll)

    return {
        "loss": mean_nll,
        "nll": mean_nll,
        "perplexity": ppl,
        "tokens": total_tokens,
        "batches": num_batches,
    }


class EarlyStopping:
    """Early stopping berbasis validation NLL terkecil."""

    def __init__(self, patience: int = 8, min_delta: float = 1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float("inf")
        self.counter = 0
        self.early_stop = False
        self.is_best = False

    def __call__(self, val_loss: float) -> bool:
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            self.is_best = True
        else:
            self.counter += 1
            self.is_best = False
            if self.counter >= self.patience:
                self.early_stop = True
        return self.early_stop
