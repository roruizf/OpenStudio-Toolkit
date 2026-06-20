# Claude Opus Review Brief - P2.1 ModelInventory

## Role

Act as a skeptical principal Python/API architect with OpenStudio awareness. Review the uncommitted P2.1 implementation against the approved architecture and the actual repository. Do not edit, install, stage, commit, or implement P2.2.

The objective is to determine whether the schemas and canonical serializer are safe to checkpoint before any SDK extractor depends on them.

## Repository state

- Repository: `/home/roruizf/projects/openstudio-toolkit`
- Branch: `feature/agent-first-core`
- Committed baseline: `21a3b858f717ece0b77646da48d05ec7fe8cd800`
- P2.1 is the current uncommitted worktree.
- P1 profile: Python 3.13, OpenStudio 3.10.0, EnergyPlus 25.1.0, uv.
- Historical G: toolkit worktree remains reference-only and must not be modified.

## Files to review

- `src/openstudio_toolkit/schemas/inventory.py`
- `src/openstudio_toolkit/schemas/__init__.py`
- `tests/schemas/test_inventory.py`
- `docs/architecture/MODEL-INVENTORY-CONTRACT.md`
- `docs/contracts/MODEL-INVENTORY-FIELD-MAP.md`
- `docs/architecture/ARCHITECTURE-VNEXT.md`

Use existing `osm_objects` extractors and OSM fixtures only as read-only comparison evidence.

## Intended decisions

- Canonical Python/JSON names use `snake_case` and explicit unit suffixes.
- Existing dict/DataFrame APIs retain human-readable OpenStudio keys.
- Each directly sourced canonical field carries lineage metadata: OSM/IDD label, SDK accessor, legacy key, and clarification.
- Handle fields are canonical relationships; resolved names are nullable human labels.
- Collections are deterministic by normalized name then handle.
- Canonical JSON sorts keys and hashes the exact UTF-8 bytes.
- P2.1 contains schemas and serialization only; SDK traversal starts in P2.2.

## Verified state

- P2.1 tests: 4 passed.
- Complete suite: 90 passed.
- Ruff: passed for changed Python files.
- mypy: passed for `schemas/inventory.py`.
- No extractor, model mutation, file output, CLI, or MCP was added.

## Known review risks

These are hypotheses to verify, not predetermined fixes:

1. `ConfigDict(frozen=True)` is shallow. Lists such as `space_handles`, `stories`, and `vertices` remain mutable after validation, so canonical bytes and hashes can change. Decide whether tuples are warranted now or whether serialization should defensively normalize/copy.
2. Derived SDK values such as `Building.floorArea()`, `Surface.grossArea()`, and `Surface.netArea()` currently receive synthetic `osm_label` strings even though they are not literal OSM text fields. Decide whether `osm_label` must be nullable and derived lineage represented separately.
3. `osm_field()` returns `Any`, reducing static type precision. Determine whether that is acceptable for a small metadata helper or should be replaced.
4. Runtime facts are copied into a Pydantic `RuntimeRecord` but not constrained to the P1 versions. Confirm that enforcement belongs only in the future extractor.
5. Count validation checks collection lengths but not relationship integrity. Confirm that relationship resolution belongs in P2.2/P3.
6. The field-map Markdown currently expands Space fully but summarizes other records. Decide whether schema metadata alone is sufficient for P2.1 or full generated documentation is required before checkpoint.
7. Vertex order is intentionally preserved rather than sorted because it defines polygon topology. Confirm that this is compatible with deterministic serialization.
8. `space_local` is provisional and awaits the P2.2 synthetic transformation test. Confirm it should remain in the schema now or be deferred until verified.

## Review questions

1. Are the canonical records minimal enough for geometry/spatial inventory, or did P2.1 prematurely encode P2.2 assumptions?
2. Are field names, units, required/null semantics, and relationship representations coherent?
3. Is the OpenStudio lineage metadata accurate and sufficient to translate back to OSM/IDD terminology for humans?
4. Is the serializer actually deterministic under mutation, Unicode, floats, collection ordering, and Pydantic version behavior?
5. Should canonical collections be tuples, immutable wrappers, or lists with defensive serialization?
6. Should `InventoryArtifact` remain a frozen dataclass or become a Pydantic record?
7. Does exporting every record from `schemas.__init__` create unnecessary public API surface?
8. Are any tests tautological, missing, or asserting implementation details rather than contract behavior?
9. Does P2.1 preserve legacy APIs without creating a second competing schema system?
10. What must change before checkpoint, and what must explicitly wait for P2.2?

## Required output

Return:

1. Verdict: accept, accept with changes, or reject.
2. Findings ordered by severity with exact file/line evidence.
3. Accept/modify/reject table for each intended decision.
4. Exact pre-checkpoint code and documentation changes.
5. Tests that must be added or changed.
6. Items that must be deferred to P2.2 rather than solved now.
7. Confirmation or revision of the human translation strategy.
8. Decisions requiring Roberto's approval.

Do not provide a replacement implementation or modify files. Stop at review.
