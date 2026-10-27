# Usage: python report_draft_render.py <dir with data.pkl> [tolerance W]. First draft shown to Roberto (bilingual, Excel + HTML); superseded by the decisions in V0.3-DECISIONS item 7.
"""Draft of the visible form: same rows rendered as Excel (openpyxl, already a dependency) and as one
self-contained HTML file (pandas.to_html + inline CSS, no JS, no new dependency). Labels bilingual."""
import html, pickle, sys
import pandas as pd
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

S = sys.argv[1]
d = pickle.load(open(f"{S}/data.pkl", "rb"))
TOL = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

COLS = {  # contract column -> visible label (ES / EN)
    "family": "Familia / Family", "key": "Espacio u objeto / Key", "field": "Campo / Field",
    "requested": "Pedido / Requested", "in_model": "En el modelo / In model",
    "difference": "Diferencia / Difference", "status": "Estado / Status",
    "parent": "Padre / Parent", "child": "Hijo / Child", "match_method": "Emparejado por / Matched by",
}
STATUS = {"match": "coincide / match", "differs": "difiere / differs", "missing": "falta / missing",
          "changed": "cambiado / changed", "added": "agregado / added", "removed": "eliminado / removed",
          "not_requested": "no pedido / not requested"}
FIELD = {"Lighting Level {W}": "Lighting Level {W} (total del espacio / space total)",
         "(object added)": "(objeto agregado / object added)",
         "(object removed)": "(objeto eliminado / object removed)"}
COLOR = {"match": "E2F0D9", "differs": "FCE4D6", "missing": "F8CBAD", "changed": "FFF2CC",
         "added": "DDEBF7", "removed": "EDEDED"}


def recompare(df):
    """Status again with the report tolerance (the rows came with 1e-6)."""
    df = df.copy()
    df["status"] = ["missing" if s == "missing" else ("match" if abs(x) <= TOL else "differs")
                    for s, x in zip(df.status, df.difference)]
    return df


def visible(df):
    out = df.copy()
    out["status"] = out.status.map(STATUS)
    if "field" in out:
        out["field"] = out.field.map(lambda f: FIELD.get(f, f) if isinstance(f, str) else "")
    for c in ("requested", "in_model", "difference"):
        if c in out:
            out[c] = out[c].round(2)
    return out.rename(columns=COLS)


cmp_ref, cmp_act, diff = recompare(d["cmp_ref"]), recompare(d["cmp_act"]), d["diff"]
req = diff[diff.status != "not_requested"]
nreq = diff[diff.status == "not_requested"]
title = "Office Hub ENE01 actual-017 -> reference-011"
meta = [("Modelo padre / Parent model", "r2f-office-hub-ene01-actual-017.osm"),
        ("Modelo hijo / Child model", "r2f-office-hub-ene01-reference-011.osm"),
        ("Mapping", "lights: Tabla/Table G3.7 (ENE01-REFERENCE-MODEL-SPEC §5) x floor area, 36 spaces"),
        ("Nivel / Scope", "Space"), ("Tolerancia / Tolerance", f"{TOL} W")]

def counts(df):
    return df.status.map(STATUS).value_counts().rename_axis("Estado / Status").reset_index(name="Filas / Rows")

summary = pd.DataFrame(
    [("Comparación hijo vs. pedido / Child vs. requested", STATUS[s], n) for s, n in cmp_ref.status.value_counts().items()]
    + [("Comparación padre vs. pedido / Parent vs. requested", STATUS[s], n) for s, n in cmp_act.status.value_counts().items()]
    + [("Cambios padre -> hijo / Changes parent -> child", STATUS[s], n) for s, n in diff.status.value_counts().items()],
    columns=["Sección / Section", "Estado / Status", "Filas / Rows"])
nreq_by_family = nreq.family.value_counts().rename_axis(COLS["family"]).reset_index(name="Filas / Rows")

# ---------------- Excel ----------------
xlsx = f"{S}/verificacion-office-hub.xlsx"
sheets = {"Resumen": summary, "Comparacion hijo": visible(cmp_ref), "Comparacion padre": visible(cmp_act),
          "Cambios pedidos": visible(req), "No pedidos por familia": nreq_by_family, "No pedidos": visible(nreq)}
with pd.ExcelWriter(xlsx, engine="openpyxl") as xw:
    meta_df = pd.DataFrame(meta, columns=["", title])
    meta_df.to_excel(xw, sheet_name="Resumen", index=False)
    for name, df in sheets.items():
        start = len(meta) + 2 if name == "Resumen" else 0
        df.to_excel(xw, sheet_name=name, index=False, startrow=start)
        ws = xw.sheets[name]
        hdr = start + 1
        for cell in ws[hdr]:
            cell.font = Font(bold=True)
        ws.freeze_panes = ws.cell(row=hdr + 1, column=1)
        ws.auto_filter.ref = f"A{hdr}:{get_column_letter(df.shape[1])}{hdr + len(df)}"
        for i, col in enumerate(df.columns, 1):
            width = max([len(str(col))] + [len(str(v)) for v in df[col].head(500)])
            ws.column_dimensions[get_column_letter(i)].width = min(width + 2, 60)
        if COLS["status"] in df:
            j = list(df.columns).index(COLS["status"]) + 1
            back = {v: k for k, v in STATUS.items()}
            for r in range(hdr + 1, hdr + 1 + len(df)):
                c = ws.cell(row=r, column=j)
                color = COLOR.get(back.get(c.value))
                if color:
                    c.fill = PatternFill("solid", fgColor=color)

# ---------------- HTML ----------------
CSS = """
:root{--bg:#fff;--fg:#1d1d1f;--mut:#666;--line:#ddd;--head:#f4f4f6}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#eee;--mut:#aaa;--line:#333;--head:#222}}
body{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif;margin:0 auto;max-width:1100px;padding:16px}
h1{font-size:20px}h2{font-size:16px;margin-top:28px}
table{border-collapse:collapse;width:100%;font-size:13px;margin:8px 0}
th,td{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}
th{background:var(--head);position:sticky;top:0}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.s{border-radius:4px;padding:1px 6px;color:#111}
details{margin:6px 0}summary{cursor:pointer;color:var(--mut)}
.meta td:first-child{color:var(--mut);width:220px}
.wrap{overflow-x:auto}
"""

def table(df):
    dfv = visible(df) if "status" in df else df
    rows = []
    back = {v: k for k, v in STATUS.items()}
    for _, r in dfv.iterrows():
        cells = []
        for c, v in r.items():
            if c == COLS["status"]:
                cells.append(f'<td><span class="s" style="background:#{COLOR.get(back.get(v), "eee")}">{html.escape(str(v))}</span></td>')
            elif isinstance(v, float):
                cells.append(f'<td class="num">{"" if pd.isna(v) else f"{v:,.2f}"}</td>')
            else:
                cells.append(f"<td>{'' if v is None or (isinstance(v, float) and pd.isna(v)) else html.escape(str(v))}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in dfv.columns)
    return f'<div class="wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

parts = [f"<h1>Informe de verificación / Verification report</h1><p>{html.escape(title)}</p>",
         '<table class="meta">' + "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>" for a, b in meta) + "</table>",
         "<h2>Resumen / Summary</h2>", table(summary),
         "<h2>Comparación del hijo con lo pedido / Child vs. requested</h2>", table(cmp_ref),
         "<h2>Comparación del padre con lo pedido / Parent vs. requested</h2>",
         f"<details><summary>{len(cmp_act)} filas / rows</summary>{table(cmp_act)}</details>",
         "<h2>Cambios pedidos / Requested changes</h2>", table(req),
         "<h2>Cambios no pedidos / Changes not requested</h2>", table(nreq_by_family)]
for fam, g in nreq.groupby("family", sort=False):
    parts.append(f"<details><summary>{html.escape(fam)}: {len(g)}</summary>{table(g)}</details>")
page = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Verificación Office Hub</title><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
open(f"{S}/verificacion-office-hub.html", "w").write(page)
print(xlsx, f"{S}/verificacion-office-hub.html")
print(summary.to_string())
