import bpy
from bpy.types import NodeTree
from ...node_tree_compilation import run_tgr_ui_generator


class TGR_NT_Data(NodeTree):
    bl_idname = "TGR_NT_Data"
    bl_label = "TGR Data Editor"
    bl_icon = "NODETREE"
    
    # Define the node tree's sockets
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'


def _deferred_ui_generate():
    run_tgr_ui_generator()
    return None


class TGR_NT_UI(NodeTree):
    bl_idname = "TGR_NT_UI"
    bl_label = "TGR UI Editor"
    bl_icon = "NODETREE"
    
    # Define the node tree's sockets
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'

    def update(self):
        """Triggers every time a node is moved, added, connected, or edited."""
        if not bpy.app.timers.is_registered(_deferred_ui_generate):
            # Defer execution by 0.1s to debounce rapid dragging edits
            bpy.app.timers.register(_deferred_ui_generate, first_interval=0.1)