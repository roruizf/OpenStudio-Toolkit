"""v0.3 contract tests: docs/contracts/v0.3.toml compared with the code by introspection.

Planned items are xfail(strict=True): when the code lands they XPASS, the run fails, and the
contract must be updated to "implemented". The contract and the code cannot drift silently.
"""

from __future__ import annotations

import ast
import importlib
import re
import sys
import tomllib
from collections.abc import Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "src" / "openstudio_toolkit"
CONTRACT = tomllib.loads((ROOT / "docs" / "contracts" / "v0.3.toml").read_text(encoding="utf-8"))
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


def _status(status: str) -> list[pytest.MarkDecorator]:
    assert status in {"implemented", "planned"}, f"unknown contract status {status!r}"
    if status == "planned":
        return [pytest.mark.xfail(strict=True, reason="planned in the v0.3 contract")]
    return []


def _marked(status: str):
    """Decorator form of _status for single (non-parametrized) tests."""
    marks = _status(status)

    def apply(fn):
        for mark in marks:
            fn = mark(fn)
        return fn

    return apply


def _module_path(dotted: str) -> Path | None:
    """Source path of openstudio_toolkit.<dotted> (module file or package __init__), if it exists."""
    base = PKG.joinpath(*dotted.split("."))
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        if candidate.exists():
            return candidate
    return None


def _package_files(dotted: str) -> list[Path]:
    """All source files of openstudio_toolkit.<dotted>, whether it is a module or a package."""
    base = PKG.joinpath(*dotted.split("."))
    if base.is_dir():
        return sorted(base.rglob("*.py"))
    path = base.with_suffix(".py")
    return [path] if path.exists() else []


def _dotted(path: Path) -> str:
    rel = path.relative_to(PKG.parent).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _imports(path: Path) -> Iterator[str]:
    """Absolute module names imported by a source file (relative imports resolved)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    package = _dotted(path) if path.name == "__init__.py" else _dotted(path).rsplit(".", 1)[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package.split(".")
                base = base[: len(base) - (node.level - 1)]
                mod = ".".join(base + ([node.module] if node.module else []))
            else:
                mod = node.module or ""
            yield mod
            for alias in node.names:
                yield f"{mod}.{alias.name}"


# ---------------------------------------------------------------------------
# Runtime and packaging
# ---------------------------------------------------------------------------


def test_requires_python_matches_contract() -> None:
    assert PYPROJECT["project"]["requires-python"] == CONTRACT["runtime"]["requires_python"]


def test_ruff_and_mypy_targets_match_contract() -> None:
    assert PYPROJECT["tool"]["ruff"]["target-version"] == CONTRACT["runtime"]["ruff_target"]
    assert PYPROJECT["tool"]["mypy"]["python_version"] == CONTRACT["runtime"]["mypy_python"]


def test_ci_matrix_matches_contract() -> None:
    match = re.search(r"python-version:\s*\[([^\]]*)\]", CI_WORKFLOW.read_text(encoding="utf-8"))
    assert match, "CI workflow has no python-version matrix"
    matrix = [v.strip().strip("\"'") for v in match.group(1).split(",")]
    assert matrix == CONTRACT["runtime"]["ci_python"]


def test_ci_matrix_is_inside_requires_python() -> None:
    low, high = re.fullmatch(r">=(\d+\.\d+),<(\d+\.\d+)", CONTRACT["runtime"]["requires_python"]).groups()
    as_tuple = lambda v: tuple(int(x) for x in v.split("."))  # noqa: E731
    for version in CONTRACT["runtime"]["ci_python"]:
        assert as_tuple(low) <= as_tuple(version) < as_tuple(high)


def test_running_interpreter_is_supported() -> None:
    from openstudio_toolkit.runtime import SUPPORTED_PYTHON_MINORS

    assert sys.version_info[:2] in SUPPORTED_PYTHON_MINORS
    supported = {f"{major}.{minor}" for major, minor in SUPPORTED_PYTHON_MINORS}
    assert set(CONTRACT["runtime"]["ci_python"]) <= supported


def test_openstudio_pin_matches_contract_and_runtime() -> None:
    from openstudio_toolkit.runtime import REFERENCE_OPENSTUDIO_VERSION

    pinned = CONTRACT["runtime"]["openstudio"]
    assert f"openstudio=={pinned}" in PYPROJECT["project"]["dependencies"]
    assert REFERENCE_OPENSTUDIO_VERSION == pinned


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "entry",
    [pytest.param(e, id=f"{e['module']}.{e['name']}", marks=_status(e["status"])) for e in CONTRACT["api"]],
)
def test_public_api(entry: dict) -> None:
    module = importlib.import_module(f"openstudio_toolkit.{entry['module']}")
    assert callable(getattr(module, entry["name"]))


@pytest.mark.parametrize(
    "kind",
    [
        pytest.param(k, marks=_status("implemented" if CONTRACT["artifact"][k]["implemented"] else "planned"))
        for k in ("compare", "diff")
    ],
)
def test_verification_artifact_schema(kind: str) -> None:
    views = importlib.import_module("openstudio_toolkit.views.verification")
    spec = CONTRACT["artifact"][kind]
    assert list(getattr(views, f"{kind.upper()}_COLUMNS")) == spec["columns"]
    assert list(getattr(views, f"{kind.upper()}_STATUS_VALUES")) == spec["status_values"]
    if kind == "diff":
        assert list(views.DIFF_MATCH_METHODS) == spec["match_methods"]


@pytest.mark.parametrize("entry", [pytest.param(CONTRACT["cli"], id="cli", marks=_status(CONTRACT["cli"]["status"]))])
def test_cli_commands(entry: dict) -> None:
    cli = importlib.import_module(f"openstudio_toolkit.{entry['module']}")
    assert PYPROJECT["project"]["scripts"][entry["entry_point"]] == f"openstudio_toolkit.{entry['module']}:main"
    assert list(cli.COMMANDS) == entry["commands"]


@pytest.mark.parametrize(
    "spec", [pytest.param(CONTRACT["families"], id="families", marks=_status(CONTRACT["families"]["status"]))]
)
def test_new_families_are_dumpable(spec: dict) -> None:
    dump = importlib.import_module("openstudio_toolkit.dump")
    assert set(spec["idd_types"]) <= set(dump.families().values())


# ---------------------------------------------------------------------------
# Boundaries
# ---------------------------------------------------------------------------

_MUTATING_CALL = re.compile(r"^(set[A-Z]\w*|save|saveAs)$")


def _mutations(nodes: Iterator[ast.AST]) -> list[str]:
    found = []
    for node in nodes:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if _MUTATING_CALL.match(node.func.attr) or node.func.attr == "system":
                found.append(f"line {node.lineno}: .{node.func.attr}()")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] + ([node.module] if isinstance(node, ast.ImportFrom) else [])
            if any(n and n.split(".")[0] == "subprocess" for n in names):
                found.append(f"line {node.lineno}: imports subprocess")
    return found


def test_read_code_does_not_mutate_or_spawn() -> None:
    bounds = CONTRACT["boundaries"]
    violations = []
    for dotted in bounds["read_modules"]:
        for path in _package_files(dotted):
            violations += [f"{path.relative_to(ROOT)} {v}" for v in _mutations(ast.walk(ast.parse(path.read_text())))]
    prefix = bounds["read_function_prefix_in_osm_objects"]
    for path in _package_files("osm_objects"):
        for fn in ast.parse(path.read_text()).body:
            if isinstance(fn, ast.FunctionDef) and fn.name.startswith(prefix):
                violations += [f"{path.relative_to(ROOT)}::{fn.name} {v}" for v in _mutations(ast.walk(fn))]
    assert not violations, "\n".join(violations)


def _import_closure(start: list[Path]) -> set[str]:
    """Transitive closure of openstudio_toolkit modules imported from the start files."""
    seen: set[str] = set()
    stack = [_dotted(p) for p in start]
    while stack:
        mod = stack.pop()
        if mod in seen:
            continue
        seen.add(mod)
        path = _module_path(mod.removeprefix("openstudio_toolkit").lstrip("."))
        if path is None:
            continue
        for imported in _imports(path):
            if imported.startswith("openstudio_toolkit"):
                stack.append(imported)
    return seen


def test_verification_never_depends_on_apply() -> None:
    bounds = CONTRACT["boundaries"]
    start = [p for m in bounds["verification_modules"] for p in _package_files(m)]
    closure = _import_closure(start)
    forbidden = [
        mod
        for mod in closure
        for f in bounds["forbidden_for_verification"]
        if mod == f"openstudio_toolkit.{f}" or mod.startswith(f"openstudio_toolkit.{f}.")
    ]
    assert not forbidden, f"compare/diff reach {sorted(forbidden)}"


def test_polars_only_in_results() -> None:
    allowed = [PKG.joinpath(*m.split(".")) for m in CONTRACT["boundaries"]["polars_only_in"]]
    offenders = [
        str(path.relative_to(ROOT))
        for path in PKG.rglob("*.py")
        if not any(path.is_relative_to(a) for a in allowed)
        and any(i.split(".")[0] == "polars" for i in _imports(path))
    ]
    assert not offenders, offenders


@pytest.mark.parametrize(
    "bounds",
    [
        pytest.param(
            CONTRACT["boundaries"], id="generic", marks=_status(CONTRACT["boundaries"]["generic_reader_status"])
        )
    ],
)
def test_generic_reader_uses_only_orphan_safe_methods(bounds: dict) -> None:
    import openstudio

    path = _module_path(bounds["generic_reader_module"])
    assert path is not None, "generic reader module does not exist"
    allowed = set(bounds["generic_reader_allowed_methods"])
    sdk_methods = {
        name
        for cls in vars(openstudio.model).values()
        if isinstance(cls, type)
        for name in dir(cls)
        if not name.startswith("_")
    }
    calls = {
        node.func.attr
        for node in ast.walk(ast.parse(path.read_text()))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert not (calls & sdk_methods) - allowed


# ---------------------------------------------------------------------------
# Invariants
# ---------------------------------------------------------------------------

INV = CONTRACT["invariants"]


@_marked(INV["dataframe_functions_return_columns_when_empty"])
def test_dataframe_functions_return_columns_when_empty() -> None:
    import inspect
    import pkgutil

    import openstudio
    import pandas as pd

    import openstudio_toolkit.osm_objects as pkg

    empty = openstudio.model.Model()
    failures = []
    for info in pkgutil.iter_modules(pkg.__path__):
        mod = importlib.import_module(f"{pkg.__name__}.{info.name}")
        for name, fn in inspect.getmembers(mod, inspect.isfunction):
            if fn.__module__ != mod.__name__ or not re.fullmatch(r"get_all_\w+_as_dataframe", name):
                continue
            try:
                df = fn(empty)
            except Exception as exc:  # noqa: BLE001 - the failure itself is the finding
                failures.append(f"{info.name}.{name}: {type(exc).__name__}: {exc}")
                continue
            if not isinstance(df, pd.DataFrame) or len(df.columns) == 0:
                failures.append(f"{info.name}.{name}: no columns")
    assert not failures, "\n".join(failures)


@_marked(INV["no_bare_optional_get_in_osm_objects"])
def test_no_bare_optional_get_in_osm_objects() -> None:
    offenders = []
    for path in _package_files("osm_objects"):
        if path.name == "_base.py":
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "get"
                and not node.args
                and not node.keywords
            ):
                offenders.append(f"{path.name}:{node.lineno}")
    assert not offenders, f"{len(offenders)} bare .get() calls, e.g. {offenders[:5]}"


@_marked(INV["orphans_reported_as_findings"])
def test_orphans_reported_as_findings() -> None:
    import openstudio

    from openstudio_toolkit.validators.references import validate_references

    fixture = ROOT / INV["orphan_fixture"]
    model = openstudio.osversion.VersionTranslator().loadModel(str(fixture)).get()
    codes = {f.code for f in validate_references(model)}
    assert {"integrity.reference.absent"} <= codes


@_marked(INV["verification_runs_on_untouched_models"])
def test_verification_runs_on_untouched_models() -> None:
    import openstudio

    from openstudio_toolkit.analysis.compare import COMPARE_FAMILIES, compare_to_mapping
    from openstudio_toolkit.analysis.diff import diff_models

    load = lambda p: openstudio.osversion.VersionTranslator().loadModel(str(p)).get()  # noqa: E731
    fixture = ROOT / "tests" / "resources" / "small_office.osm"
    assert diff_models(load(fixture), load(fixture)) is not None
    model = load(fixture)
    for by, scopes in (("space", model.getSpaces()), ("thermal_zone", model.getThermalZones())):
        mapping = {family: {s.nameString(): 0.0 for s in scopes} for family in COMPARE_FAMILIES}
        assert not compare_to_mapping(model, mapping, by=by).empty
