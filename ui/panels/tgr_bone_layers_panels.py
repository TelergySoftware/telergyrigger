import bpy
from .tgr_base_panel import TGR_PT_BASE


class TGR_PT_View3D_Panel_BoneCollections(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Edit Mode and Pose Mode
    """

    bl_label = "Bone Collections"
    bl_idname = "TGR_PT_View3D_Panel_BoneCollections"
    
    def draw_collection(self, layout, collection, edit_mode, left_margin=0):
        
        row = layout.row(align=True)
        # Create a split layout to simulate a left margin
        split = row.split(factor=left_margin / 100 if left_margin else 0.001, align=True)
        # Use the first part of the split for the separator (margin)
        split.separator()
        # Use the second part of the split for your properties
        main_row = split.row(align=True)
        
        
        active = collection.name == bpy.context.object.tgr_props.armature.data.collections.active.name
        main_row.operator('tgr.set_collection_active', icon='CHECKBOX_HLT' if active else 'CHECKBOX_DEHLT', text="").collection = collection.name  
        main_row.prop(collection, "is_visible", toggle=True, text=collection.name)
        if not edit_mode:
            main_row.operator('tgr.assign_bones_to_collection', icon='REC', text="").name = collection.name
            main_row.operator('tgr.select_layer_bones', icon='RESTRICT_SELECT_OFF', text="").name = collection.name
            try:
                lock_icon = ('UNLOCKED', 'LOCKED')[collection["locked"]]
            except KeyError:
                # collection["locked"] = False
                lock_icon = 'UNLOCKED'
            # main_row.operator('tgr.lock_bones_from_collection', icon=lock_icon, text="",
            #                 depress=collection["locked"]).collection_name = collection.name
        if edit_mode:
            main_row.operator('tgr.rename_collection', icon='GREASEPENCIL', text="").collection = collection.name
            main_row.operator("tgr.remove_collection", text="", icon='TRASH').collection = collection.name
        main_row.operator('tgr.new_collection', icon='ADD', text="").parent = collection.name

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
        row.prop(context.object.tgr_collections, "edit_mode", toggle=True, text="Edit Mode", icon='EDITMODE_HLT')
        
        edit_mode = context.object.tgr_collections.edit_mode

        for collection in collections:
            self.draw_collection(layout, collection, edit_mode)
            if collection.is_visible:
                if len(children := collection.children) > 0:
                    for child in children:
                        self.draw_collection(layout, child, edit_mode, left_margin=8)
                    

        # TRACK NEW LAYER OPERATOR
        row = layout.row(align=True)
        # Call the track new layer menu
        row.operator("tgr.new_collection", text="New", icon='ADD')
        
