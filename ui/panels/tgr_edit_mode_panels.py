from .tgr_base_panel import TGR_PT_BASE


# ------------- EDIT MODE -------------
class TGR_PT_View3D_Panel_EditMode(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Edit Mode
    """
    bl_label = "Edit Mode"
    bl_idname = "TGR_PT_View3D_Panel_EditMode"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def draw(self, context):
        layout = self.layout
        # Select the Armature and Root Bone
        row = layout.row()
        row.label(text="Root Bone:")

        row = layout.row()
        row.prop(context.object.tgr_props, "armature")
        armature = context.object.tgr_props.armature

        if armature is not None:
            if armature.type == 'ARMATURE':
                row = layout.row()
                row.prop_search(context.object.tgr_props, "root_bone", armature.data, "bones", text="Root",
                                icon='BONE_DATA')


# Edit Create Subpanel
class TGR_PT_View3D_Panel_EditMode_Create(TGR_PT_BASE):
    """
    Creates the subpanel for the Addon in Edit Mode
    """
    bl_label = "Create"
    bl_idname = "TGR_PT_View3D_Panel_EditMode_Create"
    bl_parent_id = "TGR_PT_View3D_Panel_EditMode"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def draw(self, context):
        layout = self.layout

        # Create Non-Deform Bone
        row = layout.row()
        row.operator("tgr.add_non_deform_bone", icon='BONE_DATA')

        # Create Bones on Points
        row = layout.row()
        row.operator("tgr.bones_on_points", icon='BONE_DATA')

        row = layout.row()
        row.operator("tgr.create_tgt", text="Create TGT", icon='BONE_DATA')

        row = layout.row()
        row.operator("tgr.remove_tgt", text="Remove TGT", icon='BONE_DATA')


# Edit Parenting Subpanel
class TGR_PT_View3D_Panel_EditMode_Parenting(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Edit Mode
    """
    bl_label = "Parenting"
    bl_idname = "TGR_PT_View3D_Panel_EditMode_Parenting"
    bl_parent_id = "TGR_PT_View3D_Panel_EditMode"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def draw(self, context):
        layout = self.layout
        # Parent to Root Bone
        row = layout.row()
        row.operator("tgr.parent_to_root", icon='LINKED')

        # Connect Bones
        row = layout.row()
        row.operator("tgr.connect_bones", icon='LINKED')


# Edit Utilities Subpanel
class TGR_PT_View3D_Panel_EditMode_Utilities(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Edit Mode
    """
    bl_label = "Utilities"
    bl_idname = "TGR_PT_View3D_Panel_EditMode_Utilities"
    bl_parent_id = "TGR_PT_View3D_Panel_EditMode"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def draw(self, context):
        layout = self.layout
        layout.operator("tgr.align_bone_to_world", icon='CON_ROTLIKE')
