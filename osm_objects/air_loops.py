import openstudio
import pandas as pd


def get_air_loop_hvac_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirLoopHVAC(
            handle)
        if osm_object is None:
            print(
                f"No Air Loop HVAC  object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirLoopHVACByName(
            name)
        if not osm_object:
            print(
                f"No Air Loop HVAC  object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Controller List Name': None,
        'Availability Schedule': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Availability Manager List Name': None,
        'Design Supply Air Flow Rate {m3/s}': target_object.designSupplyAirFlowRate().get() if not target_object.isDesignSupplyAirFlowRateAutosized() else 'Autosize',
        'Design Return Air Flow Fraction of Supply Air Flow': target_object.designReturnAirFlowFractionofSupplyAirFlow(),
        'Branch List Name': None,
        'Connector List Name': None,
        'Supply Side Inlet Node Name': target_object.supplyInletNode().nameString(),
        'Demand Side Outlet Node Name': target_object.demandOutletNode().nameString(),
        'Demand Side Inlet Node A': target_object.demandInletNode().nameString(),
        'Supply Side Outlet Node A': target_object.supplyOutletNode().nameString(),
        'Demand Side Inlet Node B': None,
        'Supply Side Outlet Node B': None,
        'Return Air Bypass Flow Temperature Setpoint Schedule Name': None,
        'Demand Mixer Name': target_object.demandMixer().nameString(),
        'Demand Splitter A Name': target_object.demandSplitter().nameString(),
        'Demand Splitter B Name': None,
        'Supply Splitter Name': None}
    return object_dict
