# Backlog

The **only** place for bugs, limitations, proposals and improvements of openstudio-toolkit. Whoever finds
something, a person or an agent, in this repo or while using the toolkit in a project, adds an entry here.
There is no other list: not in chat, not in a project's notes, not in `V0.3-DECISIONS.md`.

## How to add an entry

1. Take the next free number (`TK-NNN`, never reused). Add the entry at the end of **Open**.
2. Fill every field. Evidence means something another agent can rerun: a command, a script, a model name and
   version, the numbers you got. If something is not measured, write "Assumption:" before it.
3. Set `Status: new`. Only Roberto moves an entry to `accepted` or `rejected`.
4. Tell Roberto in your report which entries you added. Commit only when Roberto asks. If you are working in
   a project and cannot reach this repo, put the full entry text in your report instead. Do not fix the
   toolkit from inside a project, and do not copy its logic into a project script to work around it.

```markdown
### TK-NNN · Short title
- Type: bug | limitation | proposal | improvement
- Found: YYYY-MM-DD, by whom, where (project, model and version, toolkit version)
- Evidence: command or script, and what it returned
- Impact: what goes wrong, or what it would enable
- Status: new
- Decision: (Roberto)
```

- **bug:** the toolkit gives a wrong value, crashes or breaks its contract.
- **limitation:** it works as designed, but a case is not covered or not verified.
- **proposal:** something new (a function, a family, a report).
- **improvement:** something existing that could be better (speed, clarity, ergonomics).

## Status and what triggers a release

`new` → `accepted` or `rejected` (Roberto, with the reason) → `planned (vX.Y.Z)` → `done (vX.Y.Z, commit)`.
A done or rejected entry moves to **Closed** and stays there.

- **Patch release (v0.3.1, v0.3.2...), immediately:** an accepted **bug** that gives a wrong number or
  crashes. It does not wait for other entries. Short branch from `main`, fix and test, merge, tag.
- **Minor release (v0.4.0...), planned:** when there are **5 or more accepted entries**, or **4 weeks** have
  passed since the last release with at least one accepted entry, whichever comes first. The planning agent
  reads this file and `docs/architecture/V0.3-DECISIONS.md` only, proposes to Roberto which entries enter and
  the contract (`docs/contracts/vX.Y.toml`), and starts once Roberto approves. Process in `AGENTS.md`.

## Open

### TK-001 · Project history in one report
- Type: proposal
- Found: 2026-10-27, Roberto with Claude, v0.3 item 7 review
- Evidence: `docs/architecture/v0.3-evidence/history_chain.py`, Office Hub actual-001 → 017 (15 consecutive
  pairs): 1 to 82 diff rows per pair, 306 in total, 10 s including loading the 16 models. The 5,566 rows of
  actual → reference are a jump between series, not a step.
- Impact: one report from the first model to the current one (30-50 versions per project). Open: what was
  requested at each step (not stored per version today; candidate: the version notes of `MODEL-REGISTER.md`
  as the step title), and branches (actual → reference, FPM4 v9b) shown as branches. `write_report` already
  takes a list of pairs.
- Status: accepted, for v0.4
- Decision: Roberto 2026-10-27, "si v0.4 es lo que crees mejor, ahí"

### TK-002 · Report of the current model by building part, in Roberto's Excel style
- Type: proposal
- Found: 2026-10-27, Roberto with Claude, v0.3 item 7 review
- Evidence: reference workbooks (Drive, read-only): `Internal Projects/R2F-Office-Hub/R2F-Office-Hub-Base-Model.xlsx`
  (sheets Rooms, Space Types, Spaces, Occupancy, Lighting, ElectricEquipment, VentilationRates,
  OSGainsBySpaces, Envelope, Schedules, Thermal Zone) and
  `Dosta Tec/CCB43&FPM4/Working Files/LEED v4/FPM4-Inputs-Model-v4.xlsx` (adds UTAN, Elevators, SHW, ZoneHVAC,
  HVAC). E.g. `Spaces`: Space, Story, SpaceType, Thermal Zone, Floor Area, Ceiling Height, Volume, people,
  lighting W, equipment W, outdoor air. The OpenStudio Results sections Space Type Summary, Air Loops Detail,
  Plant Loops Detail and Zone Equipment Detail read only the model (read in `os_lib_reporting.rb`).
- Impact: tables around base objects (Space, Thermal Zone, air loop, zone HVAC, plant, sizing) with auxiliary
  columns for filtering and summing. Start with a short study (base objects, columns, source of each value) for
  Roberto's approval; the location resolver of the item 7 report is the same piece.
- Status: accepted, for v0.4
- Decision: Roberto 2026-10-27, "si v0.4 es lo que crees mejor, ahí"

### TK-003 · HVAC as a requested change
- Type: proposal
- Found: 2026-10-27, Roberto with Claude
- Evidence: a mapping holds only `people`, `lights` and `electric_equipment`; a change such as
  "ideal loads → DOAS + VRF" shows only as changes not requested (located by zone and system).
- Impact: a mapping family for HVAC (e.g. zone X served by an air loop and a VRF terminal), with tables per
  Thermal Zone and per air loop. Goes with TK-002.
- Status: accepted, for v0.4
- Decision: Roberto 2026-10-27, "ok"

### TK-004 · Unshare space loads
- Type: proposal
- Found: 2026-10-28, Claude, v0.3 item 4 (`docs/architecture/v0.3-evidence/unshare_probe.py`)
- Evidence: loads coming from a space type: reference-011 7, FPM4 v10 35, Tribe 49. `apply --existing update`
  refuses them so it never doubles a load (reference-011 would go from 7,784.85 W to 15,570.39 W).
  `Space.hardApplySpaceType(False)` keeps the totals but clones the space types (7 → 43), writes the schedules
  onto People and keeps definitions shared (236 diff rows). No shared definitions in the 4 models;
  `SpaceLoadInstance.makeUnique()` works.
- Impact: a transform that gives every Space its own copy of the loads it receives from its space type, each
  with its own definition and the Space totals unchanged, so `apply --existing update` works on models such
  as reference-011 or FPM4.
- Status: accepted, for v0.4
- Decision: Roberto 2026-10-28, accepted with the other recommendations

### TK-005 · Empty text cells read `nan` in the DataFrame readers (pandas 3)
- Type: limitation
- Found: 2026-10-28, Claude, v0.3 item 3b
- Evidence: with pandas 3, a curated reader (`get_all_*_as_dataframe`) returns `nan` for an empty text field
  instead of an empty value. Fact (code read): `diff`, `compare` and the report do not use these readers
  (`analysis/diff.py` reads through `extractors.generic.read_model_objects`), so they are not affected; a CSV
  written by `dump` shows the cell as empty.
- Impact: only Python users of the DataFrames see `nan` where the model has nothing.
- Status: new
- Decision:

### TK-006 · VRF `WaterCooled` condenser not verified on a real model
- Type: limitation
- Found: 2026-10-28, Claude, v0.3 item 3b
- Evidence: `_vrf_condenser_type` equals OpenStudio on all 18 VRFs of the corpus, all `AirCooled`. The
  `WaterCooled` branch (condenser inlet node connected) has no real model.
- Impact: none known. Close it when a project has a water-cooled VRF: run
  `docs/architecture/v0.3-evidence/families_3b_check.py` on it.
- Status: new
- Decision:

### TK-007 · SQL results in IP units not verified on a real file
- Type: limitation
- Found: 2026-10-28, Claude, v0.3 item 8
- Evidence: `results` reads the units of the tabular reports from the SQL `Units` column and is tested with
  a synthetic kBtu file. Assumption: `ZoneSizes` and `SystemSizes` are always SI; no real IP SQL was checked.
- Impact: none known in R2F projects (all SI). Close it with the first real IP `eplusout.sql`.
- Status: new
- Decision:

### TK-008 · Modules outside the contract
- Type: improvement
- Found: 2026-10-28, Claude, documentation cleanup before v0.3.0
- Evidence: `tasks/`, `workflows/`, `utils/` and the Ruby measures in `resources/measures/` are in the package
  but not in `docs/contracts/v0.3.toml`; nothing tests them as a contract. The example notebooks that used
  them were removed in v0.3.0.
- Impact: an agent may build on them believing they are stable. Decide per module: enter the contract with
  tests, or remove.
- Status: new
- Decision:

### TK-009 · No LICENSE file
- Type: improvement
- Found: 2026-10-28, Claude, documentation cleanup before v0.3.0
- Evidence: `pyproject.toml` declares MIT; the repo has no `LICENSE` file.
- Impact: the license is not formally attached to a public repo.
- Status: new
- Decision:

## Closed

### TK-010 · Autosized fields read in two spellings
- Type: bug
- Found: 2026-10-28, Claude, v0.3 item 3b
- Evidence: 38 readers wrote `'autosize'` and 44 wrote `'Autosize'` (modules `hvac_sizing`, `hvac_components`,
  `controllers`, `hvac_zone`).
- Status: done (v0.3.0). Every reader writes `'Autosize'`, the IDD key; pinned by
  `tests/osm_objects/test_dataframe_functions.py::test_autosized_fields_read_autosize_in_one_spelling`.
