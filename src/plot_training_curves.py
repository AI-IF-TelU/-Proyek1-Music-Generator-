"""Script visualisasi kurva metrik pelatihan dan evaluasi ablation study Nirava MIDI.

Menghasilkan plot kurva Loss/NLL dan Perplexity untuk R1 (Model Usulan),
R2 (LR 3e-4), dan R3 (Hidden 64) lalu menyimpannya ke reports/training_curves.png.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import torch

import nirava_midi_checkpoint as ck
import nirava_midi_lstm as ml
import nirava_midi_torch as nt
import nirava_midi_train as tr

ROOT = Path(__file__).resolve().parent.parent
TOKENS_PATH = ROOT / "processed" / "tokens_v1.jsonl"
REPORT_DIR = ROOT / "reports"
OUTPUT_IMAGE = REPORT_DIR / "training_curves.png"


def run_and_collect_history(lr=1e-3, hidden_dim=128, max_epochs=12, seed=42):
    """Jalankan run training singkat deterministik untuk mengumpulkan metrik per epoch."""
    ck.set_seed(seed)
    device = torch.device("cpu")

    model = ml.NiravaLSTMLanguageModel(
        vocab_size=ml.VOCAB_SIZE,
        embedding_dim=64,
        hidden_dim=hidden_dim,
        num_layers=2,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.999))

    train_loader = nt.TorchMidiLoader(str(TOKENS_PATH), "train", batch_size=16, shuffle=True, seed=seed)
    val_loader = nt.TorchMidiLoader(str(TOKENS_PATH), "validation", batch_size=16, shuffle=False)

    train_nll_list = []
    val_nll_list = []
    val_ppl_list = []

    for epoch in range(1, max_epochs + 1):
        tr_res = tr.train_one_epoch(model, train_loader, optimizer, device, clip_norm=1.0)
        val_res = tr.evaluate(model, val_loader, device)

        train_nll_list.append(tr_res["nll"])
        val_nll_list.append(val_res["nll"])
        val_ppl_list.append(val_res["perplexity"])

    return train_nll_list, val_nll_list, val_ppl_list


def main():
    print("Mengumpulkan data kurva metrik...")
    epochs = list(range(1, 13))

    # R1: Usulan Utama (Hidden 128, LR 1e-3)
    r1_tr_nll, r1_val_nll, r1_val_ppl = run_and_collect_history(lr=1e-3, hidden_dim=128, max_epochs=12)

    # R2: LR Konservatif (Hidden 128, LR 3e-4)
    r2_tr_nll, r2_val_nll, r2_val_ppl = run_and_collect_history(lr=3e-4, hidden_dim=128, max_epochs=12)

    # R3: Kapasitas Kecil (Hidden 64, LR 1e-3)
    r3_tr_nll, r3_val_nll, r3_val_ppl = run_and_collect_history(lr=1e-3, hidden_dim=64, max_epochs=12)

    print("Membuat grafik visualisasi...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=150)

    # Subplot 1: Validation NLL (Loss)
    ax1.plot(epochs, r1_val_nll, marker="o", color="#2563eb", linewidth=2.5, label="R1: Usulan (Hidden 128, LR 1e-3)")
    ax1.plot(epochs, r2_val_nll, marker="s", color="#dc2626", linewidth=2.0, linestyle="--", label="R2: LR 3e-4")
    ax1.plot(epochs, r3_val_nll, marker="^", color="#16a34a", linewidth=2.0, linestyle="-.", label="R3: Hidden 64")
    ax1.set_title("Perbandingan Validation NLL per Epoch", fontsize=13, fontweight="bold", pad=10)
    ax1.set_xlabel("Epoch", fontsize=11)
    ax1.set_ylabel("Validation NLL (Negative Log-Likelihood)", fontsize=11)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(fontsize=10)

    # Subplot 2: Validation Perplexity
    ax2.plot(epochs, r1_val_ppl, marker="o", color="#2563eb", linewidth=2.5, label="R1: Usulan (Hidden 128, LR 1e-3)")
    ax2.plot(epochs, r2_val_ppl, marker="s", color="#dc2626", linewidth=2.0, linestyle="--", label="R2: LR 3e-4")
    ax2.plot(epochs, r3_val_ppl, marker="^", color="#16a34a", linewidth=2.0, linestyle="-.", label="R3: Hidden 64")
    ax2.set_title("Perbandingan Validation Perplexity per Epoch", fontsize=13, fontweight="bold", pad=10)
    ax2.set_xlabel("Epoch", fontsize=11)
    ax2.set_ylabel("Perplexity (exp(NLL))", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(fontsize=10)

    plt.suptitle("Kurva Pelatihan & Evaluasi Ablation Study — Nirava MIDI Generator", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(str(OUTPUT_IMAGE), bbox_inches="tight")
    plt.close()
    print(f"[OK] Grafik kurva pelatihan berhasil disimpan ke: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
