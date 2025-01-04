# Ensure that this script is executed in a Blender context where the bpy module is available
import bpy

# ADSR parameters
# Default for frames at 60 FPS
attack = 5.0  # Speed (In frames) for initiating a key press
decay = 5.0  # Speed (In Frames) for stopping the initial attack overcommit
sustain_level = 0.7  # Level (0 to 1)
release = 2.0  # Speed (In Frames) at which the key is released
note_depth = 0.03  # Depth to which the key is pressed in blender location values

# Ensure all elements of the animation_list conform to the expected structure and data types
# Example input
animation_list = [[5, 55, 0.8582677165354331, 0, 41]]

# Calculate the ADSR envelope, confirming it produces a smooth curve across the given duration
def calculate_adsr_envelope(attack, decay, sustain_level, release, duration):
    envelope = []
    print("executed")
    for t in range(duration):
        if t < attack:
            level = t / attack
        elif t < attack + decay:
            level = 1 - (1 - sustain_level) * (t - attack) / decay
        elif t < duration - release:
            level = sustain_level
        else:
            level = sustain_level * (1 - (t - (duration - release)) / release)
        envelope.append(level)
    return envelope

# Ensure objects referenced by obj exist and have necessary properties like location
def set_kf_object(obj, start_frame, end_frame, attack, decay, sustain_level, release):
    initial_z = obj.location.z
    note_down_z = initial_z - note_depth

    # Confirm that the duration is valid and prevents negative or zero-length animations
    duration = end_frame - start_frame
    adsr_envelope = calculate_adsr_envelope(attack, decay, sustain_level, release, duration)
    
    # Insert keyframes for location.z, ensuring the note press and release are visually distinct
    for i, level in enumerate(adsr_envelope):
        current_frame = start_frame + i
        z_value = initial_z - level * note_depth
        obj.location.z = z_value
        obj.keyframe_insert(data_path="location", index=2, frame=current_frame)
    
    # Ensure the material creation logic checks for both node availability and compatibility
    material_name = "glow" + str(obj.name)
    glowingmat = bpy.data.materials.get(material_name) or bpy.data.materials.new(name=material_name)

    if not glowingmat.use_nodes:
        glowingmat.use_nodes = True
        
    obj.active_material = glowingmat
    glowingMatNodes = glowingmat.node_tree.nodes
    glowingMatLinks = glowingmat.node_tree.links

    def get_node(nodes, node_type):
        # Retrieve existing nodes of the specified type or create new ones
        for node in nodes:
            if node.type == node_type:
                return node
        return nodes.new(type=node_type)

    # Delete emission shader node if it exists
    for node in glowingMatNodes:
        if node.type == 'EMISSION':
            glowingMatNodes.remove(node)
    print("the glowing executed")
    principled_bsdf_node = get_node(glowingMatNodes, 'BSDF_PRINCIPLED')
    material_output_node = get_node(glowingMatNodes, 'OUTPUT_MATERIAL')

    # Verify that the Principled BSDF node connects properly to the output node
    if not any(link.to_node == material_output_node and link.from_node == principled_bsdf_node for link in glowingMatLinks):
        glowingMatLinks.new(principled_bsdf_node.outputs['BSDF'], material_output_node.inputs['Surface'])

    # Insert keyframes for the emission strength, ensuring the glow effect synchronizes with animation
    bpy.data.materials["glow" + str(obj.name)].node_tree.nodes["Principled BSDF"].inputs[28].default_value = 0
    principled_bsdf_node.inputs[28].keyframe_insert(data_path="default_value", frame=start_frame - 1)
    
    bpy.data.materials["glow" + str(obj.name)].node_tree.nodes["Principled BSDF"].inputs[28].default_value = 50
    principled_bsdf_node.inputs[28].keyframe_insert(data_path="default_value", frame=start_frame)
    
    bpy.data.materials["glow" + str(obj.name)].node_tree.nodes["Principled BSDF"].inputs[28].default_value = 0
    
    if start_frame + 60 > end_frame:
        principled_bsdf_node.inputs[28].keyframe_insert(data_path="default_value", frame=end_frame)
    else:
        principled_bsdf_node.inputs[28].keyframe_insert(data_path="default_value", frame=end_frame)

    # Reset object location to avoid conflicts with subsequent animations
    obj.location.z = initial_z
    obj.keyframe_insert(data_path="location", index=2, frame=end_frame + release)
    
    current_frame = start_frame
    
    # Ensure Marbles collection exists and is populated before looping
    marbleColl = bpy.data.collections.get("Marbles")
    
    noMarble = True

    while noMarble:
        for marble in marbleColl.objects:
            print("entered loop")
            
            # Validate marble keyframe logic and ensure it aligns with the animation timing
            bpy.context.scene.frame_set(current_frame - 90)
            if marble.location.x == 0 and marble.location.x == 0 and marble.location.z == 8:
                bpy.context.scene.frame_set(current_frame - 45)
                if marble.location.x == 0 and marble.location.x == 0 and marble.location.z == 8:
                    bpy.context.scene.frame_set(current_frame)
                    if marble.location.x == 0 and marble.location.x == 0 and marble.location.z == 8:
                        print("starting keyframes")
                      
                        marble.keyframe_insert(data_path="location", index=-1, frame=current_frame - 91)
                     
                        marble.location = obj.location 
                        marble.location.z = marble.location.z + 5
                       
                        marble.keyframe_insert(data_path="location", index=-1, frame=current_frame - 90)
                            
                        marble.location.z = marble.location.z - 5.3
                            
                        marble.keyframe_insert(data_path="location", index=-1, frame=current_frame)
                        
                        marble.location = (0, 0, 8)
                        
                        marble.keyframe_insert(data_path="location", index=-1, frame=current_frame + 1)
                        
                        # Check and adjust interpolation settings for all keyframes
                        action = marble.animation_data.action
                        for fcurve in action.fcurves:
                            for keyframe in fcurve.keyframe_points:
                                keyframe.interpolation = 'QUAD'
                        
                        noMarble = False
                        break
        else:
            print("NEED MORE MARBLES")
            break       
    # Reset scene frame to initial state after animation setup
    bpy.context.scene.frame_set(0)

# Iterate over animation_list, ensuring each animation conforms to the expected note, start, and end frame formats
def create_piano_animation(animation_list):
    for anim in animation_list:
        print("this code loop executed")
        note = anim[1]
        start_frame = anim[3] * 2  # Convert to 60 FPS
        end_frame = anim[4] * 2  # Convert to 60 FPS

        key_name = str(note)
        if key_name in bpy.data.objects:
            key = bpy.data.objects[key_name]
            
            # Pass validated parameters to the set_kf_object function
            set_kf_object(key, start_frame, end_frame, attack, decay, sustain_level, release)

# Set the scene frame rate to 60 FPS for consistent timing
bpy.context.scene.render.fps = 60

# Call the main animation function with the provided list
create_piano_animation(animation_list)

# CSV Data:
['[5, 55, 0.8582677165354331, 0, 41]', '[5, 47, 0.8582677165354331, 0, 41]', '[5, 52, 0.8582677165354331, 0, 41]', '[5, 69, 0.8582677165354331, 41, 61]', '[5, 54, 0.8582677165354331, 41, 82]', '[5, 71, 0.8582677165354331, 61, 82]', '[5, 45, 0.8582677165354331, 82, 123]', '[5, 62, 0.8582677165354331, 82, 123]', '[5, 57, 0.8582677165354331, 82, 123]', '[5, 66, 0.8582677165354331, 82, 123]', '[5, 62, 0.8582677165354331, 143, 153]', '[5, 47, 0.8582677165354331, 123, 163]', '[5, 64, 0.8582677165354331, 153, 163]', '[5, 57, 0.8582677165354331, 164, 204]', '[5, 61, 0.8582677165354331, 164, 204]', '[5, 66, 0.8582677165354331, 164, 204]', '[5, 55, 0.8582677165354331, 205, 225]', '[5, 54, 0.8582677165354331, 225, 235]', '[5, 57, 0.8582677165354331, 235, 245]', '[5, 57, 0.8582677165354331, 245, 327]', '[5, 61, 0.8582677165354331, 245, 327]', '[5, 64, 0.8582677165354331, 245, 327]', '[5, 45, 0.8582677165354331, 245, 327]', '[5, 74, 0.8582677165354331, 348, 368]', '[5, 71, 0.8582677165354331, 368, 388]', '[5, 55, 0.8582677165354331, 327, 409]', '[5, 64, 0.8582677165354331, 327, 409]', '[5, 67, 0.8582677165354331, 327, 409]', '[5, 52, 0.8582677165354331, 327, 409]', '[5, 69, 0.8582677165354331, 389, 409]', '[5, 43, 0.8582677165354331, 409, 450]', '[5, 57, 0.8582677165354331, 409, 470]', '[5, 66, 0.8582677165354331, 409, 470]', '[5, 62, 0.8582677165354331, 409, 470]', '[5, 62, 0.8582677165354331, 470, 480]', '[5, 47, 0.8582677165354331, 450, 491]', '[5, 64, 0.8582677165354331, 481, 491]', '[5, 57, 0.8582677165354331, 491, 532]', '[5, 61, 0.8582677165354331, 491, 532]', '[5, 66, 0.8582677165354331, 491, 532]', '[5, 69, 0.8582677165354331, 552, 562]', '[5, 54, 0.8582677165354331, 532, 573]', '[5, 66, 0.8582677165354331, 562, 573]', '[5, 45, 0.8582677165354331, 573, 654]', '[5, 57, 0.8582677165354331, 573, 654]', '[5, 61, 0.8582677165354331, 573, 654]', '[5, 64, 0.8582677165354331, 573, 654]', '[5, 59, 0.8582677165354331, 655, 695]', '[5, 64, 0.8582677165354331, 655, 695]', '[5, 67, 0.8582677165354331, 655, 695]', '[5, 52, 0.8582677165354331, 655, 695]', '[5, 69, 0.8582677165354331, 695, 716]', '[5, 54, 0.8582677165354331, 695, 736]', '[5, 71, 0.8582677165354331, 716, 736]', '[5, 66, 0.8582677165354331, 736, 777]', '[5, 62, 0.8582677165354331, 736, 777]', '[5, 43, 0.8582677165354331, 736, 777]', '[5, 57, 0.8582677165354331, 736, 777]', '[5, 74, 0.8582677165354331, 736, 777]', '[5, 59, 0.8582677165354331, 777, 798]', '[5, 62, 0.8582677165354331, 798, 808]', '[5, 78, 0.8582677165354331, 798, 808]', '[5, 64, 0.8582677165354331, 808, 818]', '[5, 76, 0.8582677165354331, 808, 818]', '[5, 69, 0.8582677165354331, 818, 859]', '[5, 61, 0.8582677165354331, 818, 859]', '[5, 57, 0.8582677165354331, 818, 859]', '[5, 73, 0.8582677165354331, 818, 859]', '[5, 74, 0.8582677165354331, 880, 890]', '[5, 55, 0.8582677165354331, 859, 900]', '[5, 66, 0.8582677165354331, 880, 900]', '[5, 73, 0.8582677165354331, 890, 900]', '[5, 69, 0.8582677165354331, 900, 982]', '[5, 59, 0.8582677165354331, 982, 1023]', '[5, 67, 0.8582677165354331, 982, 1023]', '[5, 64, 0.8582677165354331, 982, 1023]', '[5, 71, 0.8582677165354331, 1023, 1043]', '[5, 66, 0.8582677165354331, 1023, 1063]', '[5, 69, 0.8582677165354331, 1043, 1063]', '[5, 57, 0.8582677165354331, 1064, 1104]', '[5, 74, 0.8582677165354331, 1064, 1104]', '[5, 69, 0.8582677165354331, 1064, 1104]', '[5, 78, 0.8582677165354331, 1064, 1104]', '[5, 74, 0.8582677165354331, 1125, 1135]', '[5, 59, 0.8582677165354331, 1105, 1145]', '[5, 76, 0.8582677165354331, 1135, 1145]', '[5, 69, 0.8582677165354331, 1145, 1186]', '[5, 73, 0.8582677165354331, 1145, 1186]', '[5, 78, 0.8582677165354331, 1145, 1186]', '[5, 67, 0.8582677165354331, 1186, 1207]', '[5, 66, 0.8582677165354331, 1207, 1217]', '[5, 69, 0.8582677165354331, 1217, 1227]', '[5, 61, 0.8582677165354331, 1227, 1309]', '[5, 57, 0.8582677165354331, 1227, 1309]', '[5, 64, 0.8582677165354331, 1227, 1309]']