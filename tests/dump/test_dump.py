"""Item 3: dumps of the curated families, as records and as a view."""

from __future__ import annotations

import importlib
import inspect
import pkgutil
import re
import subprocess
import sys
from pathlib import Path

import openstudio
import pytest

import openstudio_toolkit.osm_objects as osm_objects
from openstudio_toolkit import dump
from openstudio_toolkit.extractors.generic import read_model_objects

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = {
    "small_office": ROOT / "tests" / "resources" / "small_office.osm",
    "office_hub": ROOT / "examples" / "R2F-Office-Hub.osm",
    "extra_families": ROOT / "tests" / "resources" / "extra_families.osm",
}
ORPHAN_FIXTURE = ROOT / "tests" / "resources" / "orphans_minimal.osm"

# Curated readers that are not one IDD type (approved by Roberto, 2026-10-27).
NOT_A_FAMILY = {
    "get_all_opaque_material_objects_as_dataframe",  # Material + Material:NoMass
    "get_all_default_construction_set_component_as_dataframe",  # resolved view of DefaultConstructionSet
    "get_all_default_schedule_set_components_as_dataframe",  # long table, no handles
}


# IDD types whose OpenStudio class name is not the type without "OS:" and colons.
SDK_CLASS = {
    "OS:Material:NoMass": "MasslessOpaqueMaterial",
    "OS:Material": "StandardOpaqueMaterial",
    "OS:WindowMaterial:SimpleGlazingSystem": "SimpleGlazing",
}


def _snake(idd_type: str) -> str:
    name = idd_type.removeprefix("OS:").replace(":", "_")
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", name).lower()


@pytest.fixture(scope="module")
def models() -> dict:
    translator = openstudio.osversion.VersionTranslator()
    return {label: translator.loadModel(str(path)).get() for label, path in FIXTURES.items()}


def test_family_names_follow_their_idd_type() -> None:
    assert len(dump.families()) == 73  # 65 + the 8 of item 3b
    for name, idd_type in dump.families().items():
        assert name == _snake(idd_type)
    assert len(set(dump.families().values())) == len(dump.families())


def test_every_curated_reader_is_a_family_or_excluded() -> None:
    readers = set()
    for info in pkgutil.iter_modules(osm_objects.__path__):
        module = importlib.import_module(f"{osm_objects.__name__}.{info.name}")
        readers |= {
            name
            for name, fn in inspect.getmembers(module, inspect.isfunction)
            if fn.__module__ == module.__name__ and re.fullmatch(r"get_all_\w+_as_dataframe", name)
        }
    in_dump = {reader.__name__ for _, reader in dump._FAMILIES.values()}

    assert readers == in_dump | NOT_A_FAMILY
    assert not in_dump & NOT_A_FAMILY


def test_view_rows_are_objects_of_their_family(models) -> None:
    wrong = []
    for label, model in models.items():
        for name, df in dump.dump_view(model).items():
            for handle in df["Handle"]:
                obj = model.getObject(openstudio.toUUID(str(handle)))
                idd_type = obj.get().iddObject().name() if obj.is_initialized() else None
                if idd_type != dump.families()[name]:
                    wrong.append((label, name, handle, idd_type))
    assert not wrong


def _hard_size(model) -> int:
    """Give every autosized field of every family object a fixed value (in memory); return how many."""
    sized = 0
    for idd_type in dump.families().values():
        cast = "to_" + SDK_CLASS.get(idd_type, idd_type.removeprefix("OS:").replace(":", ""))
        for workspace_object in model.getObjectsByType(openstudio.IddObjectType(idd_type)):
            obj = getattr(workspace_object, cast)().get()
            for name in dir(obj):
                match = re.fullmatch(r"is(\w+)Autosized", name)
                setter = f"set{match.group(1)}" if match else ""
                if match and hasattr(obj, setter) and getattr(obj, name)():
                    sized += bool(getattr(obj, setter)(0.5))
    return sized


@pytest.mark.parametrize("hard_sized", [False, True], ids=["as_is", "hard_sized"])
def test_view_cells_are_plain_values(hard_sized: bool) -> None:
    """No cell holds an OpenStudio object (e.g. an OptionalDouble that was never unwrapped).

    Hard-sizing reaches the branches that read the value only when the field is not autosized.
    """
    translator = openstudio.osversion.VersionTranslator()
    leaks = set()
    for label, path in FIXTURES.items():
        model = translator.loadModel(str(path)).get()
        if hard_sized:
            assert _hard_size(model) > 0, label
        for name, df in dump.dump_view(model).items():
            for column in df.columns:
                leaks |= {(name, column) for v in df[column] if type(v).__module__.startswith("openstudio")}
    assert not leaks, sorted(leaks)


def test_records_are_the_generic_reader_split_by_family(models) -> None:
    for model in models.values():
        records = read_model_objects(model)
        dumped = dump.dump_records(model)

        assert list(dumped) == list(dump.families())
        for name, idd_type in dump.families().items():
            assert dumped[name] == [r for r in records if r.idd_type == idd_type]


def test_view_is_the_curated_reader_cell_by_cell(models) -> None:
    for model in models.values():
        dumped = dump.dump_view(model)

        assert list(dumped) == list(dump.families())
        for name, (_, reader) in dump._FAMILIES.items():
            assert dumped[name].equals(reader(model)), name


def test_views_and_records_agree_on_handles(models) -> None:
    for model in models.values():
        records, views = dump.dump_records(model), dump.dump_view(model)
        for name in dump.families():
            assert sorted(views[name]["Handle"]) == [r.handle for r in records[name]], name


def test_empty_model_gives_every_family() -> None:
    model = openstudio.model.Model()
    records, views = dump.dump_records(model), dump.dump_view(model)

    assert list(records) == list(views) == list(dump.families())
    assert all(r == [] for r in records.values())
    assert all(df.empty and len(df.columns) > 0 for df in views.values())


def test_selection_keeps_order_and_rejects_unknown_names(models) -> None:
    model = models["office_hub"]

    assert list(dump.dump_view(model, ["space", "lights", "space"])) == ["space", "lights"]
    assert list(dump.dump_records(model, ("lights",))) == ["lights"]
    with pytest.raises(ValueError, match="lightz"):
        dump.dump_records(model, ["lights", "lightz"])
    with pytest.raises(ValueError, match="lightz"):
        dump.dump_view(model, ["lightz"])


def test_record_keeps_stored_value_and_view_resolves_it(models) -> None:
    """R2F-Office-Hub: the schedule of '0.06-WC Lights' is empty in the object, inherited from its set."""
    model = models["office_hub"]
    record = next(r for r in dump.dump_records(model, ["lights"])["lights"] if r.name == "0.06-WC Lights")
    view = dump.dump_view(model, ["lights"])["lights"].set_index("Handle").loc[record.handle]
    schedule = next(f for f in record.fields if f.name == "Schedule Name")

    assert schedule.value == "" and schedule.target is None
    assert view["Schedule Name"] == "Office Building Lighting Schedule"


def test_dumps_survive_orphan_relations() -> None:
    code = (
        "import sys, openstudio\n"
        "from openstudio_toolkit import dump\n"
        "m = openstudio.osversion.VersionTranslator().loadModel(sys.argv[1]).get()\n"
        "print(sum(map(len, dump.dump_records(m).values())), sum(map(len, dump.dump_view(m).values())))\n"
    )
    proc = subprocess.run(
        [sys.executable, "-I", "-c", code, str(ORPHAN_FIXTURE)], capture_output=True, text=True, timeout=300
    )

    assert proc.returncode == 0, f"return code {proc.returncode}: {proc.stderr[-2000:]}"
    records, rows = map(int, proc.stdout.split()[-2:])
    assert records == rows > 0
