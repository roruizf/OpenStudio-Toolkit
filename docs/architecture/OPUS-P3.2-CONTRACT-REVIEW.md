# Claude Opus Review Brief - P3.2 Naming, Composition, And Evidence

## Review Mode

Architecture and QA/QC contract review only. Do not edit files, implement code, install packages, or commit.

## Repository

`/home/roruizf/projects/openstudio-toolkit`

Branch: `feature/agent-first-core`

Committed baseline: `65b4461`

P3.1 is currently uncommitted and must be reviewed as the actual worktree, not inferred from the baseline.

## Read First

Toolkit:

1. `docs/architecture/P3.2-NAMING-COMPOSITION-CONTRACT.md`
2. `docs/architecture/P3-FINDINGS-AND-VALIDATORS-CONTRACT.md`
3. `docs/architecture/P3-CONTRACT-REVIEW-DECISION.md`
4. `docs/architecture/P3.1-EVIDENCE.md`
5. `src/openstudio_toolkit/schemas/findings.py`
6. `src/openstudio_toolkit/schemas/inventory.py`
7. `src/openstudio_toolkit/validators/integrity.py`
8. `src/openstudio_toolkit/validators/spatial.py`

Simulation OS:

1. `/home/roruizf/projects/r2f-simulation-os/docs/model-object-naming-convention.md`
2. `/home/roruizf/projects/r2f-simulation-os/docs/historical-naming-method-audit.md`
3. `/home/roruizf/projects/r2f-simulation-os/docs/phases/geometry-and-spatial-definition.md`
4. East Gate `model-object-naming-profile.md`
5. East Gate `geometry-and-zoning-strategy.md`

Verify claims against disk and current tests.

## Established Decisions

- Toolkit validators are pure over canonical `ModelInventory`.
- Simulation OS owns project mappings, disposition, release, and persistence.
- Naming is profile-driven; there is no hidden default profile.
- Room-ID lineage requires Room-to-Space mapping and is not a toolkit naming claim.
- East Gate currently has conflicting hyphen and double-underscore grammars; naming remains deferred.
- P3.1 already owns universal integrity and R2F spatial assignment findings.
- No OpenStudio, Pandas, file IO, runtime access, or mutation belongs in P3.2 validators.

## Load-Bearing Questions

1. Does `NamingProfile` expose the minimum grammar needed, or is it too weak/too configurable?
2. Can every proposed naming rule be proven from `ModelInventory` without project mapping?
3. Is diagnostic precedence correct, or would it hide material mismatches?
4. Are exact SDK tokens and literal separators robust enough without an alias/normalization layer?
5. Does the surface adjacency algorithm correctly derive the adjacent Space through the adjacent Surface?
6. Is a regex for multi-Space Thermal Zones misleading because it proves shape but not membership traceability?
7. Should `GeometryValidationReport` belong to the toolkit or be deferred to the Simulation OS adapter?
8. Is `inventory_sha256 + ruleset version + profile identity + checks_run + findings` sufficient portable evidence?
9. Is canonical exact-finding dedup useful or does it conceal validator bugs?
10. Does deterministic Markdown belong in P3.2, or is it premature presentation logic?
11. Are any fields duplicated with legacy `ValidationResult` or `TaskResult` in a harmful way?
12. Does the contract preserve the P3.1/P4 boundary and avoid scope creep?

## Known Risks To Verify

- Space or adjacent-Space names may contain the configured separator; expected-prefix construction must remain unambiguous without parsing owner names.
- Missing structural prerequisites could cause duplicate or misleading naming findings.
- A draft/incomplete profile could produce excessive observations.
- Report schema/ruleset versioning could become a second maturity system.
- Markdown projection may become an accidental canonical artifact.
- Office Hub may not conform to the proposed derived grammar and must not be treated as a golden naming fixture without an explicit profile.
- East Gate naming must remain blocked despite the existence of a draft profile document.
- Exact floating evidence or unordered dict/list data could undermine report determinism.

## Required Output

1. Verdict: accept, accept with changes, or reject.
2. Findings ordered by severity with exact file/line evidence.
3. Accept/modify/reject table for major decisions.
4. Minimum P3.2 contract after cuts.
5. Exact pre-implementation document changes.
6. Recommended validator/report test matrix.
7. Decisions requiring Roberto's approval.
8. Whether P3.2 should remain one checkpoint or be reduced further.

Finish with a concise bottom line. Make no changes.
