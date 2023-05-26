import bpy


class TGR_MT_EditMode_PieMenu(bpy.types.Menu):
    """
    Edit Mode Pie Menu
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
        # - Pie Menu BOTTOM item
        pie = layout.menu_pie()
        copy_transforms_op = pie.operator("tgr.copy_transforms", icon='CON_TRANSLIKE')
        copy_transforms_op.copy_location = True
        copy_transforms_op.copy_rotation = True
        copy_transforms_op.copy_scale = True
        # - Pie Menu DOWN item
        pie = layout.menu_pie()
        pie.operator("armature.parent_clear", icon='UNLINKED')
        # - Pie Menu TOP item
        pie = layout.menu_pie()
        pie.operator("armature.parent_set", text='Set Parent', icon='LINKED')
        # - Pie Menu LEFT item
        pie = layout.menu_pie()
        copy_location_op = pie.operator("tgr.copy_transforms", text="Copy Location", icon='CON_LOCLIKE')
        copy_location_op.copy_location = True
        copy_location_op.copy_rotation = False
        copy_location_op.copy_scale = False
        # - Pie Menu RIGHT item
        pie = layout.menu_pie()
        copy_rotation_op = pie.operator("tgr.copy_transforms", text="Copy Rotation", icon='CON_ROTLIKE')
        copy_rotation_op.copy_location = False
        copy_rotation_op.copy_rotation = True
        copy_location_op.copy_scale = False
        # - Pie Menu CENTER item
        pie = layout.menu_pie()
        copy_scale_op = pie.operator("tgr.copy_transforms", text="Copy Scale", icon='CON_SIZELIKE')
        copy_scale_op.copy_location = False
        copy_scale_op.copy_rotation = False
        copy_scale_op.copy_scale = True
