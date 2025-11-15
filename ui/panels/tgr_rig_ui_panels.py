from .tgr_base_panel import TGR_PT_BASE


class TGR_PT_RIG_UI(TGR_PT_BASE):
    bl_idname = "TGR_PT_RIG_UI"
    bl_label = "Rig UI Panel"
    bl_description = "Panel for Rig UI settings and options"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        rig_ui_props = None
        if context.object.type == "ARMATURE":
            rig_ui_props = context.object.tgr_rig_ui_props
        elif context.object.parent and context.object.parent.type == "ARMATURE":
            rig_ui_props = context.object.parent.tgr_rig_ui_props
        layout = self.layout
        
        layout.prop(rig_ui_props, "edit_mode", text="Edit Mode", toggle=True)