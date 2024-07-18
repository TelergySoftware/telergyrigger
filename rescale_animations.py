import bpy
from bpy import data as D

armature = D.objects['Heli_01']
scale_factor = 0.04
actions = D.actions


for action in actions:
    # Scale the location keyframes and the handles by the scale factor
    # Continue if the action name is H_Idle
    print(action.name)
    if action.name == 'H_Idle':
        continue
    print('Rescaling action: ', action.name)
    for fcurve in action.fcurves:
        if 'location' in fcurve.data_path:
            for keyframe in fcurve.keyframe_points:
                keyframe.co[1] *= scale_factor
                keyframe.handle_left[1] *= scale_factor
                keyframe.handle_right[1] *= scale_factor
                