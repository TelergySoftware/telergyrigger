import bpy


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
        items=[("LAYER", "LAYER", "Bone layer component"), ("LABEL", "LABEL", "Label component")],
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
        components.add()
        components[-1].component_type = self.component_type
        components[-1].value = self.value
        components[-1].line = self.line
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


class TGR_OT_RIG_UI_ModifyItem(bpy.types.Operator):
    """
    Generate the UI python script
    """

    bl_idname = "tgr.ui_modify_item"
    bl_label = "Modify Item"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        print("Item Modified")
        return {"FINISHED"}


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
        # TODO: Add condition of at least one item selected
        return is_armature and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        components = context.active_object.tgr_ui_components
        while any(filter(lambda x: x.selected, components)):
            for i, component in enumerate(components):
                if component.selected:
                    components.remove(i)
                    break
        return {"FINISHED"}
