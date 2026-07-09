import bpy


class TGR_PT_WP_PieMenu(bpy.types.Menu):
    bl_label = "Fast Brushes"
    bl_idname = "TGR_PT_WP_PieMenu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        