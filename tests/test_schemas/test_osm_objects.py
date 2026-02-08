"""Tests for OSM object Pydantic schemas.

These tests verify that schemas can validate dictionaries produced by
the osm_objects extractor functions. They do NOT require OpenStudio -
they use hand-crafted sample dicts that match the real output format.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from openstudio_toolkit.schemas.osm_objects import (
    ConstructionData,
    DefaultConstructionSetData,
    ElectricEquipmentData,
    ElectricEquipmentDefinitionData,
    LightsData,
    LightsDefinitionData,
    MasslessOpaqueMaterialData,
    OsmObjectBase,
    PeopleData,
    PeopleDefinitionData,
    SpaceData,
    StandardOpaqueMaterialData,
    SubSurfaceData,
    SurfaceData,
    ThermalZoneData,
)


class TestOsmObjectBase:
    def test_from_alias(self):
        obj = OsmObjectBase.model_validate({"Handle": "abc-123", "Name": "Test"})
        assert obj.handle == "abc-123"
        assert obj.name == "Test"

    def test_from_field_name(self):
        obj = OsmObjectBase(handle="abc-123", name="Test")
        assert obj.handle == "abc-123"

    def test_missing_handle(self):
        with pytest.raises(ValidationError):
            OsmObjectBase.model_validate({"Name": "NoHandle"})


class TestSpaceData:
    SAMPLE = {
        "Handle": "{a1b2c3d4-e5f6-7890-abcd-ef1234567890}",
        "Name": "Office-1-Floor-1",
        "Space Type Name": "OpenOffice",
        "Default Construction Set Name": None,
        "Default Schedule Set Name": None,
        "Direction of Relative North {deg}": 0.0,
        "X Origin {m}": 0.0,
        "Y Origin {m}": 0.0,
        "Z Origin {m}": 0.0,
        "Building Story Name": "Floor 1",
        "Thermal Zone Name": "Zone-Office-1",
        "Part of Total Floor Area": True,
        "Design Specification Outdoor Air Object Name": "OA-Office",
        "Building Unit Name": None,
        "Volume {m3}": 450.0,
        "Ceiling Height {m}": 3.0,
        "Floor Area {m2}": 150.0,
    }

    def test_validate_sample(self):
        space = SpaceData.model_validate(self.SAMPLE)
        assert space.name == "Office-1-Floor-1"
        assert space.floor_area_m2 == 150.0
        assert space.volume_m3 == 450.0
        assert space.thermal_zone_name == "Zone-Office-1"
        assert space.part_of_total_floor_area is True

    def test_with_enriched_orientation(self):
        enriched = {**self.SAMPLE, "Orientation": "South"}
        space = SpaceData.model_validate(enriched)
        assert space.orientation == "South"

    def test_empty_dict_fails(self):
        with pytest.raises(ValidationError):
            SpaceData.model_validate({})


class TestSurfaceData:
    SAMPLE = {
        "Handle": "{surface-handle-uuid}",
        "Name": "Office-1-Wall-South",
        "Surface Type": "Wall",
        "Construction Name": "Exterior Wall",
        "Space Name": "Office-1",
        "Outside Boundary Condition": "Outdoors",
        "Outside Boundary Condition Object": None,
        "Sun Exposure": "SunExposed",
        "Wind Exposure": "WindExposed",
        "View Factor to Ground": None,
        "Number of Vertices": None,
    }

    def test_validate_sample(self):
        surface = SurfaceData.model_validate(self.SAMPLE)
        assert surface.surface_type == "Wall"
        assert surface.outside_boundary_condition == "Outdoors"

    def test_with_enriched_data(self):
        enriched = {**self.SAMPLE, "Azimuth": 180.0, "Orientation": "South", "Number of Vertices": 4}
        surface = SurfaceData.model_validate(enriched)
        assert surface.azimuth == 180.0
        assert surface.orientation == "South"


class TestThermalZoneData:
    def test_minimal(self):
        tz = ThermalZoneData.model_validate({
            "Handle": "{tz-uuid}",
            "Name": "Zone-1",
            "Multiplier": 1,
            "Use Ideal Air Loads": False,
        })
        assert tz.multiplier == 1
        assert tz.use_ideal_air_loads is False


class TestMaterialData:
    def test_standard_opaque(self):
        mat = StandardOpaqueMaterialData.model_validate({
            "Handle": "{mat-uuid}",
            "Name": "Concrete 200mm",
            "Roughness": "MediumRough",
            "Thickness {m}": 0.2,
            "Conductivity {W/m-K}": 1.4,
            "Density {kg/m3}": 2300.0,
            "Specific Heat {J/kg-K}": 880.0,
            "Thermal Absorptance": 0.9,
            "Solar Absorptance": 0.7,
            "Visible Absorptance": 0.7,
        })
        assert mat.thickness_m == 0.2
        assert mat.conductivity_w_mk == 1.4

    def test_massless(self):
        mat = MasslessOpaqueMaterialData.model_validate({
            "Handle": "{mat-uuid}",
            "Name": "Insulation R-5",
            "Roughness": "Smooth",
            "Thermal Resistance {m2-K/W}": 5.0,
            "Thermal Absorptance": 0.9,
            "Solar Absorptance": 0.7,
            "Visible Absorptance": 0.7,
        })
        assert mat.thermal_resistance_m2kw == 5.0


class TestConstructionData:
    def test_with_layers(self):
        c = ConstructionData.model_validate({
            "Handle": "{con-uuid}",
            "Name": "Exterior Wall",
            "Surface Rendering Name": None,
            "Layer 1": "Brick",
            "Layer 2": "Insulation",
            "Layer 3": "Gypsum",
        })
        assert c.name == "Exterior Wall"
        # Dynamic layers accessible via extra fields
        assert c.model_extra["Layer 1"] == "Brick"


class TestLoadsData:
    def test_people(self):
        p = PeopleData.model_validate({
            "Handle": "{ppl-uuid}",
            "Name": "Office People",
            "People Definition Name": "Office People Def",
            "Space or Space Type Name": "OpenOffice",
            "Number of People Schedule Name": "Occ Schedule",
            "Activity Level Schedule Name": "Activity Schedule",
            "Multiplier": 1.0,
        })
        assert p.people_definition_name == "Office People Def"

    def test_lights(self):
        l = LightsData.model_validate({
            "Handle": "{lights-uuid}",
            "Name": "Office Lights",
            "Lights Definition Name": "Office Lights Def",
            "Space or SpaceType Name": "OpenOffice",
            "Schedule Name": "Lights Schedule",
            "Fraction Replaceable": 1.0,
            "Multiplier": 1.0,
            "End-Use Subcategory": "General",
        })
        assert l.lights_definition_name == "Office Lights Def"
