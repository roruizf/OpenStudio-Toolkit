# P2 Model Inventory Contract

Status: P2.1 implemented and reviewed; pending checkpoint
Date: 2026-06-20
Target capability: `inspect-openstudio-model`

## 1. Purpose

Define the smallest canonical, deterministic, read-only representation of an OpenStudio model needed for geometry and spatial review.

This contract is a toolkit domain artifact. Simulation OS owns project registration, workflow state, human review, and release decisions. DataFrame, Excel, CLI, and MCP representations are consumers of this contract, not its source of truth.

## 2. Evidence From the Current Repository

The existing `osm_objects` modules provide useful field semantics and human-oriented dict/DataFrame APIs, but they are not the canonical inventory implementation:

- Relationships are usually represented by object names rather than stable handles.
- Building extraction exists only as a DataFrame.
- Geometry fields such as areas, vertices, and orientation are inconsistent or optional.
- Shared helpers and 22 object modules currently import Pandas.
- A whole-model probe composed from legacy extractors did not complete within several minutes on Office Hub. The specific expensive field or call has not been isolated; the batch helpers themselves do pass direct object references.
- A direct, linear SDK traversal of the same model completed after model load in approximately 0.004 seconds; loading plus traversal took approximately 1.3 seconds.

Verified Office Hub baseline under the P1 runtime:

| Object | Count |
|---|---:|
| Building stories | 2 |
| Spaces | 36 |
| Thermal zones | 36 |
| Surfaces | 278 |
| Subsurfaces | 53 |

All Office Hub spaces have stories and thermal zones. All surfaces have spaces, and all subsurfaces have parent surfaces.

Decision: P2 traverses each SDK collection once and extracts only the scoped fields directly from object references. Existing functions remain unchanged and may reuse the new records later through compatibility wrappers. This decision is based on the measured minimal traversal, not on an unproven diagnosis of the legacy slowdown.

## 3. Contract Boundary

### In scope

- Source identity and SHA-256.
- Verified runtime facts.
- Building identity and orientation.
- Stories, spaces, thermal zones, surfaces, and subsurfaces.
- Stable handle-based relationships plus optional names for human readability.
- Geometry quantities required for spatial QA/QC.
- Explicit coordinate-frame metadata.
- Deterministic JSON serialization and artifact hash.
- Input hash preservation.

### Out of scope

- Validation findings or suggested fixes; these start in P3.
- Constructions, materials, schedules, loads, HVAC, and simulation settings.
- Model mutation, save, translation, measures, or EnergyPlus execution.
- DataFrame and Excel views.
- MCP or CLI transport.
- Project identifiers, workflow state, release approval, or reviewer metadata.
- A complete serialization of every OpenStudio object.

## 4. Aggregate Shape

```text
ModelInventory
  schema_version
  source
  runtime
  building
  counts
  stories[]
  spaces[]
  thermal_zones[]
  surfaces[]
  subsurfaces[]
```

`schema_version` begins at `0.1.0`. It versions the inventory contract independently from the toolkit package.

The JSON artifact SHA-256 is returned alongside the serialized bytes. It is not embedded in `ModelInventory`, avoiding a self-referential hash.

## 5. Common Rules

- Public records are Pydantic models.
- Public field names use `snake_case`.
- Units appear in field names.
- OpenStudio handles are strings and are the canonical relationship keys.
- Names are nullable labels and must never be used as unique identifiers.
- Missing optional SDK values serialize as JSON `null`, never as SWIG optional objects.
- OpenStudio SDK objects never cross the contract boundary.
- Numeric values retain SDK precision. Rounding belongs to human views.
- Collections sort by normalized name and then handle. A missing name sorts as an empty string.
- JSON is UTF-8 with stable field order and deterministic separators.
- The canonical extractor does not import Pandas.
- Records are frozen at the top level, but nested collections remain mutable in schema `0.1.x`.
- Determinism is guaranteed only for build-once records that are not mutated after construction. Serialization does not re-normalize post-construction mutations.

### 5.1 Field lineage and human translation

Canonical names do not replace OpenStudio terminology. Each directly sourced schema field carries machine-readable metadata for:

- `osm_label`: the comment label shown in OSM text, such as `Floor Area {m2}`.
- `sdk_accessor`: the OpenStudio SDK method, such as `Space.floorArea()`.
- `legacy_key`: the current dict/DataFrame key when one exists.
- `lineage_note`: clarification when canonical semantics differ from the legacy projection.

Example:

| Canonical field | OSM label | SDK accessor | Legacy key |
|---|---|---|---|
| `floor_area_m2` | `Floor Area {m2}` | `Space.floorArea()` | `Floor Area {m2}` |
| `story_handle` | `Building Story Name` | `Space.buildingStory().handle()` | none; legacy resolves the reference to a name |
| `story_name` | derived from `Building Story Name` | `Space.buildingStory().name()` | `Building Story Name` |

This metadata is the source for a human-readable field map in `docs/contracts/`. Canonical JSON always uses `snake_case`. Existing legacy dict/DataFrame APIs retain their human-readable keys during the compatibility period.

## 6. Records

### 6.1 SourceRecord

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `path` | string | yes | Input path as supplied to the controlled adapter |
| `filename` | string | yes | Basename for portable display |
| `sha256` | string | yes | Hash before model loading |
| `size_bytes` | integer | yes | Source file size |

The toolkit does not decide whether `path` is project-relative or absolute. The adapter supplies the registered path policy.

### 6.2 RuntimeRecord

Reuse the serialized facts from P1 `RuntimeInfo`:

- `python_version`
- `python_executable`
- `openstudio_version`
- `energyplus_version`
- `openstudio_module_path`

Controlled extraction calls `assert_reference_runtime()` before loading the model.

### 6.3 BuildingRecord

| Field | Type | Required |
|---|---|---:|
| `handle` | string | yes |
| `name` | string or null | yes |
| `north_axis_deg` | float | yes |
| `floor_area_m2` | float | yes |
| `conditioned_floor_area_m2` | float or null | yes |

### 6.4 StoryRecord

| Field | Type | Required |
|---|---|---:|
| `handle` | string | yes |
| `name` | string or null | yes |
| `nominal_z_m` | float or null | yes |
| `nominal_floor_to_floor_height_m` | float or null | yes |
| `nominal_floor_to_ceiling_height_m` | float or null | yes |
| `space_handles` | list of strings | yes |

### 6.5 SpaceRecord

| Field | Type | Required |
|---|---|---:|
| `handle` | string | yes |
| `name` | string or null | yes |
| `story_handle` | string or null | yes |
| `story_name` | string or null | yes |
| `thermal_zone_handle` | string or null | yes |
| `thermal_zone_name` | string or null | yes |
| `space_type_handle` | string or null | yes |
| `space_type_name` | string or null | yes |
| `part_of_total_floor_area` | boolean | yes |
| `floor_area_m2` | float | yes |
| `volume_m3` | float | yes |
| `x_origin_m` | float | yes |
| `y_origin_m` | float | yes |
| `z_origin_m` | float | yes |
| `direction_of_relative_north_deg` | float | yes |
| `surface_handles` | list of strings | yes |

### 6.6 ThermalZoneRecord

| Field | Type | Required |
|---|---|---:|
| `handle` | string | yes |
| `name` | string or null | yes |
| `multiplier` | integer | yes |
| `space_handles` | list of strings | yes |

HVAC equipment and thermostat fields are deliberately excluded from the geometry inventory.

### 6.7 Point3D

| Field | Type | Required |
|---|---|---:|
| `x_m` | float | yes |
| `y_m` | float | yes |
| `z_m` | float | yes |

For P2, surface and subsurface vertices preserve the coordinates returned by the SDK object and provisionally declare `coordinate_system = "space_local"`. Space origin and relative north are included so later consumers can transform deliberately. P2.2 must verify this frame with a synthetic space having non-zero origin and rotation. If that test contradicts the label, the schema is corrected before `0.1.0` is released. P2 must not label coordinates as site coordinates without a separately verified transformation.

### 6.8 SurfaceRecord

| Field | Type | Required |
|---|---|---:|
| `handle` | string | yes |
| `name` | string or null | yes |
| `space_handle` | string or null | yes |
| `space_name` | string or null | yes |
| `surface_type` | string | yes |
| `outside_boundary_condition` | string | yes |
| `adjacent_surface_handle` | string or null | yes |
| `construction_handle` | string or null | yes |
| `construction_name` | string or null | yes |
| `sun_exposure` | string | yes |
| `wind_exposure` | string | yes |
| `gross_area_m2` | float | yes |
| `net_area_m2` | float | yes |
| `coordinate_system` | literal `space_local` | yes |
| `vertices` | list of `Point3D` | yes |
| `subsurface_handles` | list of strings | yes |

Do not add cardinal orientation labels in P2. They are derived analysis and require a separately tested coordinate/orientation convention.

### 6.9 SubSurfaceRecord

| Field | Type | Required |
|---|---|---:|
| `handle` | string | yes |
| `name` | string or null | yes |
| `surface_handle` | string or null | yes |
| `surface_name` | string or null | yes |
| `subsurface_type` | string | yes |
| `construction_handle` | string or null | yes |
| `construction_name` | string or null | yes |
| `multiplier` | float | yes |
| `gross_area_m2` | float | yes |
| `net_area_m2` | float | yes |
| `coordinate_system` | literal `space_local` | yes |
| `vertices` | list of `Point3D` | yes |

### 6.10 ModelCounts

Counts are explicit for quick integrity checks:

- `stories`
- `spaces`
- `thermal_zones`
- `surfaces`
- `subsurfaces`

Counts must equal the corresponding collection lengths when the Pydantic model is created.

## 7. Extraction API

The first public API should remain narrow:

```python
inspect_model(path: Path, *, registered_path: str | None = None) -> ModelInventory
serialize_inventory(inventory: ModelInventory) -> InventoryArtifact
```

`InventoryArtifact` contains canonical JSON bytes and `sha256`. It is an in-memory result; writing to disk is the adapter's responsibility.

Implementation constraints:

- Assert the P1 runtime first.
- Hash before loading and again after extraction.
- Fail if the input hash changes.
- Load through `VersionTranslator` and fail explicitly when uninitialized.
- Traverse each SDK collection once.
- Extract from direct object references; do not re-fetch every object by name or handle.
- Do not call setters, `save`, translators to disk, subprocesses, measures, or simulation.

## 8. Error Policy

P2 raises explicit exceptions for:

- Runtime mismatch.
- Missing or unreadable input.
- Input hash change.
- Model load failure.
- Contract validation failure.

Missing relationships such as a space without a story are valid nullable facts in P2. They become structured findings in P3 rather than extraction failures.

## 9. Acceptance Criteria

1. The extractor runs only under the asserted P1 profile.
2. Office Hub produces exactly 2 stories, 36 spaces, 36 thermal zones, 278 surfaces, and 53 subsurfaces.
3. All Office Hub relationship handles resolve to objects present in the inventory.
4. Repeated runs produce byte-identical canonical JSON and the same artifact SHA-256.
5. The source SHA-256 is unchanged before and after each run.
6. Pydantic rejects inconsistent collection counts.
7. Optional SDK values become floats or `null`, never SWIG proxy objects.
8. The new canonical extractor and schemas do not import Pandas.
9. Existing `osm_objects` and DataFrame APIs continue to pass their tests unchanged.
10. No output file is written by the toolkit extraction or serialization functions.
11. The Office Hub result is recorded as `validated-on-fixture`; East Gate remains pending.
12. A synthetic translated and rotated space verifies the declared vertex coordinate frame before schema `0.1.0` is accepted.

No hard timing threshold is an acceptance gate. The direct SDK probe is recorded as a benchmark to detect accidental reintroduction of expensive broad-field traversal.

## 10. Minimal Implementation Sequence

### P2.1 - Schemas and canonical serialization

- Add only the Pydantic records listed here.
- Test counts, optional values, deterministic sorting, and serialization without OpenStudio.

### P2.2 - Direct SDK extractor

- Add one read-only traversal for the six scoped collections.
- Test the small fixture first, then Office Hub.
- Record source and artifact hashes.

### P2.3 - Compatibility and evidence

- Run the complete legacy suite.
- Compare canonical counts with SDK collection counts.
- Produce one non-versioned Office Hub JSON artifact in a temporary directory.
- Stop before validators, DataFrame views, CLI, or MCP.

## 11. Approval Decisions

1. Approve direct SDK traversal instead of composing legacy extractors.
2. Approve vertices in `space_local` coordinates plus explicit space transforms, deferring site-coordinate conversion.
3. Approve handle-based relationships with nullable names as labels.
4. Approve keeping findings and validation outside `ModelInventory` until P3.
5. Approve P2.1 as the next implementation increment.
