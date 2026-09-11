from .tgr_base_panel import TGR_PT_BASE


class TGR_PT_View3D_Panel_Pressets(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Pose Mode
    """
    bl_label = "Pressets"
    bl_idname = "TGR_PT_View3D_Panel_Pressets"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("tgr.create_tweak_fk_chain")
        row = layout.row()
        row.operator("tgr.create_ikfk_switch")
        