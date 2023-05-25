import bpy
from .tgr_base_panel import TGR_PT_BASE


class TGR_PT_View3D_Panel_CustomProperties(TGR_PT_BASE):
    """Creates a panel to show all the custom properties on the armature bones"""
    bl_label = "Custom Properties"
    bl_idname = "TGR_PT_View3D_Panel_CustomProperties"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and (is_edit_mode or is_pose_mode)

    def draw(self, context):
        layout = self.layout
        # Get the armature object
        armature = context.object
        # Get the armature bone list according to the current mode
        if context.mode == 'EDIT':
            bones = armature.data.edit_bones
            bone_names = [bone.name for bone in bones]
        elif context.mode == 'POSE':
            bones = armature.pose.bones
            bone_names = [bone.name for bone in bones]
        else:
            return
        # Get the custom properties list
        for bone_name in bone_names:
            bone = bones[bone_name]
            if len(bone.keys()) == 0:
                continue
            box = layout.box()
            box.label(text=bone_name)
            for prop in bone.keys():
                box.prop(bone, f'["{prop}"]')

