import bpy


class TGR_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def_prefix: bpy.props.StringProperty(
        name="Deformer Prefix",
        description="Prefix to be used on the deformer bones",
        default="DEF"
    )

    tgt_prefix: bpy.props.StringProperty(
        name="Target Prefix",
        description="Prefix to be used on the target bones",
        default="TGT"
    )

    mch_prefix: bpy.props.StringProperty(
        name="Mechanism Prefix",
        description="Prefix to be used on the mechanism bones",
        default="MCH"
    )

    ctrl_prefix: bpy.props.StringProperty(
        name="Controller Prefix",
        description="Prefix to be used on the controller bones",
        default="CTRL"
    )

    separator: bpy.props.StringProperty(
        name="Separator",
        description="Character used to separate names of bones",
        default="-"
    )

    suffix_separator: bpy.props.StringProperty(
        name="Suffix Separator",
        description="Used to separate the suffix from the bone name",
        default="."
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Prefix Defaults")

        box = layout.box()

        row = box.row()
        row.prop(self, "def_prefix")

        row = box.row()
        row.prop(self, "tgt_prefix")

        row = box.row()
        row.prop(self, "mch_prefix")

        row = box.row()
        row.prop(self, "ctrl_prefix")

        row = layout.row()
        row.label(text="Separator Defaults")

        box = layout.box()

        row = box.row()
        row.prop(self, "separator")

        row = box.row()
        row.prop(self, "suffix_separator")
