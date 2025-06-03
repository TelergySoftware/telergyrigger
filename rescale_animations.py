import bpy
from bpy import data as D

armature = D.objects['Armature']
scale_factor = .01 # Scale factor to apply to the armature and animations
# Get the actions associated with the armature
actions = D.actions


# Scale the armature object by the scale factor
armature.scale = (scale_factor, scale_factor, scale_factor)
# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')
# Select the armature object
armature.select_set(True)
# Apply the scale to the object
bpy.ops.object.transform_apply(scale=True)

for bone in armature.pose.bones:
    # If the bone has a stretch to constraint, multiply the rest length by the scale factor
    for constraint in bone.constraints:
        if constraint.type == 'STRETCH_TO':
            constraint.rest_length *= scale_factor
        
for action in actions:
    # Scale the location keyframes and the handles by the scale factor
    print('Rescaling action: ', action.name)
    for fcurve in action.fcurves:
        if 'location' in fcurve.data_path:
            for keyframe in fcurve.keyframe_points:
                keyframe.co[1] *= scale_factor
                keyframe.handle_left[1] *= scale_factor
                keyframe.handle_right[1] *= scale_factor
