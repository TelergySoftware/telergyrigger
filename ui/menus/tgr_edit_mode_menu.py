import bpy


class TGR_MT_EditMode_AddBone(bpy.types.Menu):
    bl_label = "Add Bone"
    bl_idname = "TGR_MT_EditMode_AddBone"
    
    @classmethod
    def poll(cls, context):
        is_armature = context.object is not None and context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def draw(self, context):
        layout = self.layout
        
        layout.operator("tgr.add_deform_bone", text="Deform Bone", icon="BONE_DATA")
        layout.operator("tgr.add_non_deform_bone", text="Non-Deform Bone", icon="BONE_DATA")