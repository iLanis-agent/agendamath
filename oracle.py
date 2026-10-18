#!/usr/bin/env python3
# Agenda Math oracle - mirrors engine.js.
import json, re

def _time(s, label):
    m = re.fullmatch(r"([01][0-9]|2[0-3]):([0-5][0-9])", str(s).strip())
    if not m:
        raise ValueError(f"{label} must be a time written like 09:30, from 00:00 to 23:59")
    return int(m[1]) * 60 + int(m[2])

def _show(t):
    day, r = divmod(t, 1440)
    s = f"{r // 60:02d}:{r % 60:02d}"
    if day == 0:
        return s
    return f"{s} (+{day} " + ("day)" if day == 1 else "days)")

def _plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")

def _whole(x, lo, hi, msg):
    if not isinstance(x, int) or x < lo or x > hi:
        raise ValueError(msg)
    return x

def _durations(lst):
    parts = [p.strip() for p in str(lst).split(",")]
    if len(parts) < 1 or len(parts) > 12:
        raise ValueError("enter 1 to 12 durations in minutes separated by commas")
    out = []
    for p in parts:
        if not re.fullmatch(r"[0-9]+", p) or int(p) < 1 or int(p) > 1440:
            raise ValueError("each duration must be a whole number of minutes from 1 to 1440")
        out.append(int(p))
    return out

def _gap(g):
    return _whole(g, 0, 120, "gap must be a whole number of minutes from 0 to 120")

def end_truth(start, minutes):
    a = _time(start, "start time")
    m = _whole(minutes, 0, 10000, "minutes must be a whole number from 0 to 10000")
    return f"{_show(a)} plus {_plural(m, 'minute')}: {_show(a + m)}."

def run_truth(start, lst, gap):
    a = _time(start, "start time")
    ds = _durations(lst)
    g = _gap(gap)
    cur = a
    spans = []
    for d in ds:
        s, e = cur, cur + d
        cur = e + g
        spans.append(f"{_show(s)} to {_show(e)}")
    return f"Start {_show(a)}, gap {_plural(g, 'minute')}: " + "; ".join(spans) + "."

def fit_truth(start, end, lst, gap):
    a = _time(start, "start time")
    b = _time(end, "end time")
    if b <= a:
        raise ValueError("end time must be after start time")
    ds = _durations(lst)
    g = _gap(gap)
    need = sum(ds) + g * (len(ds) - 1)
    win = b - a
    tail = f"Spare: {win - need}." if need <= win else f"Short: {need - win}."
    return f"Window {_show(a)} to {_show(b)} is {_plural(win, 'minute')}. Items and gaps need {need}. {tail}"

FNS = {"endTruth": end_truth, "runTruth": run_truth, "fitTruth": fit_truth}

CASES = [
    ("endTruth", ["09:30", 90]), ("endTruth", ["09:30", 0]), ("endTruth", ["09:30", 1]), ("endTruth", ["23:30", 90]),
    ("endTruth", ["23:59", 1]), ("endTruth", ["00:00", 1440]), ("endTruth", ["12:00", 2881]), ("endTruth", ["09:30", 10000]),
    ("endTruth", ["9:30", 90]), ("endTruth", ["24:00", 90]), ("endTruth", ["09:60", 90]), ("endTruth", ["09:30", -5]),
    ("endTruth", ["09:30", 10001]), ("endTruth", ["09:30", 1.5]),
    ("runTruth", ["09:00", "30, 30, 30", 5]), ("runTruth", ["09:00", "45", 0]), ("runTruth", ["09:00", "30, 30", 1]),
    ("runTruth", ["23:00", "30, 45, 20", 10]), ("runTruth", ["09:00", "1, 1", 0]), ("runTruth", ["09:00", "", 5]),
    ("runTruth", ["09:00", "30, x", 5]), ("runTruth", ["09:00", "30, 0", 5]), ("runTruth", ["09:00", "1441", 5]),
    ("runTruth", ["09:00", "1,2,3,4,5,6,7,8,9,10,11,12,13", 5]), ("runTruth", ["09:00", "30", 121]), ("runTruth", ["09:00", "30", -1]),
    ("runTruth", ["soon", "30", 5]),
    ("fitTruth", ["09:00", "12:00", "45, 60, 40", 5]), ("fitTruth", ["09:00", "10:00", "30, 30", 0]),
    ("fitTruth", ["09:00", "10:00", "30, 30", 5]), ("fitTruth", ["09:00", "09:01", "1", 0]), ("fitTruth", ["09:00", "09:00", "30", 5]),
    ("fitTruth", ["10:00", "09:00", "30", 5]), ("fitTruth", ["09:00", "12:00", "45, 60, 40", 200]), ("fitTruth", ["09:00", "noon", "30", 5]),
    ("fitTruth", ["09:00", "23:59", "1440", 0]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
