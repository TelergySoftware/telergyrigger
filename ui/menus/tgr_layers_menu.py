import bpy


class TGR_MT_TrackNewLayer(bpy.types.Menu):
    bl_label = "New Layer"
    bl_idname = "TGR_MT_TrackNewLayer"

    @classmethod
    def poll(cls, context):
        is_armature = context.object is not None and context.object.type == 'ARMATURE'
        return context.mode in {'POSE', 'EDIT_ARMATURE'} and is_armature

    def draw(self, context):
        layout = self.layout
        # - New Layer

        # Add fields for the new layer parameters
        col = layout.column()
        # Text field
        col.prop(context.object.tgr_layer_collection[-1], "name")
        col.prop(context.object.tgr_layer_collection[-1], "index")
        col.prop(context.object.tgr_layer_collection[-1], "description")
        col.prop(context.object.tgr_layer_collection[-1], "ui_name")
        col.prop(context.object.tgr_layer_collection[-1], "lock_selection")

        layout.operator("tgr.new_collection", text="Track New Layer")
