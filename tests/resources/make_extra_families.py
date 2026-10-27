"""Generate tests/resources/extra_families.osm, a synthetic OpenStudio 3.11 model.

What it builds: two spaces in two thermal zones, each in its own building unit, plus
at least two objects of every family that no other repo fixture covers:
OS:BuildingUnit, OS:Exterior:FuelEquipment(+Definition), OS:Exterior:WaterEquipment
(+Definition), OS:AirConditioner:VariableRefrigerantFlow with two terminal units
(OS:ZoneHVAC:TerminalUnit:VariableRefrigerantFlow, each holding its cooling and heating
DX VRF coils), OS:GasEquipment(+Definition), OS:OtherEquipment(+Definition),
OS:SteamEquipment(+Definition), OS:ZoneHVAC:UnitHeater,
OS:AirTerminal:SingleDuct:ParallelPIU:Reheat and OS:Output:Variable.

Why: the osm_objects readers for these families are only exercised with empty models
today. tests/osm_objects can load this file to check them against real objects.

Geometry, schedules and values are placeholders chosen to load and validate; the model
is not meant to be simulated. Object names are fixed; only UUID handles vary per run.

Usage (from the repository root):
    uv run python tests/resources/make_extra_families.py
"""

from __future__ import annotations

from pathlib import Path

import openstudio

OUTPUT_PATH = Path(__file__).resolve().parent / "extra_families.osm"


def _floor(model: openstudio.model.Model, name: str, x0: float, unit_name: str) -> openstudio.model.Space:
    """Create a 5 m x 5 m, 3 m high space with its own thermal zone and building unit."""
    pts = openstudio.Point3dVector()
    # Clockwise seen from above, so the floor normal points down as fromFloorPrint requires.
    for x, y in [(x0, 0.0), (x0, 5.0), (x0 + 5.0, 5.0), (x0 + 5.0, 0.0)]:
        pts.append(openstudio.Point3d(x, y, 0.0))
    space = openstudio.model.Space.fromFloorPrint(pts, 3.0, model).get()
    space.setName(name)

    zone = openstudio.model.ThermalZone(model)
    zone.setName(f"{name}_Zone")
    space.setThermalZone(zone)

    unit = openstudio.model.BuildingUnit(model)
    unit.setName(unit_name)
    space.setBuildingUnit(unit)
    return space


def build_model() -> openstudio.model.Model:
    model = openstudio.model.Model()

    office = _floor(model, "Office_Space", 0.0, "BuildingUnit_North")
    lobby = _floor(model, "Lobby_Space", 10.0, "BuildingUnit_South")
    zones = {"office": office.thermalZone().get(), "lobby": lobby.thermalZone().get()}

    fraction = openstudio.model.ScheduleConstant(model)
    fraction.setName("Fraction_Schedule_Constant")
    fraction.setValue(0.5)
    always_on = model.alwaysOnDiscreteSchedule()

    # Exterior fuel and water equipment (not attached to a space).
    for fuel, label in [("NaturalGas", "Gas"), ("Propane", "Propane")]:
        fuel_def = openstudio.model.ExteriorFuelEquipmentDefinition(model)
        fuel_def.setName(f"Exterior_{label}_Definition")
        fuel_def.setDesignLevel(1000.0)
        fuel_eq = openstudio.model.ExteriorFuelEquipment(fuel_def)
        fuel_eq.setName(f"Exterior_{label}_Equipment")
        fuel_eq.setFuelType(fuel)
        fuel_eq.setSchedule(fraction)

    for label in ["Irrigation", "Pool"]:
        water_def = openstudio.model.ExteriorWaterEquipmentDefinition(model)
        water_def.setName(f"Exterior_{label}_Water_Definition")
        water_def.setDesignLevel(0.001)
        water_eq = openstudio.model.ExteriorWaterEquipment(water_def)
        water_eq.setName(f"Exterior_{label}_Water_Equipment")
        water_eq.setSchedule(fraction)

    # Interior equipment, one definition and one instance per space.
    for space, label, level in [(office, "Office", 500.0), (lobby, "Lobby", 300.0)]:
        gas_def = openstudio.model.GasEquipmentDefinition(model)
        gas_def.setName(f"{label}_Gas_Definition")
        gas_def.setDesignLevel(level)
        gas = openstudio.model.GasEquipment(gas_def)
        gas.setName(f"{label}_Gas_Equipment")
        gas.setSpace(space)
        gas.setSchedule(fraction)

        other_def = openstudio.model.OtherEquipmentDefinition(model)
        other_def.setName(f"{label}_Other_Definition")
        other_def.setDesignLevel(level)
        other = openstudio.model.OtherEquipment(other_def)
        other.setName(f"{label}_Other_Equipment")
        other.setSpace(space)
        other.setSchedule(fraction)

        steam_def = openstudio.model.SteamEquipmentDefinition(model)
        steam_def.setName(f"{label}_Steam_Definition")
        steam_def.setDesignLevel(level)
        steam = openstudio.model.SteamEquipment(steam_def)
        steam.setName(f"{label}_Steam_Equipment")
        steam.setSpace(space)
        steam.setSchedule(fraction)

    # One VRF outdoor unit serving two terminal units, each with its own DX coils.
    vrf = openstudio.model.AirConditionerVariableRefrigerantFlow(model)
    vrf.setName("VRF_Outdoor_Unit")
    vrf.setAvailabilitySchedule(always_on)
    vrf.setGrossRatedTotalCoolingCapacity(20000.0)
    vrf.setGrossRatedHeatingCapacity(22000.0)

    for key, zone in zones.items():
        label = key.capitalize()
        cool = openstudio.model.CoilCoolingDXVariableRefrigerantFlow(model)
        cool.setName(f"{label}_VRF_Cooling_Coil")
        cool.setAvailabilitySchedule(always_on)
        cool.setRatedTotalCoolingCapacity(10000.0)
        cool.setRatedAirFlowRate(0.5)
        cool.setRatedSensibleHeatRatio(0.75)

        heat = openstudio.model.CoilHeatingDXVariableRefrigerantFlow(model)
        heat.setName(f"{label}_VRF_Heating_Coil")
        heat.setAvailabilitySchedule(always_on)
        heat.setRatedTotalHeatingCapacity(11000.0)
        heat.setRatedAirFlowRate(0.5)

        terminal = openstudio.model.ZoneHVACTerminalUnitVariableRefrigerantFlow(model)
        terminal.setName(f"{label}_VRF_Terminal_Unit")
        # The terminal constructor creates default coils; remove them so only the named ones remain.
        terminal.coolingCoil().get().remove()
        terminal.heatingCoil().get().remove()
        terminal.setCoolingCoil(cool)
        terminal.setHeatingCoil(heat)
        terminal.setTerminalUnitAvailabilityschedule(always_on)
        terminal.setSupplyAirFlowRateDuringCoolingOperation(0.5)
        terminal.setSupplyAirFlowRateDuringHeatingOperation(0.5)
        terminal.addToThermalZone(zone)

        vrf.addTerminal(terminal)

    # Unit heater and parallel PIU terminal: no other fixture has them, and the unit heater's fan, coil and
    # schedule accessors segfault when their fields are empty (validators/_fatal_references.py).
    heater = openstudio.model.ZoneHVACUnitHeater(
        model, always_on, openstudio.model.FanConstantVolume(model), openstudio.model.CoilHeatingElectric(model)
    )
    heater.setName("Lobby_Unit_Heater")
    heater.addToThermalZone(zones["lobby"])

    piu = openstudio.model.AirTerminalSingleDuctParallelPIUReheat(
        model, always_on, openstudio.model.FanConstantVolume(model), openstudio.model.CoilHeatingElectric(model)
    )
    piu.setName("Office_Parallel_PIU")

    # Output variables, one zone-level and one equipment-level.
    out_zone = openstudio.model.OutputVariable("Output:Variable", model)
    out_zone.setName("Output_Zone_Mean_Air_Temperature")
    out_zone.setVariableName("Zone Mean Air Temperature")
    out_zone.setKeyValue("*")
    out_zone.setReportingFrequency("Hourly")

    out_vrf = openstudio.model.OutputVariable("Output:Variable", model)
    out_vrf.setName("Output_VRF_Cooling_Power")
    out_vrf.setVariableName("VRF Heat Pump Cooling Electricity Energy")
    out_vrf.setKeyValue("VRF_Outdoor_Unit")
    out_vrf.setReportingFrequency("Monthly")

    return model


def main() -> None:
    model = build_model()
    if OUTPUT_PATH.exists():
        OUTPUT_PATH.unlink()
    model.save(openstudio.path(str(OUTPUT_PATH)), True)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
