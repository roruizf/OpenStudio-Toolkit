# P4 Contract Review Decision

Date: 2026-06-21
Decision: Accept with applied changes; implementation blocked on Git checkpoints

## Applied Changes

- Distinguished `source_osm_sha256` from `inventory_artifact_sha256` and `report.inventory_sha256`.
- Made `report.inventory_sha256 == artifacts[role=inventory].sha256` an explicit invariant.
- Replaced ambiguous required checks with explicit `checks_requested` and phase-owned `release_required_checks`.
- Made `uv_lock_sha256` authoritative and `toolkit_git_sha` best-effort pin/build provenance.
- Required sibling staging under the final artifact parent for same-filesystem atomic rename.
- Bound dispositions to both report hash and validator-suite version.
- Added release-time OSM re-hash regardless of human decision.
- Split implementation into P4a execution/evidence and P4b disposition/release.

## Blocking Gates

1. Commit the verified P3 toolkit work so Simulation OS can pin an immutable dependency.
2. Create an intentional initial Simulation OS baseline; the repository currently has no `HEAD` and zero tracked files.

No P4 implementation begins until both are approved and complete.

## Approved Architecture

- Stable capability plus one pinned adapter; no registry or plugin framework.
- Immutable execution bundle, mutable disposition/current-truth records, explicit release record.
- Existing Review Interview remains the human-governance mechanism.
- Blockers must be absent; current majors require accepted human exception; all remaining findings require explicit disposition.
- Zero findings never bypasses visual review or explicit human approval.
- East Gate remains deferred until its first OSM, approved naming grammar, and Room-to-Space mapping exist.
