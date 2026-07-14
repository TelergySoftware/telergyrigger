import bpy


class TGR_MT_WP_PieMenu(bpy.types.Menu):
    bl_label = "Quick Brushes"
    bl_idname = "TGR_MT_WP_PieMenu"

    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_WEIGHT'

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        brush_icons = {}
        for brush in bpy.data.brushes:
            if brush.use_paint_weight:
                brush_icons[brush.name] = brush.preview.icon_id

        pie.operator("tgr.activate_brush", text="Paint", icon_value=brush_icons['Paint']).brush = 'Paint'
        pie.operator("tgr.activate_brush", text="Blur", icon_value=brush_icons['Blur']).brush = 'Blur'
        pie.operator("tgr.activate_brush", text="Average", icon_value=brush_icons['Average']).brush = 'Average'
        pie.operator("tgr.activate_brush", text="Smear", icon_value=brush_icons['Smear']).brush = 'Smear'

