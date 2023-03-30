import bpy


class TGR_MT_EditMode_AddBone(bpy.types.Menu):
    bl_label = "Add Bone"
    bl_idname = "TGR_MT_EditMode_AddBone"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_ARMATURE'

    def draw(self, context):
        layout = self.layout
        
        layout.operator("tgr.add_deform_bone", text="Deform Bone", icon="BONE_DATA")
        layout.operator("tgr.add_non_deform_bone", text="Non-Deform Bone", icon="BONE_DATA")