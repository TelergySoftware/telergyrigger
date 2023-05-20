import bpy


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


class TGR_UIProperties(bpy.types.PropertyGroup):
    """
    Properties of the UI
    """

    panel_name: bpy.props.StringProperty(
        name="Panel Name",
        description="Name that will be shown in the N-Panel",
        default="Telergy Rig"
    )

    ui_code: bpy.props.StringProperty(
        name="UI Code",
        description="Pseudo code to represent the layers UI",
        default="Layers;\n;0;1;\n;2;3;"
    )

    enable_select: bpy.props.BoolProperty(
        name="Enable Select",
        description="Enable the selection of layers",
        default=False
    )

    selected_layers: bpy.props.StringProperty(
        name="Selected Layers",
        description="String representing which layers are selected",
        default=""
    )


class TGR_UI_Components(bpy.types.PropertyGroup):
    """Components used to create the generated UI"""

    component_type: bpy.props.StringProperty(
        name="Component Type",
        description="Can be LAYER or LABEL",
        default="LAYER",
    )

    value: bpy.props.StringProperty(
        name="Value",
        description="Describes the layer or label text",
        default=""
    )

    line: bpy.props.IntProperty(
        name="Line",
        description="Line in which the component will be placed",
        default=0,
        min=0
    )

    selected: bpy.props.BoolProperty(
        name="Selected",
    )
