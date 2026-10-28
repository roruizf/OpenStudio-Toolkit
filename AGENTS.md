# AGENTS.md

Read this first, whether you work **on** the toolkit or **with** it in a project. It is the single entry point
for agents; `CLAUDE.md` only imports it.

openstudio-toolkit reads, compares and changes OpenStudio models (`.osm`) and reads simulation results
(`eplusout.sql`), so that the work of a modeling agent can be checked against what was requested and against
the previous model version, without trusting the agent's own account of what it did.

## Where things are (one source per topic)

| Topic | File | Rule |
|---|---|---|
| What is guaranteed (public API, artifact columns, CLI commands, families, runtime) | `docs/contracts/v0.3.toml` | Enforced by `tests/contract/`. Only what is `implemented` there is stable. |
| How to verify a new model version | `docs/VERIFICATION-GUIDE.md` | Every new model version, before `MODEL-REGISTER.md`. |
| Bugs, limitations, proposals, improvements | `docs/BACKLOG.md` | The only list. Add entries there, nowhere else. |
| Why things are the way they are (measurements, Roberto's decisions) | `docs/architecture/V0.3-DECISIONS.md` | History. Scripts in `docs/architecture/v0.3-evidence/`. Not a to-do list. |
| What the package does, for people | `README.md` | Short; points here. |

If two of these disagree, the contract and its tests win, then this file. Report the disagreement as a
backlog entry.

## Using the toolkit in a project

**Install it pinned to a release tag**, never to a branch, so a new toolkit version never changes a running
project silently:

```bash
uv add "openstudio-toolkit @ git+https://github.com/roruizf/OpenStudio-Toolkit@v0.3.0"
# or: pip install "openstudio-toolkit @ git+https://github.com/roruizf/OpenStudio-Toolkit@v0.3.0"
```

Python 3.11 to 3.13 (3.14 crashes the OpenStudio binding). It brings `openstudio==3.11.0`.

**Use only the stable surface**, the `[[api]]` entries and `[cli]` of the contract:

| Need | Command line | Python |
|---|---|---|
| Curated tables of a model, one per family | `openstudio-toolkit dump model.osm --out dump/` | `dump.dump_view(model, families)` |
| Write a child model with per-Space loads from a request | `openstudio-toolkit apply parent.osm child.osm --mapping m.json [--existing update]` | `transforms.apply.apply_mapping(...)` |
| Check a model against the request | `openstudio-toolkit compare child.osm --mapping m.json` | `views.verification.compare_rows(model, mapping)` |
| Parent → child changes, the request check and the HTML report | `openstudio-toolkit diff parent.osm child.osm --mapping m.json --report r.html` | `views.verification.diff_rows(...)`, `write_report([ReportPair(...)], path)` |
| Sizes, unmet hours and end uses from a simulation | `openstudio-toolkit results eplusout.sql end_uses --units GJ=kWh` | `results.zone_sizes / system_sizes / unmet_hours / end_uses` |

Python modules are under `openstudio_toolkit.` Exit codes of the command line: `0` done and matches, `1` does
not match or `apply` refused (reasons printed), `2` usage error. Script on the exit code, not on the text.

**Rules in a project:**

- **Verify every model version** with `diff ... --mapping ... --report` (`docs/VERIFICATION-GUIDE.md`). Register
  the version only with exit code `0` and every not-requested change understood. A change made by an agent is
  checked by the toolkit, not by the agent's own list of changes.
- **Never modify an input model.** Work on copies; real models live outside git. `apply` refuses to write over
  its input.
- **Build your workflow on the library; do not copy its logic.** A project script calls the toolkit. If the
  toolkit lacks something or is wrong, do not work around it in the project: add a `docs/BACKLOG.md` entry
  (with the model, version and numbers) and tell Roberto.
- The project's own `AGENTS.md` or `CLAUDE.md` should point to this file and say which toolkit tag it uses.

## Working on the toolkit

**Setup and checks:**

```bash
uv sync                                   # the locked environment, OpenStudio 3.11.0 wheel
uv run pytest -q                          # full suite, about 2.5 min: run it in the background
uv run ruff check <the paths listed in .github/workflows/ci.yml>
uv run mypy src/openstudio_toolkit/cli.py  # and the other contract modules
```

CI (`.github/workflows/ci.yml`) runs the same on Python 3.11, 3.12 and 3.13 on every push.

**Rules (Roberto's, permanent):**

- **Roberto decides scope.** A version's scope is its contract; nothing enters without his explicit approval.
  If something approved does not work, stop and report it with evidence; do not redesign it.
- **Before building each item, propose its form with a real example from his models and wait for "ok".**
- Talk to Roberto **in Spanish**, with examples from his models, no jargon, and **one recommendation per
  decision**. Mark what is fact (measured) and what is assumption. Repo files are in English.
- **No commit or push unless Roberto asks.** Stage explicit paths, never `git add -A`. Never `git stash`.
- Real models stay outside git (locations in the project folders `~/projects/r2f-simulation-os/projects/` and
  the R2F Drive). Copy them to a scratch folder; never modify originals.
- Verify numbers as numbers, never through their text: `str()` of an OpenStudio Optional prints a number and
  hides an unwrapped value. Unwrap Optionals only with `openstudio_toolkit._sdk.opt`.
- No MCP, containers, new Ruby measures or notebooks in this repo (notebooks live in their own repo and pin a
  tag of this one).
- At the end of a session: record the wall-clock hours and the closing `date`, update the R2F-TOOL-001 row in
  `~/projects/robert-os/ops/initiatives.md`, and report what was done and what was not.

**Code patterns** (the contract tests enforce most of them):

- A curated reader is `get_all_<family>_objects_as_dataframe(model)`: every IDD field in IDD order, units in
  the column name (`{W}`, `{m3/s}`), `'Autosize'` for autosized fields, relations by name through
  `_sdk.optional_name` / `related_name`, port fields through `_sdk.connection_node_name`. It returns its columns
  when the family is empty and does not die on orphan relations.
- Read and compare modules (`extractors`, `validators`, `dump`, `analysis`, `views`) never import
  `transforms`; only `transforms.apply` creates or changes objects, and nothing deletes them.
- Measure before you decide: a probe script in a scratch folder, then the evidence script kept under
  `docs/architecture/v0.3-evidence/` (or the version's folder) when it backs a decision.

**Modules outside the contract** (`tasks/`, `workflows/`, `utils/`, `resources/measures/`) predate v0.3 and
are not guaranteed. Do not build on them; see TK-008.

## Releases

Versions are `vMAJOR.MINOR.PATCH`, tagged on `main`; `pyproject.toml` `version` matches the tag.

- **Patch (v0.3.1...)**: an accepted backlog **bug** that gives a wrong number or crashes. Branch
  `fix/TK-NNN` from `main`, test that reproduces it, fix, full suite, then (when Roberto asks) merge, tag, push.
  Move the entry to Closed with the version.
- **Minor (v0.4.0...)**: triggered by the backlog (5 or more accepted entries, or 4 weeks with at least one).
  1. Read `docs/BACKLOG.md` and `docs/architecture/V0.3-DECISIONS.md`. Nothing else is needed.
  2. Propose to Roberto, in Spanish: which entries enter, which wait, effort, order, and one recommendation
     each.
  3. With his approval: branch `vX.Y`, contract `docs/contracts/vX.Y.toml` (items as `planned`; the contract
     tests turn each one into a failing test until it is `implemented`), decisions file
     `docs/architecture/VX.Y-DECISIONS.md`.
  4. Item by item: propose the form with a real example, "ok", build, verify on real models, mark it
     `implemented`, mark the backlog entry `done (vX.Y.0)`.
  5. Close: full suite, `pyproject.toml` version, commit, push, CI green, merge to `main`, tag, all when Roberto
     asks.

## Runtime

| Component | Version | Fact |
|---|---|---|
| Python | 3.11, 3.12, 3.13 | 3.14.1 imports the binding but segfaults (exit 139) on `openstudio.model.Model()` or `VersionTranslator()` (measured 2026-06-20). |
| OpenStudio Python wheel | 3.11.0 | 3.10.0 had a ForwardTranslator bug: an `IdealLoadsAirSystem`'s own outdoor-air object was ignored for the zone's (NREL/OpenStudio PR #5505, fixed in 3.11.0). |
| EnergyPlus reported by the binding | 25.2.0 | |

`openstudio_toolkit.runtime.assert_reference_runtime()` fails if Python, OpenStudio or EnergyPlus do not match.
The PyPI wheel has no usable OpenStudio CLI, so this package does not run simulations or measures; it reads
the `eplusout.sql` of a simulation run elsewhere.
