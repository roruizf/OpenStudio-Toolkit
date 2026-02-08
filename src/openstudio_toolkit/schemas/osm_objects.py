"""Pydantic schemas for OSM object dictionaries returned by osm_objects modules.

Each schema mirrors the exact dictionary keys produced by the corresponding
get_*_object_as_dict() function. Field names use the OpenStudio convention
with units in braces (e.g. 'Floor Area {m2}').

These schemas serve three purposes:
1. Documentation: Clear, browsable contract of what each extractor returns.
2. Validation: Optional runtime validation of extracted data.
3. IDE support: Autocompletion and type checking when working with results.

Usage::

    from openstudio_toolkit.schemas.osm_objects import SpaceData
    raw_dict = spaces.get_space_object_as_dict(model, name="Office-1")
    space = SpaceData.model_validate(raw_dict)
    print(space.floor_area_m2)
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class OsmObjectBase(BaseModel):
    """Base for all OSM object schemas. Every object has a Handle and Name."""

    model_config = ConfigDict(populate_by_name=True)

    handle: str = Field(..., alias="Handle", description="Immutable UUID of the OpenStudio object.")
    name: str | None = Field(default=None, alias="Name")


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

class SpaceData(OsmObjectBase):
    """Schema for OS:Space objects (spaces.get_space_object_as_dict)."""

    space_type_name: str | None = Field(default=None, alias="Space Type Name")
    default_construction_set_name: str | None = Field(default=None, alias="Default Construction Set Name")
    default_schedule_set_name: str | None = Field(default=None, alias="Default Schedule Set Name")
    direction_of_relative_north_deg: float | None = Field(default=None, alias="Direction of Relative North {deg}")
    x_origin_m: float | None = Field(default=None, alias="X Origin {m}")
    y_origin_m: float | None = Field(default=None, alias="Y Origin {m}")
    z_origin_m: float | None = Field(default=None, alias="Z Origin {m}")
    building_story_name: str | None = Field(default=None, alias="Building Story Name")
    thermal_zone_name: str | None = Field(default=None, alias="Thermal Zone Name")
    part_of_total_floor_area: bool | None = Field(default=None, alias="Part of Total Floor Area")
    design_specification_outdoor_air_object_name: str | None = Field(
        default=None, alias="Design Specification Outdoor Air Object Name"
    )
    building_unit_name: str | None = Field(default=None, alias="Building Unit Name")
    volume_m3: float | None = Field(default=None, alias="Volume {m3}")
    ceiling_height_m: float | None = Field(default=None, alias="Ceiling Height {m}")
    floor_area_m2: float | None = Field(default=None, alias="Floor Area {m2}")
    # Enriched
    orientation: str | None = Field(default=None, alias="Orientation")


class SurfaceData(OsmObjectBase):
    """Schema for OS:Surface objects (surfaces.get_surface_object_as_dict)."""

    surface_type: str | None = Field(default=None, alias="Surface Type")
    construction_name: str | None = Field(default=None, alias="Construction Name")
    space_name: str | None = Field(default=None, alias="Space Name")
    outside_boundary_condition: str | None = Field(default=None, alias="Outside Boundary Condition")
    outside_boundary_condition_object: str | None = Field(default=None, alias="Outside Boundary Condition Object")
    sun_exposure: str | None = Field(default=None, alias="Sun Exposure")
    wind_exposure: str | None = Field(default=None, alias="Wind Exposure")
    view_factor_to_ground: float | None = Field(default=None, alias="View Factor to Ground")
    number_of_vertices: int | None = Field(default=None, alias="Number of Vertices")
    # Enriched
    azimuth: float | None = Field(default=None, alias="Azimuth")
    orientation: str | None = Field(default=None, alias="Orientation")


class SubSurfaceData(OsmObjectBase):
    """Schema for OS:SubSurface objects (subsurfaces.get_subsurface_object_as_dict)."""

    sub_surface_type: str | None = Field(default=None, alias="Sub Surface Type")
    construction_name: str | None = Field(default=None, alias="Construction Name")
    surface_name: str | None = Field(default=None, alias="Surface Name")
    outside_boundary_condition_object: str | None = Field(default=None, alias="Outside Boundary Condition Object")
    view_factor_to_ground: float | None = Field(default=None, alias="View Factor to Ground")
    multiplier: float | None = Field(default=None, alias="Multiplier")
    number_of_vertices: int | None = Field(default=None, alias="Number of Vertices")
    # Enriched
    azimuth: float | None = Field(default=None, alias="Azimuth")
    orientation: str | None = Field(default=None, alias="Orientation")
    frame_and_divider_name: str | None = Field(default=None, alias="Frame and Divider Name")


# ---------------------------------------------------------------------------
# Thermal Zones
# ---------------------------------------------------------------------------

class ThermalZoneData(OsmObjectBase):
    """Schema for OS:ThermalZone objects (thermal_zones.get_thermal_zone_object_as_dict)."""

    multiplier: int | None = Field(default=None, alias="Multiplier")
    ceiling_height_m: float | None = Field(default=None, alias="Ceiling Height {m}")
    volume_m3: float | None = Field(default=None, alias="Volume {m3}")
    floor_area_m2: float | None = Field(default=None, alias="Floor Area {m2}")
    zone_inside_convection_algorithm: str | None = Field(default=None, alias="Zone Inside Convection Algorithm")
    zone_outside_convection_algorithm: str | None = Field(default=None, alias="Zone Outside Convection Algorithm")
    zone_conditioning_equipment_list_name: str | None = Field(
        default=None, alias="Zone Conditioning Equipment List Name"
    )
    zone_air_inlet_port_list: str | None = Field(default=None, alias="Zone Air Inlet Port List")
    zone_air_exhaust_port_list: str | None = Field(default=None, alias="Zone Air Exhaust Port List")
    zone_air_node_name: str | None = Field(default=None, alias="Zone Air Node Name")
    zone_return_air_port_list: str | None = Field(default=None, alias="Zone Return Air Port List")
    primary_daylighting_control_name: str | None = Field(default=None, alias="Primary Daylighting Control Name")
    fraction_primary_daylighting: float | None = Field(
        default=None, alias="Fraction of Zone Controlled by Primary Daylighting Control"
    )
    secondary_daylighting_control_name: str | None = Field(default=None, alias="Secondary Daylighting Control Name")
    fraction_secondary_daylighting: float | None = Field(
        default=None, alias="Fraction of Zone Controlled by Secondary Daylighting Control"
    )
    illuminance_map_name: str | None = Field(default=None, alias="Illuminance Map Name")
    group_rendering_name: str | None = Field(default=None, alias="Group Rendering Name")
    thermostat_name: str | None = Field(default=None, alias="Thermostat Name")
    use_ideal_air_loads: bool | None = Field(default=None, alias="Use Ideal Air Loads")
    humidistat_name: str | None = Field(default=None, alias="Humidistat Name")
    daylighting_controls_availability_schedule_name: str | None = Field(
        default=None, alias="Daylighting Controls Availability Schedule Name"
    )


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

class StandardOpaqueMaterialData(OsmObjectBase):
    """Schema for OS:Material objects (materials.get_standard_opaque_material_object_as_dict)."""

    roughness: str | None = Field(default=None, alias="Roughness")
    thickness_m: float | None = Field(default=None, alias="Thickness {m}")
    conductivity_w_mk: float | None = Field(default=None, alias="Conductivity {W/m-K}")
    density_kg_m3: float | None = Field(default=None, alias="Density {kg/m3}")
    specific_heat_j_kgk: float | None = Field(default=None, alias="Specific Heat {J/kg-K}")
    thermal_absorptance: float | None = Field(default=None, alias="Thermal Absorptance")
    solar_absorptance: float | None = Field(default=None, alias="Solar Absorptance")
    visible_absorptance: float | None = Field(default=None, alias="Visible Absorptance")


class MasslessOpaqueMaterialData(OsmObjectBase):
    """Schema for OS:Material:NoMass objects (materials.get_massless_opaque_material_object_as_dict)."""

    roughness: str | None = Field(default=None, alias="Roughness")
    thermal_resistance_m2kw: float | None = Field(default=None, alias="Thermal Resistance {m2-K/W}")
    thermal_absorptance: float | None = Field(default=None, alias="Thermal Absorptance")
    solar_absorptance: float | None = Field(default=None, alias="Solar Absorptance")
    visible_absorptance: float | None = Field(default=None, alias="Visible Absorptance")


# ---------------------------------------------------------------------------
# Constructions
# ---------------------------------------------------------------------------

class ConstructionData(OsmObjectBase):
    """Schema for OS:Construction objects (constructions.get_construction_object_as_dict).

    Note: Layer fields are dynamic (Layer 1, Layer 2, ...) so they are not
    explicitly defined here. Use model_config extra='allow' for those.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    surface_rendering_name: str | None = Field(default=None, alias="Surface Rendering Name")


class DefaultConstructionSetData(OsmObjectBase):
    """Schema for OS:DefaultConstructionSet objects."""

    default_exterior_surface_constructions_name: str | None = Field(
        default=None, alias="Default Exterior Surface Constructions Name"
    )
    default_interior_surface_constructions_name: str | None = Field(
        default=None, alias="Default Interior Surface Constructions Name"
    )
    default_ground_contact_surface_constructions_name: str | None = Field(
        default=None, alias="Default Ground Contact Surface Constructions Name"
    )
    default_exterior_subsurface_constructions_name: str | None = Field(
        default=None, alias="Default Exterior SubSurface Constructions Name"
    )
    default_interior_subsurface_constructions_name: str | None = Field(
        default=None, alias="Default Interior SubSurface Constructions Name"
    )
    interior_partition_construction_name: str | None = Field(
        default=None, alias="Interior Partition Construction Name"
    )
    space_shading_construction_name: str | None = Field(default=None, alias="Space Shading Construction Name")
    building_shading_construction_name: str | None = Field(default=None, alias="Building Shading Construction Name")
    site_shading_construction_name: str | None = Field(default=None, alias="Site Shading Construction Name")
    adiabatic_surface_construction_name: str | None = Field(
        default=None, alias="Adiabatic Surface Construction Name"
    )


# ---------------------------------------------------------------------------
# Internal Loads
# ---------------------------------------------------------------------------

class PeopleData(OsmObjectBase):
    """Schema for OS:People objects (loads.get_people_object_as_dict)."""

    people_definition_name: str | None = Field(default=None, alias="People Definition Name")
    space_or_spacetype_name: str | None = Field(default=None, alias="Space or SpaceType Name")
    number_of_people_schedule_name: str | None = Field(default=None, alias="Number of People Schedule Name")
    activity_level_schedule_name: str | None = Field(default=None, alias="Activity Level Schedule Name")
    surface_name_angle_factor_list_name: str | None = Field(default=None, alias="Surface Name/Angle Factor List Name")
    work_efficiency_schedule_name: str | None = Field(default=None, alias="Work Efficiency Schedule Name")
    clothing_insulation_schedule_name: str | None = Field(default=None, alias="Clothing Insulation Schedule Name")
    air_velocity_schedule_name: str | None = Field(default=None, alias="Air Velocity Schedule Name")
    multiplier: float | None = Field(default=None, alias="Multiplier")


class LightsData(OsmObjectBase):
    """Schema for OS:Lights objects (loads.get_lights_object_as_dict)."""

    lights_definition_name: str | None = Field(default=None, alias="Lights Definition Name")
    space_or_space_type_name: str | None = Field(default=None, alias="Space or SpaceType Name")
    schedule_name: str | None = Field(default=None, alias="Schedule Name")
    fraction_replaceable: float | None = Field(default=None, alias="Fraction Replaceable")
    multiplier: float | None = Field(default=None, alias="Multiplier")
    end_use_subcategory: str | None = Field(default=None, alias="End-Use Subcategory")


class ElectricEquipmentData(OsmObjectBase):
    """Schema for OS:ElectricEquipment objects (loads.get_electric_equipment_object_as_dict)."""

    electric_equipment_definition_name: str | None = Field(default=None, alias="Electric Equipment Definition Name")
    space_or_space_type_name: str | None = Field(default=None, alias="Space or SpaceType Name")
    schedule_name: str | None = Field(default=None, alias="Schedule Name")
    multiplier: float | None = Field(default=None, alias="Multiplier")
    end_use_subcategory: str | None = Field(default=None, alias="End-Use Subcategory")


# ---------------------------------------------------------------------------
# Load Definitions
# ---------------------------------------------------------------------------

class PeopleDefinitionData(OsmObjectBase):
    """Schema for OS:People:Definition objects."""

    number_of_people_calculation_method: str | None = Field(
        default=None, alias="Number of People Calculation Method"
    )
    number_of_people: float | None = Field(default=None, alias="Number of People {people}")
    people_per_floor_area: float | None = Field(default=None, alias="People per Space Floor Area {person/m2}")
    floor_area_per_person: float | None = Field(default=None, alias="Space Floor Area per Person {m2/person}")
    fraction_radiant: float | None = Field(default=None, alias="Fraction Radiant")
    sensible_heat_fraction: float | None = Field(default=None, alias="Sensible Heat Fraction")
    carbon_dioxide_generation_rate: float | None = Field(
        default=None, alias="Carbon Dioxide Generation Rate {m3/s-W}"
    )


class LightsDefinitionData(OsmObjectBase):
    """Schema for OS:Lights:Definition objects."""

    design_level_calculation_method: str | None = Field(default=None, alias="Design Level Calculation Method")
    lighting_level_w: float | None = Field(default=None, alias="Lighting Level {W}")
    watts_per_floor_area: float | None = Field(default=None, alias="Watts per Space Floor Area {W/m2}")
    watts_per_person: float | None = Field(default=None, alias="Watts per Person {W/person}")
    fraction_radiant: float | None = Field(default=None, alias="Fraction Radiant")
    fraction_visible: float | None = Field(default=None, alias="Fraction Visible")
    return_air_fraction: float | None = Field(default=None, alias="Return Air Fraction")


class ElectricEquipmentDefinitionData(OsmObjectBase):
    """Schema for OS:ElectricEquipment:Definition objects."""

    design_level_calculation_method: str | None = Field(default=None, alias="Design Level Calculation Method")
    design_level_w: float | None = Field(default=None, alias="Design Level {W}")
    watts_per_floor_area: float | None = Field(default=None, alias="Watts per Space Floor Area {W/m2}")
    watts_per_person: float | None = Field(default=None, alias="Watts per Person {W/person}")
    fraction_latent: float | None = Field(default=None, alias="Fraction Latent")
    fraction_radiant: float | None = Field(default=None, alias="Fraction Radiant")
    fraction_lost: float | None = Field(default=None, alias="Fraction Lost")


# ---------------------------------------------------------------------------
# Infiltration & Outdoor Air
# ---------------------------------------------------------------------------

class SpaceInfiltrationData(OsmObjectBase):
    """Schema for OS:SpaceInfiltration:DesignFlowRate objects."""

    space_or_space_type_name: str | None = Field(default=None, alias="Space or SpaceType Name")
    schedule_name: str | None = Field(default=None, alias="Schedule Name")
    design_flow_rate_calculation_method: str | None = Field(
        default=None, alias="Design Flow Rate Calculation Method"
    )
    design_flow_rate_m3s: float | None = Field(default=None, alias="Design Flow Rate {m3/s}")
    flow_per_floor_area: float | None = Field(default=None, alias="Flow per Space Floor Area {m3/s-m2}")
    flow_per_exterior_surface_area: float | None = Field(
        default=None, alias="Flow per Exterior Surface Area {m3/s-m2}"
    )
    air_changes_per_hour: float | None = Field(default=None, alias="Air Changes per Hour {1/hr}")


class DesignSpecOutdoorAirData(OsmObjectBase):
    """Schema for OS:DesignSpecification:OutdoorAir objects."""

    outdoor_air_method: str | None = Field(default=None, alias="Outdoor Air Method")
    outdoor_air_flow_per_person: float | None = Field(
        default=None, alias="Outdoor Air Flow per Person {m3/s-person}"
    )
    outdoor_air_flow_per_floor_area: float | None = Field(
        default=None, alias="Outdoor Air Flow per Floor Area {m3/s-m2}"
    )
    outdoor_air_flow_rate: float | None = Field(default=None, alias="Outdoor Air Flow Rate {m3/s}")
    outdoor_air_flow_ach: float | None = Field(
        default=None, alias="Outdoor Air Flow Air Changes per Hour {1/hr}"
    )


# ---------------------------------------------------------------------------
# HVAC Availability
# ---------------------------------------------------------------------------

class AvailabilityManagerNightCycleData(OsmObjectBase):
    """Schema for OS:AvailabilityManager:NightCycle objects
    (availability_managers.get_availability_manager_night_cycle_object_as_dict).
    """

    applicability_schedule: str | None = Field(
        default=None, alias="Applicability Schedule"
    )
    fan_schedule: str | None = Field(default=None, alias="Fan Schedule")
    control_type: str | None = Field(default=None, alias="Control Type")
    thermostat_tolerance_deltac: float | None = Field(
        default=None, alias="Thermostat Tolerance {deltaC}"
    )
    cycling_run_time_control_type: str | None = Field(
        default=None, alias="Cycling Run Time Control Type"
    )
    cycling_run_time_s: float | None = Field(default=None, alias="Cycling Run Time {s}")
    control_zone_or_zone_list_name: str | None = Field(
        default=None, alias="Control Zone or Zone List Name"
    )
    cooling_control_zone_or_zone_list_name: str | None = Field(
        default=None, alias="Cooling Control Zone or Zone List Name"
    )
    heating_control_zone_or_zone_list_name: str | None = Field(
        default=None, alias="Heating Control Zone or Zone List Name"
    )
    heating_zone_fans_only_zone_or_zone_list_name: str | None = Field(
        default=None, alias="Heating Zone Fans Only Zone or Zone List Name"
    )
