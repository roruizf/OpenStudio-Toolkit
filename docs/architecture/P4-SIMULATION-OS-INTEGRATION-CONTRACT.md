# P4 Simulation OS Integration Contract

Status: Reviewed; implementation blocked on approved Git checkpoints
Date: 2026-06-20
Scope: Direct `inspect-openstudio-model` capability, immutable evidence bundle, finding disposition, and human geometry-release gate

## 1. Objective

Integrate the completed read-only OpenStudio Toolkit vertical into R2F Simulation OS without moving project workflow, human decisions, or release authority into the toolkit.

P4 proves one end-to-end boundary:

```text
registered human-created OSM
  -> Simulation OS capability request
  -> pinned OpenStudio Toolkit adapter
  -> immutable inventory + QA/QC evidence bundle
  -> Simulation OS finding disposition
  -> mandatory visual/programmatic human review
  -> explicit geometry release record
```

The adapter inspects and records. It never mutates or releases an OSM.

## 2. Blocking Preconditions For Implementation

P4 design may proceed now. P4 code must not begin until:

1. P3.1/P3.2 are intentionally committed in `openstudio-toolkit` and have an immutable Git SHA.
2. R2F Simulation OS receives an intentional initial baseline commit; it currently has no `HEAD` and nearly all files are untracked.
3. The Simulation OS uv project pins the toolkit dependency to the approved commit/version; no ambient `PYTHONPATH`, editable install, Conda environment, or unpinned local checkout is accepted.
4. The provisional runtime remains Python 3.13, OpenStudio 3.10.0, and EnergyPlus 25.1.0 unless a separately evidenced profile change is approved.

These are reproducibility gates, not architecture abstractions.

## 3. Ownership Boundary

### OpenStudio Toolkit owns

- OpenStudio runtime assertion and read-only OSM traversal.
- Canonical `ModelInventory` and portable inventory hash.
- Pure integrity, spatial, and optional naming validators.
- `GeometryValidationReport`, canonical JSON, and deterministic Markdown.
- Stable finding codes and default severity.

### Simulation OS capability owns

- Explicit project/engagement/phase/model invocation context.
- Selection of required checks and approved naming profile.
- Calling one pinned toolkit adapter.
- Immutable run manifest and evidence-bundle publication.
- Verification of all cross-artifact hashes and source immutability.
- Finding fingerprints scoped to one validation report.
- Review packet, disposition records, and release-readiness evaluation.

### Human/phase governance owns

- Visual geometry review.
- Finding acceptance, deferral, correction decision, and rationale.
- Project naming-profile approval.
- Global phase decision and geometry release.
- Model-state transition to `released` and any released-file registration/copy.

The capability cannot silently promote a model state or close a phase.

## 4. Minimum Architecture

Retain the previously approved two concepts:

```text
Simulation OS workflow/skill
  -> CAPABILITY: inspect-openstudio-model
  -> ADAPTER: pinned openstudio-toolkit Python API
  -> evidence bundle
  -> existing Review Interview and model-lineage rules
```

Proposed implementation shape after the Git gates are closed:

```text
src/r2f_simulation_os/
  capabilities/inspect_openstudio_model.py
  adapters/openstudio_toolkit.py
  schemas/geometry_review.py
  geometry_release.py
tests/
  capabilities/
  adapters/
  geometry_release/
```

Create only these packages when the vertical fills them. Do not add a registry framework, plugin system, task engine, remote executor, or generic artifact service.

The existing `define-spatial-model` skill remains procedural guidance. After P4 is proven, its Audit step may call the capability; the skill does not own domain logic.

## 5. Capability Contract

Stable capability identifier:

```text
inspect-openstudio-model
```

Python interface:

```python
execute_inspect_openstudio_model(
    request: InspectOpenStudioModelRequest,
    *,
    adapter: OpenStudioToolkitAdapter,
) -> InspectionRunResult
```

### 5.1 Request

```text
InspectOpenStudioModelRequest
  request_schema_version
  run_id
  project_id
  engagement_id
  phase_id
  model_id
  model_revision
  source_path
  registered_path
  artifact_directory
  checks_requested[]
  release_required_checks[]
  naming_profile
  naming_profile_approval_ref
```

Rules:

- `run_id` is caller-supplied, unique within the engagement, and filesystem-safe.
- `model_revision` is an explicit three-digit revision such as `001`; filenames and model state remain governed by Simulation OS model-lineage rules.
- `source_path` and `artifact_directory` are execution-envelope paths, never part of semantic hashes.
- `registered_path` is the stable project-relative label passed into the toolkit run envelope.
- `checks_requested` contains sorted unique `integrity`, `spatial`, and optionally `naming`.
- `release_required_checks` is an explicit Simulation OS/phase decision and must be a subset of `checks_requested`; it is never inferred from profile presence.
- `integrity` and `spatial` are always both requested and release-required for this capability.
- If `naming` is requested, a structured `NamingProfile` must be supplied.
- A naming profile is rejected when `naming` is not in `checks_requested`; checks cannot run implicitly.
- Naming may be requested with a draft profile for preview. It satisfies `release_required_checks` only with an approved profile and matching human approval reference.
- `naming_profile_approval_ref` points to the Simulation OS human decision approving the exact profile ID/version. A profile's internal `status: approved` cannot self-prove governance.
- The request contains no finding dispositions or human approval.

### 5.2 Adapter

The adapter:

1. invokes `inspect_model()` from the pinned toolkit;
2. serializes the canonical inventory;
3. builds `GeometryValidationReport` with the supplied profile, if any;
4. serializes report JSON and Markdown;
5. snapshots the exact structured naming profile when supplied;
6. returns bytes, hashes, `InventoryRun` provenance, and toolkit/ruleset identity to the capability;
7. never writes files and never imports OpenStudio directly.

This makes the adapter transport/binding code. Toolkit logic remains toolkit logic.

### 5.3 Capability execution

The capability:

- rejects a missing source, existing final run directory, malformed revision, or unsatisfied required check before publication;
- hashes the OSM before and after execution and fails on change;
- writes only to a sibling staging directory under the same artifact-directory parent as the final bundle, guaranteeing an intra-filesystem rename;
- verifies every serialized artifact before publication;
- writes the manifest last;
- atomically renames staging to the final `run_id` directory;
- never overwrites or merges an existing run bundle;
- leaves no published partial bundle on failure.

Failure diagnostics may be returned to the caller/log, but a failed attempt is not a successful evidence bundle.

## 6. Immutable Evidence Bundle

Logical bundle:

```text
<artifact_directory>/<run_id>/
  run-manifest.json
  inventory.json
  geometry-validation.json
  geometry-validation.md
  naming-profile.json        # only when naming ran
```

The bundle is immutable after publication. Simulation OS may register a different storage path, but the roles and cross-hash rules remain stable.

### 6.1 Run manifest

```text
InspectionRunManifest
  schema_version
  run_id
  capability_id
  capability_contract_version
  adapter_id
  adapter_version
  toolkit_package_version
  toolkit_git_sha
  uv_lock_sha256
  project_id
  engagement_id
  phase_id
  model_id
  model_revision
  source_registered_path
  source_osm_sha256
  source_size_bytes
  inventory_artifact_sha256
  runtime
  checks_requested[]
  release_required_checks[]
  completed_checks[]
  naming_profile_identity
  naming_profile_approval_ref
  artifacts[]
  started_at
  completed_at
  warnings[]
```

`runtime` records Python, OpenStudio, EnergyPlus, executable, and module path from `InventoryRun`. Paths/timestamps are intentionally run-envelope facts and are excluded from semantic inventory/report hashes.

`uv_lock_sha256` is the authoritative implementation-binding identifier. `toolkit_git_sha` is best-effort provenance populated from the immutable pin/build metadata or the pinned SHA recorded by `uv.lock`; bundle publication must not depend on a runtime `.git` directory being present.

Each artifact entry records:

```text
role
relative_path
media_type
sha256
size_bytes
```

### 6.2 Required cross-artifact invariants

- Current OSM file SHA-256 equals manifest `source_osm_sha256`.
- Inventory `source.sha256` equals manifest `source_osm_sha256`; this is the hash of the OSM bytes, not the inventory JSON.
- Manifest `inventory_artifact_sha256` equals the SHA-256 of the canonical `inventory.json` bytes.
- Validation report `inventory_sha256` equals manifest `inventory_artifact_sha256` and `artifacts[role=inventory].sha256`; it never denotes the OSM file hash.
- Every artifact's bytes equal its manifest SHA-256 and size.
- `completed_checks` equals report `checks_run` and contains every `checks_requested` entry.
- Naming identity is absent everywhere when naming did not run.
- When naming ran, request, profile snapshot, report, findings, and manifest use the same profile ID/version/status.
- A release-required naming check links the exact structured profile snapshot to its human approval record.
- `uv_lock_sha256` authoritatively identifies the exact dependency binding; `toolkit_git_sha`, when present, agrees with the pinned toolkit specification.

## 7. Finding Reference And Disposition

Toolkit findings intentionally have no cross-revision stable ID. Simulation OS creates a report-scoped reference:

```text
finding_fingerprint = sha256(canonical JSON bytes of the complete Finding)
```

Because P3 removes canonically identical duplicates, the fingerprint is unique within one report. It is not a cross-revision identity and must always be paired with `report_sha256`.

```text
GeometryFindingDisposition
  report_sha256
  validator_suite_version
  finding_fingerprint
  code
  object_handle
  disposition
  rationale
  reviewer
  decided_at
  affected_outputs[]
```

Disposition vocabulary reuses the Geometry phase:

- `open`
- `accepted`
- `corrected`
- `deferred`

Rules:

- Newly reviewed findings begin `open`; the immutable toolkit report itself is unchanged.
- `accepted` and `deferred` require human rationale.
- `corrected` records history against the old report but cannot prove the current OSM is corrected; a new inspection run is required.
- Dispositions never change toolkit severity or evidence.
- A disposition record pointing to a missing report/fingerprint is invalid.
- A new model revision/report is re-reviewed; fingerprints are not silently carried forward.
- A disposition is valid only for its bound `report_sha256` and `validator_suite_version`. A new report or ruleset version forces re-disposition, including when only Finding message text changed.

Disposition storage belongs to active phase records or engagement current truth, not inside the immutable execution bundle.

## 8. Review Packet

Simulation OS prepares one human review interface bound to the exact model and report:

```text
GeometryReviewPacket
  project/engagement/phase context
  model_id + revision + source_osm_sha256
  run_id + report_sha256
  checks completed / explicitly not run
  severity summary
  material findings and proposed actions
  visual-review checklist
  disposition questions
  release decision requested
```

The packet may project toolkit Markdown but adds workflow context and disposition fields. It is not the canonical machine report.

Reuse the existing Review Interview:

1. Roberto reads the focused `REVIEW.md`/review packet.
2. The agent asks one decision question at a time.
3. Responses use existing `approve`, `correct`, `defer`, or `reject` interview vocabulary.
4. Finding-level effects are recorded as `accepted`, `corrected`, or `deferred` dispositions.
5. Current effects propagate to phase history/live registers.
6. Geometry release is a separate explicit global decision.

P4 must not add a competing review lifecycle.

## 9. Release-Readiness Evaluation

The system may compute readiness; only the human approves release.

```python
evaluate_geometry_release(
    manifest,
    report,
    dispositions,
    visual_review,
) -> ReleaseReadiness
```

`ReleaseReadiness` contains `ready: bool` plus deterministic blocking reasons. It is not a model state.

### Programmatic conditions

- Bundle integrity and all cross-artifact invariants pass.
- Every `checks_requested` entry completed, and every explicit `release_required_checks` entry is present in the report.
- Whether naming is release-required comes only from `release_required_checks`, which is recorded by the Simulation OS phase/request; it is not inferred from profile presence.
- If naming is release-required, the exact profile status is `approved`.
- If naming is release-required, the exact profile ID/version has a valid human `naming_profile_approval_ref`.
- No blocker finding exists in the release-candidate report.
- Every major finding in the current report is explicitly `accepted` with rationale; otherwise rework is required.
- Every minor and observation is explicitly `accepted` or `deferred` with rationale.
- No current-report finding remains `open`.
- A current-report finding marked `corrected` blocks readiness until a new run proves it absent.

### Human conditions

- Visual geometry review is explicitly complete and bound to model/report hashes.
- The human global decision is `approved` or `approved-with-corrections`.
- `approved-with-corrections` is valid only when corrections do not change the bound OSM or invalidate the report; model-affecting corrections require a new revision/run/review.
- Immediately before creating the release record, re-hash the current OSM and require equality with manifest `source_osm_sha256`. Any byte change forces a new run regardless of human decision.

Even a zero-finding report cannot release geometry without visual review and an explicit human decision.

## 10. Geometry Release Record

After human approval, Simulation OS records:

```text
GeometryReleaseRecord
  project_id
  engagement_id
  phase_id
  model_id
  model_revision
  source_osm_sha256
  run_id
  inventory_sha256
  report_sha256
  human_decision
  approved_by
  approved_at
  accepted_limitations[]
  handoff_target
```

The release record binds approval to exact evidence. It does not contain the OSM bytes and does not mutate the model.

Any copy/registration into a released-model location is a separate explicit Simulation OS operation that must preserve the exact SHA-256. Released revisions are immutable under `model-lineage.md`.

## 11. Agent And Skill Interaction

After implementation:

- `define-spatial-model` calls the capability during `Audit And Release` rather than hand-implementing SDK inspection.
- The skill supplies project context, source model identity, required checks, and approved profile selection.
- The skill presents the generated review packet and conducts the existing human interview.
- The skill never edits the evidence bundle or marks release automatically.

No MCP is needed. A thin Python module entry point may expose this one capability for agent execution, but P4 does not create a general CLI framework.

## 12. Acceptance Criteria

1. Simulation OS uses uv and pins the exact toolkit Git SHA/runtime profile.
2. Adapter imports the toolkit API but not OpenStudio or Pandas directly.
3. Office Hub produces a complete bundle without modifying the OSM.
4. Repeated semantic runs produce identical inventory/report hashes; manifests may differ by envelope fields.
5. Bundle publication is atomic and refuses overwrite.
6. Failure leaves no published partial bundle.
7. All manifest artifact and cross-hashes verify.
8. Office Hub proves `report.inventory_sha256 == inventory_artifact_sha256` while both remain semantically distinct from `source_osm_sha256`.
9. Requested naming fails preflight without a profile and release-required naming cannot use a draft profile.
10. An `approved` profile without a matching human approval reference cannot satisfy release readiness.
11. Naming-not-requested is recorded as not run, never passed.
12. A wheel/runtime without `.git` still publishes using authoritative `uv_lock_sha256` binding evidence.
13. Fingerprints are deterministic within a report and reject cross-report or cross-ruleset misuse.
14. Blocker, major, minor, observation, `open`, `corrected`, accepted/deferred rationale rules are tested.
15. Zero findings still requires visual review and human approval.
16. A corrected or out-of-band modified model requires a new immutable revision/run; release-time re-hash catches byte changes.
17. Adapter/capability do not mutate, copy, rename, or release the OSM.
18. Existing Simulation OS Review Interview and live-register propagation remain the governance mechanism.
19. East Gate remains pending until its first OSM and naming-profile decision exist.

## 13. First Fixture And East Gate Boundary

P4 is implemented and accepted against `R2F-Office-Hub.osm` first.

This proves adapter execution, evidence publication, disposition mechanics, and human-gate enforcement. It does not validate Room-lineage QA or East Gate naming.

East Gate remains pending until:

- a registered first OSM revision exists;
- one naming grammar is human-approved and represented as structured `NamingProfile`;
- Room-to-Space mapping data is available for Simulation OS-owned reconciliation.

## 14. Explicit Non-Goals

- OSM mutation, rename preview, or save-as.
- MCP server or MCP tool exposure.
- Container/VPS/remote execution.
- Multi-runtime compatibility matrix.
- Generic capability registry or plugin framework.
- Automatic finding disposition or human approval.
- Room-lineage validation inside the toolkit.
- Model Assembly, simulation, standards, HPXML, Ladybug, or results adapters.

## 15. Decisions Requiring Roberto Approval

1. Authorise the P3 toolkit checkpoint commit so Simulation OS can pin it.
2. Authorise an intentional Simulation OS initial baseline commit before P4 code.
3. Approve report-scoped finding fingerprints rather than introducing stable cross-revision IDs.
4. Approve the release policy: blocker must be absent; major requires accepted exception; all other current findings require explicit disposition.
5. Approve separate immutable execution bundle, mutable disposition/current-truth records, and explicit release record.
6. Confirm East Gate naming remains deferred.

## 16. Implementation Sequence

### P4a - Execution And Evidence

- uv project and exact toolkit pin;
- request/manifest schemas;
- write-free toolkit adapter;
- capability execution and same-filesystem atomic bundle publication;
- all source/inventory/report/profile hash invariants;
- Office Hub evidence.

Acceptance: deterministic semantic artifacts, valid run manifest, atomic/no-overwrite publication, unchanged OSM, and no human-governance writes.

### P4b - Disposition And Release Gate

- report-scoped fingerprints and disposition schemas;
- review packet using the existing Review Interview;
- deterministic release-readiness evaluation;
- release-time OSM re-hash;
- explicit geometry release record and skill integration.

Acceptance: severity/disposition policy, zero-finding human gate, stale-report rejection, no automatic release, and current-truth propagation through existing Simulation OS records.

## 17. Stop Boundary

P4 stops after one local direct adapter, one capability, immutable bundle, disposition/review schemas, deterministic release-readiness evaluation, Office Hub evidence, and existing-skill integration.

Then close the vertical. Do not continue automatically into mutation, MCP, containers, or additional domain tools.
