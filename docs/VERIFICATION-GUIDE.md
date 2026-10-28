# Verifying a model version

**When:** every time a new version of a model is saved, **before** it is entered in the project's
`MODEL-REGISTER.md`.
**Who:** whoever made the change, a person or an agent.
**Why:** to confirm that the new model (the *child*) has what was requested, and to see every other change
against the previous version (the *parent*), so that nothing changes by accident.

## What you need

- The parent model (the version the change started from) and the child model (the new version), both
  `.osm`. Work on copies; the toolkit never modifies an input model.
- The request as a **mapping** file in JSON: family -> {Space name -> requested total}. The families are
  `people` (people), `lights` (W) and `electric_equipment` (W). Example, lighting from ASHRAE 90.1 Table G3.7
  × each Space's floor area:

  ```json
  {"lights": {"1.10-MeetingRoom": 335.76, "0.05-Storage": 43.05, "1.24-Office": 130.24}}
  ```

  (Three of the 36 Spaces of R2F Office Hub; values rounded here.)

  The value is the total that reaches the Space, whether the load sits on the Space or on its space type,
  as EnergyPlus simulates it.

## Steps

1. **Verify** parent -> child and write the report:

   ```
   openstudio-toolkit diff actual-017.osm reference-011.osm --mapping g37.json --tolerance 0.5 \
       --report verification.html --language es
   ```

   On Office Hub (actual-017 -> reference-011, G3.7 lighting) this prints:

   ```
   diff: 14 added, 5480 not_requested, 72 removed
   child vs mapping: 36 match
   report -> verification.html
   ```

   Use `--tolerance 0.5` (W per Space) for G3.7 mappings: the table is rounded to two decimals in SI, the
   model holds the exact IP value.

2. **Read the exit code:** `0` the child matches the mapping; `1` at least one Space differs or is missing;
   `2` the command could not run (file not found, bad mapping). An agent must not register the version
   unless the code is `0`.

3. **Read the report** (`verification.html`, one self-contained file):
   - *Child vs requested*: every row should be `match`. A `differs` row shows the requested value, the value
     in the model and the difference.
   - *Changes not requested*: there is no ideal state. Read them, by building part (Spaces, envelope, air
     systems, zone equipment, plants, schedules, other) and by location (Space, Thermal Zone, System), and
     confirm that each one was intended. A schedule or construction used in several places shows
     "shared (used by N)".
   - Counts are rows of changes (one per changed field, one per added or removed object), not objects.

4. **Register** the version in `MODEL-REGISTER.md` only when the request matches and every not-requested
   change is understood. Note the report next to the version.

## Other commands

| Command | What it does |
|---|---|
| `openstudio-toolkit compare child.osm --mapping g37.json --out compare.csv` | Only the request check (exit 0/1). |
| `openstudio-toolkit apply parent.osm child.osm --mapping g37.json [--existing update]` | Writes the child with the requested per-Space loads. By default it refuses a Space that already has a load; `--existing update` changes only the value of a single, unshared load. A load coming from the space type is always refused, so it is never doubled. |
| `openstudio-toolkit dump model.osm --families lights,space --out dump/` | One CSV per family, as OpenStudio resolves it. |
| `openstudio-toolkit results eplusout.sql end_uses --units GJ=kWh` | Results of a simulation: `zone_sizes`, `system_sizes`, `unmet_hours`, `end_uses`. EnergyPlus units unless `--units` is given (`GJ=kWh`, `m3/s=m3/h`, `m3/s=L/s`, `W=kW`). |
