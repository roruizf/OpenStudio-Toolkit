"""Dumps of the curated families, as records and as a view.

A family is one IDD object type with a curated reader in ``osm_objects``. Its name is the IDD type
without ``OS:``, in snake case (``OS:Coil:Cooling:Water`` -> ``coil_cooling_water``).

- ``dump_records`` gives what is stored in the model: every IDD field from the generic reader, with
  the handle of each reference target. The diff (item 6) works on these.
- ``dump_view`` gives what OpenStudio resolves: the curated DataFrame, including values inherited
  from default sets. In R2F-Office-Hub the light "0.06-WC Lights" has an empty Schedule Name field
  (record) and "Office Building Lighting Schedule" from its schedule set (view).

Three curated readers are not one IDD type and stay outside the dumps (still available in
``osm_objects``): ``get_all_opaque_material_objects_as_dataframe`` (Material + Material:NoMass),
``get_all_default_construction_set_component_as_dataframe`` (resolved view of
DefaultConstructionSet) and ``get_all_default_schedule_set_components_as_dataframe`` (long table
without handles).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from types import MappingProxyType
from typing import Any

import pandas as pd

from openstudio_toolkit.extractors.generic import ObjectRecord, read_model_objects
from openstudio_toolkit.osm_objects import (
    availability_managers,
    building_stories,
    building_units,
    component_curves,
    constructions,
    controllers,
    exterior_equipment,
    hvac_air_loops,
    hvac_components,
    hvac_sizing,
    hvac_zone,
    loads,
    materials,
    outputs,
    schedules,
    space_types,
    spaces,
    subsurfaces,
    surfaces,
    thermal_zones,
)

_FAMILIES: dict[str, tuple[str, Callable[[Any], pd.DataFrame]]] = {
    "air_conditioner_variable_refrigerant_flow": (
        "OS:AirConditioner:VariableRefrigerantFlow",
        hvac_components.get_all_air_conditioner_variable_refrigerant_flow_objects_as_dataframe,
    ),
    "air_loop_hvac": ("OS:AirLoopHVAC", hvac_air_loops.get_all_air_loop_hvac_objects_as_dataframe),
    "air_loop_hvac_outdoor_air_system": (
        "OS:AirLoopHVAC:OutdoorAirSystem",
        hvac_air_loops.get_all_air_loop_hvac_outdoor_air_system_objects_as_dataframe,
    ),
    "air_loop_hvac_unitary_system": (
        "OS:AirLoopHVAC:UnitarySystem",
        hvac_air_loops.get_all_air_loop_hvac_unitary_system_objects_as_dataframe,
    ),
    "air_terminal_single_duct_parallel_piu_reheat": (
        "OS:AirTerminal:SingleDuct:ParallelPIU:Reheat",
        hvac_zone.get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dataframe,
    ),
    "availability_manager_night_cycle": (
        "OS:AvailabilityManager:NightCycle",
        availability_managers.get_all_availability_manager_night_cycle_objects_as_dataframe,
    ),
    "boiler_hot_water": ("OS:Boiler:HotWater", hvac_components.get_all_boiler_hot_water_objects_as_dataframe),
    "building_story": ("OS:BuildingStory", building_stories.get_all_building_stories_objects_as_dataframe),
    "building_unit": ("OS:BuildingUnit", building_units.get_all_building_unit_objects_as_dataframe),
    "chiller_electric_eir": (
        "OS:Chiller:Electric:EIR",
        hvac_components.get_all_chiller_electric_eir_objects_as_dataframe,
    ),
    "coil_cooling_dx_variable_refrigerant_flow": (
        "OS:Coil:Cooling:DX:VariableRefrigerantFlow",
        hvac_components.get_all_coil_cooling_dx_variable_refrigerant_flow_objects_as_dataframe,
    ),
    "coil_cooling_water": ("OS:Coil:Cooling:Water", hvac_components.get_all_coil_cooling_water_objects_as_dataframe),
    "coil_heating_dx_variable_refrigerant_flow": (
        "OS:Coil:Heating:DX:VariableRefrigerantFlow",
        hvac_components.get_all_coil_heating_dx_variable_refrigerant_flow_objects_as_dataframe,
    ),
    "coil_heating_gas": ("OS:Coil:Heating:Gas", hvac_components.get_all_coil_heating_gas_objects_as_dataframe),
    "coil_heating_water": ("OS:Coil:Heating:Water", hvac_components.get_all_coil_heating_water_objects_as_dataframe),
    "construction": ("OS:Construction", constructions.get_all_construction_objects_as_dataframe),
    "controller_outdoor_air": (
        "OS:Controller:OutdoorAir",
        controllers.get_all_controller_outdoor_air_objects_as_dataframe,
    ),
    "cooling_tower_two_speed": (
        "OS:CoolingTower:TwoSpeed",
        hvac_components.get_all_cooling_tower_two_speed_objects_as_dataframe,
    ),
    "cooling_tower_variable_speed": (
        "OS:CoolingTower:VariableSpeed",
        hvac_components.get_all_cooling_tower_variable_speed_objects_as_dataframe,
    ),
    "curve_biquadratic": ("OS:Curve:Biquadratic", component_curves.get_all_curve_biquadratic_objects_as_dataframe),
    "curve_cubic": ("OS:Curve:Cubic", component_curves.get_all_curve_cubic_objects_as_dataframe),
    "curve_exponent": ("OS:Curve:Exponent", component_curves.get_all_curve_exponent_objects_as_dataframe),
    "curve_quadratic": ("OS:Curve:Quadratic", component_curves.get_all_curve_quadratic_objects_as_dataframe),
    "default_construction_set": (
        "OS:DefaultConstructionSet",
        constructions.get_all_default_construction_set_objects_as_dataframe,
    ),
    "default_schedule_set": ("OS:DefaultScheduleSet", schedules.get_all_default_schedule_set_objects_as_dataframe),
    "default_sub_surface_constructions": (
        "OS:DefaultSubSurfaceConstructions",
        constructions.get_all_default_subsurface_construction_objects_as_dataframe,
    ),
    "default_surface_constructions": (
        "OS:DefaultSurfaceConstructions",
        constructions.get_all_default_surface_construction_objects_as_dataframe,
    ),
    "design_specification_outdoor_air": (
        "OS:DesignSpecification:OutdoorAir",
        loads.get_all_design_specification_outdoor_air_objects_as_dataframe,
    ),
    "electric_equipment": ("OS:ElectricEquipment", loads.get_all_electric_equipment_objects_as_dataframe),
    "electric_equipment_definition": (
        "OS:ElectricEquipment:Definition",
        loads.get_all_electric_equipment_definition_objects_as_dataframe,
    ),
    "exterior_fuel_equipment_definition": (
        "OS:Exterior:FuelEquipment:Definition",
        exterior_equipment.get_all_exterior_fuel_equipment_definition_objects_as_dataframe,
    ),
    "exterior_lights_definition": (
        "OS:Exterior:Lights:Definition",
        exterior_equipment.get_all_exterior_lights_definition_objects_as_dataframe,
    ),
    "exterior_water_equipment_definition": (
        "OS:Exterior:WaterEquipment:Definition",
        exterior_equipment.get_all_exterior_water_equipment_definition_objects_as_dataframe,
    ),
    "fan_constant_volume": ("OS:Fan:ConstantVolume", hvac_components.get_all_fan_constant_volume_objects_as_dataframe),
    "fan_on_off": ("OS:Fan:OnOff", hvac_components.get_all_fan_on_off_objects_as_dataframe),
    "fan_variable_volume": ("OS:Fan:VariableVolume", hvac_components.get_all_fan_variable_volume_objects_as_dataframe),
    "gas_equipment": ("OS:GasEquipment", loads.get_all_gas_equipment_objects_as_dataframe),
    "gas_equipment_definition": (
        "OS:GasEquipment:Definition",
        loads.get_all_gas_equipment_definition_objects_as_dataframe,
    ),
    "heat_exchanger_air_to_air_sensible_and_latent": (
        "OS:HeatExchanger:AirToAir:SensibleAndLatent",
        hvac_components.get_all_hx_air_to_air_sensible_and_latent_as_dataframe,
    ),
    "lights": ("OS:Lights", loads.get_all_lights_objects_as_dataframe),
    "lights_definition": ("OS:Lights:Definition", loads.get_all_lights_definition_objects_as_dataframe),
    "material": ("OS:Material", materials.get_all_standard_opaque_material_objects_as_dataframe),
    "material_no_mass": ("OS:Material:NoMass", materials.get_all_massless_opaque_material_objects_as_dataframe),
    "other_equipment": ("OS:OtherEquipment", loads.get_all_other_equipment_objects_as_dataframe),
    "other_equipment_definition": (
        "OS:OtherEquipment:Definition",
        loads.get_all_other_equipment_definition_objects_as_dataframe,
    ),
    "output_variable": ("OS:Output:Variable", outputs.get_all_output_variable_objects_as_dataframe),
    "people": ("OS:People", loads.get_all_people_objects_as_dataframe),
    "people_definition": ("OS:People:Definition", loads.get_all_people_definition_objects_as_dataframe),
    "pump_constant_speed": ("OS:Pump:ConstantSpeed", hvac_components.get_all_pump_constant_speed_objects_as_dataframe),
    "pump_variable_speed": ("OS:Pump:VariableSpeed", hvac_components.get_all_pump_variable_speed_objects_as_dataframe),
    "schedule_day": ("OS:Schedule:Day", schedules.get_all_schedule_day_objects_as_dataframe),
    "schedule_rule": ("OS:Schedule:Rule", schedules.get_all_schedule_rule_objects_as_dataframe),
    "schedule_ruleset": ("OS:Schedule:Ruleset", schedules.get_all_schedule_ruleset_objects_as_dataframe),
    "schedule_type_limits": ("OS:ScheduleTypeLimits", schedules.get_all_schedule_type_limit_objects_as_dataframe),
    "sizing_system": ("OS:Sizing:System", hvac_sizing.get_all_air_sizing_system_objects_as_dataframe),
    "sizing_zone": ("OS:Sizing:Zone", hvac_sizing.get_all_sizing_zone_objects_as_dataframe),
    "space": ("OS:Space", spaces.get_all_space_objects_as_dataframe),
    "space_infiltration_design_flow_rate": (
        "OS:SpaceInfiltration:DesignFlowRate",
        loads.get_all_space_infiltration_design_flowrate_objects_as_dataframe,
    ),
    "space_type": ("OS:SpaceType", space_types.get_all_space_types_objects_as_dataframe),
    "steam_equipment": ("OS:SteamEquipment", loads.get_all_steam_equipment_objects_as_dataframe),
    "steam_equipment_definition": (
        "OS:SteamEquipment:Definition",
        loads.get_all_steam_equipment_definition_objects_as_dataframe,
    ),
    "sub_surface": ("OS:SubSurface", subsurfaces.get_all_subsurface_objects_as_dataframe),
    "surface": ("OS:Surface", surfaces.get_all_surface_objects_as_dataframe),
    "thermal_zone": ("OS:ThermalZone", thermal_zones.get_all_thermal_zones_objects_as_dataframe),
    "thermostat_setpoint_dual_setpoint": (
        "OS:ThermostatSetpoint:DualSetpoint",
        hvac_zone.get_all_thermostat_setpoint_dual_setpoint_objects_as_dataframe,
    ),
    "water_use_equipment": ("OS:WaterUse:Equipment", loads.get_all_water_use_equipment_objects_as_dataframe),
    "water_use_equipment_definition": (
        "OS:WaterUse:Equipment:Definition",
        loads.get_all_water_use_equipment_definition_objects_as_dataframe,
    ),
    "window_material_simple_glazing_system": (
        "OS:WindowMaterial:SimpleGlazingSystem",
        materials.get_all_window_material_simple_glazing_system_objects_as_dataframe,
    ),
    "zone_hvac_equipment_list": (
        "OS:ZoneHVAC:EquipmentList",
        hvac_zone.get_all_zone_hvac_equipment_list_objects_as_dataframe,
    ),
    "zone_hvac_four_pipe_fan_coil": (
        "OS:ZoneHVAC:FourPipeFanCoil",
        hvac_zone.get_all_four_pipe_fan_coil_objects_as_dataframe,
    ),
    "zone_hvac_ideal_loads_air_system": (
        "OS:ZoneHVAC:IdealLoadsAirSystem",
        hvac_zone.get_all_zone_hvac_ideal_loads_air_system_objects_as_dataframe,
    ),
    "zone_hvac_terminal_unit_variable_refrigerant_flow": (
        "OS:ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
        hvac_zone.get_all_zone_hvac_terminal_unit_variant_refrigerant_flow_objects_as_dataframe,
    ),
    "zone_hvac_unit_heater": ("OS:ZoneHVAC:UnitHeater", hvac_zone.get_all_zone_hvac_unit_heater_objects_as_dataframe),
}

_IDD_TYPES = MappingProxyType({name: idd_type for name, (idd_type, _) in _FAMILIES.items()})


def families() -> Mapping[str, str]:
    """Family name -> IDD object type, for every family the dumps cover."""
    return _IDD_TYPES


def _selected(names: Iterable[str] | None) -> list[str]:
    if names is None:
        return list(_FAMILIES)
    selected = list(dict.fromkeys(names))
    unknown = [name for name in selected if name not in _FAMILIES]
    if unknown:
        raise ValueError(f"unknown families: {', '.join(unknown)}")
    return selected


def dump_records(model: Any, families: Iterable[str] | None = None) -> dict[str, list[ObjectRecord]]:
    """Generic records of each requested family (all when None), keyed by family name.

    Every requested family is present, with an empty list when the model has no objects of it.
    Records keep the generic reader's order (by handle within a type).
    """
    selected = _selected(families)
    by_type: dict[str, list[ObjectRecord]] = {_IDD_TYPES[name]: [] for name in selected}
    for record in read_model_objects(model):
        if record.idd_type in by_type:
            by_type[record.idd_type].append(record)
    return {name: by_type[_IDD_TYPES[name]] for name in selected}


def dump_view(model: Any, families: Iterable[str] | None = None) -> dict[str, pd.DataFrame]:
    """Curated DataFrame of each requested family (all when None), keyed by family name.

    Every requested family is present; an empty family is a DataFrame with its columns.
    """
    return {name: _FAMILIES[name][1](model) for name in _selected(families)}
