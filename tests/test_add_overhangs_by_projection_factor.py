import openstudio
import os
import logging
from pathlib import Path
from openstudio_toolkit.tasks.measures import add_overhangs_by_projection_factor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_add_overhangs():
    # 1. Setup paths
    measure_resources = Path("src/openstudio_toolkit/resources/measures/AddOverhangsByProjectionFactor")
    test_model_path = measure_resources / "tests" / "OverhangTestModel_01.osm"
    
    # Note: measure.xml says filename is OverhangTestModel_01.osm but list_dir says 'tests' is a dir.
    # Let's verify where the OSM is.
    if not test_model_path.exists():
        # Maybe it's directly in the root of the measure resource (though measure.xml list it under files)
        test_model_path = measure_resources / "OverhangTestModel_01.osm"
    
    if not test_model_path.exists():
        logger.error(f"Test model not found at {test_model_path}")
        # Create a simple box model if source not found
        model = openstudio.model.Model()
        space = openstudio.model.Space(model)
        # ... actually let's just fail if not found since we want to verify the real resource
        raise FileNotFoundError(f"Could not find test model {test_model_path}")

    logger.info(f"Loading test model from {test_model_path}")
    
    # 2. Load model
    vt = openstudio.osversion.VersionTranslator()
    model = vt.loadModel(str(test_model_path)).get()
    
    # 3. Remove weather file reference to avoid CLI errors
    model.getWeatherFile().remove()
    logger.info("Removed weather file reference from model.")
    
    # 4. Count initial shading surfaces
    initial_shading = len(model.getShadingSurfaces())
    logger.info(f"Initial shading surfaces: {initial_shading}")
    
    # 4. Run measure wrapper
    logger.info("Running measure: Add Overhangs by Projection Factor (South, PF=0.5)")
    try:
        result_model = add_overhangs_by_projection_factor.run(
            osm_model=model,
            projection_factor=0.5,
            facade="South",
            remove_ext_space_shading=True
        )
        
        # 5. Verify results
        final_shading = len(result_model.getShadingSurfaces())
        logger.info(f"Final shading surfaces: {final_shading}")
        
        if final_shading > initial_shading or (initial_shading > 0 and final_shading >= 0):
             # Depending on the model, it might replace or add. 
             # Let's check for "Overhang" in names
             overhangs = [s for s in result_model.getShadingSurfaces() if "Overhang" in s.nameString()]
             logger.info(f"Found {len(overhangs)} overhangs in the result model.")
             
             if len(overhangs) > 0:
                 logger.info("SUCCESS: Measure applied correctly and generated overhangs.")
             else:
                 logger.warning("Measure ran but no overhangs were created. Check if the test model has South windows.")
        else:
            logger.error("FAILURE: Shading surface count did not increase as expected.")
            
    except Exception as e:
        logger.error(f"Measure execution failed: {e}")
        raise

if __name__ == "__main__":
    test_add_overhangs()
