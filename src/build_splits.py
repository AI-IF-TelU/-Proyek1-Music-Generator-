"""Bangun split work-disjoint 80/10/10 dan token JSONL (pilot, stdlib).

Output: processed/tokens_v1.jsonl (tidak di Git), reports/split_manifest.csv,
reports/work_groups.csv, reports/split_summary.txt.
Augmentasi tidak dijalankan di sini.
"""

import csv
import hashlib
import json
import random
from pathlib import Path

import nirava_midi_grouping as gp
import nirava_midi_tokenizer as tk

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"
PROCESSED_DIR = ROOT / "processed"

SEED = 20261028
SIM_THRESHOLD = 0.25   # dipilih konservatif dari distribusi di summary
RATIOS = (0.8, 0.1, 0.1)


def find_melody_dir():
    return max((p for p in (ROOT / "data").rglob("melody") if p.is_dir()),
               key=lambda p: len(list(p.glob("*.mid"))))


def assign_splits(groups, sizes, seed=SEED, ratios=RATIOS):
    """groups: {gid: [names]}. Pembagian per group, tanpa memecah group."""
    gids = sorted(groups)
    random.Random(seed).shuffle(gids)
    total = sum(sizes[g] for g in gids)
    targets = [ratios[0] * total, (ratios[0] + ratios[1]) * total]
    split_of, running = {}, 0
    for g in gids:
        name = "train" if running < targets[0] else \
               "validation" if running < targets[1] else "test"
        split_of[g] = name
        running += sizes[g]
    return split_of


def main():
    melody = find_melody_dir()
    pieces = {}
    for path in sorted(melody.glob("*.mid")):
        raw = path.read_bytes()
        try:
            tokens, meta = tk.encode_smf_bytes(raw)
        except (tk.Reject, tk.SmfError):
            continue
        pieces[path.name] = {
            "tokens": tokens, "meta": meta,
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "tokens_sha256": hashlib.sha256(bytes(tokens)).hexdigest(),
        }

    # Dedup token identik: simpan yang pertama (urut nama), sisanya dikecualikan.
    seen, excluded = {}, []
    for name in sorted(pieces):
        h = pieces[name]["tokens_sha256"]
        if h in seen:
            excluded.append((name, "exact_duplicate_tokens", seen[h]))
        else:
            seen[h] = name
    kept = sorted(seen.values())

    prints = {n: gp.fingerprint(pieces[n]["tokens"]) for n in kept}
    sims = gp.pairwise_similarities(prints, floor=0.05)
    raw_groups = gp.group_by_threshold(kept, sims, SIM_THRESHOLD)
    groups = {f"w{i:04d}": sorted(v) for i, (_, v) in
              enumerate(sorted(raw_groups.items(), key=lambda kv: kv[0]))}
    sizes = {g: len(v) for g, v in groups.items()}
    split_of = assign_splits(groups, sizes)

    rows, group_of = [], {}
    for gid, names in groups.items():
        for n in names:
            group_of[n] = gid
    for n in kept:
        p = pieces[n]
        rows.append({
            "piece_id": "p" + p["tokens_sha256"][:12],
            "filename": n,
            "work_group_id": group_of[n],
            "split": split_of[group_of[n]],
            "file_sha256": p["file_sha256"],
            "tokens_sha256": p["tokens_sha256"],
            "steps": p["meta"]["steps"],
            "bars": p["meta"]["bars"],
            "token_count": len(p["tokens"]),
            "tokenizer": tk.TOKENIZER_VERSION,
            "tokenizer_hash": tk.tokenizer_hash(),
            "grouping": f"jaccard{NGRAM_LABEL}>={SIM_THRESHOLD}",
        })

    REPORT_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    with (REPORT_DIR / "split_manifest.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with (REPORT_DIR / "work_groups.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["work_group_id", "split", "size", "files"])
        for gid, names in groups.items():
            w.writerow([gid, split_of[gid], len(names), ";".join(names)])
    with (REPORT_DIR / "split_exclusions.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["filename", "reason", "kept_instead"])
        w.writerows(excluded)
    with (PROCESSED_DIR / "tokens_v1.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({
                "piece_id": r["piece_id"], "work_group_id": r["work_group_id"],
                "split": r["split"], "tokens_sha256": r["tokens_sha256"],
                "tokens": pieces[r["filename"]]["tokens"]}) + "\n")

    # Pemeriksaan leakage: tidak ada group lintas split, tidak ada token identik lintas split.
    leaks = [g for g, names in groups.items()
             if len({r["split"] for r in rows if r["work_group_id"] == g}) > 1]
    hash_splits = {}
    for r in rows:
        hash_splits.setdefault(r["tokens_sha256"], set()).add(r["split"])
    hash_leaks = [h for h, s in hash_splits.items() if len(s) > 1]

    lines = [f"seed={SEED} threshold={SIM_THRESHOLD} tokenizer_hash={tk.tokenizer_hash()}",
             f"pieces_encoded={len(pieces)} excluded_duplicates={len(excluded)} kept={len(kept)}",
             f"work_groups={len(groups)} multi_file_groups={sum(1 for v in groups.values() if len(v)>1)}"]
    for s in ("train", "validation", "test"):
        sr = [r for r in rows if r["split"] == s]
        lines.append(f"{s}: pieces={len(sr)} groups={len({r['work_group_id'] for r in sr})} "
                     f"steps={sum(r['steps'] for r in sr)} tokens={sum(r['token_count'] for r in sr)}")
    lines.append(f"leak_group_lintas_split={len(leaks)}")
    lines.append(f"leak_token_identik_lintas_split={len(hash_leaks)}")
    text = "\n".join(lines)
    (REPORT_DIR / "split_summary.txt").write_text(text, encoding="utf-8")
    print(text)


NGRAM_LABEL = f"(n={gp.NGRAM})"

if __name__ == "__main__":
    main()

