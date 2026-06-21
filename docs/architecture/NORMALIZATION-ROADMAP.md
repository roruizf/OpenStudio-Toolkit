# First Vertical Normalization Roadmap

Status: Active
Date: 2026-06-20

## Completed

- P0: architecture review and clean standalone repository.
- P1: verified uv/OpenStudio runtime.
- P2.1: canonical inventory schemas and serialization.
- P2.2: read-only SDK extractor and portable run envelope.
- P2.3: compatibility, edge fixtures, and caller-owned artifact evidence.
- P3 contract: Finding ownership, severity, validator boundaries, and naming-profile gating reviewed.
- P3.1: deterministic findings plus pure integrity and spatial validators.
- P3.2: profile-driven naming, composition, and portable QA/QC evidence.

## Remaining Checkpoints

1. **P4 integration:** P4a execution/evidence and P4b disposition/release gate — complete and checkpointed in `r2f-simulation-os` (`f36730c`, `b73bee3`).
2. **Vertical closure:** end-to-end fixture run wiring P4b outputs into the phase lifecycle — complete on the R2F Office Hub fixture plus a synthetic approved naming profile (see `r2f-simulation-os/docs/vertical-closure-evidence.md`). Read-only inventory/QA capability maturity stays `provisional` until validated on East Gate's first OSM.
   - Still pending and gated on Roberto approval: East Gate validation when its OSM exists, toolkit version `0.3.x`, reachable immutable pin replacing the local `git+file://` source, and branch review/merge/tag.

Do not add MCP, containers, remote execution, a second runtime, or mutation tools inside these checkpoints.

## After Normalization

Stop and evaluate the completed vertical rather than extending the taxonomy automatically.

Decision order:

1. Run the vertical on East Gate's first OSM and record gaps, maintenance cost, and human usefulness.
2. Select the next capability from observed project need.
3. Likely next candidate: controlled naming/model-setup mutations with preview, change set, save-as, and human approval.
4. Reassess the custom OpenStudio MCP only after at least one read-only and one controlled-mutation capability have stable contracts.
5. Add container/VPS infrastructure only when reproducibility or remote execution creates a demonstrated need.
6. Consider standards, simulation, results, Ladybug, or HPXML adapters as separate verticals driven by project scope.

The objective after normalization is delivery through real projects, not continuous framework construction.
