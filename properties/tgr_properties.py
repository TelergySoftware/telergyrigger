import bpy


class TGR_PP_Layer:
    name: bpy.props.StringProperty(name="Name", default="")
    index: bpy.props.IntProperty(name="Index", default=0, min=0, max=31)
    description: bpy.props.StringProperty(name="Description", default="")
    ui_name: bpy.props.StringProperty(name="UI Name", default="")
    lock_selection: bpy.props.BoolProperty(name="Lock Selection", default=False)
    
    def __str__(self) -> str:
        return f'Layer: {self.name}, Index: {self.index}\n\t{self.description}.'


def layer_factory(name: str, index: int, description: str="", ui_name: str="Layer", lock_selection: bool=False) -> TGR_PP_Layer:
    layer = TGR_PP_Layer()
    layer.name = name
    layer.index = index
    layer.description = description
    layer.ui_name = ui_name
    layer.lock_selection = lock_selection
    return layer


class TGR_Properties(bpy.types.PropertyGroup):
    """
    General properties to be used by the addon.
    """
    # ---- MAIN PROPERTIES ----
    # -- Naming --
    prefix: bpy.props.StringProperty(name="Prefix", default="")
    
    def_prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Prefix to be added to the deform bones.",
        default="DEF-",
    )
    
    tgt_prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Prefix to be added to the target bones.",
        default="TGT-",
    )
    
    mch_prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Prefix to be added to the mechanism bones.",
        default="MCH-",
    )
    
    ctrl_prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Prefix to be added to the control bones.",
        default="CTRL-",
    )
    
    suffix: bpy.props.StringProperty(
        name="Suffix",
        description="Suffix to be added to the name of the bone.",
        default="",
    )
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
    # ---- UTILITIES ----
    search_bone_name: bpy.props.StringProperty(name="Search Bone Name")


class TGR_LayerProperties(bpy.types.PropertyGroup):
    """
    Properties of a layer.
    """
    name: bpy.props.StringProperty(
        name="Name",
        description="Name of the layer",
        default="Layer",
    )
    index: bpy.props.IntProperty(
        name="Index",
        description="Index of the layer",
        default=0,
    )
    description: bpy.props.StringProperty(
        name="Description",
        description="Description of the layer",
        default="",
    )
    ui_name: bpy.props.StringProperty(
        name="UI Name",
        description="Name of the layer as it appears in the UI",
        default="Layer",
    )
    lock_selection: bpy.props.BoolProperty(
        name="Lock Selection",
        description="Lock the selection of the layer",
        default=False,
    )