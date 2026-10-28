# Usage: python report_check.py <dir with models/ and verification-office-hub.html>
# Checks every number and count of the HTML against the rows, as numbers.
import sys, re, collections, openstudio
from html.parser import HTMLParser
from openstudio_toolkit.views.verification import compare_rows, diff_rows
S = sys.argv[1]
load = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
actual = load(f"{S}/models/r2f-office-hub-ene01-actual-017.osm"); ref = load(f"{S}/models/r2f-office-hub-ene01-reference-011.osm")
G37 = {"Office": 11.84, "MeetingRoom": 13.99, "Circulations": 5.38, "BreakRoom": 12.92, "Storage": 8.61, "WC": 9.69, "Lobby": 13.99}
mapping = {"lights": {s.nameString(): G37[s.spaceType().get().nameString()] * s.floorArea() for s in ref.getSpaces()}}
cmp = compare_rows(ref, mapping, tolerance=0.5); diff = diff_rows(actual, ref, mapping)

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.rows = []; s.cur = None; s.cell = None; s.depth = 0
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == "tr" and "data-status" in a: s.cur = {"status": a["data-status"], "family": a["data-family"], "cells": []}
        elif tag == "td" and s.cur is not None: s.cell = {"v": a.get("data-v"), "place": a.get("data-place"), "text": ""}
    def handle_endtag(s, tag):
        if tag == "td" and s.cell is not None: s.cur["cells"].append(s.cell); s.cell = None
        elif tag == "tr" and s.cur is not None: s.rows.append(s.cur); s.cur = None
    def handle_data(s, d):
        if s.cell is not None: s.cell["text"] += d
p = P(); page = open(f"{S}/verification-office-hub.html", encoding="utf-8").read(); p.feed(page)
crow = [r for r in p.rows if len(r["cells"]) == 7]; drow = [r for r in p.rows if len(r["cells"]) == 10]
bad = 0
assert len(crow) == len(cmp), (len(crow), len(cmp))
html_by_key = {r["cells"][1]["text"]: r for r in crow}
for r in cmp.itertuples():
    h = html_by_key[r.key]
    for i, col in ((3, "requested"), (4, "in_model"), (5, "difference")):
        v = getattr(r, col); c = h["cells"][i]
        if float(c["v"]) != float(v): bad += 1; print("data-v", r.key, col, c["v"], v)
        if abs(float(c["text"].replace(",", "")) - float(v)) > 0.005 + 1e-12: bad += 1; print("text", r.key, col, c["text"], v)
    if h["status"] != r.status: bad += 1
print("compare rows", len(crow), "numbers checked", 3 * len(crow), "bad", bad)
print("compare status", cmp.status.value_counts().to_dict(), "max |difference|", cmp.difference.abs().max())
assert len(drow) == len(diff), (len(drow), len(diff))
print("diff rows html", collections.Counter(r["status"] for r in drow), "rows", diff.status.value_counts().to_dict())
# counts shown in summary and groups
for m in re.finditer(r'class="s s-(\w+)"><span data-t="status\.\w+">', page): pass
summ = re.findall(r'<span class="s s-(\w+)">([\d,]+) <span', page)
print("summary chips", summ)
groups = re.findall(r'<details open class="group" data-family="([^"]+)"><summary><code>[^<]+</code> <span class="count"><span data-t="rows" data-n="([\d,]+)"', page)
tot = sum(int(n.replace(",", "")) for _, n in groups); print("group rows sum", tot, "=", len(cmp) + len(diff))
parts = re.findall(r'<h4><span data-t="part\.(\w+)">[^<]+</span> <span class="count"><span data-t="rows" data-n="([\d,]+)"', page)
print("parts", parts, sum(int(n.replace(",", "")) for _, n in parts), "=", (diff.status == "not_requested").sum())
placed = sum(1 for r in drow if any(c["place"] for c in r["cells"][7:]))
print("diff rows with a location", placed, "of", len(drow))
shared = collections.Counter(c["text"].split("(")[0].strip() for r in drow for c in r["cells"][7:] if c["place"] and "|" in c["place"])
print("shared cells", sum(shared.values()))
