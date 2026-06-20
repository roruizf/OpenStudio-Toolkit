# P3 Contract Review Decision

Date: 2026-06-20
Decision: Accept with applied changes

## Applied Cuts

- Removed `spatial.space.missing_space_type`; an assigned OSM SpaceType is not equivalent to the project preliminary use concept.
- Restricted toolkit naming validation to pattern and model-relationship conformance.
- Kept Room-ID lineage reconciliation in Simulation OS, where the Room-to-Space mapping exists.
- Made duplicate-name severity class-aware: major for Spaces/ThermalZones, minor for other scoped geometry objects.
- Declared findings revision-scoped; Simulation OS re-runs and re-dispositions on a new model revision.
- Collapsed P3 from four internal checkpoints to two.

## East Gate Decision

The naming conflict is explicitly deferred:

- Hyphen grammar in `model-object-naming-profile.md`.
- Double-underscore grammar in `geometry-and-zoning-strategy.md`.

No East Gate naming conformance will be claimed until Roberto approves one profile revision. This does not block P3.1 integrity and spatial validators.

## P3.1 Scope

- Finding and NamingProfile schemas.
- Deterministic ordering.
- Pure integrity validator.
- Pure spatial-assignment validator.
- Synthetic and Office Hub tests.

No naming validator, composer, automatic fix, disposition, OpenStudio access, or file output is included in P3.1.
