"""Pengelompokan work/near-duplicate berbasis fingerprint token (stdlib).

Fingerprint invarian transposisi: tiap note -> (interval dari note sebelumnya,
durasi langkah, jeda REST sebelum note). Set n-gram dibandingkan dengan Jaccard.
"""

import nirava_midi_tokenizer as tk

NGRAM = 6


def note_events(tokens):
    """Token kanonik -> [(pitch, duration, rest_before)]."""
    notes = tk.decode_tokens(tokens)
    events, prev_end = [], None
    for on, off, pitch in notes:
        gap = 0 if prev_end is None else on - prev_end
        events.append((pitch, off - on, gap))
        prev_end = off
    return events


def fingerprint(tokens, n=NGRAM):
    ev = note_events(tokens)
    feats = []
    for i, (pitch, dur, gap) in enumerate(ev):
        interval = 0 if i == 0 else pitch - ev[i - 1][0]
        feats.append((interval, dur, gap))
    return {tuple(feats[i:i + n]) for i in range(max(len(feats) - n + 1, 1))}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class UnionFind:
    def __init__(self, items):
        self.parent = {i: i for i in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def pairwise_similarities(prints, floor=0.0):
    """Hasilkan (nama_a, nama_b, jaccard) untuk pasangan dengan sim > floor."""
    names = sorted(prints)
    out = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            s = jaccard(prints[a], prints[b])
            if s > floor:
                out.append((a, b, s))
    return out


def group_by_threshold(names, sims, threshold):
    uf = UnionFind(names)
    for a, b, s in sims:
        if s >= threshold:
            uf.union(a, b)
    groups = {}
    for n in names:
        groups.setdefault(uf.find(n), []).append(n)
    return groups

