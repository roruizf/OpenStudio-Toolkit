import pytest
import openstudio
from openstudio_toolkit.osm_objects import spaces
from openstudio_toolkit.utils import osm_utils
import os

@pytest.fixture
def osm_model():
    # Path to the example model
    base_dir = os.path.dirname(os.path.dirname(__file__))
    example_path = os.path.join(base_dir, "examples", "cabana-60.osm")
    return osm_utils.load_osm_file_as_model(example_path)

def test_get_all_spaces(osm_model):
    # Test the refactored get_all_space_objects_as_dataframe
    df = spaces.get_all_space_objects_as_dataframe(osm_model)
    
    # cabana-60.osm has spaces
    assert not df.empty
    assert "Name" in df.columns
    assert "Handle" in df.columns
    print(f"Verified {len(df)} spaces in cabana-60.osm")

def test_get_single_space_by_name(osm_model):
    # Get the name of the first space
    all_spaces = osm_model.getSpaces()
    first_space_name = all_spaces[0].nameString()
    
    # Test lookup by name
    space_dict = spaces.get_space_object_as_dict(osm_model, name=first_space_name)
    assert space_dict["Name"] == first_space_name
    assert "Handle" in space_dict

def test_get_single_space_by_handle(osm_model):
    """
    Test that get_space_object_as_dict correctly retrieves a space using a handle string.
    This specifically tests the helpers.fetch_object function with handle-based retrieval.
    """
    # Get the first space and extract its handle as a string
    all_spaces = osm_model.getSpaces()
    assert len(all_spaces) > 0, "Model must have at least one space for this test"
    
    first_space = all_spaces[0]
    first_space_handle = str(first_space.handle())  # Handle as string
    first_space_name = first_space.nameString()
    
    # Test lookup by handle (this uses helpers.fetch_object internally)
    space_dict = spaces.get_space_object_as_dict(osm_model, handle=first_space_handle)
    
    # Verify the correct space was retrieved
    assert space_dict is not None, "Space dict should not be None"
    assert space_dict != {}, "Space dict should not be empty"
    assert space_dict["Handle"] == first_space_handle, "Handle should match"
    assert space_dict["Name"] == first_space_name, "Name should match"
    
    # Verify that key attributes are present
    assert "Space Type Name" in space_dict
    assert "Thermal Zone Name" in space_dict
    assert "Floor Area {m2}" in space_dict
    assert "Volume {m3}" in space_dict
    assert "Ceiling Height {m}" in space_dict
    
    print(f"✅ Successfully retrieved space '{first_space_name}' using handle string: {first_space_handle}")
    print(f"   Floor Area: {space_dict['Floor Area {m2}']} m²")
    print(f"   Volume: {space_dict['Volume {m3}']} m³")

def test_fetch_object_with_handle_string(osm_model):
    """
    Explicit test for helpers.fetch_object using a handle string.
    This test directly verifies that openstudio.toUUID(handle) works correctly.
    """
    from openstudio_toolkit.utils import helpers
    
    # Get a space and its handle as a string
    all_spaces = osm_model.getSpaces()
    assert len(all_spaces) > 0, "Model must have at least one space"
    
    test_space = all_spaces[0]
    handle_string = str(test_space.handle())
    expected_name = test_space.nameString()
    
    # Test helpers.fetch_object with handle string
    retrieved_space = helpers.fetch_object(
        osm_model=osm_model,
        object_type="Space",
        handle=handle_string,
        name=None,
        _object_ref=None
    )
    
    # Verify the correct object was retrieved
    assert retrieved_space is not None, "fetch_object should return a space object"
    assert retrieved_space.nameString() == expected_name, "Retrieved space name should match"
    assert str(retrieved_space.handle()) == handle_string, "Retrieved space handle should match"
    
    print(f"✅ helpers.fetch_object successfully retrieved space using handle string")
    print(f"   Handle: {handle_string}")
    print(f"   Name: {expected_name}")
