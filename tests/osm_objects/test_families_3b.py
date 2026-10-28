"""Item 3b: the eight new curated families, and port fields read as node names.

A port field (``Inlet Node Name``, ``Water Outlet Node Name``, ...) stores the handle of an
``OS:Connection``; the view gives the name of the node on the other side, the same node OpenStudio's
``inletModelObject()`` / ``outletModelObject()`` return. Before 3b, ``pump_variable_speed``,
``fan_constant_volume`` and ``fan_on_off`` returned ``inletPort()`` / ``outletPort()``, the port
index (2, 3), under those columns.
"""

from __future__ import annotations

import re
from pathlib import Path

import openstudio
import pandas as pd
import pytest

from openstudio_toolkit import dump
from openstudio_toolkit._sdk import opt

M = openstudio.model
EXTRA = Path(__file__).resolve().parents[1] / "resources" / "extra_families.osm"
NEW = {
    "thermostat_setpoint_dual_setpoint": "OS:ThermostatSetpoint:DualSetpoint",
    "window_material_simple_glazing_system": "OS:WindowMaterial:SimpleGlazingSystem",
    "fan_variable_volume": "OS:Fan:VariableVolume",
    "pump_constant_speed": "OS:Pump:ConstantSpeed",
    "cooling_tower_two_speed": "OS:CoolingTower:TwoSpeed",
    "cooling_tower_variable_speed": "OS:CoolingTower:VariableSpeed",
    "boiler_hot_water": "OS:Boiler:HotWater",
    "zone_hvac_ideal_loads_air_system": "OS:ZoneHVAC:IdealLoadsAirSystem",
}


@pytest.fixture(scope="module")
def extra():
    return openstudio.osversion.VersionTranslator().loadModel(str(EXTRA)).get()


def _blank(value) -> bool:
    return value is None or (isinstance(value, float) and pd.isna(value))


@pytest.mark.parametrize("family", sorted(NEW))
def test_columns_are_every_idd_field(family: str) -> None:
    idd = openstudio.IddFactory.instance().getObject(openstudio.IddObjectType(NEW[family])).get()
    fields = [idd.getField(i).get().name() for i in range(idd.numFields())]
    columns = dump.dump_view(M.Model(), [family])[family].columns
    assert [re.sub(r" \{.*\}$", "", c) for c in columns] == fields


@pytest.mark.parametrize("family", sorted(NEW))
def test_fixture_has_two_or_more_rows(extra, family: str) -> None:
    expected = 1 if family.startswith("cooling_tower") else 2
    assert len(dump.dump_view(extra, [family])[family]) >= expected


def test_port_fields_give_the_node_openstudio_connects(extra) -> None:
    view = dump.dump_view(extra, ["pump_constant_speed", "boiler_hot_water", "fan_variable_volume"])
    checked = 0
    for family, getter, inlet, outlet in [
        ("pump_constant_speed", "getPumpConstantSpeeds", "Inlet Node Name", "Outlet Node Name"),
        ("boiler_hot_water", "getBoilerHotWaters", "Boiler Water Inlet Node Name", "Boiler Water Outlet Node Name"),
        ("fan_variable_volume", "getFanVariableVolumes", "Air Inlet Node Name", "Air Outlet Node Name"),
    ]:
        rows = view[family].set_index("Name")
        for obj in getattr(extra, getter)():
            for column, side in ((inlet, obj.inletModelObject()), (outlet, obj.outletModelObject())):
                node = opt(side)
                cell = rows.loc[obj.nameString(), column]
                if node is None:
                    assert _blank(cell)
                else:
                    assert cell == node.nameString() and cell.startswith("Node")
                    checked += 1
    assert checked == 2 * (1 + 2 + 2)  # two ports each: 1 pump on a loop (the spare one is not), 2 boilers, 2 fans


def test_existing_readers_give_node_names_not_port_indices() -> None:
    model = M.Model()
    loop = M.PlantLoop(model)
    pump = M.PumpVariableSpeed(model)
    pump.setName("VS Pump")
    pump.addToNode(loop.supplyInletNode())
    air = M.AirLoopHVAC(model)
    fan = M.FanConstantVolume(model)
    fan.setName("CV Fan")
    fan.addToNode(air.supplyOutletNode())
    view = dump.dump_view(model, ["pump_variable_speed", "fan_constant_volume"])
    pump_row = view["pump_variable_speed"].iloc[0]
    fan_row = view["fan_constant_volume"].iloc[0]
    assert pump_row["Inlet Node Name"] == opt(pump.inletModelObject()).nameString()
    assert pump_row["Outlet Node Name"] == opt(pump.outletModelObject()).nameString()
    assert fan_row["Air Inlet Node Name"] == opt(fan.inletModelObject()).nameString()
    assert fan_row["Air Outlet Node Name"] == opt(fan.outletModelObject()).nameString()


def test_autosize_and_numbers(extra) -> None:
    tower = dump.dump_view(extra, ["cooling_tower_two_speed"])["cooling_tower_two_speed"].iloc[0]
    assert tower["Design Water Flow Rate {m3/s}"] == "Autosize"
    assert tower["High Fan Speed Fan Power {W}"] == 600.0
    assert tower["Number of Cells"] == 1  # empty in the file: OpenStudio's default
    boilers = dump.dump_view(extra, ["boiler_hot_water"])["boiler_hot_water"].set_index("Name")
    assert boilers.loc["Lead_Boiler", "Nominal Capacity {W}"] == 50000.0
    thermostats = dump.dump_view(extra, ["thermostat_setpoint_dual_setpoint"])["thermostat_setpoint_dual_setpoint"]
    assert set(thermostats["Heating Setpoint Temperature Schedule Name"]) == {"Heating_Setpoint_Schedule"}
