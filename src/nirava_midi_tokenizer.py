"""Tokenizer nirava-midi-step-v1 (pilot pra-GO, hanya stdlib).

Mengikuti docs/MIDI_TOKENIZATION.md: monofonik, 4/4, 16 langkah per bar,
V=133. Parser SMF minimal ditulis sendiri agar tidak menambah dependensi.
"""

import hashlib
import struct

TOKENIZER_VERSION = "nirava-midi-step-v1"

PAD, BOS, EOS, REST, HOLD = 0, 1, 2, 3, 4
NOTE_BASE = 5
VOCAB_SIZE = 133
STEPS_PER_BAR = 16
STEPS_PER_QUARTER = 4

EXPORT_PPQ = 480
EXPORT_TICKS_PER_STEP = EXPORT_PPQ // STEPS_PER_QUARTER  # 120
EXPORT_VELOCITY = 80

MAX_FILE_BYTES = 1_000_000
MAX_EVENTS = 200_000


class SmfError(Exception):
    """File SMF tidak valid atau tidak didukung parser."""


class Reject(Exception):
    """Piece ditolak oleh aturan filter v1; .reason berisi alasan."""

    def __init__(self, reason, detail=""):
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason
        self.detail = detail


def tokenizer_hash():
    spec = f"{TOKENIZER_VERSION}|V={VOCAB_SIZE}|spb={STEPS_PER_BAR}|" \
           f"PAD,BOS,EOS,REST,HOLD,NOTE_0..127"
    return hashlib.sha256(spec.encode()).hexdigest()


def note_token(pitch):
    if not 0 <= pitch <= 127:
        raise ValueError(f"pitch di luar 0..127: {pitch}")
    return NOTE_BASE + pitch


def token_pitch(token):
    return token - NOTE_BASE


def is_note(token):
    return NOTE_BASE <= token < VOCAB_SIZE


# ---------------------------------------------------------------- parsing

def _read_varlen(data, pos):
    value = 0
    for _ in range(4):
        if pos >= len(data):
            raise SmfError("varlen terpotong")
        byte = data[pos]
        pos += 1
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            return value, pos
    raise SmfError("varlen lebih dari 4 byte")


def parse_smf(data):
    """Parse SMF type 0/1. Mengembalikan dict info; tidak mengubah musik."""
    if len(data) > MAX_FILE_BYTES:
        raise SmfError("file melebihi batas ukuran")
    if len(data) < 14 or data[:4] != b"MThd":
        raise SmfError("header MThd tidak ada")
    hdr_len, fmt, ntrks, division = struct.unpack(">IHHH", data[4:14])
    if hdr_len < 6:
        raise SmfError("panjang header tidak valid")
    if fmt == 2:
        raise SmfError("SMF type 2 tidak didukung")
    if division & 0x8000:
        raise SmfError("pembagian waktu SMPTE tidak didukung")
    if division <= 0:
        raise SmfError("PPQ harus positif")

    pos = 8 + hdr_len
    info = {
        "format": fmt, "ppq": division, "track_count": ntrks,
        "time_sigs": [], "tempos": [], "tracks": [],
        "pedal_or_bend": False, "neutral_bends": 0, "unmatched": 0,
    }
    total_events = 0

    for _ in range(ntrks):
        if pos + 8 > len(data) or data[pos:pos + 4] != b"MTrk":
            raise SmfError("chunk MTrk tidak ditemukan")
        length = struct.unpack(">I", data[pos + 4:pos + 8])[0]
        pos += 8
        end = pos + length
        if end > len(data):
            raise SmfError("chunk track terpotong")
        notes, active = [], {}
        tick, running = 0, None
        while pos < end:
            delta, pos = _read_varlen(data, pos)
            tick += delta
            total_events += 1
            if total_events > MAX_EVENTS:
                raise SmfError("jumlah event melebihi batas")
            if pos >= end:
                raise SmfError("event terpotong")
            status = data[pos]
            if status == 0xFF:
                if pos + 2 > end:
                    raise SmfError("meta terpotong")
                mtype = data[pos + 1]
                mlen, pos = _read_varlen(data, pos + 2)
                body = data[pos:pos + mlen]
                pos += mlen
                if mtype == 0x58 and mlen >= 2:
                    info["time_sigs"].append((body[0], 1 << body[1], tick))
                elif mtype == 0x51 and mlen == 3:
                    info["tempos"].append(int.from_bytes(body, "big"))
                continue
            if status in (0xF0, 0xF7):
                slen, pos = _read_varlen(data, pos + 1)
                pos += slen
                continue
            if status & 0x80:
                running = status
                pos += 1
            elif running is None:
                raise SmfError("running status tanpa status awal")
            kind, chan = running & 0xF0, running & 0x0F
            nbytes = 1 if kind in (0xC0, 0xD0) else 2
            if pos + nbytes > end:
                raise SmfError("pesan kanal terpotong")
            d1 = data[pos]
            d2 = data[pos + 1] if nbytes == 2 else 0
            pos += nbytes
            if kind == 0x90 and d2 > 0:
                active.setdefault((chan, d1), []).append(tick)
            elif kind == 0x80 or (kind == 0x90 and d2 == 0):
                queue = active.get((chan, d1))
                if queue:
                    notes.append((queue.pop(0), tick, d1, chan))
                else:
                    info["unmatched"] += 1
            elif kind == 0xE0:
                # Bend netral (8192) bukan bend aktif; hanya hitung deviasi.
                if (d2 << 7 | d1) != 8192:
                    info["pedal_or_bend"] = True
                else:
                    info["neutral_bends"] += 1
            elif kind == 0xB0 and d1 == 64 and d2 >= 64:
                info["pedal_or_bend"] = True
        pos = end
        info["unmatched"] += sum(len(q) for q in active.values())
        info["tracks"].append(notes)
    return info


# ----------------------------------------------------- melody + quantize

def extract_melody(info):
    """Pilih tepat satu part berpitch dan validasi meter. Raise Reject."""
    sigs = {(n, d) for n, d, _ in info["time_sigs"]}
    if not sigs:
        raise Reject("meter_not_explicit")
    if sigs != {(4, 4)}:
        raise Reject("non_4_4_meter", ";".join(f"{n}/{d}" for n, d in sorted(sigs)))
    if info["pedal_or_bend"]:
        raise Reject("pedal_or_pitch_bend")
    if info["unmatched"]:
        raise Reject("unmatched_note_on_off", str(info["unmatched"]))
    parts = [t for t in info["tracks"] if t]
    if not parts:
        raise Reject("empty_piece")
    if len(parts) > 1:
        raise Reject("multiple_pitched_parts", str(len(parts)))
    notes = parts[0]
    if any(chan == 9 for _, _, _, chan in notes):
        raise Reject("drum_channel")
    return sorted((on, off, pitch) for on, off, pitch, _ in notes)


def quantize_notes(notes, ppq):
    """Ke grid 4 langkah/quarter. Kembalikan (grid_notes, stats). Raise Reject."""
    grid, adjusted = [], 0
    errors = []
    for on, off, pitch in notes:
        q_on, q_off = on / ppq * STEPS_PER_QUARTER, off / ppq * STEPS_PER_QUARTER
        g_on, g_off = int(q_on + 0.5), int(q_off + 0.5)
        errors.append(abs(q_on - g_on))
        errors.append(abs(q_off - g_off))
        if g_off <= g_on:
            g_off = g_on + 1
            adjusted += 1
        grid.append((g_on, g_off, pitch))
    grid.sort()
    for prev, cur in zip(grid, grid[1:]):
        if cur[0] < prev[1]:
            raise Reject("overlap_after_quantization",
                         f"onset {cur[0]} < end {prev[1]}")
    stats = {
        "note_count": len(grid),
        "min_duration_adjusted": adjusted,
        "max_quant_error_steps": max(errors) if errors else 0.0,
        "mean_quant_error_steps": sum(errors) / len(errors) if errors else 0.0,
        "off_grid_events": sum(1 for e in errors if e > 0.25),
    }
    return grid, stats


# -------------------------------------------------------- encode / decode

def encode_grid_notes(grid):
    """grid_notes -> (tokens, meta). Trim leading silence, pad ke bar penuh."""
    if not grid:
        raise Reject("empty_piece")
    offset = grid[0][0]
    shifted = [(on - offset, off - offset, p) for on, off, p in grid]
    length = shifted[-1][1]
    total = -(-length // STEPS_PER_BAR) * STEPS_PER_BAR
    steps = [REST] * total
    for on, off, pitch in shifted:
        steps[on] = note_token(pitch)
        for i in range(on + 1, off):
            steps[i] = HOLD
    meta = {"leading_offset_steps": offset, "trailing_pad_steps": total - length,
            "steps": total, "bars": total // STEPS_PER_BAR}
    return [BOS] + steps + [EOS], meta


def encode_smf_bytes(data):
    """Pipeline lengkap: bytes SMF -> (tokens, meta). Raise Reject/SmfError."""
    info = parse_smf(data)
    notes = extract_melody(info)
    grid, stats = quantize_notes(notes, info["ppq"])
    tokens, meta = encode_grid_notes(grid)
    meta.update(stats)
    meta["source_ppq"] = info["ppq"]
    return tokens, meta


def decode_tokens(tokens):
    """tokens -> grid_notes [(onset, end, pitch)] setelah validasi grammar."""
    if len(tokens) < 3 or tokens[0] != BOS or tokens[-1] != EOS:
        raise ValueError("sequence harus [BOS, steps..., EOS]")
    steps = tokens[1:-1]
    if len(steps) % STEPS_PER_BAR:
        raise ValueError("jumlah langkah bukan kelipatan 16")
    notes, active = [], None  # active = [onset, pitch]
    for i, tok in enumerate(steps):
        if tok in (PAD, BOS, EOS):
            raise ValueError(f"token {tok} tidak sah di langkah {i}")
        if not 0 <= tok < VOCAB_SIZE:
            raise ValueError(f"token di luar vocabulary: {tok}")
        if tok == HOLD:
            if active is None:
                raise ValueError(f"HOLD tanpa nada aktif di langkah {i}")
            continue
        if active is not None:
            notes.append((active[0], i, active[1]))
            active = None
        if is_note(tok):
            active = [i, token_pitch(tok)]
    if active is not None:
        notes.append((active[0], len(steps), active[1]))
    return notes


# ------------------------------------------------------------------ export

def _varlen(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(out))


def write_smf(events, ppq, time_sig, end_tick, fmt=0):
    """events: [(tick, 'on'|'off', pitch)] -> bytes SMF (satu track, ch 0)."""
    num, den = time_sig
    body = bytearray()
    body += b"\x00\xFF\x51\x03" + (500000).to_bytes(3, "big")
    body += b"\x00\xFF\x58\x04" + bytes([num, den.bit_length() - 1, 24, 8])
    body += b"\x00\xC0\x00"
    order = {"off": 0, "on": 1}
    last = 0
    for tick, kind, pitch in sorted(events, key=lambda e: (e[0], order[e[1]])):
        body += _varlen(tick - last)
        last = tick
        if kind == "on":
            body += bytes([0x90, pitch, EXPORT_VELOCITY])
        else:
            body += bytes([0x80, pitch, 0])
    body += _varlen(max(end_tick - last, 0)) + b"\xFF\x2F\x00"
    header = b"MThd" + struct.pack(">IHHH", 6, fmt, 1, ppq)
    return header + b"MTrk" + struct.pack(">I", len(body)) + bytes(body)


def export_smf(tokens):
    """tokens kanonik -> bytes SMF type 0, PPQ480, 120 BPM, piano, vel 80."""
    notes = decode_tokens(tokens)
    events = []
    for on, off, pitch in notes:
        events.append((on * EXPORT_TICKS_PER_STEP, "on", pitch))
        events.append((off * EXPORT_TICKS_PER_STEP, "off", pitch))
    total_steps = len(tokens) - 2
    return write_smf(events, EXPORT_PPQ, (4, 4),
                     total_steps * EXPORT_TICKS_PER_STEP)
