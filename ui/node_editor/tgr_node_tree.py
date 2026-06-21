import bpy
from bpy.types import NodeTree


class TGR_NT_Data(NodeTree):
    bl_idname = "TGR_NT_Data"
    bl_label = "TGR Data Editor"
    bl_icon = "NODETREE"
    
    # Define the node tree's sockets
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'


class TGR_NT_UI(NodeTree):
    bl_idname = "TGR_NT_UI"
    bl_label = "TGR UI Editor"
    bl_icon = "NODETREE"
    
    # Define the node tree's sockets
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'