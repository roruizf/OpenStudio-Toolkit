# Claude Opus Review Brief - P2.2 Read-Only Extractor

## Role

Act as a skeptical principal Python/OpenStudio architect. Review the uncommitted P2.2 extractor against the checkpointed P2.1 contract and actual fixtures. Do not edit, install, stage, commit, or begin P2.3.

## Repository state

- Repository: `/home/roruizf/projects/openstudio-toolkit`
- Branch: `feature/agent-first-core`
- P2.1 checkpoint: `4cab3a8`
- P2.2 is the current uncommitted worktree.
- Runtime: Python 3.13, OpenStudio 3.10.0, EnergyPlus 25.1.0, uv.

## Review files

- `src/openstudio_toolkit/extractors/model_inventory.py`
- `src/openstudio_toolkit/extractors/__init__.py`
- `tests/extractors/test_model_inventory.py`
- `src/openstudio_toolkit/schemas/inventory.py`
- `docs/architecture/MODEL-INVENTORY-CONTRACT.md`
- `docs/architecture/P2.2-EVIDENCE.md`

## Verified evidence

- P2.2: 6 tests passed.
- Full suite: 102 tests passed.
- Ruff and mypy passed.
- Office Hub: 2 stories, 36 spaces, 36 zones, 278 surfaces, 53 subsurfaces.
- Office Hub extraction: ~1.378 s; serialization: ~0.006 s; 276,332 bytes.
- Two local runs produced identical artifact hash `98f8dc2a122d9b1a80b4314c2794ee52c59a6b1eb959596cad1e07a83e8afa56`.
- Input hash preservation, explicit load errors, runtime gate, and simulated input-change failure are tested.

## Known review risks

1. `RuntimeRecord` contains absolute Python executable and module paths. `SourceRecord.path` may also be absolute. These fields make canonical bytes environment-dependent even when model semantics are identical. Decide whether determinism is local-run only, whether paths should be normalized, or whether environment facts belong outside the hashed domain inventory.
2. `coordinate_system` is always `space_local`, but `SurfaceRecord.space_handle` is nullable. Determine the correct representation for orphan surfaces and their subsurfaces.
3. Input SHA-256 before/after detects on-disk mutation but not in-memory SDK mutation. Confirm this is the intentionally scoped guarantee.
4. `VersionTranslator` may update the model in memory. Confirm this is acceptable for read-only inspection and should be recorded separately from source mutation.
5. Relationship maps are built from direct references, then records are reconstructed with `model_validate()` to apply sorting. Review correctness and cost.
6. SWIG optional conversion is generic and relies on `is_initialized()`. Check whether all scoped optional values and references use that interface in OpenStudio 3.10.
7. The Office Hub relationship test assumes every space has one story/zone. Confirm nullable relationships remain correct for other valid models.
8. Artifact hash is documented as evidence but should not become a permanent golden value if it embeds machine-specific paths.

## Review questions

1. Does `inspect_model()` satisfy the no-write/no-mutation contract precisely?
2. Are exceptions and failure ordering appropriate?
3. Is the extraction genuinely linear and minimal, or are there hidden expensive SDK calls?
4. Are all canonical fields populated with correct OpenStudio semantics and Python/null conversion?
5. Are relationship maps complete, deterministic, and correctly scoped?
6. Should runtime/source paths remain in `ModelInventory`, be normalized, or move to a run envelope?
7. How should coordinate systems represent surfaces with no parent space?
8. Are the tests sufficient and non-tautological? Identify missing edge fixtures.
9. Which changes are blocking checkpoint versus deferrable to P2.3/P3?

## Required output

Return:

1. Verdict: accept, accept with changes, or reject.
2. Findings by severity with exact file/line evidence.
3. Accept/modify/reject table for extraction decisions.
4. Exact pre-checkpoint changes and required tests.
5. Items to defer to P2.3, P3, or the Simulation OS adapter.
6. Decisions requiring Roberto's approval.

Do not provide implementation code or modify files. Stop at review.
