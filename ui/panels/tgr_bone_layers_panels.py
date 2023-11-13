import bpy
from .tgr_base_panel import TGR_PT_BASE


class TGR_PT_View3D_Panel_BoneCollections(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Edit Mode and Pose Mode
    """

    bl_label = "Bone Collections"
    bl_idname = "TGR_PT_View3D_Panel_BoneCollections"

    def __init__(self) -> None:
        super().__init__()
        # If the tgr_layer_collection is empty,
        # add the default layers: "DEF", "TGT" and "MCH"
        # TODO: Create a prefences panel for default layers
        collections = bpy.context.active_object.data.collections
        if len(collections) == 1 and collections[0].name == "Bones":
            collections[0].name = "DEF"
            collections[0]["locked"] = False
            collections.new(name="TGT")["locked"] = False
            collections.new(name="MCH")["locked"] = False

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and (is_edit_mode or is_pose_mode)

    def draw(self, context):
        layout = self.layout
        armature = context.object.tgr_props.armature
        collections = armature.data.collections

        row = layout.row(align=True)
        for i, collection in enumerate(collections):
            if i % 2 == 0:
                row = layout.row(align=True)

            row.prop(collection, "is_visible", toggle=True, text=collection.name)
            row.operator('tgr.assign_bones_to_collection', icon='REC', text="").name = collection.name
            row.operator('tgr.select_layer_bones', icon='RESTRICT_SELECT_OFF', text="").name = collection.name
            try:
                lock_icon = ('UNLOCKED', 'LOCKED')[collection["locked"]]
            except KeyError:
                collection["locked"] = False
                lock_icon = 'UNLOCKED'
            row.operator('tgr.lock_bones_from_collection', icon=lock_icon, text="",
                         depress=collection["locked"]).collection_name = collection.name
            row.separator()

        # TRACK NEW LAYER OPERATOR
        row = layout.row(align=True)
        row.alignment = 'CENTER'
        # Call the track new layer menu
        row.operator("tgr.new_collection", text="New", icon='ADD')
        row.operator("tgr.edit_layer", text="Rename", icon='GREASEPENCIL')
        row.operator("tgr.remove_collection", text="Remove", icon='REMOVE')
