import bpy
from .tgr_base_panel import TGR_PT_BASE


def layer_name_by_index(context, index: int) -> str:
    layers = context.active_object.tgr_layer_collection

    for layer in layers:
        if layer.index == index:
            return layer.ui_name

    return "NOT NAMED LAYER"


class TGR_PT_View3D_Panel_RigUI(TGR_PT_BASE):
    """
    Rig UI panel, used to create the final Rig UI script.
    """

    bl_label = "Rig UI"
    bl_idname = "TGR_PT_View3D_Panel_RigUI"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and (is_edit_mode or is_pose_mode)

    def draw(self, context):
        ui_props = context.active_object.tgr_ui_props
        ui_components = context.active_object.tgr_ui_components
        layout = self.layout

        # PREVIEW OF THE RIG UI
        current_line = -1
        for component in ui_components:
            if component.line > current_line:
                row = layout.row(align=True)
                current_line = component.line
            if component.component_type == "LAYER":
                row.prop(component, "selected", toggle=True, text=component.value)
            if component.component_type == "LABEL":
                row.prop(component, "selected", expand=True, text=component.value)

        row = layout.row()
        row.separator()

        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.scale_x = 3
        row.operator("tgr.ui_add_component", icon='ADD', text='')
        row.operator("tgr.ui_add_label", icon='OUTLINER_OB_FONT', text='')

        if any(filter(lambda x: x.selected, ui_components)):
            row = layout.row(align=True)
            row.operator("tgr.ui_remove_item", icon='TRASH')
            row.operator("tgr.ui_modify_item", icon='MODIFIER')

        row = layout.row()
        row.operator("tgr.ui_clear", icon='FILE_REFRESH')
        row = layout.row()
        row.operator("tgr.generate_ui", icon='MOD_BUILD')
