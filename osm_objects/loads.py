import openstudio
import pandas as pd

# People
# --------


def get_all_people_objects_as_dafarame(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieves all the people objects in an OpenStudio model and returns them as a DataFrame.

    Parameters:
        osm_model (openstudio.model.Model): The OpenStudio model containing the people objects.

    Returns:
        pd.DataFrame: A DataFrame containing the people objects and their attributes.
    """

    # Get all people in the OpenStudio model.
    all_people = osm_model.getPeoples()

    # Define the attributes to retrieve in a dictionary.
    object_attr = {
        'Handle': [str(x.handle()) for x in all_people],
        'Name': [x.name().get() for x in all_people],
        'People Definition Name': [x.peopleDefinition().nameString() for x in all_people],
        'Space or SpaceType Name': [
            x.spaceType().get().name().get() if not x.spaceType().isNull() else
            (x.space().get().name().get() if not x.space().isNull() else None)
            for x in all_people
        ],
        'Number of People Schedule Name': [x.numberofPeopleSchedule().get().name().get() if not x.numberofPeopleSchedule().isNull() else None for x in all_people],
        'Activity Level Schedule Name': [x.activityLevelSchedule().get().name().get() if not x.activityLevelSchedule().isNull() else None for x in all_people],
        'Surface Name/Angle Factor List Name': None,
        'Work Efficiency Schedule Name': [x.workEfficiencySchedule().get().name().get() if not x.workEfficiencySchedule().isNull() else None for x in all_people],
        'Clothing Insulation Schedule Name': [x.clothingInsulationSchedule().get().name().get() if not x.clothingInsulationSchedule().isNull() else None for x in all_people],
        'Air Velocity Schedule Name': [x.airVelocitySchedule().get().name().get() if not x.airVelocitySchedule().isNull() else None for x in all_people],
        'Multiplier': None,
        'Ankle Level Air Velocity Schedule Name': [x.ankleLevelAirVelocitySchedule().get().name().get() if not x.ankleLevelAirVelocitySchedule().isNull() else None for x in all_people],
        'Cold Stress Temperature Threshold {C}': None,
        'Heat Stress Temperature Threshold {C}': None
    }

    # Create a DataFrame of all people objects.
    all_people_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_people_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes.
    all_people_df = all_people_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_people_df.shape[0]} people objects")

    return all_people_df


def get_all_people_definition_objects_as_dafarame(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:People:Definition
    # Get all People Definition in the OpenStudio model.
    all_people_definition = osm_model.getPeopleDefinitions()
    floorArea = [x.floorArea() for x in all_people_definition]

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_people_definition],
                   'Name': [x.name().get() for x in all_people_definition],
                   'Number of People Calculation Method': [x.numberofPeopleCalculationMethod() for x in all_people_definition],
                   'Number of People {people}': [result for x, y in zip(all_people_definition, floorArea) for result in [x.getNumberOfPeople(y)]],
                   'People per Space Floor Area {person/m2}': [1/result if result != 0 else 0 for x, y in zip(all_people_definition, floorArea) for result in [x.getFloorAreaPerPerson(y) if x.getNumberOfPeople(y) != 0 else 0]],
                   'Space Floor Area per Person {m2/person}': [result if result != 0 else 0 for x, y in zip(all_people_definition, floorArea) for result in [x.getFloorAreaPerPerson(y) if x.getNumberOfPeople(y) != 0 else 0]],
                   'Fraction Radiant': [x.fractionRadiant() for x in all_people_definition],
                   'Sensible Heat Fraction': [x.sensibleHeatFraction() if not x.sensibleHeatFraction().isNull() else None for x in all_people_definition],
                   'Carbon Dioxide Generation Rate {m3/s-W}': [x.carbonDioxideGenerationRate() for x in all_people_definition],
                   'Enable ASHRAE 55 Comfort Warnings': None}

    # Create a DataFrame of all people objects.
    all_people_definition_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_people_definition_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_people_definition_df = all_people_definition_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_people_definition_df.shape[0]} people definition objects")

    return all_people_definition_df

# Lights
# --------


def get_all_lights_objects_as_dafarame(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:Lights
    # Get all spaces in the OpenStudio model.
    all_lights = osm_model.getLightss()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_lights],
                   'Name': [x.name().get() for x in all_lights],
                   'Lights Definition Name': None,
                   'Space or SpaceType Name': [x.spaceType().get().name().get() if not x.spaceType().isNull() else
                                               (x.space().get().name().get()
                                                if not x.space().isNull() else None)
                                               for x in all_lights],
                   'Schedule Name': None,
                   'Fraction Replaceable': None,
                   'Multiplier': None,
                   'End-Use Subcategory': None}

    # Create a DataFrame of all lights objects.
    all_lights_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_lights_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_lights_df = all_lights_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_lights_df.shape[0]} lights objects")

    return all_lights_df


def get_all_lights_definition_objects_as_dafarame(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:Lights:Definition
    # Get all lights Definition in the OpenStudio model.
    all_lights_definition = osm_model.getLightsDefinitions()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_lights_definition],
                   'Name': [x.name().get() for x in all_lights_definition],
                   'Design Level Calculation Method': None,
                   'Lighting Level {W}': None,
                   'Watts per Space Floor Area {W/m2}': None,
                   'Watts per Person {W/person}': None,
                   'Fraction Radiant': None,
                   'Fraction Visible': None,
                   'Return Air Fraction': None}

    # Create a DataFrame of all lights objects.
    all_lights_definition_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_lights_definition_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_lights_definition_df = all_lights_definition_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_lights_definition_df.shape[0]} lights definition objects")

    return all_lights_definition_df

# Electric Equipment
# --------------------


def get_all_electric_equipment_objects_as_dafarame(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:ElectricEquipment
    # Get all spaces in the OpenStudio model.
    all_electric_equipment = osm_model.getElectricEquipments()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_electric_equipment],
                   'Name': [x.name().get() for x in all_electric_equipment],
                   'Electric Equipment Definition Name': None,
                   'Space or SpaceType Name': [x.spaceType().get().name().get() if not x.spaceType().isNull() else
                                               (x.space().get().name().get()
                                                if not x.space().isNull() else None)
                                               for x in all_electric_equipment],
                   'Schedule Name': None,
                   'Multiplier': None,
                   'End-Use Subcategory': None}
    # Create a DataFrame of all electric_equipment objects.
    all_electric_equipment_df = pd.DataFrame(columns=object_attr.keys())

    for key in object_attr.keys():
        all_electric_equipment_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_electric_equipment_df = all_electric_equipment_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_electric_equipment_df.shape[0]} electric equipment objects")

    return all_electric_equipment_df


def get_all_electric_equipment_definition_objects_as_dafarame(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:ElectricEquipment:Definition
    # Get all electric equipment Definition in the OpenStudio model.
    all_electric_equipment_definition = osm_model.getElectricEquipmentDefinitions()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_electric_equipment_definition],
                   'Name': [x.name().get() for x in all_electric_equipment_definition],
                   'Design Level Calculation Method': None,
                   'Design Level {W}': None,
                   'Watts per Space Floor Area {W/m2}': None,
                   'Watts per Person {W/person}': None}

    # Create a DataFrame of all electric_equipment objects.
    all_electric_equipment_definition_df = pd.DataFrame(
        columns=object_attr.keys())
    for key in object_attr.keys():
        all_electric_equipment_definition_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_electric_equipment_definition_df = all_electric_equipment_definition_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_electric_equipment_definition_df.shape[0]} electric equipment definition objects")

    return all_electric_equipment_definition_df


# Space Infiltration
# --------------------
def get_all_space_infiltration_design_flowrate_objects_as_dafarame(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # OS:ElectricEquipment
    # Get all spaces in the OpenStudio model.
    all_space_infiltration_design_flowrate = osm_model.getSpaceInfiltrationDesignFlowRates()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_space_infiltration_design_flowrate],
                   'Name': [x.name().get() for x in all_space_infiltration_design_flowrate],
                   'Space or SpaceType Name': [x.spaceType().get().name().get() if not x.spaceType().isNull() else
                                               (x.space().get().name().get()
                                                if not x.space().isNull() else None)
                                               for x in all_space_infiltration_design_flowrate],
                   'Schedule Name': None,
                   'Design Flow Rate Calculation Method': None,
                   'Design Flow Rate {m3/s}': None,
                   'Flow per Space Floor Area {m3/s-m2}': None,
                   'Flow per Exterior Surface Area {m3/s-m2}': None,
                   'Air Changes per Hour {1/hr}': None,
                   'Constant Term Coefficient': None,
                   'Temperature Term Coefficient': None,
                   'Velocity Term Coefficient': None,
                   'Velocity Squared Term Coefficient': None}
    # Create a DataFrame of all space_infiltration_design_flowrate objects.
    all_space_infiltration_design_flowrate_df = pd.DataFrame(
        columns=object_attr.keys())

    for key in object_attr.keys():
        all_space_infiltration_design_flowrate_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_space_infiltration_design_flowrate_df = all_space_infiltration_design_flowrate_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_space_infiltration_design_flowrate_df.shape[0]} design infiltration flow rate objects")

    return all_space_infiltration_design_flowrate_df
