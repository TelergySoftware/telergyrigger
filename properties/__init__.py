import bpy
# Add classes from tgr_properties
from .tgr_properties import TGR_Properties, TGR_RIG_UI_Properties, TGR_Collection_Properties


def register():
    bpy.utils.register_class(TGR_Properties)
    bpy.utils.register_class(TGR_RIG_UI_Properties)
    bpy.utils.register_class(TGR_Collection_Properties)


def unregister():
    bpy.utils.unregister_class(TGR_Properties)
    bpy.utils.unregister_class(TGR_RIG_UI_Properties)
    bpy.utils.unregister_class(TGR_Collection_Properties)
