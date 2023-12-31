from .tgr_base_panel import TGR_PT_BASE


# ------------- UTILITIES -------------
class TGR_PT_View3D_Panel_Utilities(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Utilities
    """
    bl_label = "Utilities"
    bl_idname = "TGR_PT_View3D_Panel_Utilities"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and (is_edit_mode or is_pose_mode)

    def draw(self, context):
        pass


# Naming Subpanel
class TGR_PT_View3D_Panel_Utilities_Naming(TGR_PT_BASE):
    """
    Creates a subpanel for Utilities with the naming operators
    """
    bl_label = "Naming"
    bl_idname = "TGR_PT_View3D_Panel_Utilities_Naming"
    bl_parent_id = "TGR_PT_View3D_Panel_Utilities"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and (is_edit_mode or is_pose_mode)

    def draw(self, context):
        layout = self.layout
        # ADD
        row = layout.row()
        row.label(text="Add Prefix or Suffix")
        # Add Prefix
        # - Prefix text field
        row = layout.row()
        row.operator("tgr.add_prefix", text="Add Prefix", icon='ADD')
        # Add Suffix
        row = layout.row()
        row.operator("tgr.add_suffix", text="Add Suffix", icon='ADD')
        # REMOVE
        row = layout.row()
        row.label(text="Remove Prefix or Suffix")
        # Remove Prefix
        row = layout.row()
        row.operator("tgr.remove_prefix", text="Remove Prefix", icon='REMOVE')
        # Remove Suffix
        row = layout.row()
        row.operator("tgr.remove_suffix", text="Remove Suffix", icon='REMOVE')
        # Clean Name Up
        row = layout.row()
        row.label(text="Clean Up")

        row = layout.row()
        row.operator("tgr.clean_name_up", text="Clean Name Up", icon='BRUSH_DATA')


# Selection Subpanel
class TGR_PT_View3D_Panel_Utilities_Selection(TGR_PT_BASE):
    """
    Creates a subpanel for Utilities with the selection operators.
    """
    bl_label = "Selection"
    bl_idname = "TGR_PT_View3D_Panel_Utilities_Selection"
    bl_parent_id = "TGR_PT_View3D_Panel_Utilities"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and (is_edit_mode or is_pose_mode)

    def draw(self, context):
        layout = self.layout
        # Search Select
        row = layout.row()
        row.operator("tgr.select_bones_by_name", text="Search and Select", icon="BORDERMOVE")
