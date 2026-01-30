import bpy
from bpy.types import NodeTree

from .tgr_socket import TGR_UISocket


class TGR_RigNodeTree(NodeTree):
    bl_idname = "TGR_RigNodeTree"
    bl_label = "TGR UI Editor"
    bl_icon = "OUTLINER_DATA_ARMATURE"
    
    # Define the node tree's sockets
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'
