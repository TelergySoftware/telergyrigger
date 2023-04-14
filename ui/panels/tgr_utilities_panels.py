from .tgr_base_panel import TGR_PT_BASE


# ------------- UTILITIES -------------
class TGR_PT_View3D_Panel_Utilities(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Utilities.
    This panel is only visible when in Edit Mode or Pose Mode,
    and only if the selected object is an Armature.
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
    Creates a subpanel for Utilities with the naming operators.
    This panel is only visible when in Edit Mode or Pose Mode,
    and only if the selected object is an Armature.
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
        row.prop(context.object.tgr_props, "prefix")
        row = layout.row()
        row.operator("tgr.add_prefix", text="Add Prefix", icon='ADD')
        # Add Suffix
        row = layout.row()
        row.prop(context.object.tgr_props, "suffix")
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
        tgr_props = context.object.tgr_props
        layout = self.layout
        # Search Select
        row = layout.row()
        row.label(text="Select by Search Match")
        row = layout.row()
        row.prop(tgr_props, "search_bone_name", text="Match Name")
        row = layout.row()
        row.operator("tgr.select_bones_by_name", text="Search and Select", icon="BORDERMOVE").bone_name = tgr_props.search_bone_name