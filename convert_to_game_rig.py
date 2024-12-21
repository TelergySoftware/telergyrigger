import bpy
from bpy import context

def convert():
    if context.active_object.type != 'ARMATURE':
        print("The active object is not an armature")
        return
    if bpy.context.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')
    
    armature = context.active_object
    bones = armature.pose.bones
    for bone in bones:
        bone.rotation_mode = 'XYZ'
        for constraint in bone.constraints:
            print(constraint.type)
            if constraint.type == 'STRETCH_TO':
                subtarget = constraint.subtarget
                bone.constraints.remove(constraint)
                damped_track = bone.constraints.new('DAMPED_TRACK')
                damped_track.target = armature
                damped_track.subtarget = subtarget

convert()
