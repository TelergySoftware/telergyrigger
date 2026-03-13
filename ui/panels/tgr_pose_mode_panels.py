from .tgr_base_panel import TGR_PT_BASE


# ------------- POSE MODE -------------
class TGR_PT_View3D_Panel_PoseMode(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Pose Mode
    """
    bl_label = "Pose Mode"
    bl_idname = "TGR_PT_View3D_Panel_PoseMode"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def draw(self, context):
        pass


# Pose ORG Subpanel
class TGR_PT_View3D_Panel_PoseMode_ORG(TGR_PT_BASE):
    """
    Creates the subpanel for the Addon in Pose Mode
    """
    bl_label = "ORG"
    bl_idname = "TGR_PT_View3D_Panel_PoseMode_ORG"
    bl_parent_id = "TGR_PT_View3D_Panel_PoseMode"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def draw(self, context):
        layout = self.layout
        # Bind and Unbind ORG bones
        row = layout.row()
        row.operator("tgr.bind_org", icon='LOCKED')

        row = layout.row()
        row.operator("tgr.unbind_org", icon='UNLOCKED')


# Pose Constraints Subpanel
class TGR_PT_View3D_Panel_PoseMode_Constraints(TGR_PT_BASE):
    """
    Creates the subpanel for the Addon in Pose Mode.
    This panel is only visible when in Pose Mode,
    and only if the selected object is an Armature.
    """
    bl_label = "Constraints"
    bl_idname = "TGR_PT_View3D_Panel_PoseMode_Constraints"
    bl_parent_id = "TGR_PT_View3D_Panel_PoseMode"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def draw(self, context):
        layout = self.layout

        # Isolate ORG bone rotation
        row = layout.row()
        row.operator("tgr.isolate_bone", icon='UNLINKED', text="Isolate Bone")
        
        # Sample Transforms
        row = layout.row()
        row.operator("tgr.sample_transforms", icon='EYEDROPPER', text="Sample Transforms")
        
        # Create Tweak Chain
        row = layout.row()
        row.operator("tgr.create_tweak_chain", icon='ACTION_TWEAK')
        
        # Create FK From Tweak Chain
        row = layout.row()
        row.operator("tgr.fk_from_tweak_chain", icon='TRACKING_REFINE_FORWARDS')

        # Create Rotation Chain
        row = layout.row()
        row.operator("tgr.create_rotation_chain", icon='CON_ROTLIKE')
        
        # Create Single Controller Stretch
        row = layout.row()
        row.operator("tgr.create_single_controller_stretch", icon='CON_STRETCHTO')

        row = layout.row()
        row.operator("tgr.copy_transforms_to_chain", icon='CON_TRANSFORM')

        row = layout.row()
        row.operator("tgr.create_ik_pole_target", icon='CON_TRACKTO')
        
        row = layout.row()
        row.operator("tgr.add_pivot_controller", icon='PIVOT_CURSOR')
