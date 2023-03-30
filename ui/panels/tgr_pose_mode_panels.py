from .tgr_base_panel import TGR_PT_BASE


# ------------- POSE MODE -------------
class TGR_PT_View3D_Panel_PoseMode(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Pose Mode.
    This panel is only visible when in Pose Mode,
    and only if the selected object is an Armature.
    """
    bl_label = "Pose Mode"
    bl_idname = "TGR_PT_View3D_Panel_PoseMode"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def draw(self, context):
        layout = self.layout
        # Pose Mode
        row = layout.row()
        row.label(text="Pose Mode")


# Pose TGT Subpanel
class TGR_PT_View3D_Panel_PoseMode_TGT(TGR_PT_BASE):
    """
    Creates the subpanel for the Addon in Pose Mode.
    This panel is only visible when in Pose Mode,
    and only if the selected object is an Armature.
    """
    bl_label = "TGT"
    bl_idname = "TGR_PT_View3D_Panel_PoseMode_TGT"
    bl_parent_id = "TGR_PT_View3D_Panel_PoseMode"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def draw(self, context):
        layout = self.layout
        # Bind and Unbind TGT bones
        row = layout.row()
        
        col = row.column()
        col.operator("tgr.bind_tgt", icon='LOCKED')

        col = row.column()
        col.operator("tgr.unbind_tgt", icon='UNLOCKED')

        # Isolate TGT bone rotation
        row = layout.row()
        row.operator("tgr.isolate_bone_rotation", icon='UNLINKED', text="Isolate Rotation")

        # Create IK FK Switch Chain
        row = layout.row()
        row.operator("tgr.create_ikfk_switch_chain", icon='BONE_DATA')
        
        # Create Stretch to Chain
        row = layout.row()
        row.operator("tgr.create_stretch_to_chain", icon='BONE_DATA')
        
        #Create Rotation Chain
        row = layout.row()
        row.operator("tgr.create_rotation_chain", icon='CON_ROTLIKE')