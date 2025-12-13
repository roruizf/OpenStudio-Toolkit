import os
import sys

# Ensure we can import the local toolkit source FIRST (before any other imports)
sys.path.insert(0, os.path.abspath("src"))

from openstudio_toolkit.tasks.measures.apply_space_type_and_construction_set_wizard import run, validator
import openstudio


def test_measure_execution():
    print("🚀 Starting Space Type Wizard Test...")

    # 1. Create a Seed Model
    model = openstudio.model.Model()
    print(
        f"📦 Seed Model Created. Initial Space Types: {len(model.getSpaceTypes())}")

    # 2. Define Arguments
    args = {
        "building_type": "SecondarySchool",
        "template": "90.1-2019",
        "climate_zone": "ASHRAE 169-2013-5A",
        "create_space_types": True,
        "create_construction_set": True,
        "set_building_defaults": True
    }

    # 3. Test Validator
    print("\n🔍 Running Validator...")
    # Note: We pass args individually as kwargs matching the function signature
    val_result = validator(model, **args)
    print(f"Validation Result: {val_result}")

    if val_result['status'] != 'READY':
        print("❌ Validation Failed!")
        return

    # 4. Run Measure
    print("\n⚡ Running Measure (calling OpenStudio CLI)...")
    try:
        # The run function returns a NEW model object
        new_model = run(model, **args)

        # 5. Verify Results
        space_types = new_model.getSpaceTypes()
        constructions = new_model.getDefaultConstructionSets()

        print("\n✅ Execution Successful!")
        print(f"📊 Stats:")
        print(f"   - Generated Space Types: {len(space_types)}")
        print(f"   - Construction Sets: {len(constructions)}")

        if len(space_types) > 0:
            print(f"   - Example: {space_types[0].nameString()}")
            new_model.save("test_output.osm", True)
            print("\n💾 Saved 'test_output.osm' for inspection.")
        else:
            print("⚠️ Warning: Measure ran but no space types were found.")

    except Exception as e:
        print(f"\n❌ Critical Error:\n{e}")


if __name__ == "__main__":
    test_measure_execution()
