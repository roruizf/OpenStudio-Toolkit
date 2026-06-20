# Claude Opus Review Brief - OpenStudio Toolkit vNext

## Role

Act as a skeptical principal architect. Review the attached `ARCHITECTURE-VNEXT.md` against the repository on disk. Do not implement, edit, install, move, or commit anything.

Your purpose is to cut unnecessary architecture, expose incorrect assumptions, and ensure the proposal evolves the existing toolkit rather than quietly rewriting it.

## Repository and evidence

- Clean repository: `/home/roruizf/projects/openstudio-toolkit`
- Baseline commit: `d3d625e4ff5bd79abb201adab4265525564c7f02`
- Architecture draft: `/home/roruizf/projects/openstudio-toolkit/docs/architecture/ARCHITECTURE-VNEXT.md`
- Historical dirty worktree: `/mnt/g/My Drive/R2F-EES/Development/openstudio-ecosystem/openstudio-toolkit`
- Simulation OS: `/home/roruizf/projects/r2f-simulation-os`
- Custom MCP candidate: `/home/roruizf/projects/openstudio-mcp-server`

The historical worktree is read-only evidence. Do not clean it, stash it, reset it, or use it as the implementation workspace.

## Established context

- Toolkit began as manually executed Python functions and Google Colab notebooks.
- It currently exposes many OpenStudio object extractors as dictionaries and Pandas DataFrames.
- It includes mutations, tasks, measures, Pydantic schemas, and a nascent `ProjectSpec` concept.
- Its future primary consumers are agents, skills, direct Python adapters, and potentially an MCP server.
- DataFrames and notebooks remain useful but should not dictate machine contracts.
- Robert-OS owns governance; Simulation OS owns project workflows and human gates; toolkit owns reusable domain operations.
- No total rewrite or restart is authorized.
- New Python dependency management must use `uv`; Conda is prohibited.
- The provisional stack is OpenStudio 3.10.0 plus EnergyPlus 25.1.0, but the non-Conda binding path is not yet proven.
- Generic `python3` previously imported OpenStudio 3.6.1 while the CLI was 3.10.0; silent mismatch is a blocking risk.
- The first vertical is read-only model inventory and geometry QA/QC.
- MCP, VPS/container infrastructure, multi-runtime support, and mutations are deferred.

## External references already assessed

- OpenStudio SDK should influence conceptual boundaries, not be copied as a directory tree.
- `openstudio-standards` is a knowledge source and possible future isolated adapter, not a Python core dependency.
- OpenStudio-HPXML is useful for schema, validation, packaging, and test patterns but not currently relevant as a runtime integration.

Verify these claims from official sources only if necessary. Do not expand the audit into a general ecosystem survey.

## Review questions

1. Which statements in the draft are unsupported by the current repository?
2. Does the proposed target package shape solve observed problems, or is it premature taxonomy?
3. Is the distinction among extractor, validator, analysis, transform, capability, adapter, and view clear and minimal?
4. Does the canonical-record approach preserve the legitimate value of existing DataFrame APIs?
5. Is the migration path truly incremental, including current imports, tasks, measures, schemas, and notebooks?
6. Are `ProjectSpec` and `TaskStep` correctly assigned away from the toolkit, or is that separation artificial?
7. Is `uv` sufficient for the Python layer while OpenStudio remains an externally coupled runtime? Identify the smallest credible non-Conda profile proof.
8. Is OpenStudio 3.10.0 the right provisional target given the current code and available bindings, or should the draft avoid selecting it yet?
9. Are read-only guarantees enforceable as written? Identify any missing technical boundary.
10. Is the first vertical small enough and valuable enough to validate the architecture?
11. What should be deleted, deferred, or rewritten in the specification before implementation?
12. What repo-level risks, dirty-state risks, licensing issues, or test gaps are missing?

## Required output

Return:

1. Verdict: accept, accept with changes, or reject.
2. Findings ordered by severity with file/line evidence.
3. A table of accept/modify/reject for each major architectural decision.
4. The minimum architecture you recommend after making cuts.
5. Exact changes required in `ARCHITECTURE-VNEXT.md` before approval.
6. A smallest-credible P1 runtime proof using `uv` and no Conda.
7. Confirmation or revision of the first vertical and its acceptance criteria.
8. Decisions that require Roberto's approval.

Do not produce implementation code. Stop at architectural review.
