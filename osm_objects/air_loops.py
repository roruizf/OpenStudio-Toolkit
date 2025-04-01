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


def get_all_air_loop_hvac_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all Air Loop HVAC objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about Air Loop HVAC objects.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getAirLoopHVACs()

    all_objects_dicts = []

    for target_object in all_objects:
        air_loop_hvac_handle = str(target_object.handle())
        object_dict = get_air_loop_hvac_object_as_dict(
            osm_model, air_loop_hvac_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_air_loop_hvac_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Air Loop HVAC objects from the OpenStudio model using a specified method and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all Air Loop HVAC objects.
    """

    all_objects_dicts = get_all_air_loop_hvac_objects_as_dicts(osm_model)

    # Create a DataFrame of all spaces.
    all_air_loop_hvac_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_air_loop_hvac_df = all_air_loop_hvac_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_air_loop_hvac_df.shape[0]} Air Loop HVAC objects")

    return all_air_loop_hvac_df
