import bpy


class TGR_Properties(bpy.types.PropertyGroup):
    """
    General properties to be used by the addon.
    """
    # ---- MAIN PROPERTIES ----
    # ---- EDIT MODE ----
    armature: bpy.props.PointerProperty(
        name="Armature",
        type=bpy.types.Object,
        description="Armature object to be used by the addon.",
        update=None
    )
    root_bone: bpy.props.StringProperty(
        name="Root Bone",
        description="The root bone of the armature",
        default="ROOT",
    )
    

class TGR_Collection_Properties(bpy.types.PropertyGroup):
    """ Properties to be used by the collections """
    
    edit_mode: bpy.props.BoolProperty(
        name="Edit Mode",
        description="Toggle edit mode",
        default=False
    )
    
    locked_collections: set = set()


class TGR_RIG_UI_Properties(bpy.types.PropertyGroup):
    """ Properties for the Rig UI panel """
    
    edit_mode: bpy.props.BoolProperty(
        name="Edit Mode",
        description="Toggle edit mode for Rig UI",
        default=False
    )
    
    ui_structure: dict = {}
    
