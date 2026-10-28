"""Sistem checkpointing dan reproducibility nirava-midi-checkpoint-v1.

Mengikuti docs/TRAINING_CONTRACT.md:
- Format versi: nirava-midi-checkpoint-v1
- Menyimpan: model_state, optimizer_state, epoch, global_step, tokens_seen,
  best_val_nll, patience_counter, RNG seeds, tokenizer_hash, config
- Ekspor inference model: bobot bersih tanpa optimizer untuk integrasi backend
- SHA-256 checksum untuk validasi integritas checkpoint
- Determinisme seed across Python random and PyTorch
"""

import hashlib
import os
from pathlib import Path
import random
from typing import Any, Dict, Optional, Tuple
import torch
import torch.nn as nn

import nirava_midi_lstm as ml
import nirava_midi_tokenizer as tk

CHECKPOINT_FORMAT_VERSION = "nirava-midi-checkpoint-v1"


def set_seed(seed: int = 42):
    """Kunci seluruh seed RNG agar eksperimen dapat direproduksi secara deterministik."""
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    # Flag deterministik PyTorch
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def calculate_file_sha256(filepath: str) -> str:
    """Hitung checksum SHA-256 dari file checkpoint."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def save_checkpoint(
    filepath: str,
    model: nn.Module,
    optimizer: Optional[torch.optim.Optimizer] = None,
    epoch: int = 0,
    global_step: int = 0,
    tokens_seen: int = 0,
    best_val_nll: float = float("inf"),
    patience_counter: int = 0,
    config: Optional[Dict[str, Any]] = None,
    is_inference_only: bool = False,
) -> str:
    """Simpan checkpoint model ke disk.

    Args:
        filepath: path tujuan penyimpanan berkas (.pt)
        model: instance model NiravaLSTMLanguageModel
        optimizer: instance optimizer (opsional jika is_inference_only=True)
        epoch: epoch saat ini
        global_step: total batch update saat ini
        tokens_seen: total token musik yang telah dilihat selama training
        best_val_nll: validation NLL terbaik yang pernah dicapai
        patience_counter: state patience early stopping
        config: dictionary hyperparameter
        is_inference_only: jika True, optimizer_state_dict tidak disimpan

    Returns:
        sha256: checksum SHA-256 dari file yang disimpan
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    if config is None:
        config = {
            "vocab_size": getattr(model, "vocab_size", ml.VOCAB_SIZE),
            "embedding_dim": getattr(model, "embedding_dim", ml.EMBEDDING_DIM),
            "hidden_dim": getattr(model, "hidden_dim", ml.HIDDEN_DIM),
            "num_layers": getattr(model, "num_layers", ml.NUM_LAYERS),
        }

    checkpoint = {
        "format_version": CHECKPOINT_FORMAT_VERSION,
        "model_version": ml.MODEL_VERSION,
        "tokenizer_version": tk.TOKENIZER_VERSION,
        "tokenizer_hash": tk.tokenizer_hash(),
        "config": config,
        "epoch": epoch,
        "global_step": global_step,
        "tokens_seen": tokens_seen,
        "best_val_nll": best_val_nll,
        "patience_counter": patience_counter,
        "model_state_dict": model.state_dict(),
        "rng_state": {
            "torch": torch.get_rng_state(),
            "python": random.getstate(),
        },
    }

    if not is_inference_only and optimizer is not None:
        checkpoint["optimizer_state_dict"] = optimizer.state_dict()

    torch.save(checkpoint, str(path))
    sha256 = calculate_file_sha256(str(path))
    return sha256


def load_checkpoint(
    filepath: str,
    model: Optional[nn.Module] = None,
    optimizer: Optional[torch.optim.Optimizer] = None,
    device: torch.device = torch.device("cpu"),
    restore_rng: bool = True,
) -> Dict[str, Any]:
    """Muat checkpoint dari disk dan verifikasi kompatibilitas format.

    Args:
        filepath: path ke file .pt
        model: model tujuan untuk memuat bobot (opsional)
        optimizer: optimizer tujuan untuk memuat state (opsional)
        device: target torch device
        restore_rng: jika True, pulihkan state RNG

    Returns:
        checkpoint dict berisi seluruh metadata
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Checkpoint tidak ditemukan: {filepath}")

    checkpoint = torch.load(str(path), map_location=device, weights_only=False)

    # Validasi integritas kontrak format
    fmt = checkpoint.get("format_version")
    if fmt != CHECKPOINT_FORMAT_VERSION:
        raise ValueError(
            f"Versi format checkpoint tidak kompatibel: '{fmt}', diharapkan '{CHECKPOINT_FORMAT_VERSION}'"
        )

    tok_hash = checkpoint.get("tokenizer_hash")
    expected_hash = tk.tokenizer_hash()
    if tok_hash != expected_hash:
        raise ValueError(
            f"Tokenizer hash mismatch: checkpoint '{tok_hash}' != sistem '{expected_hash}'"
        )

    # Muat bobot model
    if model is not None and "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])

    # Muat state optimizer jika ada dan diminta
    if optimizer is not None and "optimizer_state_dict" in checkpoint:
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

    # Pulihkan state RNG jika diminta
    if restore_rng and "rng_state" in checkpoint:
        rng = checkpoint["rng_state"]
        if "torch" in rng:
            torch.set_rng_state(rng["torch"])
        if "python" in rng:
            random.setstate(rng["python"])

    return checkpoint


def export_inference_model(filepath: str, model: nn.Module, config: Optional[Dict[str, Any]] = None) -> str:
    """Ekspor bobot bersih untuk inferensi/deployment (tanpa optimizer state)."""
    return save_checkpoint(
        filepath=filepath,
        model=model,
        optimizer=None,
        config=config,
        is_inference_only=True,
    )
