import bpy

from ..utils import bone_layers_by_number, get_addon_name


# ------------- ADD PREFIX OR SUFFIX -------------
def add_prefix_suffix(context, bones, prefix="", suffix=""):
    tgr_props = context.active_object.tgr_props

    if not prefix == "":
        for bone in bones:
            # Root bone doesn't need a prefix
            if bone.name == tgr_props.root_bone:
                continue
            # Check if the prefix is already in the name
            if not bone.name.startswith(prefix):
                # Add the prefix to the name
                bone.name = prefix + bone.name
    if not suffix == "":
        for bone in bones:
            # Root bone doesn't need a prefix
            if bone.name == tgr_props.root_bone:
                continue
            # Check if the suffix is already in the name
            if not bone.name.endswith(suffix):
                # Add the suffix to the name
                bone.name = bone.name + suffix


class TGR_OT_AddPrefix(bpy.types.Operator):
    """
    Add a prefix to the selected bone.
    """
    bl_idname = "tgr.add_prefix"
    bl_label = "Add Prefix"
    bl_options = {"REGISTER", "UNDO"}

    prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Prefix to be added",
        default=""
    )

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        if context.mode == 'EDIT_ARMATURE':
            # Check if there are any bones selected
            if len(edit_bones := context.selected_bones) > 0:
                add_prefix_suffix(context, bones=edit_bones, prefix=self.prefix)
            else:
                # Add the prefix to all bones
                edit_bones = context.object.data.edit_bones
                add_prefix_suffix(context, bones=edit_bones, prefix=self.prefix)
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones := context.selected_pose_bones) > 0:
                add_prefix_suffix(context, bones=pose_bones, prefix=self.prefix)
            else:
                # Add the prefix to all bones
                pose_bones = context.object.pose.bones
                add_prefix_suffix(context, bones=pose_bones, prefix=self.prefix)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.prop(self, "prefix")


class TGR_OT_AddSuffix(bpy.types.Operator):
    """
    Add a suffix to the selected bone.
    """
    bl_idname = "tgr.add_suffix"
    bl_label = "Add Suffix"
    bl_options = {"REGISTER", "UNDO"}

    suffix: bpy.props.StringProperty(
        name="Suffix",
        description="Suffix to be added",
        default=""
    )

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        if context.mode == 'EDIT_ARMATURE':
            # Check if there are any bones selected
            if len(edit_bones := context.selected_bones) > 0:
                add_prefix_suffix(context, bones=edit_bones, suffix=self.suffix)
            else:
                # Add the suffix to all bones
                edit_bones = context.object.data.edit_bones
                add_prefix_suffix(context, bones=edit_bones, suffix=self.suffix)
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones := context.selected_pose_bones) > 0:
                add_prefix_suffix(context, bones=pose_bones, suffix=self.suffix)
            else:
                # Add the suffix to all bones
                pose_bones = context.object.pose.bones
                add_prefix_suffix(context, bones=pose_bones, suffix=self.suffix)

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.prop(self, "suffix")


# ------------- REMOVE PREFIX OR SUFFIX -------------
def remove_prefix_suffix(bones, prefix="", suffix=""):
    if not prefix == "":
        for bone in bones:
            # Check if the prefix is already in the name
            if bone.name.startswith(prefix):
                # Remove the prefix to the name
                bone.name = bone.name.replace(prefix, "")
    if not suffix == "":
        for bone in bones:
            # Check if the suffix is already in the name
            if bone.name.endswith(suffix):
                # Remove the suffix to the name
                bone.name = bone.name.replace(suffix, "")


class TGR_OT_RemovePrefix(bpy.types.Operator):
    """
    Remove the prefix from the selected bone.
    """
    bl_idname = "tgr.remove_prefix"
    bl_label = "Remove Prefix"
    bl_options = {"REGISTER", "UNDO"}

    prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Prefix to be removed",
        default=""
    )

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        if context.mode == 'EDIT_ARMATURE':
            # Check if there are any bones selected
            if len(edit_bones := context.selected_bones) > 0:
                remove_prefix_suffix(bones=edit_bones, prefix=self.prefix)
            else:
                # Remove the prefix from all bones
                edit_bones = context.object.data.edit_bones
                remove_prefix_suffix(bones=edit_bones, prefix=self.prefix)
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones := context.selected_pose_bones) > 0:
                remove_prefix_suffix(bones=pose_bones, prefix=self.prefix)
            else:
                # Remove the prefix from all bones
                pose_bones = context.object.pose.bones
                remove_prefix_suffix(bones=pose_bones, prefix=self.prefix)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.prop(self, "prefix")


class TGR_OT_RemoveSuffix(bpy.types.Operator):
    """
    Remove the suffix from the selected bone.
    """
    bl_idname = "tgr.remove_suffix"
    bl_label = "Remove Suffix"
    bl_options = {"REGISTER", "UNDO"}

    suffix: bpy.props.StringProperty(
        name="Suffix",
        description="Suffix to be removed",
        default=""
    )

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        if context.mode == 'EDIT_ARMATURE':
            # Check if there are any bones selected
            if len(edit_bones := context.selected_bones) > 0:
                remove_prefix_suffix(bones=edit_bones, suffix=self.suffix)
            else:
                # Remove the suffix from all bones
                edit_bones = context.object.data.edit_bones
                remove_prefix_suffix(bones=edit_bones, suffix=self.suffix)
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones := context.selected_pose_bones) > 0:
                remove_prefix_suffix(bones=pose_bones, suffix=self.suffix)
            else:
                # Remove the suffix from all bones
                pose_bones = context.object.pose.bones
                remove_prefix_suffix(bones=pose_bones, suffix=self.suffix)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.prop(self, "suffix")


# ------------- CLEAN UP -------------

def clean_up_name(context, name: str) -> str:
    """
    Change the .001, .002, .003, ... suffixes to be before the .L or .R suffixes if
    they exist and change the dots to dashs.
    """
    preferences = context.preferences.addons[get_addon_name()].preferences
    suffix_separator = preferences.suffix_separator
    separator = preferences.separator
    # Check if the last three characters are numbers
    if (digit := name[-3:]).isdigit():
        # Check if the name has Left or Right suffixes in it
        lr_suffix = ""
        for suffix in [f"{suffix_separator}L", f"{suffix_separator}R"]:
            if suffix in name.upper():
                lr_suffix = suffix
                break
        if lr_suffix != "":
            name = name.replace(lr_suffix, "")
            name = name.replace(f".{digit}", "")
            name = name + f"{separator}{digit}" + lr_suffix
        else:
            name = name[:-4] + f"{separator}{digit}"
    return name


class TGR_OT_CleanNameUp(bpy.types.Operator):
    """
    Clean up the name of the selected bone.
    """
    bl_idname = "tgr.clean_name_up"
    bl_label = "Clean Name Up"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        if context.mode == 'EDIT_ARMATURE':
            # Check if there are any bones selected
            if len(edit_bones := context.selected_bones) > 0:
                for bone in edit_bones:
                    # Clean up the name of the selected bone
                    bone.name = clean_up_name(context, bone.name)
            else:
                # Clean up the name of all bones
                edit_bones = context.object.data.edit_bones
                for bone in edit_bones:
                    # Clean up the name of the selected bone
                    bone.name = clean_up_name(context, bone.name)
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones := context.selected_pose_bones) > 0:
                for bone in pose_bones:
                    # Clean up the name of the selected bone
                    bone.name = clean_up_name(context, bone.name)
            else:
                # Clean up the name of all bones
                pose_bones = context.object.pose.bones
                for bone in pose_bones:
                    # Clean up the name of the selected bone
                    bone.name = clean_up_name(context, bone.name)
        return {"FINISHED"}


# ------------- SELECTION -------------
class TGR_OT_SelectBonesByName(bpy.types.Operator):
    """
    Select all the bones of that match the searched name.
    """
    bl_idname = "tgr.select_bones_by_name"
    bl_label = "Select Bones By Name"
    bl_options = {"REGISTER", "UNDO"}

    bone_name: bpy.props.StringProperty(name="Bone Name", description="Name of bones to be selected")

    def __init__(self):
        self.shift = False

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        if not self.shift:
            # Deselect all bones
            if context.mode == 'EDIT_ARMATURE':
                bpy.ops.armature.select_all(action='DESELECT')
            elif context.mode == 'POSE':
                bpy.ops.pose.select_all(action='DESELECT')

        if context.mode == 'EDIT_ARMATURE':
            for edit_bone in context.active_object.data.edit_bones:
                if self.bone_name in edit_bone.name:
                    edit_bone.select = True
                    edit_bone.select_head = True
                    edit_bone.select_tail = True
        elif context.mode == 'POSE':
            for pose_bone in context.active_object.pose.bones:
                if self.bone_name in pose_bone.name:
                    pose_bone.bone.select = True

        return {"FINISHED"}

    def invoke(self, context, event):
        # Check if the shift key is pressed
        self.shift = event.shift
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class TGR_OT_SelectLayerBones(bpy.types.Operator):
    """
    Select all the bones of the specified layer.
    """
    bl_idname = "tgr.select_layer_bones"
    bl_label = "Select Layer Bones"
    bl_options = {"REGISTER", "UNDO"}

    layer: bpy.props.IntProperty(name="Layer", default=0, min=0, max=31)

    def __init__(self):
        self.shift = False

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        if not self.shift:
            # Deselect all bones
            if context.mode == 'EDIT_ARMATURE':
                bpy.ops.armature.select_all(action='DESELECT')
            elif context.mode == 'POSE':
                bpy.ops.pose.select_all(action='DESELECT')

        # Select all the bones of the specified layer
        if context.mode == 'EDIT_ARMATURE':
            for edit_bone in context.active_object.data.edit_bones:
                if edit_bone.layers[self.layer]:
                    edit_bone.select = True
                    edit_bone.select_head = True
                    edit_bone.select_tail = True
        elif context.mode == 'POSE':
            for pose_bone in context.active_object.pose.bones:
                if pose_bone.bone.layers[self.layer]:
                    pose_bone.bone.select = True

        return {"FINISHED"}

    def invoke(self, context, event):
        # Check if the shift key is pressed
        self.shift = event.shift
        return self.execute(context)


# ------------- LAYERS -------------
class TGR_OT_SetBonesLayer(bpy.types.Operator):
    """
    Set the layer of the selected bones.
    """
    bl_idname = "tgr.set_bones_layer"
    bl_label = "Set Bones Layer"
    bl_options = {"REGISTER", "UNDO"}

    layer: bpy.props.IntProperty(name="Layer", default=0, min=0, max=31)

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        layers = bone_layers_by_number(self.layer)

        if context.mode == 'EDIT_ARMATURE':
            # Set the layer of the selected bones
            for bone in context.selected_bones:
                bone.layers = layers if not self.shift else [old or new for old, new in zip(bone.layers, layers)]
        elif context.mode == 'POSE':
            # Set the layer of the selected bones
            for bone in context.selected_pose_bones:
                bone.bone.layers = layers if not self.shift else [old or new for old, new in
                                                                  zip(bone.bone.layers, layers)]
        return {"FINISHED"}

    def invoke(self, context, event):
        # Check if the shift key is pressed
        self.shift = event.shift
        return self.execute(context)


class TGR_OT_LockBonesFromLayer(bpy.types.Operator):
    """
    Lock all bones that belongs to the specified layer.
    """
    bl_idname = "tgr.lock_bones_from_layer"
    bl_label = "Lock Bones From Layer"
    bl_options = {"REGISTER", "UNDO"}

    layer_name: bpy.props.StringProperty(name="Layer", default="")

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        layer = context.object.tgr_layer_collection[self.layer_name]

        # Deselect all bones
        if context.mode == 'EDIT_ARMATURE':
            bpy.ops.armature.select_all(action='DESELECT')
        elif context.mode == 'POSE':
            bpy.ops.pose.select_all(action='DESELECT')

        # Select all the bones of the specified layer
        bpy.ops.tgr.select_layer_bones(layer=layer.index)

        layer.lock_selection = not layer.lock_selection

        # Lock all the selected bones
        if context.mode == "EDIT_ARMATURE":
            selected_bones = context.selected_bones
        elif context.mode == "POSE":
            selected_bones = context.selected_pose_bones
        else:
            selected_bones = []

        for bone in selected_bones:
            if context.mode == "EDIT_ARMATURE":
                bone.hide_select = layer.lock_selection
            elif context.mode == "POSE":
                bone.bone.hide_select = layer.lock_selection

        # Deselect all bones
        if context.mode == 'EDIT_ARMATURE':
            bpy.ops.armature.select_all(action='DESELECT')
        elif context.mode == 'POSE':
            bpy.ops.pose.select_all(action='DESELECT')

        return {"FINISHED"}


class TGR_OT_TrackNewLayer(bpy.types.Operator):
    """
    Track a new layer.
    """
    bl_idname = "tgr.track_new_layer"
    bl_label = "Track New Layer"
    bl_options = {"REGISTER", "UNDO"}

    # Layer attributes
    name: bpy.props.StringProperty(name="Name", default="Layer")
    index: bpy.props.IntProperty(name="Index", default=31, min=0, max=31)
    description: bpy.props.StringProperty(name="Description", default="")
    ui_name: bpy.props.StringProperty(name="UI Name", default="Layer")
    lock_selection: bpy.props.BoolProperty(name="Lock Selection", default=False)

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        # Create a new layer
        layer = context.object.tgr_layer_collection.add()
        layer.name = self.name
        layer.index = self.index
        layer.description = self.description
        layer.ui_name = self.ui_name
        layer.lock_selection = self.lock_selection
        # update the view layer
        context.view_layer.update()

        return {"FINISHED"}


class TGR_OT_RemoveLayer(bpy.types.Operator):
    """
    Remove a layer.
    """
    bl_idname = "tgr.remove_layer"
    bl_label = "Remove Layer"
    bl_options = {"REGISTER", "UNDO"}

    def get_layer_names(self, context):
        return [(layer.name, layer.ui_name, "") for layer in context.object.tgr_layer_collection]

    layers: bpy.props.EnumProperty(name="Layers", items=get_layer_names)

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout
        row = layout.row()
        row.label(text="Choose the layer to remove:")

        row = layout.row()
        row.prop(self, "layers", text="")

    def execute(self, context):
        # Remove the layer
        layer_index = -1
        for i, layer in enumerate(context.object.tgr_layer_collection):
            if layer.name == self.layers:
                layer_index = i
                break

        context.object.tgr_layer_collection.remove(layer_index)
        # update the view layer
        context.view_layer.update()

        return {"FINISHED"}


class TGR_OT_EditLayer(bpy.types.Operator):
    """
    Edit a layer.
    """
    bl_idname = "tgr.edit_layer"
    bl_label = "Edit Layer"
    bl_options = {"REGISTER", "UNDO"}

    def get_layer_names(self, context):
        return [(layer.name, layer.ui_name, "") for layer in context.object.tgr_layer_collection]

    # Layer parameters
    edit_layer_name: bpy.props.EnumProperty(name="Layer", items=get_layer_names)

    @classmethod
    def poll(cls, context):
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        # Choose the layer to edit
        layout = self.layout

        row = layout.row()
        row.label(text="Choose the layer to edit:")
        row = layout.row()
        row.prop(self, "edit_layer_name", text="")

        # Return if no layer is selected
        if self.edit_layer_name == "":
            return

        # Set the default values
        self.collection_index = -1
        for i, layer in enumerate(context.object.tgr_layer_collection):
            if layer.name == self.edit_layer_name:
                self.collection_index = i
                break
        self.edit_layer = context.object.tgr_layer_collection[self.collection_index]

        # Draw the layer parameters
        row = layout.row()
        row.label(text="Layer parameters:")

        row = layout.row()
        row.prop(self.edit_layer, "name", text="Name")
        row = layout.row()
        row.prop(self.edit_layer, "index", text="Index")
        row = layout.row()
        row.prop(self.edit_layer, "description", text="Description")
        row = layout.row()
        row.prop(self.edit_layer, "ui_name", text="UI Name")

    def execute(self, context):

        return {"FINISHED"}
