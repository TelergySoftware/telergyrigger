import bpy
from bpy.types import NodeTree
from ...node_tree_compilation import run_tgr_ui_generator

_pending_compile_timers = {}


def _schedule_compile(armature, tree):
    """Schedules a deferred compilation for the given node tree."""
    tree_pointer = tree.as_pointer()
    previous_timer = _pending_compile_timers.pop(tree_pointer, None)

    if previous_timer and bpy.app.timers.is_registered(previous_timer):
        bpy.app.timers.unregister(previous_timer)

    def compile_tree():
        _pending_compile_timers.pop(tree_pointer, None)

        target_tree = next(
            (
                candidate
                for candidate in bpy.data.node_groups
                if candidate.as_pointer() == tree_pointer
            ),
            None,
        )
        if target_tree is not None and target_tree.bl_idname == "TGR_NT_UI":
            run_tgr_ui_generator(armature=armature, tree=target_tree)

        return None  # Stop the timer

    _pending_compile_timers[tree_pointer] = compile_tree
    bpy.app.timers.register(compile_tree, first_interval=0.5)


class TGR_NT_UI(NodeTree):
    bl_idname = "TGR_NT_UI"
    bl_label = "TGR UI Editor"
    bl_icon = "NODETREE"

    armature: bpy.props.PointerProperty(
        name="Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE',
    )
    
    # Define the node tree's sockets
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'

    def update(self):
        """Triggers every time a node is moved, added, connected, or edited."""
        _schedule_compile(self.armature, self)