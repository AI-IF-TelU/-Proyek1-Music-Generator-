"""Jalankan tokenizer nirava-midi-step-v1 pada seluruh folder melody.

Output (di reports/): tokenizer_audit.csv, tokenizer_audit_summary.txt.
Tidak menulis token/MIDI hasil ke Git; hanya laporan.
"""

import collections
import csv
import hashlib
import statistics
from pathlib import Path

import nirava_midi_tokenizer as tk

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"


def find_melody_dir():
    candidates = [p for p in (ROOT / "data").rglob("melody") if p.is_dir()]
    if not candidates:
        raise FileNotFoundError("folder melody tidak ditemukan")
    return max(candidates, key=lambda p: len(list(p.glob("*.mid"))))


def main():
    melody = find_melody_dir()
    files = sorted(melody.glob("*.mid"))
    rows, reasons = [], collections.Counter()
    seen_tokens = {}
    ok = rt_ok = 0
    token_lengths = []

    for path in files:
        row = {"filename": path.name, "status": "", "reason": "", "detail": "",
               "bars": "", "steps": "", "token_count": "",
               "mean_quant_error_steps": "", "max_quant_error_steps": "",
               "off_grid_events": "", "min_duration_adjusted": "",
               "round_trip": "", "tokens_sha256": ""}
        try:
            tokens, meta = tk.encode_smf_bytes(path.read_bytes())
        except tk.Reject as rej:
            row.update(status="rejected", reason=rej.reason, detail=rej.detail)
            reasons[rej.reason] += 1
            rows.append(row)
            continue
        except tk.SmfError as err:
            row.update(status="rejected", reason="smf_parse_error", detail=str(err))
            reasons["smf_parse_error"] += 1
            rows.append(row)
            continue

        ok += 1
        token_lengths.append(len(tokens))
        digest = hashlib.sha256(bytes(tokens)).hexdigest()
        exported = tk.export_smf(tokens)
        try:
            tokens2, _ = tk.encode_smf_bytes(exported)
            round_trip = "pass" if tokens2 == tokens else "FAIL"
        except Exception as err:  # dicatat apa adanya, bukan disembunyikan
            round_trip = f"FAIL:{type(err).__name__}"
        rt_ok += round_trip == "pass"
        seen_tokens.setdefault(digest, []).append(path.name)
        row.update(
            status="ok", bars=meta["bars"], steps=meta["steps"],
            token_count=len(tokens),
            mean_quant_error_steps=round(meta["mean_quant_error_steps"], 4),
            max_quant_error_steps=round(meta["max_quant_error_steps"], 4),
            off_grid_events=meta["off_grid_events"],
            min_duration_adjusted=meta["min_duration_adjusted"],
            round_trip=round_trip, tokens_sha256=digest)
        rows.append(row)

    REPORT_DIR.mkdir(exist_ok=True)
    fields = list(rows[0].keys())
    with (REPORT_DIR / "tokenizer_audit.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    good = [r for r in rows if r["status"] == "ok"]
    dup_groups = {h: n for h, n in seen_tokens.items() if len(n) > 1}
    lines = [
        f"tokenizer={tk.TOKENIZER_VERSION} hash={tk.tokenizer_hash()}",
        f"sumber={melody}",
        f"total_file={len(files)}",
        f"encoded_ok={ok}",
        f"rejected={len(files) - ok}",
        "alasan_reject:",
    ]
    lines += [f"  {k}: {v}" for k, v in reasons.most_common()]
    lines.append(f"round_trip_pass={rt_ok}/{ok}")
    if good:
        steps = [int(r["steps"]) for r in good]
        means = [float(r["mean_quant_error_steps"]) for r in good]
        lines += [
            f"total_steps={sum(steps)}",
            f"total_tokens_incl_bos_eos={sum(token_lengths)}",
            f"steps_per_piece min/median/max={min(steps)}/{statistics.median(steps)}/{max(steps)}",
            f"mean_quant_error_steps(rata2 per file)={sum(means)/len(means):.4f}",
            f"max_quant_error_steps(tertinggi)={max(float(r['max_quant_error_steps']) for r in good)}",
            f"file_dengan_off_grid_events(>0.25 step)={sum(1 for r in good if int(r['off_grid_events'])>0)}",
            f"total_off_grid_events={sum(int(r['off_grid_events']) for r in good)}",
            f"file_dengan_min_duration_adjusted={sum(1 for r in good if int(r['min_duration_adjusted'])>0)}",
            f"window128_stride128_estimasi={sum(-(-(int(r['token_count'])-1)//128) for r in good)}",
            f"grup_duplikat_token_identik={len(dup_groups)}",
        ]
        for names in dup_groups.values():
            lines.append("  " + ", ".join(names))
    text = "\n".join(lines)
    (REPORT_DIR / "tokenizer_audit_summary.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

