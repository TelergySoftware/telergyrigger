import bpy
from .tgr_base_panel import TGR_PT_BASE


class TGR_PT_View3D_Panel_BoneCollections(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Edit Mode and Pose Mode
    """

    bl_label = "Bone Collections"
    bl_idname = "TGR_PT_View3D_Panel_BoneCollections"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    def draw_collection(self, layout, collection, edit_mode, left_margin=0):
        
        armature = bpy.context.object.parent if bpy.context.object.parent else bpy.context.object
        tgr_props = armature.tgr_props
        collection_props = armature.tgr_collections
        
        row = layout.row(align=True)
        # Create a split layout to simulate a left margin
        split = row.split(factor=left_margin / 100 if left_margin else 0.001, align=True)
        # Use the first part of the split for the separator (margin)
        split.separator()
        # Use the second part of the split for your properties
        main_row = split.row(align=True)
        
        
        active = collection.name == armature.data.collections.active.name
        main_row.operator('tgr.set_collection_active', icon='CHECKBOX_HLT' if active else 'CHECKBOX_DEHLT', text="").collection = collection.name
        main_row.prop(collection, "is_solo", toggle=True, text="", icon='SOLO_ON' if collection.is_solo else 'SOLO_OFF')
        main_row.prop(collection, "is_visible", toggle=True, text=collection.name)
        lock_icon = 'UNLOCKED' if collection.name not in collection_props.locked_collections else 'LOCKED'
        if not edit_mode:
            main_row.operator('tgr.assign_bones_to_collection', icon='REC', text="").name = collection.name
            main_row.operator('tgr.select_layer_bones', icon='RESTRICT_SELECT_OFF', text="").name = collection.name            
        if edit_mode:
            main_row.operator('tgr.rename_collection', icon='GREASEPENCIL', text="").collection = collection.name
            main_row.operator("tgr.remove_collection", text="", icon='TRASH').collection = collection.name
        
        main_row.operator('tgr.lock_bones_from_collection', icon=lock_icon, text="",
                        depress=lock_icon == 'LOCKED').collection_name = collection.name
        main_row.operator('tgr.new_collection', icon='ADD', text="").parent = collection.name
        
        if collection.is_visible:
                if len(children := collection.children) > 0:
                    for child in children:
                        self.draw_collection(layout, child, edit_mode, left_margin=left_margin + 8)

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        # Check if the active object is parented to an armature or is an armature itself
        if context.object.parent and context.object.parent.type == 'ARMATURE':
            return True
        if context.object.type == 'ARMATURE':
            return True
        return False

    def draw(self, context):
        layout = self.layout
        armature = context.object.parent if context.object.parent else context.object
        collections = armature.data.collections
        
        row = layout.row(align=True)
        row.prop(armature.tgr_collections, "edit_mode", toggle=True, text="Edit Mode", icon='EDITMODE_HLT')
        row.operator('tgr.auto_correct_use_deform', icon='FILE_REFRESH', text="Fix Deform")
        
        row = layout.row(align=True)
        row.operator('tgr.toggle_deformer_constraint', icon='CONSTRAINT_BONE', text="Toggle Deformer")
        
        edit_mode = armature.tgr_collections.edit_mode

        for collection in collections:
            self.draw_collection(layout, collection, edit_mode)


        # TRACK NEW LAYER OPERATOR
        row = layout.row(align=True)
        # Call the track new layer menu
        row.operator("tgr.new_collection", text="New", icon='ADD').parent = ""
        
