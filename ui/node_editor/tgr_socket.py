import bpy
from bpy.types import NodeSocket


class TGR_UISocket(NodeSocket):
    bl_idname = "TGR_UISocket"
    bl_label = "UI Element"
    
    # Define socket properties here
    socket_type: bpy.props.StringProperty(name="Socket Type", default="DEFAULT")
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.8, 0.2, 0.2, 1.0)  # Red color for the socket


class TGR_PropertySocket(NodeSocket):
    bl_idname = "TGR_PropertySocket"
    bl_label = "Property"
    
    # Define socket properties here
    property_name: bpy.props.StringProperty(name="Property Name", default="property")
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.3, 0.4, 0.3, 1.0)  # Gray-green color for the socket
    

class TGR_EnumItemSocket(NodeSocket):
    bl_idname = "TGR_EnumItemSocket"
    bl_label = "Enum Item"
    
    # Define socket properties here
    item_name: bpy.props.StringProperty(name="Item Name", default="item")
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        return (0.2, 0.6, 0.8, 1.0)  # Blue color for the socket