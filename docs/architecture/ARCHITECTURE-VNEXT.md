# OpenStudio Toolkit vNext Architecture

Status: **Superseded** on 2026-10-26 by the v0.3 contract (`docs/contracts/v0.3.toml`, enforced by
`tests/contract/`). Kept as the historical rationale for the design; do not read it as current fact.
Known stale statements: §1.1 and §12 say `tests/output/` is tracked and that OpenStudio is not
declared; both are false since the runtime pin (`openstudio==3.11.0` in `pyproject.toml`) and the
P0 cleanup.

Previous status: Approved for incremental implementation; P1 verified
Date: 2026-06-20
Scope: Evolution of `openstudio-toolkit` from a notebook-oriented helper library into an agent-ready domain library without a rewrite.

## 1. Decision Summary

OpenStudio Toolkit remains the reusable Python domain library for inspecting, validating, analyzing, and transforming OpenStudio models. It does not become an agent, an MCP server, a project workflow engine, or a replacement for the OpenStudio SDK.

The evolution is incremental:

- Preserve the current public API during the first migration stages.
- Introduce stable machine-oriented contracts beneath compatibility wrappers.
- Keep DataFrame, Excel, and notebook interfaces as human-oriented views.
- Separate read-only operations from model mutations technically and visibly.
- Pin and assert the OpenStudio runtime used for verification.
- Add structure only when a delivered capability requires it.

The first vertical is a deterministic, read-only whole-model inventory used by Simulation OS for geometry review.

### 1.1 Current baseline constraints

The target architecture is not the current implementation. At baseline `0.2.0`:

- `pyproject.toml` declares Pandas, OpenPyXL, and Pydantic, but does not declare OpenStudio. The binding is supplied by the ambient interpreter.
- Pandas is imported by the shared `osm_objects/_base.py` helpers and by 22 current `osm_objects` modules. DataFrames are therefore coupled to the present extractor layer.
- `tests/output/test_hard_size_hvac_result.osm` is a tracked generated artifact.
- `ProjectSpec` and `TaskStep` live in `schemas/project.py`; the `workflows` package is empty.

These are migration inputs and debts, not invariants the repository already satisfies.

## 2. System Boundary

```text
Robert-OS
  governance, priorities, constraints, decisions
        |
R2F Simulation OS
  project lifecycle, skills, workflows, human gates, release evidence
        |
Capability adapter
  Python, CLI, or later an allowlisted MCP interface
        |
OpenStudio Toolkit
  reusable domain operations and machine contracts
        |
OpenStudio SDK / CLI / EnergyPlus
  model API, translation, simulation runtime
```

### Toolkit owns

- Runtime detection and compatibility assertions.
- Loading models for domain operations.
- Typed extraction and serialization of model data.
- Pure validation and analysis functions.
- Explicit in-memory transformations.
- Result and change-set contracts.
- OpenStudio measures maintained as toolkit resources.
- Human-oriented projections such as DataFrames and Excel exports.
- Unit, integration, determinism, and compatibility tests for these operations.

### Toolkit does not own

- Agent prompts, skills, planning, or tool selection.
- Project lifecycle, phase state, deliverable release, or human approval gates.
- Simulation OS `ProjectSpec` or cross-capability workflow orchestration.
- MCP sessions, model registries, broad filesystem access, or transport concerns.
- Infrastructure provisioning, containers, VPS management, or credentials.
- A parallel object model that attempts to reproduce the OpenStudio SDK.

`ProjectSpec`, `TaskStep`, and the empty `workflows` package are compatibility surfaces during migration, but their intended owner is Simulation OS.

## 3. Design Principles

1. **Capability-driven, not taxonomy-driven.** Add or reorganize modules when a real project capability requires it.
2. **One source of domain logic.** CLI, MCP, notebooks, and agent adapters call the same toolkit functions.
3. **Read and write are separate contracts.** A caller must know whether an operation can mutate a model before invoking it.
4. **No implicit persistence.** Transformations modify an in-memory model only; saving is a separate explicit operation.
5. **Move toward machine contract first, human view second.** New canonical contracts use typed records and JSON. Existing DataFrame and Excel APIs remain supported while their current coupling is reduced incrementally.
6. **Deterministic where the domain permits.** Collections have defined ordering and outputs exclude volatile data unless declared.
7. **Fail loudly on runtime mismatch.** A claimed execution profile is verified at runtime, not trusted as configuration text.
8. **Compatibility before cleanup.** Existing imports and notebook workflows receive deprecation paths rather than abrupt removal.
9. **The SDK is a dependency, not a folder template.** Borrow conceptual boundaries and official vocabulary, not its C++ structure.
10. **Observed need controls automation.** No MCP expansion, runtime matrix, registry, or remote execution layer before a vertical requires it.

## 4. Core Concepts

### 4.1 Operation

An operation is a reusable domain function with an explicit contract. The following names are semantic tags, not a required class hierarchy or a mandate for four packages:

| Class | Reads model | Mutates model | Writes files | Example |
|---|---:|---:|---:|---|
| Extractor | Yes | No | No | Extract spaces |
| Validator | Yes | No | No | Validate spatial mapping |
| Analysis | Yes | No | No | Calculate WWR |
| Transform | Yes | In memory | No | Normalize names |

The load-bearing technical split is between read-only operations and transforms. Extractor and analysis distinguish direct retrieval from derived calculation, but may share implementation structure until observed needs justify separation.

Persistence, export, translation, and simulation are explicit boundary operations. They must not be hidden inside extractors, validators, analyses, or transforms.

### 4.2 Capability

A capability is the stable verb exposed to Simulation OS, for example `inspect-openstudio-model`. A capability may compose several toolkit operations. The capability contract belongs to the adapter/Simulation OS boundary; its domain records belong in the toolkit.

### 4.3 Adapter

An adapter binds a capability to one execution mechanism and runtime. Initially this is a direct Python adapter using the toolkit. CLI and MCP adapters may be added after the capability contract stabilizes.

### 4.4 Views

Views convert canonical records into forms optimized for people or external systems:

- Pandas DataFrame
- Excel workbook
- Notebook display
- JSON serialization

Pandas remains supported and is currently a base dependency coupled into the extractor helpers and many object modules. For new canonical extraction and validation contracts, the target is to avoid requiring Pandas unless an analysis genuinely depends on tabular computation. Decoupling the existing API is migration work, not a prerequisite for the first vertical and not a claim about the baseline.

## 5. Target Package Shape

This is a directional map, not a mandate for an immediate file move.

```text
src/openstudio_toolkit/
  runtime/       # version detection, assertions, compatibility facts
  extractors/    # read-only SDK -> typed records
  schemas/       # records, findings, results, change sets
  validators/    # pure findings from records/model
  transforms/    # explicit in-memory model changes
  analysis/      # derived engineering calculations, when a vertical requires separation
  simulation/    # translation/run/result boundaries when required
  measures/      # invocation and packaged OpenStudio measures
  views/         # dataframe, Excel, JSON, notebook projections
  compat/        # temporary compatibility helpers where useful
```

Existing `osm_objects`, `tasks`, `utils`, and `resources/measures` remain in place initially. New vertical code uses the target boundaries; existing functions are wrapped or migrated opportunistically with tests.

Do not create every target directory at once. A directory is created when it receives production code for an accepted vertical. Extractors and analyses may remain together until their contracts or dependencies materially diverge.

## 6. Canonical Data Contracts

### 6.1 General rules

Canonical machine records use:

- Pydantic models at public boundaries.
- `snake_case` field names.
- Explicit unit suffixes such as `_m2`, `_m3`, `_w_per_m2_k` where appropriate.
- `schema_version` on released aggregate documents.
- Stable object identity using the OpenStudio handle plus type and optional name.
- Deterministic collection ordering, normally by object type, normalized name, then handle.
- JSON-compatible values with no OpenStudio SDK objects embedded.

Human labels such as `Floor Area {m2}` remain available through legacy dict/DataFrame views. They are not the preferred new machine contract.

### 6.2 Inventory document

The first aggregate contract is conceptually:

```text
ModelInventory
  schema_version
  source
    path
    sha256
  runtime
    openstudio_version
    energyplus_version
    python_version
  model
    building
    stories[]
    spaces[]
    thermal_zones[]
    surfaces[]
    subsurfaces[]
  counts
  warnings[]
```

The exact record fields are implemented from the needs of geometry QA/QC. The first version must not attempt to serialize every OpenStudio object.

### 6.3 Findings

Validators return structured findings rather than log text alone:

```text
Finding
  code
  severity        # info | warning | error
  message
  object_type
  object_handle
  object_name
  evidence
  suggested_action
```

Validation is observational. It never fixes the model automatically.

### 6.4 Transform results

Transforms return an explicit result with counts, warnings, errors, and a change set. The result states that the model was changed in memory. Saving the resulting model is a separate caller decision.

The existing `TaskResult` can evolve or be adapted into this contract. Existing legacy dictionaries remain supported during the compatibility period.

## 7. Read-Only and Mutation Policy

For the first vertical, read-only guarantees that the source file is not mutated on disk. It does not claim immutable OpenStudio objects in process. The guarantee is enforced through code boundaries rather than agent instruction alone:

- Extractors, validators, and analyses do not call SDK setters, `save`, translation-to-disk, or subprocesses.
- The capability adapter hashes the input before and after execution and fails if it changed.
- Tests verify input hash preservation for file-backed operations.
- Container or filesystem read-only mounts may be added later as defense in depth.

A setter accidentally called in memory would not be detected by a file hash if the model is never saved. Static review and focused tests enforce the operation convention; the acceptance-blocking guarantee for vertical 1 is preservation of the registered source file.

Mutation rules:

- Every transform is named as an action and declares `read_only = false` at the capability boundary.
- Preconditions run before mutation.
- Changes occur in memory and return a structured change set.
- The caller selects the output path and explicitly invokes persistence.
- Overwriting the registered input is disallowed by the controlled adapter.
- Released transformations retain input and output hashes.

## 8. Runtime and Dependency Policy

### 8.1 Python dependencies

`uv` is the required Python project and dependency manager for development and controlled execution:

- `pyproject.toml` remains the package definition.
- `uv.lock` pins Python dependencies after the first implementation change.
- Development commands use `uv sync`, `uv run`, and locked dependencies.
- Conda environments are not supported or documented.

### 8.2 OpenStudio and EnergyPlus

OpenStudio is not currently declared in `pyproject.toml`. The toolkit works only when an ambient interpreter happens to provide an importable binding. P1 therefore establishes an explicit, reproducible binding strategy for the first time; it does not merely refine an existing dependency declaration.

OpenStudio is not treated like an ordinary pure-Python dependency until the non-Conda proof determines whether the selected wheel or system distribution can be managed that way. The execution profile records and asserts the coupled stack:

- OpenStudio version
- EnergyPlus version
- Python version and executable
- Toolkit commit/version
- Platform as needed

The provisional reference profile is OpenStudio 3.10.0 with EnergyPlus 25.1.0, subject to an executable, non-Conda integration proof. The adapter must import the binding from the intended environment and assert `openstudio.openStudioVersion()` before loading a model.

Until that proof exists, 3.10.0 is a candidate profile, not a guaranteed supported profile. Generic `python3` must never be assumed to resolve the correct OpenStudio binding.

The runtime assertion and the no-on-disk-mutation boundary are the two acceptance-blocking technical guarantees across P1 and P2.

### 8.3 Version policy

- One reference profile first; no compatibility matrix before observed need.
- Toolkit releases declare verified profiles rather than broad claims such as `OpenStudio 3.x`.
- Runtime mismatch is a hard error in controlled execution.
- Exploration may use an unverified runtime only when outputs are clearly marked non-authoritative.

## 9. External Repositories and Integrations

### OpenStudio SDK

Use as the authoritative model API and vocabulary. Borrow separation between model, translation, workflow, measures, and utilities. Do not reproduce its class-per-IDD-object or C++ build architecture.

### openstudio-standards

Treat as a knowledge source and possible future external adapter for standards-driven baselines or checks. It is a Ruby/OpenStudio dependency and must not enter the Python core. Compatibility must be pinned by OpenStudio plus gem version.

### OpenStudio-HPXML

Use selectively as a reference for strict schemas, validation, packaged runtime releases, fixtures, and deterministic workflow testing. Defer integration unless R2F enters a residential HPXML use case.

### MCP servers

Defer MCP implementation decisions until the first capability contract is stable. The existing R2F MCP server remains a candidate for adaptation as an allowlisted thin transport. MCP must not duplicate toolkit logic or become the canonical API.

### Notebooks

Preserve existing notebooks as historical examples and human-facing recipes. Do not bulk-port them. Harvest logic only when a capability needs it, then make the notebook call the tested toolkit API.

## 10. Compatibility and Migration

The repository is version `0.2.0`; the next architecture should target a compatible `0.3.x` evolution rather than claim a complete 2.0 rewrite.

### Compatibility promises for the first migration stages

- Existing `openstudio_toolkit.osm_objects.*` imports continue to work.
- Existing dict outputs retain their human-readable keys.
- Existing DataFrame functions remain available.
- Existing task functions are not moved merely for structural purity.
- Deprecations include a replacement path and tests before removal.

### Migration mechanism

1. Build the new canonical contract for a real capability.
2. Reuse current extractors where correct, adapting their output at the boundary.
3. Add regression tests around relied-upon legacy behavior.
4. Move shared logic only when duplication or contract pressure is demonstrated.
5. Add compatibility wrappers when a public import must move.
6. Remove old surfaces only in a later, explicitly approved release.

The dirty historical worktree is not a migration source by default. Each unpublished change is reviewed independently before selective reapplication.

## 11. First Vertical: Inspect OpenStudio Model

### Purpose

Provide Simulation OS with a deterministic, read-only inventory for geometry and spatial review of a human-created OSM.

### In scope

- Assert the intended runtime before model loading.
- Hash and register the input path.
- Extract the geometry-relevant subset of building, stories, spaces, thermal zones, surfaces, and subsurfaces.
- Produce a versioned JSON inventory.
- Produce structured warnings for missing or inconsistent spatial relationships.
- Preserve the input hash.
- Support a DataFrame/Excel projection later without making it canonical.

### Out of scope

- Renaming or normalizing model objects.
- Adding Ideal Loads or changing HVAC.
- Saving or translating the model.
- Running EnergyPlus.
- Daylight, standards, or certification analysis.
- MCP exposure.
- Remote execution or containers.

### Acceptance criteria

1. Execution aborts when the asserted OpenStudio version does not match the reference profile.
2. The inventory validates against its Pydantic schema and serializes to deterministic JSON.
3. Repeated runs on the R2F Office Hub fixture produce identical semantic content and object counts.
4. The input SHA-256 is identical before and after execution.
5. No read-only operation contains a model setter or persistence call.
6. Inside the uv-managed environment, the imported OpenStudio binding resolves to the asserted version and is demonstrably not the ambient 3.6.1 interpreter previously observed.
7. The vertical is recorded as `validated-on-fixture` against R2F Office Hub. Determinism on that fixture does not establish generalization to other geometries.
8. Validation against East Gate remains pending until its first OSM exists.
9. Simulation OS requires a recorded human geometry-review decision before using the inventory as released evidence.

## 12. Testing Strategy

Use the smallest test pyramid that establishes trust:

- Unit tests for canonical schemas, ordering, views, and pure validators.
- Integration tests against small committed OSM fixtures under the exact asserted runtime.
- Golden JSON only for stable aggregate contracts; ignore or normalize volatile fields deliberately.
- Hash-preservation tests for every read-only file-backed capability.
- Mutation tests that verify in-memory changes and explicit persistence boundaries.
- Compatibility tests for public legacy imports used by notebooks and current tasks.

New and corrected tests must write generated artifacts to temporary directories, never tracked `tests/output` paths. The baseline violates this target: `tests/output/test_hard_size_hvac_result.osm` is currently tracked and must be moved or untracked in an approved cleanup change.

## 13. Delivery Phases

### P0 - Review and hygiene

Status: Completed 2026-06-20.

- Roberto approved the revised specification.
- Claude Opus architecture review completed; verified corrections incorporated.
- `feature/agent-first-core` created from the clean published baseline.
- The historical dirty worktree remains reference-only and was not merged.

### P1 - Runtime proof

Status: Completed 2026-06-20. See `docs/runtime/REFERENCE-PROFILE.md`.

- The uv-managed profile uses Python 3.13, OpenStudio 3.10.0, and EnergyPlus 25.1.0.
- The OpenStudio PyPI wheel supplies the verified Python binding; CLI execution remains outside this proof.
- Runtime inspection and hard assertion are implemented and tested.
- The assertion passes inside the managed environment and fails loudly for the known ambient mismatch.
- The complete suite passes under the locked profile.

### P2 - Inventory contract

- Implement the minimum geometry schemas and deterministic inventory.
- Reuse current extractors through adapters where practical.
- Add JSON serialization and input/output hashes.

### P3 - Pure geometry validators

- Add spatial mapping and naming findings.
- Generate geometry QA/QC findings without mutation.

### P4 - Simulation OS adapter and human gate

- Implement one direct Python capability adapter.
- Connect inventory evidence to the existing geometry review interview.
- Stop and evaluate before adding MCP, another runtime, or mutations.

## 14. Explicit Non-Decisions

This draft does not yet decide:

- The permanent product name for Simulation OS.
- Container versus VPS execution.
- The final MCP server implementation.
- Support for more than one OpenStudio profile.
- Whether every existing task should migrate to the target package shape.
- Whether Pandas remains a required core dependency or becomes an optional `views` extra.
- The final schema fields beyond those proven by the first vertical.

These decisions require evidence from implementation or a real project need.

## 15. Approval Questions

1. Is the toolkit boundary narrow enough, particularly the separation from Simulation OS workflows?
2. Is the incremental compatibility policy preferable to a fork or rewrite?
3. Should Pandas remain a base dependency during 0.3.x, then be reconsidered after the first vertical?
4. Is OpenStudio 3.10.0 plus EnergyPlus 25.1.0 acceptable as a provisional profile pending the non-Conda proof?
5. Are `ProjectSpec` and `TaskStep` correctly classified as compatibility surfaces whose future owner is Simulation OS?
6. Does the first vertical provide enough evidence before investing in MCP or infrastructure?
