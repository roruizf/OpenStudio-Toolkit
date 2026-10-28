"""Visible form of the verification report: one self-contained HTML file (item 7, approved by Roberto).

Decisions (V0.3-DECISIONS.md, "Item 7: visible form of the report"): one HTML file with inline CSS and
a little inline JS, no new dependency; labels in one selectable language (English by default, Spanish,
French), OpenStudio terms always in English; a summary with a description and the ideal state of each
row; child vs. requested and the changes, grouped by family (the OpenStudio type) in collapsible groups,
all expanded and with no filter active by default, with filters on status and family; the tolerance in
the header; Space / Thermal Zone / System columns and sections by building part for the changes.

The report takes a list of pairs so that a project history (v0.4) is presentation only.
"""

from __future__ import annotations

import html
import json
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit.analysis.compare import SCOPES, LoadMapping
from openstudio_toolkit.analysis.diff import _key
from openstudio_toolkit.dump import families as dump_families
from openstudio_toolkit.extractors.generic import read_model_objects
from openstudio_toolkit.views._location import OWNED_TYPES, Location, Locator

LANGUAGES = ("en", "es", "fr")


@dataclass(frozen=True)
class ReportPair:
    """One parent -> child step of the report and the mapping its child is checked against.

    ``parent_name``, ``child_name`` and ``mapping_name`` are shown as written (e.g. the model file names
    and where the requested values come from). ``by`` and ``tolerance`` are those of
    ``compare_to_mapping``; the tolerance is absolute, in the unit of each family (W, people).
    """

    parent: Any
    child: Any
    mapping: LoadMapping
    parent_name: str = "parent"
    child_name: str = "child"
    mapping_name: str = ""
    by: str = "space"
    tolerance: float = 1e-6


# Report labels. OpenStudio terms (types, field names, Space, Thermal Zone) are never translated.
_T: dict[str, dict[str, str]] = {
    "report.title": {"en": "Verification report", "es": "Informe de verificación", "fr": "Rapport de vérification"},
    "language": {"en": "Language", "es": "Idioma", "fr": "Langue"},
    "meta.parent": {"en": "Parent model", "es": "Modelo padre", "fr": "Modèle parent"},
    "meta.child": {"en": "Child model", "es": "Modelo hijo", "fr": "Modèle enfant"},
    "meta.mapping": {
        "en": "Requested values (mapping)",
        "es": "Valores pedidos (mapping)",
        "fr": "Valeurs demandées (mapping)",
    },
    "meta.scope": {"en": "Compared by", "es": "Comparado por", "fr": "Comparé par"},
    "meta.tolerance": {"en": "Tolerance", "es": "Tolerancia", "fr": "Tolérance"},
    "tolerance.note": {
        "en": "absolute, in the unit of each family (W, people)",
        "es": "absoluta, en la unidad de cada familia (W, personas)",
        "fr": "absolue, dans l'unité de chaque famille (W, personnes)",
    },
    "meta.generated": {"en": "Generated with", "es": "Generado con", "fr": "Généré avec"},
    "h.summary": {"en": "Summary", "es": "Resumen", "fr": "Synthèse"},
    "col.what": {"en": "Table", "es": "Tabla", "fr": "Tableau"},
    "col.rows": {"en": "Rows", "es": "Filas", "fr": "Lignes"},
    "col.description": {"en": "What it is", "es": "Qué es", "fr": "Ce que c'est"},
    "col.ideal": {"en": "Ideal state", "es": "Estado ideal", "fr": "État idéal"},
    "sum.compare": {"en": "Child vs. requested", "es": "Hijo vs. pedido", "fr": "Enfant vs. demandé"},
    "sum.compare.desc": {
        "en": "Each requested value against the total OpenStudio resolves in the child model (loads on the Space "
        "and on its space type), which is what EnergyPlus simulates.",
        "es": "Cada valor pedido contra el total que OpenStudio resuelve en el modelo hijo (cargas del Space y de "
        "su space type), que es lo que simula EnergyPlus.",
        "fr": "Chaque valeur demandée face au total qu'OpenStudio résout dans le modèle enfant (charges du Space "
        "et de son space type), c'est-à-dire ce que simule EnergyPlus.",
    },
    "sum.compare.ideal": {
        "en": "Every row match.",
        "es": "Todas las filas coinciden.",
        "fr": "Toutes les lignes conformes.",
    },
    "sum.requested": {
        "en": "Requested changes (parent → child)",
        "es": "Cambios pedidos (padre → hijo)",
        "fr": "Modifications demandées (parent → enfant)",
    },
    "sum.requested.desc": {
        "en": "Changes between parent and child on the loads of a family in the mapping (or their definitions) "
        "that reach a Space or Thermal Zone of the mapping.",
        "es": "Cambios entre padre e hijo en las cargas de una familia del mapping (o sus definiciones) que "
        "llegan a un Space o Thermal Zone del mapping.",
        "fr": "Modifications entre parent et enfant sur les charges d'une famille du mapping (ou leurs "
        "définitions) qui atteignent un Space ou une Thermal Zone du mapping.",
    },
    "sum.requested.ideal": {
        "en": "No fixed ideal: they should be the changes you asked for.",
        "es": "Sin ideal fijo: deben ser los cambios que pediste.",
        "fr": "Pas d'idéal fixe : ce doivent être les modifications demandées.",
    },
    "sum.not_requested": {
        "en": "Changes not requested",
        "es": "Cambios no pedidos",
        "fr": "Modifications non demandées",
    },
    "sum.not_requested.desc": {
        "en": "Every other difference between parent and child. Counted in rows of changes, not objects in the "
        "model: one row per changed field, one per added or removed object.",
        "es": "Toda otra diferencia entre padre e hijo. Se cuentan filas de cambios, no objetos del modelo: una "
        "fila por campo cambiado, una por objeto agregado o eliminado.",
        "fr": "Toute autre différence entre parent et enfant. On compte des lignes de modifications, pas des "
        "objets du modèle : une ligne par champ modifié, une par objet ajouté ou supprimé.",
    },
    "sum.not_requested.ideal": {
        "en": "No ideal state: review them and confirm they are expected.",
        "es": "Sin estado ideal: revísalos y confirma que son esperados.",
        "fr": "Pas d'état idéal : les revoir et confirmer qu'elles sont attendues.",
    },
    "part.spaces": {"en": "Spaces and loads", "es": "Espacios y cargas", "fr": "Espaces et charges"},
    "part.envelope": {"en": "Envelope", "es": "Envolvente", "fr": "Enveloppe"},
    "part.air": {"en": "Air systems", "es": "Sistemas de aire", "fr": "Systèmes d'air"},
    "part.zone": {"en": "Zone equipment", "es": "Equipos de zona", "fr": "Équipements de zone"},
    "part.plant": {"en": "Plants", "es": "Plantas", "fr": "Boucles d'eau"},
    "part.schedules": {"en": "Schedules", "es": "Horarios", "fr": "Horaires"},
    "part.other": {
        "en": "Other and shared resources",
        "es": "Otros y recursos compartidos",
        "fr": "Autres et ressources partagées",
    },
    "col.family": {
        "en": "Family (OpenStudio type)",
        "es": "Familia (tipo de OpenStudio)",
        "fr": "Famille (type OpenStudio)",
    },
    "col.key": {"en": "Object", "es": "Objeto", "fr": "Objet"},
    "col.field": {"en": "Field", "es": "Campo", "fr": "Champ"},
    "col.requested": {"en": "Requested", "es": "Pedido", "fr": "Demandé"},
    "col.in_model": {"en": "In the model", "es": "En el modelo", "fr": "Dans le modèle"},
    "col.difference": {
        "en": "Difference (model − requested)",
        "es": "Diferencia (modelo − pedido)",
        "fr": "Écart (modèle − demandé)",
    },
    "col.status": {"en": "Status", "es": "Estado", "fr": "Statut"},
    "col.parent": {"en": "Parent", "es": "Padre", "fr": "Parent"},
    "col.child": {"en": "Child", "es": "Hijo", "fr": "Enfant"},
    "col.match_method": {"en": "Matched by", "es": "Emparejado por", "fr": "Apparié par"},
    "col.system": {"en": "System", "es": "Sistema", "fr": "Système"},
    "status.match": {"en": "match", "es": "coincide", "fr": "conforme"},
    "status.differs": {"en": "differs", "es": "difiere", "fr": "diffère"},
    "status.missing": {"en": "missing", "es": "falta", "fr": "manquant"},
    "status.changed": {"en": "changed", "es": "cambiado", "fr": "modifié"},
    "status.added": {"en": "added", "es": "agregado", "fr": "ajouté"},
    "status.removed": {"en": "removed", "es": "eliminado", "fr": "supprimé"},
    "status.not_requested": {"en": "not requested", "es": "no pedido", "fr": "non demandé"},
    "field.space": {"en": "space total", "es": "total del espacio", "fr": "total de l'espace"},
    "field.thermal_zone": {"en": "zone total", "es": "total de la zona", "fr": "total de la zone"},
    "field.added": {"en": "(object added)", "es": "(objeto agregado)", "fr": "(objet ajouté)"},
    "field.removed": {"en": "(object removed)", "es": "(objeto eliminado)", "fr": "(objet supprimé)"},
    "method.handle": {"en": "handle", "es": "handle", "fr": "handle"},
    "method.type_name": {"en": "type + name", "es": "tipo + nombre", "fr": "type + nom"},
    "shared": {"en": "shared (used by {n})", "es": "compartido (usado por {n})", "fr": "partagé (utilisé par {n})"},
    "rows": {"en": "{n} rows", "es": "{n} filas", "fr": "{n} lignes"},
    "filter.all": {"en": "all", "es": "todos", "fr": "tous"},
    "expand": {"en": "Expand all", "es": "Desplegar todo", "fr": "Tout déplier"},
    "collapse": {"en": "Collapse all", "es": "Plegar todo", "fr": "Tout replier"},
    "empty": {"en": "No rows.", "es": "Sin filas.", "fr": "Aucune ligne."},
}

_PARTS = ("spaces", "envelope", "air", "zone", "plant", "schedules", "other")
# IDD type prefixes -> building part; first match wins. Types not listed take the part of their location.
_PART_BY_TYPE: tuple[tuple[str, str], ...] = (
    ("OS:Schedule", "schedules"),
    ("OS:DefaultScheduleSet", "schedules"),
    ("OS:Space", "spaces"),  # Space, SpaceType, SpaceInfiltration:*
    ("OS:ThermalZone", "spaces"),
    ("OS:BuildingStory", "spaces"),
    ("OS:Building", "spaces"),
    ("OS:People", "spaces"),
    ("OS:Lights", "spaces"),
    ("OS:Luminaire", "spaces"),
    ("OS:ElectricEquipment", "spaces"),
    ("OS:GasEquipment", "spaces"),
    ("OS:HotWaterEquipment", "spaces"),
    ("OS:SteamEquipment", "spaces"),
    ("OS:OtherEquipment", "spaces"),
    ("OS:InternalMass", "spaces"),
    ("OS:DesignSpecification:OutdoorAir", "spaces"),
    ("OS:Surface", "envelope"),
    ("OS:SubSurface", "envelope"),
    ("OS:ShadingSurface", "envelope"),
    ("OS:InteriorPartitionSurface", "envelope"),
    ("OS:ShadingControl", "envelope"),
    ("OS:Construction", "envelope"),
    ("OS:Material", "envelope"),
    ("OS:WindowMaterial", "envelope"),
    ("OS:WindowProperty", "envelope"),
    ("OS:DefaultConstructionSet", "envelope"),
    ("OS:DefaultSurfaceConstructions", "envelope"),
    ("OS:DefaultSubSurfaceConstructions", "envelope"),
    ("OS:StandardsInformation", "envelope"),
    ("OS:Foundation", "envelope"),
    ("OS:Site:GroundTemperature:FCfactorMethod", "envelope"),
    ("OS:PlantLoop", "plant"),
    ("OS:Sizing:Plant", "plant"),
    ("OS:Boiler", "plant"),
    ("OS:Chiller", "plant"),
    ("OS:CoolingTower", "plant"),
    ("OS:Pump", "plant"),
    ("OS:WaterHeater", "plant"),
    ("OS:WaterUse", "plant"),
    ("OS:PlantEquipmentOperation", "plant"),
    ("OS:DistrictHeating", "plant"),
    ("OS:DistrictCooling", "plant"),
    ("OS:AirLoopHVAC", "air"),
    ("OS:Sizing:System", "air"),
    ("OS:Controller:OutdoorAir", "air"),
    ("OS:Controller:MechanicalVentilation", "air"),
    ("OS:ZoneHVAC", "zone"),
    ("OS:AirTerminal", "zone"),
    ("OS:Sizing:Zone", "zone"),
    ("OS:ThermostatSetpoint", "zone"),
    ("OS:ZoneControl", "zone"),
    ("OS:ZoneTerminalUnitList", "zone"),
    ("OS:AirConditioner:VariableRefrigerantFlow", "zone"),
    ("OS:Fan:ZoneExhaust", "zone"),
    ("OS:Output", "other"),
    ("OS:SimulationControl", "other"),
    ("OS:WeatherFile", "other"),
    ("OS:Site", "other"),
    ("OS:Rendering", "other"),
)


def _part(idd_type: str, location: Location) -> str:
    for prefix, part in _PART_BY_TYPE:
        if idd_type == prefix or idd_type.startswith(prefix):
            return part
    if "OS:AirLoopHVAC" in location.system_types:
        return "air"
    if "OS:PlantLoop" in location.system_types:
        return "plant"
    if location.system_types or location.zones and not location.spaces:
        return "zone"
    if location.spaces:
        return "spaces"
    return "other"


def _toolkit_version() -> str:
    try:
        return version("openstudio-toolkit")
    except PackageNotFoundError:  # pragma: no cover - source checkout without metadata
        return "unknown"


class _Html:
    """HTML pieces with labels rendered in the initial language and tagged for the language selector."""

    def __init__(self, language: str) -> None:
        self.language = language

    def t(self, key: str, n: int | None = None, tag: str = "span") -> str:
        text = _T[key][self.language]
        attrs = f' data-t="{key}"'
        if n is not None:
            text = text.replace("{n}", f"{n:,}")
            attrs += f' data-n="{n:,}"'
        return f"<{tag}{attrs}>{html.escape(text)}</{tag}>"

    @staticmethod
    def e(value: Any) -> str:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return ""
        return html.escape(str(value))

    def number(self, value: Any) -> str:
        if value is None or pd.isna(value):
            return '<td class="num"></td>'
        return f'<td class="num" data-v="{float(value)!r}">{float(value):,.2f}</td>'

    def status(self, status: str) -> str:
        return f'<td><span class="s s-{status}">{self.t(f"status.{status}")}</span></td>'

    def place(self, names: tuple[str, ...]) -> str:
        if not names:
            return "<td></td>"
        if len(names) == 1:
            return f'<td data-place="{self.e(names[0])}">{self.e(names[0])}</td>'
        items = "".join(f"<li>{self.e(n)}</li>" for n in names)
        return (
            f'<td data-place="{self.e(" | ".join(names))}"><details class="shared"><summary>'
            f"{self.t('shared', n=len(names))}</summary><ul>{items}</ul></details></td>"
        )


def _filters(h: _Html, statuses: list[str], families: list[str]) -> str:
    status_options = "".join(
        f'<option value="{s}" data-t="status.{s}">{html.escape(_T[f"status.{s}"][h.language])}</option>'
        for s in statuses
    )
    family_options = "".join(f'<option value="{h.e(f)}">{h.e(f)}</option>' for f in families)
    all_option = f'<option value="" data-t="filter.all">{html.escape(_T["filter.all"][h.language])}</option>'
    return (
        '<div class="filters">'
        f'<label>{h.t("col.status")} <select data-filter="status">{all_option}{status_options}</select></label>'
        f'<label>{h.t("col.family")} <select data-filter="family">{all_option}{family_options}</select></label>'
        f'<button type="button" data-toggle="open">{h.t("expand")}</button>'
        f'<button type="button" data-toggle="close">{h.t("collapse")}</button>'
        "</div>"
    )


def _groups(h: _Html, head: str, rows_by_family: dict[str, list[str]]) -> str:
    out = []
    for family in sorted(rows_by_family):
        rows = rows_by_family[family]
        out.append(
            f'<details open class="group" data-family="{h.e(family)}"><summary><code>{h.e(family)}</code> '
            f'<span class="count">{h.t("rows", n=len(rows))}</span></summary>'
            f'<div class="wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            "</details>"
        )
    return "".join(out)


def _block(h: _Html, inner: str, statuses: list[str], families: list[str]) -> str:
    if not families:
        return f'<p class="empty">{h.t("empty")}</p>'
    return f'<div class="block">{_filters(h, statuses, families)}{inner}</div>'


class _PairView:
    """Rows and locations of one pair, ready to render."""

    def __init__(self, pair: ReportPair) -> None:
        from openstudio_toolkit.views.verification import compare_rows, diff_rows  # verification re-exports this module

        if pair.by not in SCOPES:
            raise ValueError(f"by must be one of {', '.join(SCOPES)}, not {pair.by!r}")
        self.pair = pair
        self.compare = compare_rows(pair.child, pair.mapping, by=pair.by, tolerance=pair.tolerance)
        self.diff = diff_rows(pair.parent, pair.child, pair.mapping, by=pair.by)
        self._idd_type = {name: idd_type for name, idd_type in dump_families().items()}
        self._sides: dict[str, tuple[Locator, dict[tuple[str, str], list[str]]]] = {}
        for side, model in (("parent", pair.parent), ("child", pair.child)):
            records = read_model_objects(model)
            by_handle = {r.handle: r for r in records}
            index: dict[tuple[str, str], list[str]] = defaultdict(list)
            for r in records:
                index[(r.idd_type, _key(r, by_handle))].append(r.handle)
            self._sides[side] = (Locator(model, records), index)

    def idd_type(self, family: str) -> str:
        return self._idd_type.get(family, family)

    def locate(self, row: Any) -> tuple[Location, str]:
        """Location and building part of one diff row (removed objects: in the parent; others: the child)."""
        side = "parent" if row.status == "removed" or row.field == "(object removed)" else "child"
        locator, index = self._sides[side]
        idd_type = self.idd_type(row.family)
        handles = index.get((idd_type, row.key), [])
        found = [locator.locate(handle) for handle in handles]
        location = Location(
            spaces=tuple(sorted({n for each in found for n in each.spaces})),
            zones=tuple(sorted({n for each in found for n in each.zones})),
            systems=tuple(sorted({n for each in found for n in each.systems})),
            system_types=tuple(sorted({n for each in found for n in each.system_types})),
        )
        part_type = idd_type
        if idd_type in OWNED_TYPES and handles:
            part_type = locator.owner_type(handles[0]) or idd_type
        return location, _part(part_type, location)


def _compare_section(h: _Html, view: _PairView) -> str:
    by = view.pair.by
    scope = "Space" if by == "space" else "Thermal Zone"
    head = "".join(
        [
            f"<th>{h.t('col.family')}</th>",
            f"<th>{scope}</th>",
            f"<th>{h.t('col.field')}</th>",
            f"<th>{h.t('col.requested')}</th>",
            f"<th>{h.t('col.in_model')}</th>",
            f"<th>{h.t('col.difference')}</th>",
            f"<th>{h.t('col.status')}</th>",
        ]
    )
    rows: dict[str, list[str]] = defaultdict(list)
    for r in view.compare.itertuples(index=False):
        family = view.idd_type(r.family)
        rows[family].append(
            f'<tr data-status="{r.status}" data-family="{h.e(family)}"><td><code>{h.e(family)}</code></td>'
            f"<td>{h.e(r.key)}</td><td>{h.e(r.field)} ({h.t(f'field.{by}')})</td>"
            f"{h.number(r.requested)}{h.number(r.in_model)}{h.number(r.difference)}{h.status(r.status)}</tr>"
        )
    statuses = [s for s in ("match", "differs", "missing") if s in set(view.compare.status)]
    return _block(h, _groups(h, head, rows), statuses, sorted(rows))


def _diff_head(h: _Html) -> str:
    return "".join(
        [
            f"<th>{h.t('col.family')}</th>",
            f"<th>{h.t('col.key')}</th>",
            f"<th>{h.t('col.field')}</th>",
            f"<th>{h.t('col.parent')}</th>",
            f"<th>{h.t('col.child')}</th>",
            f"<th>{h.t('col.status')}</th>",
            f"<th>{h.t('col.match_method')}</th>",
            "<th>Space</th>",
            "<th>Thermal Zone</th>",
            f"<th>{h.t('col.system')}</th>",
        ]
    )


def _diff_row(h: _Html, family: str, r: Any, location: Location) -> str:
    field = {"(object added)": h.t("field.added"), "(object removed)": h.t("field.removed")}.get(r.field, h.e(r.field))
    method = h.t(f"method.{r.match_method}") if isinstance(r.match_method, str) else ""
    return (
        f'<tr data-status="{r.status}" data-family="{h.e(family)}"><td><code>{h.e(family)}</code></td>'
        f"<td>{h.e(r.key)}</td><td>{field}</td><td>{h.e(r.parent)}</td><td>{h.e(r.child)}</td>"
        f"{h.status(r.status)}<td>{method}</td>"
        f"{h.place(location.spaces)}{h.place(location.zones)}{h.place(location.systems)}</tr>"
    )


def _diff_sections(h: _Html, view: _PairView) -> tuple[str, str, dict[str, int]]:
    head = _diff_head(h)
    requested: dict[str, list[str]] = defaultdict(list)
    by_part: dict[str, dict[str, list[str]]] = {part: defaultdict(list) for part in _PARTS}
    for r in view.diff.itertuples(index=False):
        family = view.idd_type(r.family)
        location, part = view.locate(r)
        row = _diff_row(h, family, r, location)
        if r.status == "not_requested":
            by_part[part][family].append(row)
        else:
            requested[family].append(row)
    statuses = [s for s in ("changed", "added", "removed") if s in set(view.diff.status)]
    requested_html = _block(h, _groups(h, head, requested), statuses, sorted(requested))
    parts_html, counts = [], {}
    families = sorted({f for part in by_part.values() for f in part})
    for part in _PARTS:
        groups = by_part[part]
        counts[part] = sum(len(rows) for rows in groups.values())
        if groups:
            parts_html.append(
                f'<section class="part"><h4>{h.t(f"part.{part}")} '
                f'<span class="count">{h.t("rows", n=counts[part])}</span></h4>{_groups(h, head, groups)}</section>'
            )
    not_requested = _block(h, "".join(parts_html), ["not_requested"] if families else [], families)
    return requested_html, not_requested, counts


def _counts(h: _Html, statuses: pd.Series, order: Sequence[str]) -> str:
    present = statuses.value_counts()
    items = [f'<span class="s s-{s}">{int(present[s]):,} {h.t(f"status.{s}")}</span>' for s in order if s in present]
    return " ".join(items) or "0"


def _pair_section(h: _Html, view: _PairView, number: int) -> str:
    pair = view.pair
    families = ", ".join(f"{view.idd_type(f)} ({len(v)})" for f, v in pair.mapping.items())
    meta = [
        (h.t("meta.parent"), h.e(pair.parent_name)),
        (h.t("meta.child"), h.e(pair.child_name)),
        (h.t("meta.mapping"), f"{h.e(pair.mapping_name)}<br><code>{h.e(families)}</code>"),
        (h.t("meta.scope"), "Space" if pair.by == "space" else "Thermal Zone"),
        (h.t("meta.tolerance"), f"<b>{pair.tolerance:g}</b> ({h.t('tolerance.note')})"),
    ]
    requested_html, not_requested_html, _ = _diff_sections(h, view)
    diff_status = view.diff.status
    summary = [
        ("sum.compare", _counts(h, view.compare.status, ("match", "differs", "missing"))),
        ("sum.requested", _counts(h, diff_status[diff_status != "not_requested"], ("changed", "added", "removed"))),
        ("sum.not_requested", _counts(h, diff_status[diff_status == "not_requested"], ("not_requested",))),
    ]
    summary_rows = "".join(
        f'<tr><td><a href="#p{number}-{key.split(".")[1]}">{h.t(key)}</a></td><td>{counts}</td>'
        f"<td>{h.t(f'{key}.desc')}</td><td>{h.t(f'{key}.ideal')}</td></tr>"
        for key, counts in summary
    )
    return (
        f'<section class="pair" id="p{number}"><h2>{h.e(pair.parent_name)} → {h.e(pair.child_name)}</h2>'
        '<table class="meta">' + "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in meta) + "</table>"
        f'<h3>{h.t("h.summary")}</h3><div class="wrap"><table class="summary"><thead><tr>'
        f"<th>{h.t('col.what')}</th><th>{h.t('col.rows')}</th><th>{h.t('col.description')}</th>"
        f"<th>{h.t('col.ideal')}</th></tr></thead><tbody>{summary_rows}</tbody></table></div>"
        f'<h3 id="p{number}-compare">{h.t("sum.compare")}</h3>{_compare_section(h, view)}'
        f'<h3 id="p{number}-requested">{h.t("sum.requested")}</h3>{requested_html}'
        f'<h3 id="p{number}-not_requested">{h.t("sum.not_requested")}</h3>'
        f'<p class="note">{h.t("sum.not_requested.desc")}</p>{not_requested_html}'
        "</section>"
    )


_CSS = """
:root{--bg:#fff;--fg:#1d1d1f;--mut:#5f6368;--line:#dadce0;--head:#f3f4f6;--card:#fafafa;
--match:#d7f0d4;--differs:#fde2cf;--missing:#f8c4b4;--changed:#fff1c2;--added:#d6e8fa;--removed:#e6e6e6;
--not_requested:#ececf3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#151618;--fg:#e8e8ea;--mut:#a0a4aa;
--line:#34363a;--head:#1f2124;--card:#1b1c1f;--match:#244b2a;--differs:#5a3a22;--missing:#6a2f25;
--changed:#5a4d1c;--added:#1f3f5f;--removed:#3a3a3a;--not_requested:#30303d}}
:root[data-theme="dark"]{--bg:#151618;--fg:#e8e8ea;--mut:#a0a4aa;--line:#34363a;--head:#1f2124;--card:#1b1c1f;
--match:#244b2a;--differs:#5a3a22;--missing:#6a2f25;--changed:#5a4d1c;--added:#1f3f5f;--removed:#3a3a3a;
--not_requested:#30303d}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;
margin:0 auto;max-width:1400px;padding:16px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between}
h1{font-size:22px;margin:4px 0}h2{font-size:18px;margin:28px 0 8px;border-top:2px solid var(--line);padding-top:16px}
h3{font-size:16px;margin:24px 0 6px}h4{font-size:15px;margin:18px 0 4px}
a{color:inherit}code{font-size:12.5px}
table{border-collapse:collapse;width:100%;font-size:13px;margin:6px 0}
th,td{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}
thead th{background:var(--head);position:sticky;top:0}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.meta{width:auto}table.meta th{background:none;color:var(--mut);font-weight:normal;padding-right:16px}
.wrap{overflow-x:auto}
.s{border-radius:4px;padding:1px 6px;white-space:nowrap;display:inline-block}
.s-match{background:var(--match)}.s-differs{background:var(--differs)}.s-missing{background:var(--missing)}
.s-changed{background:var(--changed)}.s-added{background:var(--added)}.s-removed{background:var(--removed)}
.s-not_requested{background:var(--not_requested)}
details.group{border:1px solid var(--line);border-radius:6px;margin:6px 0;background:var(--card)}
details.group>summary{cursor:pointer;padding:6px 10px}
details.group>.wrap{padding:0 8px 6px}
details.shared summary{cursor:pointer;color:var(--mut)}details.shared ul{margin:4px 0;padding-left:18px}
.count{color:var(--mut);font-weight:normal;font-size:12.5px}
.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:6px 0;position:sticky;top:0;
background:var(--bg);padding:6px 0;z-index:2}
select,button{font:inherit;color:var(--fg);background:var(--card);border:1px solid var(--line);border-radius:4px;
padding:2px 6px}
.note,.empty,footer{color:var(--mut)}
.hidden{display:none}
"""

_JS = """
const T = __T__;
function setLang(lang){
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-t]').forEach(e => {
    let s = T[e.dataset.t][lang];
    if (e.dataset.n) s = s.replace('{n}', e.dataset.n);
    e.textContent = s;
  });
}
function applyFilters(block){
  const want = {};
  block.querySelectorAll('select[data-filter]').forEach(s => want[s.dataset.filter] = s.value);
  block.querySelectorAll('tbody tr').forEach(tr => {
    const ok = (!want.status || tr.dataset.status === want.status)
      && (!want.family || tr.dataset.family === want.family);
    tr.classList.toggle('hidden', !ok);
  });
  block.querySelectorAll('details.group').forEach(g => {
    g.classList.toggle('hidden', !g.querySelector('tbody tr:not(.hidden)'));
  });
  block.querySelectorAll('section.part').forEach(p => {
    p.classList.toggle('hidden', !p.querySelector('details.group:not(.hidden)'));
  });
}
document.addEventListener('DOMContentLoaded', () => {
  const sel = document.getElementById('lang');
  sel.addEventListener('change', () => setLang(sel.value));
  document.querySelectorAll('.block').forEach(block => {
    block.querySelectorAll('select[data-filter]').forEach(s => s.addEventListener('change', () => applyFilters(block)));
    block.querySelectorAll('button[data-toggle]').forEach(b => b.addEventListener('click', () => {
      block.querySelectorAll('details.group').forEach(g => g.open = b.dataset.toggle === 'open');
    }));
  });
});
"""


def _render_report(pairs: Sequence[ReportPair], title: str | None = None, language: str = "en") -> str:
    """HTML of the report for ``pairs`` (see ``write_report``)."""
    if language not in LANGUAGES:
        raise ValueError(f"language must be one of {', '.join(LANGUAGES)}, not {language!r}")
    if not pairs:
        raise ValueError("pairs is empty: the report needs at least one parent -> child pair")
    h = _Html(language)
    sections = "".join(_pair_section(h, _PairView(pair), i) for i, pair in enumerate(pairs, 1))
    heading = h.e(title) if title else h.t("report.title")
    page_title = h.e(title) if title else html.escape(_T["report.title"][language])
    options = "".join(
        f'<option value="{code}"{" selected" if code == language else ""}>{name}</option>'
        for code, name in (("en", "English"), ("es", "Español"), ("fr", "Français"))
    )
    tool = f"openstudio-toolkit {_toolkit_version()}, OpenStudio {openstudio.openStudioVersion()}"
    script = _JS.replace("__T__", json.dumps(_T, ensure_ascii=False))
    return (
        f'<!doctype html><html lang="{language}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{page_title}</title><style>{_CSS}</style></head><body>"
        f'<header><h1>{heading}</h1><label>{h.t("language")} <select id="lang">{options}</select></label></header>'
        f"{sections}<footer><p>{h.t('meta.generated')} {html.escape(tool)}</p></footer>"
        f"<script>{script}</script></body></html>"
    )


def write_report(
    pairs: Sequence[ReportPair],
    path: str | Path,
    title: str | None = None,
    language: str = "en",
) -> Path:
    """Write the verification report of ``pairs`` as one self-contained HTML file and return its path.

    For each pair: the child compared with the mapping (``compare_rows``), the requested changes and the
    changes not requested (``diff_rows``), with the Space / Thermal Zone / System of every change and the
    changes not requested split by building part. ``language`` (``en``, ``es``, ``fr``) is the initial
    language of the labels; the reader can switch it in the page. Neither model is modified.
    """
    out = Path(path)
    out.write_text(_render_report(pairs, title=title, language=language), encoding="utf-8")
    return out
