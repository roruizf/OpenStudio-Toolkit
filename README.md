# OpenStudio Toolkit

Read, compare and change OpenStudio models (`.osm`), and read simulation results (`eplusout.sql`), from Python
or the command line. Built to check the work of a modeling agent: compare the new model with what was
requested and with the previous version, and read every change in one HTML report.

**Built by** [Roberto Ruiz](https://github.com/roruizf). Agents: read [`AGENTS.md`](AGENTS.md) first.

## Install

Python 3.11 to 3.13. Install a release tag:

```bash
uv add "openstudio-toolkit @ git+https://github.com/roruizf/OpenStudio-Toolkit@v0.3.0"
# or: pip install "openstudio-toolkit @ git+https://github.com/roruizf/OpenStudio-Toolkit@v0.3.0"
```

It brings the OpenStudio 3.11.0 Python wheel (EnergyPlus 25.2.0). It does not run simulations.

## Verify a model version

The request is a JSON *mapping*: family → Space → requested total. Example, three of the 36 Spaces of R2F
Office Hub with lighting from ASHRAE 90.1 Table G3.7:

```json
{"lights": {"1.10-MeetingRoom": 335.76, "0.05-Storage": 43.05, "1.24-Office": 130.24}}
```

```bash
openstudio-toolkit diff actual-017.osm reference-011.osm --mapping g37.json --tolerance 0.5 \
    --report verification.html --language es
# diff: 14 added, 5480 not_requested, 72 removed
# child vs mapping: 36 match
```

Exit code `0`: the child matches the request; `1`: it does not; `2`: the command could not run. The full
procedure is in [`docs/VERIFICATION-GUIDE.md`](docs/VERIFICATION-GUIDE.md).

## Commands

| Command | What it does |
|---|---|
| `dump model.osm --out dump/` | One CSV per family (Spaces, loads, constructions, HVAC...), as OpenStudio resolves it |
| `apply parent.osm child.osm --mapping m.json` | Writes the child with the requested per-Space loads; never modifies the parent, never doubles a space-type load |
| `compare model.osm --mapping m.json` | The model against the request, by Space or Thermal Zone |
| `diff parent.osm child.osm --mapping m.json --report r.html` | Every change parent → child, the request check, and the HTML report (English, Spanish or French) |
| `results eplusout.sql end_uses --units GJ=kWh` | `zone_sizes`, `system_sizes`, `unmet_hours`, `end_uses` |

The same functions are available from Python; the stable list is the contract,
[`docs/contracts/v0.3.toml`](docs/contracts/v0.3.toml).

## Develop

```bash
git clone https://github.com/roruizf/OpenStudio-Toolkit.git && cd OpenStudio-Toolkit
uv sync
uv run pytest -q
```

Rules, patterns and the release process: [`AGENTS.md`](AGENTS.md). Bugs and ideas:
[`docs/BACKLOG.md`](docs/BACKLOG.md).

## License

MIT, as declared in `pyproject.toml`.
