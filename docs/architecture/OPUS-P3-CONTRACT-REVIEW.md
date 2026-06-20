# Claude Opus Review Brief - P3 Findings And Validators

## Role

Act as a skeptical principal architecture and QA/QC-contract reviewer. Review the proposed P3 contract against the checkpointed inventory implementation and the actual Simulation OS geometry/naming rules. Do not edit, implement, stage, commit, or design automatic fixes.

## Repositories

- Toolkit: `/home/roruizf/projects/openstudio-toolkit`
- Simulation OS: `/home/roruizf/projects/r2f-simulation-os`
- Toolkit branch: `feature/agent-first-core`
- Latest checkpoint: `65b4461`

## Review files

- `docs/architecture/P3-FINDINGS-AND-VALIDATORS-CONTRACT.md`
- `docs/architecture/NORMALIZATION-ROADMAP.md`
- `src/openstudio_toolkit/schemas/inventory.py`
- `src/openstudio_toolkit/extractors/model_inventory.py`
- Simulation OS `docs/phases/geometry-and-spatial-definition.md`
- Simulation OS `docs/model-object-naming-convention.md`
- East Gate `model-object-naming-profile.md`
- East Gate `geometry-and-zoning-strategy.md`

## Intended decisions

- Findings contain technical facts and default severity, not workflow disposition.
- Simulation OS owns acceptance, correction, deferral, and release.
- Integrity and spatial validators are profile-independent.
- Exact naming validation requires an explicit `NamingProfile`.
- P3 validators consume only canonical `ModelInventory` and profile records.
- No OpenStudio, Pandas, file IO, clocks, environment, mutation, or automatic fix.
- East Gate naming is not validated until its conflicting grammar is approved.

## Known review risks

1. Some proposed spatial rules are R2F phase expectations, not universal OpenStudio validity. Confirm findings plus external disposition is the right boundary.
2. `missing_space_type` may be premature because the geometry phase speaks of a preliminary use concept, which might live in project data rather than an actual OSM SpaceType.
3. Severity defaults may be too strong or too weak without project context.
4. Duplicate names may need severity by object class or OpenStudio uniqueness behavior.
5. Surface adjacency reciprocity and SubSurface-area tolerance require precise numeric/relationship semantics.
6. Finding IDs are omitted because handles are revision-local; verify that Simulation OS can disposition findings without a stable ID.
7. Regex-based Space naming may be insufficient for Room-lineage reconciliation, which requires project mapping data unavailable to the toolkit.
8. The proposed composer may be premature before individual validators stabilize.
9. The P3.1-P3.4 split may be too many checkpoints for a small library.
10. Current East Gate naming documents conflict; verify the contract neither chooses nor obscures that conflict.

## Review questions

1. Is `Finding` minimal and sufficient for later human disposition?
2. Should severity live in the toolkit finding, a rule catalog, or Simulation OS?
3. Which proposed rules are universal inventory integrity versus R2F project-policy checks?
4. Should spatial assignment require a separate phase/profile input like naming does?
5. Are codes stable, precise, and appropriately namespaced?
6. Is omission of stable finding ID correct for this vertical?
7. Are evidence and suggested-action fields structured enough without becoming a patch language?
8. Is deterministic ordering/de-duplication well-defined?
9. Which rules must be cut or deferred from the first P3 implementation?
10. Is the remaining four-checkpoint roadmap appropriately small?

## Required output

Return:

1. Verdict: accept, accept with changes, or reject.
2. Findings ordered by severity with file/line evidence.
3. Accept/modify/reject table for contract decisions.
4. Minimum P3 contract after cuts.
5. Exact pre-implementation document changes.
6. Recommended first validator set and tests.
7. Decisions requiring Roberto's approval.
8. Confirmation or revision of the remaining roadmap count.

Do not implement code. Stop at contract review.
