# P3 Findings And Pure Validators Contract

Status: P3.1 and P3.2 implemented and verified
Date: 2026-06-20
Scope: Geometry and spatial QA/QC over canonical `ModelInventory`

## 1. Purpose

Convert inventory facts into deterministic, structured QA/QC findings without loading, modifying, saving, or translating an OpenStudio model.

P3 validators consume only `ModelInventory` plus an explicit project profile where required. They never consume SDK objects, DataFrames, prompts, workbook state, or implicit project conventions.

## 2. Ownership Boundary

### Toolkit owns

- Finding and validator-profile schemas.
- Pure deterministic validation functions.
- Stable finding codes and default severities.
- Evidence derived from the canonical inventory.
- Deterministic finding ordering.
- Validator unit tests and fixture evidence.

### Simulation OS owns

- Project Room register and Room-to-Space mapping.
- Selection and approval of the project naming profile.
- Finding disposition: `open`, `accepted`, `corrected`, or `deferred`.
- Human exceptions, rationale, owner, due date, and release decision.
- Comparison against project sources and expected room/space registers.
- Geometry release gate and artifact persistence.

The toolkit reports facts and conformance. It does not approve exceptions or release geometry.

## 3. Finding Contract

```text
Finding
  code
  severity
  message
  object_type
  object_handle
  object_name
  related_handles[]
  evidence{}
  suggested_action
  profile_id
  profile_version
```

### Fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `code` | string | yes | Stable dotted rule identifier |
| `severity` | enum | yes | `blocker`, `major`, `minor`, or `observation` |
| `message` | string | yes | Human-readable explanation, not the identity |
| `object_type` | enum | yes | `model`, `building_story`, `space`, `thermal_zone`, `surface`, or `subsurface` |
| `object_handle` | string or null | yes | Primary affected object |
| `object_name` | string or null | yes | Human label at validation time |
| `related_handles` | list of strings | yes | Other directly relevant objects |
| `evidence` | JSON object | yes | Expected/actual and measured facts |
| `suggested_action` | string or null | yes | Proposed next action; never an automatic mutation |
| `profile_id` | string or null | yes | Naming/profile source when applicable |
| `profile_version` | string or null | yes | Exact profile revision when applicable |

### Deliberate exclusions

- No timestamp: it would make findings non-deterministic.
- No disposition/status: workflow state belongs to Simulation OS.
- No user, owner, or approval: human governance belongs to Simulation OS.
- No stable cross-revision finding ID yet: OpenStudio handles are revision-local, and project stable IDs are not part of `ModelInventory`.
- No proposed model patch in P3.

Findings are scoped to one model revision. When a new revision is inspected, Simulation OS re-runs validators and re-associates or re-dispositions findings; no cross-revision identity is implied.

## 4. Finding Determinism

Validators return findings sorted by:

1. severity rank: blocker, major, minor, observation;
2. code;
3. object type;
4. normalized object name;
5. object handle.

`related_handles` are sorted. Evidence keys serialize canonically. Repeated validation of the same inventory/profile produces byte-equivalent findings.

Message text may improve in later schema versions; downstream logic must use `code`, not parse messages.

## 5. Severity Policy

Use the active Simulation OS geometry-phase meaning:

| Severity | Toolkit interpretation |
|---|---|
| `blocker` | Inventory/model relationships are internally inconsistent or cannot be trusted |
| `major` | Could materially affect geometry, physics, scope, adjacency, zoning, or reporting |
| `minor` | Traceability, naming, or low-impact inconsistency |
| `observation` | Review item, profile gap, or future improvement that does not block release by itself |

Severity is the default phase treatment. Simulation OS may accept or defer a finding but must not silently rewrite the finding's original severity.

## 6. Validator Classes

The classes below are organizational tags, not a class hierarchy.

### 6.1 Inventory integrity

Function:

```python
validate_inventory_integrity(inventory: ModelInventory) -> list[Finding]
```

Initial rules:

| Code | Default severity | Condition |
|---|---|---|
| `integrity.reference.unresolved` | blocker | A scoped handle references an object absent from its inventory collection |
| `integrity.relationship.nonreciprocal` | blocker | Parent/child or adjacency relationships disagree |
| `integrity.name.duplicate` | class-aware | Duplicate Space or ThermalZone names are major; duplicate Story, Surface, or SubSurface names are minor |
| `integrity.name.missing` | minor | A controlled geometry object has no visible name |
| `integrity.geometry.nonpositive_space_area` | major | Space floor area is zero or negative |
| `integrity.geometry.nonpositive_space_volume` | major | Space volume is zero or negative |
| `integrity.geometry.invalid_surface_polygon` | blocker | Surface has fewer than three vertices or non-positive gross area |
| `integrity.geometry.invalid_subsurface_polygon` | major | SubSurface has fewer than three vertices or non-positive gross area |
| `integrity.geometry.subsurface_exceeds_surface` | major | Aggregated gross SubSurface area exceeds parent gross Surface area beyond numeric tolerance |

This validator is project-independent.

### 6.2 Spatial assignment

Function:

```python
validate_spatial_assignments(inventory: ModelInventory) -> list[Finding]
```

Initial rules:

| Code | Default severity | Condition |
|---|---|---|
| `spatial.space.missing_story` | major | Space has no BuildingStory |
| `spatial.space.missing_thermal_zone` | major | Space has no candidate ThermalZone assignment |
| `spatial.surface.missing_space` | major | Surface is orphaned from a Space |
| `spatial.subsurface.missing_surface` | major | SubSurface is orphaned from a Surface |
| `spatial.space.no_surfaces` | blocker | Space contains no Surfaces |
| `spatial.thermal_zone.no_spaces` | observation | ThermalZone contains no Spaces |
| `spatial.story.no_spaces` | observation | BuildingStory contains no Spaces |

These defaults match the R2F Geometry phase. A generic OpenStudio model may intentionally omit some assignments; Simulation OS handles approved exceptions rather than weakening the observed finding.

### 6.3 Naming conformance

Function:

```python
validate_model_object_naming(
    inventory: ModelInventory,
    profile: NamingProfile,
) -> list[Finding]
```

Naming conformance is never run without an explicit profile.

Toolkit naming validation is limited to pattern shape and relationships visible in `ModelInventory`. Verifying that every source Room ID is preserved in a Space name requires the Room-to-Space mapping and remains exclusively Simulation OS responsibility.

Initial rules:

| Code | Default severity | Condition |
|---|---|---|
| `naming.space.profile_mismatch` | minor | Space name does not match approved project pattern shape; it does not prove Room lineage |
| `naming.thermal_zone.one_to_one_mismatch` | minor | A one-Space zone is not named from that Space according to profile |
| `naming.thermal_zone.multi_space_rule_missing` | observation | Profile does not define naming for a multi-Space zone |
| `naming.surface.owner_mismatch` | minor | Surface name does not expose actual owning Space |
| `naming.surface.relationship_mismatch` | minor | Surface name does not expose actual type and boundary/adjacent Space |
| `naming.surface.sequence_missing` | minor | Surface name lacks required positive sequence |
| `naming.subsurface.parent_mismatch` | minor | SubSurface name does not inherit actual parent Surface |
| `naming.subsurface.type_or_sequence_mismatch` | minor | SubSurface type/sequence does not match profile |
| `naming.profile.incomplete` | observation | Required grammar is absent or explicitly unresolved |

P3 only reports mismatches. Deterministic rename previews and mutation belong to a later controlled-mutation vertical.

## 7. NamingProfile Contract

```text
NamingProfile
  profile_id
  version
  status
  space_pattern
  one_to_one_zone_template
  multi_space_zone_pattern
  surface_separator
  subsurface_separator
  require_surface_sequence
  require_subsurface_sequence
```

### Rules

- `status` is `draft` or `approved`.
- Running a draft profile is allowed for preview but adds `naming.profile.draft` as an observation.
- `space_pattern` is a regular expression selected by the project, not a toolkit default.
- The default reusable relationship grammar may be represented in a profile, but is not silently activated.
- Multi-Space Thermal Zone validation runs only when the profile defines its grammar.
- Exceptions/dispositions remain outside the profile and outside the toolkit.

### East Gate conflict requiring human resolution

Current project documents disagree:

- `model-object-naming-profile.md` v0.2: hyphen grammar such as `B2-0.03-0.07-Restroom`.
- `geometry-and-zoning-strategy.md`: double-underscore grammar such as `B2-1.21__sales-manager-office`.

The naming profile is the intended governing document but remains `active-draft-pending-human-approval`. P3 must not hardcode either grammar or claim East Gate naming conformance until Roberto approves one profile revision. This decision is explicitly deferred and blocks only East Gate naming validation, not integrity or spatial validation.

## 8. Composition

P3 exposes a small composer:

```python
validate_geometry_inventory(
    inventory: ModelInventory,
    *,
    naming_profile: NamingProfile | None = None,
) -> list[Finding]
```

It always runs integrity and spatial assignment validators. Naming runs only when a profile is supplied. The composer sorts and de-duplicates exact duplicate findings; it does not change severity or disposition.

## 9. Purity And Safety

Validators:

- accept immutable-by-convention canonical records;
- do not import OpenStudio or Pandas;
- do not read files, environment variables, clocks, or network resources;
- do not mutate inventory or profile;
- do not write artifacts;
- do not infer missing project mappings or naming rules;
- return findings even when severe issues exist, unless the inventory itself cannot be validated.

## 10. Acceptance Criteria

1. Finding schema rejects unknown severities, object types, and extra fields.
2. Identical inventory/profile inputs produce identical ordered findings.
3. Validators do not change canonical inventory bytes or hash.
4. Integrity rules detect broken and non-reciprocal synthetic relationships.
5. Spatial rules detect the P2.3 null-assignment/orphan fixture.
6. Office Hub produces no unresolved-reference or orphan-geometry findings.
7. Naming validators require an explicit profile and identify relationship-derived stale names.
8. A draft profile emits an observation and never becomes silently approved.
9. Legacy extractors/DataFrames remain unchanged.
10. Full toolkit suite continues to pass.

## 11. Implementation Sequence

### P3.1 - Findings, integrity, and spatial validation

- Implement `Finding`, `NamingProfile`, ordering, integrity rules, spatial rules, and tests.
- Exclude OSM SpaceType assignment as a proxy for the project preliminary use concept.

### P3.2 - Naming, composition, and QA/QC evidence

- Implement derived ownership checks.
- Use synthetic approved profiles for tests.
- Do not claim East Gate conformance until its profile is approved.
- Compose deterministic findings for Office Hub.
- Produce caller-owned temporary JSON/Markdown projections.
- Stop before automatic fixes, dispositions, or release gating.

## 12. Approval Decisions

1. Approve Finding without workflow disposition/status.
2. Approve the four-level severity taxonomy from Simulation OS.
3. Approve profile-independent integrity/spatial rules and profile-driven naming rules.
4. Approve missing ThermalZone/Story as findings with human exception handling outside the toolkit; preliminary use/SpaceType concept remains Simulation OS-owned.
5. Explicitly defer the East Gate naming grammar conflict until human approval; integrity/spatial validation may proceed.
6. Approve P3.1 as the next code checkpoint after review.
