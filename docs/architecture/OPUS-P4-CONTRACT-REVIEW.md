# Claude Opus Review Brief - P4 Simulation OS Integration

## Review Mode

Architecture, reproducibility, and human-gate contract review only. Do not edit, implement, install, commit, or create a baseline.

## Primary Contract

`/home/roruizf/projects/openstudio-toolkit/docs/architecture/P4-SIMULATION-OS-INTEGRATION-CONTRACT.md`

## Repositories

### OpenStudio Toolkit

Path: `/home/roruizf/projects/openstudio-toolkit`

Branch: `feature/agent-first-core`

Committed baseline: `65b4461`

P3.1/P3.2 are uncommitted in the current worktree. Review actual disk state.

Read:

- `docs/architecture/P3-FINDINGS-AND-VALIDATORS-CONTRACT.md`
- `docs/architecture/P3.2-NAMING-COMPOSITION-CONTRACT.md`
- `docs/architecture/P3.2-EVIDENCE.md`
- `src/openstudio_toolkit/schemas/inventory.py`
- `src/openstudio_toolkit/schemas/findings.py`
- `src/openstudio_toolkit/schemas/validation.py`
- `src/openstudio_toolkit/validators/geometry.py`

### R2F Simulation OS

Path: `/home/roruizf/projects/r2f-simulation-os`

Important current fact: repository has no initial commit/`HEAD`; nearly all content is untracked. Do not normalize or commit it.

Read:

- `docs/architecture.md`
- `docs/phase-lifecycle.md`
- `docs/model-lineage.md`
- `docs/rule-maturity.md`
- `docs/phases/geometry-and-spatial-definition.md`
- `.codex/skills/define-spatial-model/SKILL.md`
- East Gate Geometry `PHASE.md` and engagement `STATUS.md`
- Kickoff `REVIEW.md` and `history/REVIEW-DECISIONS.md` as the existing Review Interview pattern

## Established Decisions

- Capability is the stable verb; adapter is the pinned implementation binding.
- Toolkit owns domain extraction/validation; Simulation OS owns project workflow, artifacts, disposition, and release.
- P3 semantic hashes exclude machine paths/runtime; P4 manifest intentionally records run-envelope facts.
- No silent model mutation and no automatic release.
- Geometry always requires complementary programmatic and visual human review.
- Existing Review Interview and live registers remain governance; P4 must not add a competing lifecycle.
- East Gate has no first OSM and no approved naming grammar yet.
- No MCP, container, VPS, second runtime, mutation tools, or generic registry in P4.

## Load-Bearing Questions

1. Are the two Git/baseline prerequisites genuinely blocking P4 implementation?
2. Is the capability/adapter split minimal, or does the proposed package shape introduce unnecessary layers?
3. Is the adapter correctly kept write-free while the capability owns atomic artifact publication?
4. Is the run manifest minimal and sufficient for reproducibility, or over-recorded?
5. Is snapshotting `NamingProfile` necessary and sufficient to reproduce naming checks?
6. Are all cross-artifact hash invariants correct, especially inventory semantic hash versus inventory file hash?
7. Is report-scoped `sha256(canonical Finding)` a safe disposition reference without pretending to be cross-revision stable?
8. Does keeping dispositions outside the immutable bundle preserve auditability, or create drift risk?
9. Are release-readiness severity/disposition rules consistent with the Geometry phase?
10. Should a current major finding be releasable only as `accepted`, and should a current `corrected` status always require rerun?
11. Does zero findings still enforce the visual/human gate technically rather than by instruction?
12. Does the release record duplicate model lineage or correctly bind it to evidence?
13. Is a thin Python module entry point enough for agent execution without MCP/CLI framework?
14. Is Office Hub sufficient to accept P4 pending East Gate?

## Risks To Probe

- Manifest may confuse canonical inventory artifact SHA with `report.inventory_sha256` semantic hash.
- Toolkit Git SHA may be hard to obtain reliably from an installed wheel/path dependency.
- Atomic directory rename behavior may differ across filesystems.
- Disposition fingerprints change if non-identity message text changes.
- Mutable dispositions could silently diverge from the bound report.
- `accepted` major findings may become an overly permissive release escape hatch.
- `approved-with-corrections` could release evidence bound to stale OSM bytes.
- Naming profile Markdown and structured snapshot could drift.
- Simulation OS's no-commit state could make implementation evidence unauditable.
- Updating `define-spatial-model` before the capability is stable could encode premature instructions.

## Required Output

1. Verdict: accept, accept with changes, or reject.
2. Findings ordered by severity with exact file/line evidence.
3. Accept/modify/reject table for major decisions.
4. Minimum P4 architecture after cuts.
5. Exact pre-implementation contract changes.
6. Recommended schemas, gate rules, and test matrix.
7. Decisions requiring Roberto approval.
8. Whether P4 should be one implementation checkpoint or split once.

Finish with a concise bottom line. Make no changes.
