import bpy
from bl_ui.space_toolsystem_common import ToolSelectPanelHelper


class TGR_MT_WP_PieMenu(bpy.types.Menu):
    bl_label = "Quick Brushes"
    bl_idname = "TGR_MT_WP_PieMenu"

    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_WEIGHT'        

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        wp_brushes = [brush for brush in bpy.data.brushes if brush.use_paint_weight]
        if len(wp_brushes) < 4:
            pie.operator("tgr.load_wp_brushes", text="Load Brushes", icon="FILE_REFRESH")
            return

        brush_icons = {}
        for brush in wp_brushes:
            try:
                brush_icons[brush.name] = brush.preview.icon_id
            except AttributeError:
                pass

        pie.operator("tgr.activate_brush", text="Paint", icon_value=brush_icons['Paint']).brush = 'Paint'
        pie.operator("tgr.activate_brush", text="Blur", icon_value=brush_icons['Blur']).brush = 'Blur'
        pie.operator("tgr.activate_brush", text="Average", icon_value=brush_icons['Average']).brush = 'Average'
        pie.operator("tgr.activate_brush", text="Smear", icon_value=brush_icons['Smear']).brush = 'Smear'
        gradient_icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.paint.weight_gradient")
        pie.operator("wm.tool_set_by_id", text="Gradient", icon_value=gradient_icon_id).name = "builtin.gradient"


class TGR_MT_WP_Extras_PieMenu(bpy.types.Menu):
    bl_label = "Quick Extras"
    bl_idname = "TGR_MT_WP_Extras_PieMenu"

    @classmethod
    def poll(cls, context):
        return context.mode == "PAINT_WEIGHT"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.separator()
        pie.separator()
        # South
        pie.operator("tgr.wp_clean_up", text="Clean All", icon="BRUSH_DATA")
        # North
        icon = "HIDE_OFF" if context.space_data.overlay.show_bones else "HIDE_ON"
        pie.prop(context.space_data.overlay, "show_bones", icon=icon)
        pie.separator()
        pie.separator()
        pie.separator()
        pie.separator()
