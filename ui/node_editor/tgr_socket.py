import bpy
from bpy.types import NodeSocket


class TGR_SKT_EnumItem(NodeSocket):
    bl_idname = "TGR_SKT_EnumItem"
    bl_label = "Enum Item"
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.2, 0.3, 0.8, 1.0)


class TGR_SKT_Enum(NodeSocket):
    bl_idname = "TGR_SKT_Enum"
    bl_label = "Enum"
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.8, 0.3, 0.2, 1.0)


class TGR_SKT_Property(NodeSocket):
    bl_idname = "TGR_SKT_Property"
    bl_label = "Property"
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.3, 0.8, 0.2, 1.0)


class TGR_SKT_Executable(NodeSocket):
    bl_idname = "TGR_SKT_Executable"
    bl_label = "Executable"
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.8, 0.8, 0.2, 1.0)


class TGR_SKT_Layout(NodeSocket):
    bl_idname = "TGR_SKT_Layout"
    bl_label = "Layout"
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.2, 0.8, 0.8, 1.0)


class TGR_SKT_SplitItem(NodeSocket):
    bl_idname = "TGR_SKT_SplitItem"
    bl_label = "Split Item"
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 1.0)