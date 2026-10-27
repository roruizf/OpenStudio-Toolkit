"""Item 2: every get_all_*_as_dataframe in osm_objects, found by introspection (present and future).

Per function:
- an empty family yields a DataFrame with its columns;
- on the repo fixtures that have objects of the family it returns rows with those same columns;
- with every field of FATAL_WHEN_ABSENT blanked on every object of the fixtures (orphan relations,
  as in East-Gate-Pro-A2-030 or Tribe-Hotel-015) it neither raises nor dies.

The last two run one subprocess per function, so a segfault fails that function only.

Modules listed in PENDING_MODULES have not been migrated to the item-2 pattern yet (columns passed
to build_dataframe, relations through _sdk.related/related_name, Optionals through _sdk.opt); their
tests are expected to fail. Remove a module from the set when it is migrated. The contract
invariant test_dataframe_functions_return_columns_when_empty stays strict until the set is empty.
"""

from __future__ import annotations

import importlib
import inspect
import json
import os
import pkgutil
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import openstudio
import pandas as pd
import pytest

import openstudio_toolkit.osm_objects as osm_objects
from openstudio_toolkit._sdk import opt
from openstudio_toolkit.validators._fatal_references import FATAL_WHEN_ABSENT

ROOT = Path(__file__).resolve().parents[2]
WORKER = Path(__file__).with_name("dataframe_worker.py")
FIXTURES = {
    "small_office": ROOT / "tests" / "resources" / "small_office.osm",
    "office_hub": ROOT / "examples" / "R2F-Office-Hub.osm",
    # Families no other fixture has (VRF, gas/steam/other equipment, ...); built by make_extra_families.py.
    "extra_families": ROOT / "tests" / "resources" / "extra_families.osm",
}
ORPHAN_FIXTURE = ROOT / "tests" / "resources" / "orphans_minimal.osm"

PENDING_MODULES: set[str] = set()


def _discover() -> list[tuple[str, str]]:
    found = []
    for info in pkgutil.iter_modules(osm_objects.__path__):
        module = importlib.import_module(f"{osm_objects.__name__}.{info.name}")
        for name, fn in inspect.getmembers(module, inspect.isfunction):
            if fn.__module__ == module.__name__ and re.fullmatch(r"get_all_\w+_as_dataframe", name):
                found.append((info.name, name))
    return found


FUNCTIONS = _discover()


def _params() -> list:
    pending = pytest.mark.xfail(strict=False, reason="module not migrated to the item-2 pattern yet")
    return [
        pytest.param(f, id=f"{f[0]}.{f[1]}", marks=[pending] if f[0] in PENDING_MODULES else [])
        for f in FUNCTIONS
    ]


def _function(entry: tuple[str, str]):
    return getattr(importlib.import_module(f"{osm_objects.__name__}.{entry[0]}"), entry[1])


def _blank_fatal_references(model) -> int:
    """Empty every FATAL_WHEN_ABSENT field on every object that has it set; return how many."""
    blanked = 0
    for idd_type, field in FATAL_WHEN_ABSENT:
        for obj in model.getObjectsByType(openstudio.IddObjectType(idd_type)):
            index = opt(obj.iddObject().getFieldIndex(field))
            if index is not None and index < obj.numFields() and opt(obj.getString(index)):
                blanked += bool(obj.setString(index, ""))
    return blanked


@pytest.fixture(scope="module")
def blanked_fixtures(tmp_path_factory) -> dict[str, Path]:
    out = tmp_path_factory.mktemp("blanked")
    translator = openstudio.osversion.VersionTranslator()
    paths = {}
    for label, source in FIXTURES.items():
        model = translator.loadModel(str(source)).get()
        assert _blank_fatal_references(model) > 0, f"nothing to blank in {label}"
        paths[label] = out / source.name
        assert model.save(str(paths[label]), True)
    return paths


@pytest.fixture(scope="module")
def worker_results(request, blanked_fixtures) -> dict[tuple[str, str], dict]:
    """One subprocess per selected function: fixtures as-is, then blanked fixtures and the orphan fixture."""
    selected = {
        item.callspec.params["entry"]
        for item in request.session.items
        if item.path == Path(__file__) and hasattr(item, "callspec") and "entry" in item.callspec.params
    }
    models = [f"fixture:{label}={path}" for label, path in FIXTURES.items()]
    models += [f"blanked:{label}={path}" for label, path in blanked_fixtures.items()]
    models.append(f"blanked:orphans_minimal={ORPHAN_FIXTURE}")

    def run(entry: tuple[str, str]) -> dict:
        proc = subprocess.run(
            [sys.executable, "-I", str(WORKER), *entry, *models],
            capture_output=True,
            text=True,
            timeout=600,
        )
        lines = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
        return {"returncode": proc.returncode, "lines": lines, "expected": [m.split("=")[0] for m in models]}

    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        entries = [f for f in FUNCTIONS if f in selected]
        return dict(zip(entries, pool.map(run, entries)))


def _lines(result: dict, prefix: str) -> list[dict]:
    return [line for line in result["lines"] if line["model"].startswith(prefix)]


@pytest.mark.parametrize("entry", _params())
def test_empty_family_has_columns(entry: tuple[str, str]) -> None:
    df = _function(entry)(openstudio.model.Model())

    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert len(df.columns) > 0


@pytest.mark.parametrize("entry", _params())
def test_works_on_fixtures_with_objects(entry: tuple[str, str], worker_results) -> None:
    result = worker_results[entry]
    lines = _lines(result, "fixture:")

    assert len(lines) == len(FIXTURES), f"process died (return code {result['returncode']})"
    assert not [line for line in lines if "error" in line]
    populated = [line for line in lines if line["rows"]]
    if not populated:
        pytest.skip("no repo fixture has objects of this family")
    columns = list(_function(entry)(openstudio.model.Model()).columns)
    for line in populated:
        assert line["columns"] == columns, f"columns on {line['model']} differ from the empty-family columns"


@pytest.mark.parametrize("entry", _params())
def test_survives_orphan_relations(entry: tuple[str, str], worker_results) -> None:
    result = worker_results[entry]

    assert result["returncode"] >= 0, f"process killed by signal {-result['returncode']}"
    assert [line["model"] for line in result["lines"]] == result["expected"]
    assert not [line for line in _lines(result, "blanked:") if "error" in line]
