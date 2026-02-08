"""Tests for OSM object Pydantic schemas.

These tests verify that schemas can validate dictionaries produced by
the osm_objects extractor functions. They do NOT require OpenStudio -
they use hand-crafted sample dicts that match the real output format.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from openstudio_toolkit.schemas.osm_objects import (
    AvailabilityManagerNightCycleData,
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
            "Space or SpaceType Name": "OpenOffice",
            "Number of People Schedule Name": "Occ Schedule",
            "Activity Level Schedule Name": "Activity Schedule",
            "Surface Name/Angle Factor List Name": None,
            "Work Efficiency Schedule Name": None,
            "Clothing Insulation Schedule Name": None,
            "Air Velocity Schedule Name": None,
            "Multiplier": 1.0,
        })
        assert p.people_definition_name == "Office People Def"
        assert p.space_or_spacetype_name == "OpenOffice"

    def test_people_definition(self):
        pd = PeopleDefinitionData.model_validate({
            "Handle": "{ppl-def-uuid}",
            "Name": "Office People Def",
            "Number of People Calculation Method": "People",
            "Number of People {people}": 10.0,
            "People per Space Floor Area {person/m2}": None,
            "Space Floor Area per Person {m2/person}": None,
            "Fraction Radiant": 0.3,
            "Sensible Heat Fraction": 0.6,
            "Carbon Dioxide Generation Rate {m3/s-W}": 3.82e-8,
        })
        assert pd.number_of_people_calculation_method == "People"
        assert pd.fraction_radiant == 0.3

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

    def test_lights_definition(self):
        ld = LightsDefinitionData.model_validate({
            "Handle": "{lights-def-uuid}",
            "Name": "Office Lights Def",
            "Design Level Calculation Method": "LightingLevel",
            "Lighting Level {W}": 1000.0,
            "Watts per Space Floor Area {W/m2}": None,
            "Watts per Person {W/person}": None,
            "Fraction Radiant": 0.42,
            "Fraction Visible": 0.18,
            "Return Air Fraction": 0.0,
        })
        assert ld.design_level_calculation_method == "LightingLevel"
        assert ld.lighting_level_w == 1000.0

    def test_electric_equipment(self):
        ee = ElectricEquipmentData.model_validate({
            "Handle": "{ee-uuid}",
            "Name": "Office Equipment",
            "Electric Equipment Definition Name": "Office Equipment Def",
            "Space or SpaceType Name": "OpenOffice",
            "Schedule Name": "Equipment Schedule",
            "Multiplier": 1.0,
            "End-Use Subcategory": "General",
        })
        assert ee.electric_equipment_definition_name == "Office Equipment Def"

    def test_electric_equipment_definition(self):
        eed = ElectricEquipmentDefinitionData.model_validate({
            "Handle": "{ee-def-uuid}",
            "Name": "Office Equipment Def",
            "Design Level Calculation Method": "EquipmentLevel",
            "Design Level {W}": 500.0,
            "Watts per Space Floor Area {W/m2}": None,
            "Watts per Person {W/person}": None,
            "Fraction Latent": 0.0,
            "Fraction Radiant": 0.2,
            "Fraction Lost": 0.0,
        })
        assert eed.design_level_calculation_method == "EquipmentLevel"
        assert eed.design_level_w == 500.0


class TestAvailabilityManagerNightCycleData:
    SAMPLE = {
        "Handle": "{61a28efb-7132-4c2c-8a1a-2af5fe6eff77}",
        "Name": "Availability Manager Night Cycle 1",
        "Applicability Schedule": "Always On Discrete",
        "Fan Schedule": None,
        "Control Type": "CycleOnAny",
        "Thermostat Tolerance {deltaC}": 1.0,
        "Cycling Run Time Control Type": "FixedRunTime",
        "Cycling Run Time {s}": 1800.0,
        "Control Zone or Zone List Name": "Thermal Zone 1",
        "Cooling Control Zone or Zone List Name": None,
        "Heating Control Zone or Zone List Name": None,
        "Heating Zone Fans Only Zone or Zone List Name": None,
    }

    def test_validate_sample(self):
        obj = AvailabilityManagerNightCycleData.model_validate(self.SAMPLE)
        assert obj.name == "Availability Manager Night Cycle 1"
        assert obj.control_type == "CycleOnAny"
        assert obj.thermostat_tolerance_deltac == 1.0
        assert obj.cycling_run_time_s == 1800.0
        assert obj.control_zone_or_zone_list_name == "Thermal Zone 1"
        assert obj.fan_schedule is None

    def test_with_thermostat_cycling_control(self):
        """Variant with StayOff + Thermostat cycling (R2F-Office-Hub pattern)."""
        sample = {
            **self.SAMPLE,
            "Control Type": "StayOff",
            "Thermostat Tolerance {deltaC}": 1.9999,
            "Cycling Run Time Control Type": "Thermostat",
            "Cycling Run Time {s}": 3600.0,
        }
        obj = AvailabilityManagerNightCycleData.model_validate(sample)
        assert obj.control_type == "StayOff"
        assert obj.thermostat_tolerance_deltac == 1.9999
        assert obj.cycling_run_time_control_type == "Thermostat"
        assert obj.cycling_run_time_s == 3600.0

    def test_with_multiple_control_zones(self):
        """Comma-separated zone names validate as string."""
        sample = {
            **self.SAMPLE,
            "Control Zone or Zone List Name": "Zone 1, Zone 2, Zone 3",
        }
        obj = AvailabilityManagerNightCycleData.model_validate(sample)
        assert obj.control_zone_or_zone_list_name == "Zone 1, Zone 2, Zone 3"

    def test_missing_handle_fails(self):
        with pytest.raises(ValidationError):
            AvailabilityManagerNightCycleData.model_validate({"Name": "No Handle"})

    def test_empty_dict_fails(self):
        with pytest.raises(ValidationError):
            AvailabilityManagerNightCycleData.model_validate({})
