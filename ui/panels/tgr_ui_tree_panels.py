import bpy
from bpy.types import Panel


class TGR_PT_NodeTreeSettings(Panel):
    bl_idname = "TGR_PT_NodeTreeSettings"
    bl_label = "Node Tree Settings"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'TGR UI'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'TGR_NT_UI'

    def draw(self, context):
        layout = self.layout
        tree = context.space_data.edit_tree

        if tree:
            layout.prop(tree, "armature", text="Armature")