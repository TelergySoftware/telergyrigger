import bpy
from .tgr_base_panel import TGR_PT_BASE


class TGR_PT_View3D_Panel_BoneLayers(TGR_PT_BASE):
    """
    Creates the panel for the Addon in Edit Mode and Pose Mode.
    This panel is only visible in Edit Mode and Pose Mode
    and if the active object is an armature.
    """
    
    bl_label = "Bone Layers"
    bl_idname = "TGR_PT_View3D_Panel_BoneLayers"
    
    def __init__(self) -> None:
        super().__init__()
        # If the tgr_layer_collection is empty,
        # add the default layers: "DEF", "TGT" and "MCH"
        self.layer_collection = bpy.context.active_object.tgr_layer_collection
        if len(self.layer_collection) == 0:
            # TODO: Create a prefences panel for default layers
            for _ in range(3):
                self.layer_collection.add()
            self.layer_collection[0].name = "Deform Layer"
            self.layer_collection[0].index = 0
            self.layer_collection[0].description = "Layer used to store the deform bones."
            self.layer_collection[0].ui_name = "DEF"
            self.layer_collection[0].lock_selection = False
            
            self.layer_collection[1].name = "Target Layer"
            self.layer_collection[1].index = 1
            self.layer_collection[1].description = "Layer used to store the target bones."
            self.layer_collection[1].ui_name = "TGT"
            self.layer_collection[1].lock_selection = False
            
            self.layer_collection[2].name = "Mechanics Layer"
            self.layer_collection[2].index = 2
            self.layer_collection[2].description = "Layer used to store the mechanism bones."
            self.layer_collection[2].ui_name = "MCH"
            self.layer_collection[2].lock_selection = False
    
    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and (is_edit_mode or is_pose_mode)
    
    def draw(self, context):
        layout = self.layout
        tgr_layers = context.object.tgr_layer_collection
        
        row = layout.row(align=True)
        for i, layer in enumerate(tgr_layers):
            if i % 2 == 0: row = layout.row(align=True)
             # DEF LAYER
            
            row.prop(context.object.data, "layers", index=layer.index, toggle=True, text=layer.ui_name)
            row.operator('tgr.set_bones_layer', icon='REC', text="").layer = layer.index
            row.operator('tgr.select_layer_bones', icon='RESTRICT_SELECT_OFF', text="").layer = layer.index
            lock_icon = ('UNLOCKED', 'LOCKED')[layer.lock_selection]
            row.operator('tgr.lock_bones_from_layer', icon=lock_icon, text="", depress=layer.lock_selection).layer_name = layer.name
            row.separator()
                
        # TRACK NEW LAYER OPERATOR
        row = layout.row(align=True)
        row.alignment = 'CENTER'
        # Call the track new layer menu
        row.operator("tgr.track_new_layer", text="Track New")
        row.operator("tgr.edit_layer", text="Edit")
        row.operator("tgr.remove_layer", text="Remove")
