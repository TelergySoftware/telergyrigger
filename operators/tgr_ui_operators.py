import bpy

COMPONENT_TYPES = [
    ("LAYER", "LAYER", "Bone layer component"),
    ("LABEL", "LABEL", "Label component")
]


def sort_components(context):
    components = context.active_object.tgr_ui_components
    n = len(components)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if components[j].line > components[j + 1].line:
                components[j].component_type, components[j + 1].component_type = components[j + 1].component_type, \
                    components[j].component_type
                components[j].value, components[j + 1].value = components[j + 1].value, components[j].value
                components[j].selected, components[j + 1].selected = components[j + 1].selected, components[j].selected
                components[j].line, components[j + 1].line = components[j + 1].line, components[j].line
                components[j].layer_index, components[j + 1].layer_index = components[j + 1].layer_index, components[
                    j].layer_index
                swapped = True
        if not swapped:
            break


def layer_name_by_index(context, index: int) -> str:
    layers = context.active_object.tgr_layer_collection

    for layer in layers:
        if layer.index == index:
            return layer.ui_name

    return "NOT NAMED LAYER"


class TGR_OT_GenerateUI(bpy.types.Operator):
    """
    Generate the UI python script
    """

    bl_idname = "tgr.generate_ui"
    bl_label = "Generate UI"
    bl_options = {'REGISTER', 'UNDO'}

    panel_name: bpy.props.StringProperty(
        name="Panel Name",
        description="Name that will show on the N panel tab",
        default="Rig UI"
    )

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        components = context.active_object.tgr_ui_components
        try:
            text = bpy.data.texts["TGR_RigUI.py"]
            text.clear()
        except KeyError:
            text = bpy.data.texts.new("TGR_RigUI.py")

        # Header comments
        text.write("# ----- RIG UI Created by TelergyRigger -----\n")
        # Imports
        text.write("import bpy\n")
        text.write("\n\n")
        # Properties class
        text.write(
            "class TGR_RIG_Properties(bpy.types.PropertyGroup):\n"
            "\tpass\n"
        )
        text.write("\n\n")
        # Rig layers panel
        text.write(
            "class TGR_RIG_PT_Layers_Panel(bpy.types.Panel):\n"
            "\tbl_label = 'Bone Layers'\n"
            "\tbl_idname = 'TGR_RIG_PT_Layers_Panel'\n"
            "\tbl_space_type = 'VIEW_3D'\n"
            "\tbl_region_type = 'UI'\n"
            f"\tbl_category = '{self.panel_name}'\n"
            "\n"
            "\tdef draw(self, context):\n"
            "\t\tarmature = context.active_object.data\n"
            "\t\tlayout = self.layout\n"
            "\t\t# Toggle bone layer visibility\n"
            "\n"
        )
        current_line = -1
        for component in components:
            if component.line > current_line:
                text.write(
                    "\t\trow = layout.row(align=True)\n"
                )
                current_line = component.line
            if component.component_type == "LAYER":
                text.write(
                    f"\t\trow.prop(armature, 'layers', index={component.layer_index},"
                    f" toggle=True, text='{component.value}')\n"
                )
            elif component.component_type == "LABEL":
                text.write(
                    f"\t\trow.label(text='{component.value}')\n"
                )
        text.write("\n\n")
        # Rig properties panel
        text.write(
            "class TGR_RIG_PT_Properties_Panel(bpy.types.Panel):\n"
            "\tbl_label = 'Rig Properties'\n"
            "\tbl_idname = 'TGR_RIG_PT_Properties_Panel'\n"
            "\tbl_space_type = 'VIEW_3D'\n"
            "\tbl_region_type = 'UI'\n"
            f"\tbl_category = '{self.panel_name}'\n"
            "\n"
            "\tdef draw(self, context):\n"
            "\t\tlayout = self.layout\n"
            "\t\tarmature = context.active_object\n"
            "\t\tif context.mode == 'EDIT':\n"
            "\t\t\tbones = armature.edit_bones\n"
            "\t\t\tbone_names = [bone.name for bone in bones]\n"
            "\t\telif context.mode == 'POSE':\n"
            "\t\t\tbones = armature.pose.bones\n"
            "\t\t\tbone_names = [bone.name for bone in bones]\n"
            "\t\telse:\n"
            "\t\t\treturn\n"
            "\n"
            "\t\tfor bone_name in bone_names:\n"
            "\t\t\tbone = bones[bone_name]\n"
            "\t\t\tif len(bone.keys()) == 0:\n"
            "\t\t\t\tcontinue\n"
            "\t\t\tbox = layout.box()\n"
            "\t\t\tbox.label(text=bone_name)\n"
            "\t\t\tfor key in bone.keys():\n"
            "\t\t\t\tbox.prop(bone, f'[\"{key}\"]')\n"
        )
        text.write("\n\n")
        # Register classes and properties
        text.write(
            "def register():\n"
            "\tbpy.utils.register_class(TGR_RIG_PT_Layers_Panel)\n"
            "\tbpy.utils.register_class(TGR_RIG_Properties)\n"
            "\tbpy.utils.register_class(TGR_RIG_PT_Properties_Panel)\n"
            "\n"
            "\tbpy.types.Scene.rig_ui_properties = bpy.props.PointerProperty(type=TGR_RIG_Properties)\n"
            "\n"
            "\tbpy.types.Scene.rig_props = bpy.props.PointerProperty(type=TGR_RIG_Properties)\n"
        )
        text.write("\n\n")
        # Unregister classes and properties
        text.write(
            "def unregister():\n"
            "\tdel bpy.types.Scene.rig_props\n"
            "\n"
            "\tbpy.utils.unregister_class(TGR_RIG_PT_Layers_Panel)\n"
            "\tbpy.utils.unregister_class(TGR_RIG_Properties)\n"
            "\tbpy.utils.unregister_class(TGR_RIG_PT_Properties_Panel)\n"
        )
        text.write("\n\n")
        # Relink drivers
        text.write(
            "def relink_drivers():\n"
            "\t'''Update dependencies of drivers'''\n"
            "\tfor obj in bpy.data.objects:\n"
            "\t\tif obj.animation_data:\n"
            "\t\t\tfor driver in obj.animation_data.drivers:\n"
            "\t\t\t\tdriver.driver.expression = driver.driver.expression\n"
        )
        text.write("\n\n")
        # Main
        text.write(
            "if __name__ == '__main__':\n"
            "\tregister()\n"
            "\trelink_drivers()\n"
        )

        return {"FINISHED"}


class TGR_OT_RIG_UI_AddComponent(bpy.types.Operator):
    """
    Generate the UI python script
    """

    bl_idname = "tgr.ui_add_component"
    bl_label = "Add Layer"
    bl_options = {'REGISTER', 'UNDO'}

    component_type: bpy.props.EnumProperty(
        name="Type",
        items=COMPONENT_TYPES,
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

    layer_name: bpy.props.StringProperty(
        name="Layer Name",
        description="Layer to get the information from",
        default=""
    )

    def __init__(self):
        tgr_components = bpy.context.active_object.tgr_ui_components
        components_line = [component.line for component in tgr_components]
        if len(components_line) == 0:
            self.line = 0
        else:
            self.line = max(components_line) + 1

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        components = context.active_object.tgr_ui_components
        layers = context.active_object.tgr_layer_collection
        components.add()
        components[-1].component_type = self.component_type
        components[-1].value = self.value
        components[-1].line = self.line
        for layer in layers:
            if layer.name == self.layer_name:
                components[-1].layer_index = layer.index
                break
        sort_components(context)
        print("New Layer Added")
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout
        row = layout.row()
        row.prop(self, "component_type")

        row = layout.row()
        row.prop(self, "value")

        if self.component_type == "LAYER":
            row = layout.row()
            row.label(text="Choose a layer:")

            row = layout.row()
            row.prop_search(self, "layer_name", context.active_object, "tgr_layer_collection")

        row = layout.row()
        row.prop(self, "line")


def get_selected_components(context) -> list:
    components = context.active_object.tgr_ui_components
    return list(filter(lambda x: x.selected, components))


class TGR_OT_RIG_UI_ModifyItem(bpy.types.Operator):
    """
    Generate the UI python script
    """

    bl_idname = "tgr.ui_modify_item"
    bl_label = "Modify Item"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.component = None

    def selected_items(self, context):
        return [(item.value, item.value, "") for i, item in enumerate(get_selected_components(context))]

    items: bpy.props.EnumProperty(
        items=selected_items,
        name="Selected Items"
    )
    component_type: bpy.props.EnumProperty(
        items=COMPONENT_TYPES,
        name="Type"
    )
    layer_name: bpy.props.StringProperty(
        name="Layer Name",
        description="Layer to get the information from",
        default=""
    )

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        layers = context.active_object.tgr_layer_collection
        if self.component_type == "LAYER" and self.layer_name == "":
            self.report({"ERROR"}, "Layer name cannot be empty")
            return {"CANCELLED"}

        self.component.component_type = self.component_type

        if self.component_type == "LAYER":
            for layer in layers:
                if layer.name == self.layer_name:
                    self.component.layer_index = layer.index
                    break

        sort_components(context)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        components = context.active_object.tgr_ui_components

        layout = self.layout
        row = layout.row()
        if get_selected_components(context).__len__() > 1:
            row.label(text="Choose the component to modify:")

            row = layout.row()
            row.prop(self, "items")

            for component in components:
                if component.value == str(self.items):
                    self.component = component
                    break

        else:
            self.component = get_selected_components(context)[0]

        row = layout.row()
        row.label(text="Edit component:")

        row = layout.row()
        row.prop(self, "component_type")

        row = layout.row()
        row.prop(self.component, "value")

        if self.component_type == "LAYER":
            row = layout.row()
            row.label(text="Choose a layer:")

            row = layout.row()
            row.prop_search(self, "layer_name", context.active_object, "tgr_layer_collection")

        row = layout.row()
        row.prop(self.component, "line")


class TGR_OT_RIG_UI_Clear(bpy.types.Operator):
    """
    Generate the UI python script
    """

    bl_idname = "tgr.ui_clear"
    bl_label = "Clear"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        components = context.active_object.tgr_ui_components
        components.clear()
        self.report({"INFO"}, "RIG UI Cleared!")
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Confirm to clear the RIG UI")


class TGR_OT_RIG_UI_RemoveItem(bpy.types.Operator):
    """
    Generate the UI python script
    """

    bl_idname = "tgr.ui_remove_item"
    bl_label = "Remove Item"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        at_least_one = any(get_selected_components(context))
        return is_armature and at_least_one and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        components = context.active_object.tgr_ui_components
        while any(get_selected_components(context)):
            for i, component in enumerate(components):
                if component.selected:
                    components.remove(i)
                    break
        return {"FINISHED"}
