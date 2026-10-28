"""Command line: ``openstudio-toolkit dump | apply | compare | diff | results`` (item 9).

Approved by Roberto (2026-10-28, "ok 9"). The mapping file is JSON with the ``LoadMapping`` shape,
``{"lights": {"1.10-MeetingRoom": 335.76}}``. Tables are written as CSV; the screen gets a short summary.

Exit codes, so a script or an agent knows the result without reading the report:

- 0: done, and the model matches the mapping (``compare``; ``diff`` with ``--mapping``);
- 1: the model does not match (a row ``differs`` or ``missing``), or ``apply`` refused (reasons printed);
- 2: usage error (bad argument, file not found, model that does not load).

See ``docs/VERIFICATION-GUIDE.md`` for when and how to run the verification.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Any

COMMANDS = ("dump", "apply", "compare", "diff", "results")
RESULTS = ("zone_sizes", "system_sizes", "unmet_hours", "end_uses")


class _UsageError(Exception):
    pass


def _model(path: str) -> Any:
    import openstudio

    from openstudio_toolkit._sdk import opt

    if not Path(path).is_file():
        raise _UsageError(f"model not found: {path}")
    model = opt(openstudio.osversion.VersionTranslator().loadModel(openstudio.path(path)))
    if model is None:
        raise _UsageError(f"model does not load: {path}")
    return model


def _mapping(path: str | None) -> dict[str, dict[str, float]]:
    if path is None:
        return {}
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise _UsageError(f"mapping not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise _UsageError(f"mapping is not valid JSON: {path}: {exc}") from exc
    ok = isinstance(data, dict) and all(
        isinstance(v, dict) and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v.values())
        for v in data.values()
    )
    if not ok:
        raise _UsageError(f'mapping must be {{family: {{name: number}}}}, e.g. {{"lights": {{"A": 120.0}}}}: {path}')
    return {family: {k: float(x) for k, x in values.items()} for family, values in data.items()}


def _units(text: str | None) -> dict[str, str] | None:
    if not text:
        return None
    pairs = [p.split("=", 1) for p in text.split(",")]
    if any(len(p) != 2 or not p[0] or not p[1] for p in pairs):
        raise _UsageError(f"--units must look like GJ=kWh,m3/s=m3/h, not {text!r}")
    return {a.strip(): b.strip() for a, b in pairs}


def _summary(statuses: Sequence[str]) -> str:
    counts = Counter(statuses)
    return ", ".join(f"{n} {s}" for s, n in sorted(counts.items())) or "no rows"


def _dump(args: argparse.Namespace) -> int:
    from openstudio_toolkit import dump

    families = args.families.split(",") if args.families else None
    try:
        views = dump.dump_view(_model(args.model), families)
    except ValueError as exc:
        raise _UsageError(str(exc)) from exc
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, df in views.items():
        df.to_csv(out / f"{name}.csv", index=False)
    print(f"{len(views)} families, {sum(len(df) for df in views.values())} rows -> {out}")
    return 0


def _apply(args: argparse.Namespace) -> int:
    from openstudio_toolkit.transforms.apply import ApplyError, apply_mapping

    if not Path(args.model_input).is_file():
        raise _UsageError(f"model not found: {args.model_input}")
    try:
        results = apply_mapping(args.model_input, args.model_output, _mapping(args.mapping), existing=args.existing)
    except ValueError as exc:
        raise _UsageError(str(exc)) from exc
    except ApplyError as exc:
        print(exc, file=sys.stderr)
        if args.existing == "refuse" and any("existing=" in p for p in exc.problems):
            print("(on the command line: --existing update)", file=sys.stderr)
        return 1
    for r in results:
        print(
            f"{r.family}: {r.spaces_created} created, {r.spaces_updated} updated, "
            f"{r.spaces_skipped_zero} zero (no load), total {r.total_value:g}"
        )
    print(f"-> {args.model_output}")
    return 0


def _compare(args: argparse.Namespace) -> int:
    from openstudio_toolkit.views.verification import compare_rows

    try:
        rows = compare_rows(_model(args.model), _mapping(args.mapping), by=args.by, tolerance=args.tolerance)
    except ValueError as exc:
        raise _UsageError(str(exc)) from exc
    if args.out:
        rows.to_csv(args.out, index=False)
    print(f"compare: {_summary(rows.status.tolist())}" + (f" -> {args.out}" if args.out else ""))
    return 0 if set(rows.status) <= {"match"} else 1


def _diff(args: argparse.Namespace) -> int:
    from openstudio_toolkit.views.verification import ReportPair, compare_rows, diff_rows, write_report

    parent, child, mapping = _model(args.parent), _model(args.child), _mapping(args.mapping)
    try:
        rows = diff_rows(parent, child, mapping, by=args.by)
        compared = compare_rows(child, mapping, by=args.by, tolerance=args.tolerance) if mapping else None
        if args.report:
            pair = ReportPair(
                parent, child, mapping, parent_name=Path(args.parent).name, child_name=Path(args.child).name,
                mapping_name=Path(args.mapping).name if args.mapping else "", by=args.by, tolerance=args.tolerance,
            )
            write_report([pair], args.report, language=args.language)
    except ValueError as exc:
        raise _UsageError(str(exc)) from exc
    if args.out:
        rows.to_csv(args.out, index=False)
    print(f"diff: {_summary(rows.status.tolist())}" + (f" -> {args.out}" if args.out else ""))
    if compared is not None:
        print(f"child vs mapping: {_summary(compared.status.tolist())}")
    if args.report:
        print(f"report -> {args.report}")
    return 0 if compared is None or set(compared.status) <= {"match"} else 1


def _results(args: argparse.Namespace) -> int:
    from openstudio_toolkit import results

    try:
        df = getattr(results, args.table)(args.sql, units=_units(args.units))
    except FileNotFoundError as exc:
        raise _UsageError(f"SQL not found: {args.sql}") from exc
    except ValueError as exc:
        raise _UsageError(str(exc)) from exc
    if args.out:
        df.write_csv(args.out)
        print(f"{args.table}: {len(df)} rows -> {args.out}")
    else:
        sys.stdout.write(df.write_csv())
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openstudio-toolkit", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("dump", help="curated tables of a model, one CSV per family")
    p.add_argument("model")
    p.add_argument("--families", help="comma-separated family names (default: all)")
    p.add_argument("--out", required=True, help="output folder")
    p.set_defaults(run=_dump)

    p = sub.add_parser("apply", help="write a model with the per-Space loads of a mapping")
    p.add_argument("model_input")
    p.add_argument("model_output")
    p.add_argument("--mapping", required=True, help="JSON mapping file")
    p.add_argument("--existing", choices=("refuse", "update"), default="refuse")
    p.set_defaults(run=_apply)

    for name, help_text in (("compare", "a model against a mapping"), ("diff", "parent -> child, against a mapping")):
        p = sub.add_parser(name, help=help_text)
        if name == "compare":
            p.add_argument("model")
            p.add_argument("--mapping", required=True, help="JSON mapping file")
        else:
            p.add_argument("parent")
            p.add_argument("child")
            p.add_argument("--mapping", help="JSON mapping file (without it every change is not requested)")
            p.add_argument("--report", help="write the HTML verification report here")
            p.add_argument("--language", choices=("en", "es", "fr"), default="en")
        p.add_argument("--by", choices=("space", "thermal_zone"), default="space")
        p.add_argument("--tolerance", type=float, default=1e-6, help="absolute (default 1e-6; 0.5 W for G3.7)")
        p.add_argument("--out", help="CSV file for the rows")
        p.set_defaults(run=_compare if name == "compare" else _diff)

    p = sub.add_parser("results", help="a results table from eplusout.sql")
    p.add_argument("sql")
    p.add_argument("table", choices=RESULTS)
    p.add_argument("--units", help="conversions, e.g. GJ=kWh,m3/s=m3/h (default: EnergyPlus units)")
    p.add_argument("--out", help="CSV file (default: print the CSV)")
    p.set_defaults(run=_results)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        code: int = args.run(args)
    except _UsageError as exc:
        print(f"openstudio-toolkit {args.command}: {exc}", file=sys.stderr)
        return 2
    return code


if __name__ == "__main__":
    sys.exit(main())
