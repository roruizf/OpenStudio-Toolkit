
import pytest
import openstudio
import pandas as pd
from openstudio_toolkit.osm_objects import hvac_air_loops
from openstudio_toolkit.osm_objects import availability_managers
from openstudio_toolkit.osm_objects import component_curves
from openstudio_toolkit.osm_objects import space_types
from openstudio_toolkit.osm_objects import constructions
from openstudio_toolkit.osm_objects import materials
from openstudio_toolkit.osm_objects import surfaces
from openstudio_toolkit.osm_objects import subsurfaces
from openstudio_toolkit.osm_objects import hvac_components
from openstudio_toolkit.osm_objects import building
from openstudio_toolkit.osm_objects import building_stories
from openstudio_toolkit.osm_objects import exterior_equipment
from openstudio_toolkit.osm_objects import outputs
from openstudio_toolkit.osm_objects import hvac_sizing
from openstudio_toolkit.osm_objects import hvac_zone
from openstudio_toolkit.osm_objects import controllers
from openstudio_toolkit.osm_objects import loads
from openstudio_toolkit.osm_objects import schedules
from openstudio_toolkit.osm_objects import spaces
from openstudio_toolkit.osm_objects import thermal_zones

import os

@pytest.fixture
def empty_model():
    return openstudio.model.Model()

@pytest.fixture
def model_with_objects():
    # Load the real model provided by the user
    # We use VersionTranslator as it handles string paths and versioning more robustly
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    osm_path = os.path.join(base_dir, "examples", "R2F-Office-Hub.osm")
    
    if not os.path.exists(osm_path):
        # Alternative for different root contexts
        osm_path = os.path.join(os.getcwd(), "examples", "R2F-Office-Hub.osm")

    if not os.path.exists(osm_path):
        raise FileNotFoundError(f"OSM file not found at {osm_path}")

    vt = openstudio.osversion.VersionTranslator()
    optional_m = vt.loadModel(osm_path)
    
    if optional_m.isNull():
        raise FileNotFoundError(f"Could not load model at {osm_path} via VersionTranslator")
    
    return optional_m.get()

def test_hvac_air_loops(model_with_objects):
    loops = hvac_air_loops.get_all_air_loop_hvac_objects_as_dicts(model_with_objects)
    if loops:
        assert 'Name' in loops[0]
        # Test single get
        handle = loops[0]['Handle']
        single = hvac_air_loops.get_air_loop_hvac_object_as_dict(model_with_objects, handle=handle)
        assert single['Name'] == loops[0]['Name']

def test_component_curves(model_with_objects):
    # This model might not have CurveCubic, try different curve types
    curves = component_curves.get_all_curve_cubic_objects_as_dicts(model_with_objects)
    if not curves:
        curves = component_curves.get_all_curve_biquadratic_objects_as_dicts(model_with_objects)
    
    if curves:
        assert 'Name' in curves[0]

def test_space_types(model_with_objects):
    types = space_types.get_all_space_types_as_dicts(model_with_objects)
    if types:
        assert 'Name' in types[0]

def test_constructions_dataframe(model_with_objects):
    df = constructions.get_all_construction_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert 'Name' in df.columns

def test_materials(model_with_objects):
    mats = materials.get_all_standard_opaque_material_objects_as_dicts(model_with_objects)
    if mats:
        assert 'Name' in mats[0]

def test_surfaces(model_with_objects):
    surfs = surfaces.get_all_surface_objects_as_dicts(model_with_objects)
    if surfs:
        assert 'Name' in surfs[0]

def test_subsurfaces(model_with_objects):
    subs = subsurfaces.get_all_subsurface_objects_as_dicts(model_with_objects)
    if subs:
        assert 'Name' in subs[0]

def test_hvac_components(model_with_objects):
    # Try common components
    df = hvac_components.get_all_pump_variable_speed_objects_as_dataframe(model_with_objects)
    if df.empty:
        df = hvac_components.get_all_chiller_electric_eir_objects_as_dataframe(model_with_objects)
    
    assert isinstance(df, pd.DataFrame)

def test_building_and_stories(model_with_objects):
    df = building.get_building_object_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert 'Name' in df.columns
    
    stories = building_stories.get_all_building_stories_objects_as_dataframe(model_with_objects)
    assert isinstance(stories, pd.DataFrame)

def test_exterior_equipment(model_with_objects):
    ext = exterior_equipment.get_all_exterior_fuel_equipment_definition_objects_as_dataframe(model_with_objects)
    assert isinstance(ext, pd.DataFrame)

def test_outputs(model_with_objects):
    outs = outputs.get_all_output_variable_objects_as_dataframe(model_with_objects)
    assert isinstance(outs, pd.DataFrame)

def test_hvac_sizing(model_with_objects):
    sizing = hvac_sizing.get_all_sizing_zone_objects_as_dataframe(model_with_objects)
    assert isinstance(sizing, pd.DataFrame)

def test_hvac_zone(model_with_objects):
    zone_hvac = hvac_zone.get_all_zone_hvac_equipment_list_objects_as_dataframe(model_with_objects)
    assert isinstance(zone_hvac, pd.DataFrame)

def test_controllers(model_with_objects):
    ctrls = controllers.get_all_controller_outdoor_air_objects_as_dataframe(model_with_objects)
    assert isinstance(ctrls, pd.DataFrame)

def test_loads(model_with_objects):
    ppl = loads.get_all_people_objects_as_dataframe(model_with_objects)
    assert isinstance(ppl, pd.DataFrame)

def test_schedules(model_with_objects):
    schs = schedules.get_all_schedule_ruleset_objects_as_dataframe(model_with_objects)
    assert isinstance(schs, pd.DataFrame)

def test_spaces(model_with_objects):
    sps = spaces.get_all_space_objects_as_dataframe(model_with_objects)
    assert isinstance(sps, pd.DataFrame)
    if not sps.empty:
        assert 'Name' in sps.columns

def test_thermal_zones(model_with_objects):
    tzs = thermal_zones.get_all_thermal_zones_objects_as_dataframe(model_with_objects)
    assert isinstance(tzs, pd.DataFrame)
    if not tzs.empty:
        assert 'Name' in tzs.columns

def test_availability_manager_night_cycle(model_with_objects):
    dicts = availability_managers.get_all_availability_manager_night_cycle_objects_as_dicts(model_with_objects)
    assert len(dicts) > 0, "R2F-Office-Hub should have NightCycle objects"

    first = dicts[0]
    assert "Handle" in first
    assert "Name" in first
    assert "Control Type" in first
    assert "Thermostat Tolerance {deltaC}" in first
    assert "Cycling Run Time {s}" in first

    # Test single get by handle
    handle = first["Handle"]
    single = availability_managers.get_availability_manager_night_cycle_object_as_dict(
        model_with_objects, handle=handle
    )
    assert single["Name"] == first["Name"]


def test_availability_manager_night_cycle_dataframe(model_with_objects):
    df = availability_managers.get_all_availability_manager_night_cycle_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert "Name" in df.columns
        assert "Control Type" in df.columns


def test_fetch_object_helpers_integration(model_with_objects):
    # Verify strict argument validation still works via the modules
    with pytest.raises(ValueError):
        space_types.get_space_type_as_dict(model_with_objects, space_type_handle="fake", space_type_name="fake")

    with pytest.raises(ValueError):
        space_types.get_space_type_as_dict(model_with_objects) # Neither provided


# ---------------------------------------------------------------------------
# Loads Tests
# ---------------------------------------------------------------------------

def test_people(model_with_objects):
    dicts = loads.get_all_people_objects_as_dicts(model_with_objects)
    assert len(dicts) > 0, "R2F-Office-Hub should have People objects"

    first = dicts[0]
    assert "Handle" in first
    assert "Name" in first
    assert "People Definition Name" in first
    assert "Space or SpaceType Name" in first
    assert "Multiplier" in first


def test_people_dataframe(model_with_objects):
    df = loads.get_all_people_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "R2F-Office-Hub should have People objects"
    assert "Name" in df.columns
    assert "People Definition Name" in df.columns


def test_people_definition(model_with_objects):
    dicts = loads.get_all_people_definition_objects_as_dicts(model_with_objects)
    assert len(dicts) > 0, "R2F-Office-Hub should have People Definition objects"

    first = dicts[0]
    assert "Handle" in first
    assert "Name" in first
    assert "Number of People Calculation Method" in first
    assert "Fraction Radiant" in first


def test_people_definition_dataframe(model_with_objects):
    df = loads.get_all_people_definition_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "R2F-Office-Hub should have People Definition objects"
    assert "Name" in df.columns


def test_lights(model_with_objects):
    dicts = loads.get_all_lights_objects_as_dicts(model_with_objects)
    assert len(dicts) > 0, "R2F-Office-Hub should have Lights objects"

    first = dicts[0]
    assert "Handle" in first
    assert "Name" in first
    assert "Lights Definition Name" in first
    assert "Space or SpaceType Name" in first
    assert "Multiplier" in first


def test_lights_dataframe(model_with_objects):
    df = loads.get_all_lights_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "R2F-Office-Hub should have Lights objects"
    assert "Name" in df.columns
    assert "Lights Definition Name" in df.columns


def test_lights_definition(model_with_objects):
    dicts = loads.get_all_lights_definition_objects_as_dicts(model_with_objects)
    assert len(dicts) > 0, "R2F-Office-Hub should have Lights Definition objects"

    first = dicts[0]
    assert "Handle" in first
    assert "Name" in first
    assert "Design Level Calculation Method" in first
    assert "Fraction Radiant" in first


def test_lights_definition_dataframe(model_with_objects):
    df = loads.get_all_lights_definition_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "R2F-Office-Hub should have Lights Definition objects"
    assert "Name" in df.columns


def test_electric_equipment(model_with_objects):
    dicts = loads.get_all_electric_equipment_objects_as_dicts(model_with_objects)
    assert len(dicts) > 0, "R2F-Office-Hub should have ElectricEquipment objects"

    first = dicts[0]
    assert "Handle" in first
    assert "Name" in first
    assert "Electric Equipment Definition Name" in first
    assert "Space or SpaceType Name" in first
    assert "Multiplier" in first


def test_electric_equipment_dataframe(model_with_objects):
    df = loads.get_all_electric_equipment_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "R2F-Office-Hub should have ElectricEquipment objects"
    assert "Name" in df.columns
    assert "Electric Equipment Definition Name" in df.columns


def test_electric_equipment_definition(model_with_objects):
    dicts = loads.get_all_electric_equipment_definition_objects_as_dicts(model_with_objects)
    assert len(dicts) > 0, "R2F-Office-Hub should have ElectricEquipment Definition objects"

    first = dicts[0]
    assert "Handle" in first
    assert "Name" in first
    assert "Design Level Calculation Method" in first
    assert "Fraction Radiant" in first


def test_electric_equipment_definition_dataframe(model_with_objects):
    df = loads.get_all_electric_equipment_definition_objects_as_dataframe(model_with_objects)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "R2F-Office-Hub should have ElectricEquipment Definition objects"
    assert "Name" in df.columns
