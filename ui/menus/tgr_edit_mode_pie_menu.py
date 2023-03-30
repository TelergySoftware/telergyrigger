import bpy


class TGR_MT_EditMode_PieMenu(bpy.types.Menu):
    """
    Edit Mode Pie Menu.

    conditions:
        - Edit Mode:
            - Armature.
    """
    bl_idname = "TGR_MT_EditMode_PieMenu"
    bl_label = "Edit Mode TGR tools"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def draw(self, context):
        layout = self.layout
        # - Pie Menu UP item
        pie = layout.menu_pie()
        pie.operator("tgr.parent_to_root", icon='LINKED')
        # - Pie Menu RIGHT item
        pie = layout.menu_pie()
        pie.operator("tgr.connect_bones", icon='LINKED')
        # - Pie Menu DOWN item
        pie = layout.menu_pie()
        pie.operator("armature.parent_clear", icon='UNLINKED')
        # - Pie Menu TOP item
        pie = layout.menu_pie()
        pie.operator("armature.parent_set", text='Set Parent' , icon='LINKED')
        # - Pie Menu TOP item
        pie = layout.menu_pie()
        pie.operator("armature.select_linked", text='Select Linked' , icon='LINKED')
        # - Pie Menu BOTTOM item
        pie = layout.menu_pie()
        pie.operator("tgr.add_non_deform_bone", icon='BONE_DATA')