# Model Inventory Field Map

The canonical inventory uses `snake_case` for stable Python and JSON contracts. OpenStudio OSM labels and legacy dict/DataFrame keys remain documented and available as schema metadata.

## Space

| Canonical field | OSM/IDD label | SDK accessor | Legacy key or note |
|---|---|---|---|
| `handle` | `Handle` | `Space.handle()` | `Handle` |
| `name` | `Name` | `Space.name()` | `Name` |
| `story_handle` | `Building Story Name` | `Space.buildingStory().handle()` | OSM stores the referenced handle |
| `story_name` | derived from `Building Story Name` | `Space.buildingStory().name()` | `Building Story Name` |
| `thermal_zone_handle` | `Thermal Zone Name` | `Space.thermalZone().handle()` | OSM stores the referenced handle |
| `thermal_zone_name` | derived from `Thermal Zone Name` | `Space.thermalZone().name()` | `Thermal Zone Name` |
| `space_type_handle` | `Space Type Name` | `Space.spaceType().handle()` | OSM stores the referenced handle |
| `space_type_name` | derived from `Space Type Name` | `Space.spaceType().name()` | `Space Type Name` |
| `part_of_total_floor_area` | `Part of Total Floor Area` | `Space.partofTotalFloorArea()` | `Part of Total Floor Area` |
| `floor_area_m2` | `Floor Area {m2}` | `Space.floorArea()` | `Floor Area {m2}` |
| `volume_m3` | `Volume {m3}` | `Space.volume()` | `Volume {m3}` |
| `x_origin_m` | `X Origin {m}` | `Space.xOrigin()` | `X Origin {m}` |
| `y_origin_m` | `Y Origin {m}` | `Space.yOrigin()` | `Y Origin {m}` |
| `z_origin_m` | `Z Origin {m}` | `Space.zOrigin()` | `Z Origin {m}` |
| `direction_of_relative_north_deg` | `Direction of Relative North {deg}` | `Space.directionofRelativeNorth()` | `Direction of Relative North {deg}` |
| `surface_handles` | derived relationship | `Space.surfaces()` | New canonical relationship |

## Other scoped records

The same rule applies to Building, BuildingStory, ThermalZone, Surface, and SubSurface:

- Direct OSM fields retain their exact OSM/IDD label in Pydantic `json_schema_extra.openstudio`.
- Referenced objects expose both a canonical handle and a nullable resolved name.
- SDK-derived geometry values identify their accessor and state that they are not direct text fields.
- Collection relationships such as `surface_handles` are marked as derived.

The generated Pydantic JSON schema is the machine-readable source of truth. This document is the human-oriented projection and will expand alongside accepted inventory fields.

## Coordinate Frames

- `space_local`: raw SDK vertices belong to geometry assigned to a Space; use the Space origin and relative-north transformation deliberately.
- `model`: raw SDK vertices belong to orphan Surface/SubSurface objects without a parent Space or surface group.
- Site-coordinate conversion is not implicit in the inventory.
