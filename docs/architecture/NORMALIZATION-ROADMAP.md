# Roadmap: openstudio-toolkit v0.3

The scope of v0.3 is closed. The contract is `docs/contracts/v0.3.toml`; whether each item is done
is what `tests/contract/` says (an item is done when its status there is `implemented` and its tests
pass). This file only orders the work and does not repeat facts the tests assert.

Anything not listed here needs Roberto's explicit approval to enter v0.3.

Measurements, approved decisions and the next-session plan: `V0.3-DECISIONS.md`.

## Core (proves the thesis)

| # | Item | Verified by |
|---|---|---|
| 1 | Clean install from a tag on the CI Python matrix | `.github/workflows/ci.yml`, `test_requires_python_matches_contract`, `test_ci_matrix_*` |
| 2 | Every `get_all_*_as_dataframe` (found by introspection) returns a DataFrame with its columns when the family is empty, works on fixtures that have objects, and does not die on orphan relations | `test_dataframe_functions_return_columns_when_empty`, `tests/osm_objects/` |
| — | Generic reader over every model object (IDD fields, orphan-safe), and orphan relations reported as findings | `test_public_api[extractors.generic.*]`, `test_generic_reader_uses_only_orphan_safe_methods`, `test_orphans_reported_as_findings` |
| 3 | Dumps of the existing families, as records and as a view | `test_public_api[dump.*]` |
| 6 | Parent → child diff per family, built on the generic reader | `test_public_api[analysis.diff.diff_models]`, `test_verification_runs_on_untouched_models` |
| 5 | Compare the model against a `Mapping`, by Space or Thermal Zone | `test_public_api[analysis.compare.compare_to_mapping]` |
| 7 | Verification artifact with the fixed schema and golden output | `test_verification_artifact_schema[*]` |

Work order: 1 → 2 → generic reader → 3 → 6 → 5 → 7. The diff comes before compare because it carries
the most risk.

## Volume (cut first if needed)

| # | Item | Verified by |
|---|---|---|
| 3b | New curated families (list in the contract's `[families]`) | `test_new_families_are_dumpable` |
| 4 | `apply` from a `Mapping`, adopting the `r2f-simulation-os` `base_model_space_loads.py` contract | `test_public_api[transforms.apply.apply_mapping]` |
| 8 | Results in polars: zone sizes, system sizes, unmet hours, end uses | `test_public_api[results.*]` |
| 9 | CLI: `dump`, `apply`, `compare`, `diff`, `results` | `test_cli_commands` |

Cut order: CLI → results → `apply` → new families. Volume is built in the reverse order.

## Invariants (tested from day one)

`test_read_code_does_not_mutate_or_spawn`, `test_verification_never_depends_on_apply`,
`test_polars_only_in_results`, `test_no_bare_optional_get_in_osm_objects`.

## Capacity

At most 10 h per week on the toolkit, logged by wall-clock time per session in
`robert-os/ops/initiatives.md`.

## History

P0–P4 and the first vertical closure (inventory, findings, validators, Simulation OS P4 integration)
were completed before v0.3; see git history and `r2f-simulation-os/docs/vertical-closure-evidence.md`.
