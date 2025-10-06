import openstudio
from typing import Dict, List, Any

def validator(reference_model: openstudio.model.Model, target_model: openstudio.model.Model, **kwargs) -> Dict[str, Any]:
    """
    Validates if the target model is ready to receive subsurface geometry from the reference model.

    This validator checks for the following conditions:
    1. Both models have the same number of subsurfaces.
    2. The names of all subsurfaces are identical between the two models.
    3. Each corresponding subsurface pair has the same type (e.g., 'FixedWindow', 'Door').
    4. Each corresponding subsurface pair belongs to a parent surface with the same orientation (azimuth).

    Args:
        reference_model (openstudio.model.Model): The source model from which geometry will be copied.
        target_model (openstudio.model.Model): The destination model that will be modified.
        **kwargs: Additional keyword arguments (not used).

    Returns:
        Dict[str, Any]: A dictionary containing the validation 'status' ('READY', 'SKIP', 'ERROR')
                        and a list of 'messages'.
    """
    messages = []
    
    # Create maps of subsurface names to objects for easier lookup
    ref_subsurfaces = {s.name().get(): s for s in reference_model.getSubSurfaces()}
    target_subsurfaces = {s.name().get(): s for s in target_model.getSubSurfaces()}

    # 1. Check for the same number of subsurfaces
    if len(ref_subsurfaces) != len(target_subsurfaces):
        messages.append(f"ERROR: The number of subsurfaces does not match. Reference has {len(ref_subsurfaces)}, target has {len(target_subsurfaces)}.")
        return {"status": "ERROR", "messages": messages}

    # 2. Check if the set of names is identical
    if set(ref_subsurfaces.keys()) != set(target_subsurfaces.keys()):        
        messages.append("ERROR: The names of the subsurfaces in the two models do not match.")
        return {"status": "ERROR", "messages": messages}
        
    if not ref_subsurfaces:
        messages.append("SKIP: No subsurfaces found in the models to process.")
        return {"status": "SKIP", "messages": messages}

    # 3 & 4. Check type and parent surface orientation for each subsurface
    for name, ref_sub in ref_subsurfaces.items():
        target_sub = target_subsurfaces[name]

        # Check subsurface type
        if ref_sub.subSurfaceType() != target_sub.subSurfaceType():
            messages.append(f"ERROR: Subsurface '{name}' has a different type. Reference is '{ref_sub.subSurfaceType()}', target is '{target_sub.subSurfaceType()}'.")
            return {"status": "ERROR", "messages": messages}

        # Check parent surface azimuth
        ref_surface = ref_sub.surface()
        target_surface = target_sub.surface()
        if ref_surface.is_initialized() and target_surface.is_initialized():
            if abs(ref_surface.get().azimuth() - target_surface.get().azimuth()) > 0.01: # Use a small tolerance
                messages.append(f"ERROR: Subsurface '{name}' has a different parent surface azimuth. Reference is {ref_surface.get().azimuth():.2f}, target is {target_surface.get().azimuth():.2f}.")
                return {"status": "ERROR", "messages": messages}
        else:
            messages.append(f"ERROR: Could not find parent surface for subsurface '{name}'.")
            return {"status": "ERROR", "messages": messages}
    
    messages.append("Validation successful. Both models have matching subsurfaces.")
    return {"status": "READY", "messages": messages}


def run(reference_model: openstudio.model.Model, target_model: openstudio.model.Model, **kwargs) -> openstudio.model.Model:
    """
    Copies the vertices from each subsurface in the reference model to the corresponding
    subsurface in the target model.

    This function assumes that the models have been validated and that a one-to-one
    correspondence exists between subsurfaces based on their names.

    Args:
        reference_model (openstudio.model.Model): The source model with the correct geometry.
        target_model (openstudio.model.Model): The destination model whose geometry will be updated.
        **kwargs: Additional keyword arguments (not used).

    Returns:
        openstudio.model.Model: The modified target_model with updated subsurface vertices.
    """
    print("Starting the subsurface geometry copy process...")
    
    # Create a map of reference subsurfaces for efficient lookup
    ref_subsurfaces_map = {s.name().get(): s for s in reference_model.getSubSurfaces()}
    
    # Iterate through target subsurfaces and update their vertices
    for target_sub in target_model.getSubSurfaces():
        target_sub_name = target_sub.name().get()
        if target_sub_name in ref_subsurfaces_map:
            ref_sub = ref_subsurfaces_map[target_sub_name]
            
            # Get vertices from reference and set them on the target
            ref_vertices = ref_sub.vertices()
            target_sub.setVertices(ref_vertices)
            print(f"Successfully copied vertices for subsurface: '{target_sub_name}'")

    print("Subsurface geometry copy process completed.")
    return target_model