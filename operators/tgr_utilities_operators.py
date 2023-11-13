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
    valid_symbols = ".!@#$%^&*()_-+={}[]"
    # Check if the name has Left or Right suffixes in it
    lr_suffix = ""
    for suffix in [f"{suffix_separator}L", f"{suffix_separator}R"]:
        if suffix in name.upper():
            lr_suffix = suffix
            break

    real_name = name.replace(lr_suffix, "")
    digit_ended = False
    if (digit := real_name[-3:]).isdigit():
        if real_name[-4:] == f".{digit}":
            real_name = real_name.replace(f".{digit}", "")
            digit_ended = True

    for symbol in valid_symbols:
        if symbol in real_name:
            real_name = real_name.replace(f"{symbol}", separator)

    if digit_ended:
        real_name += separator + digit

    real_name += lr_suffix

    return real_name


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


class TGR_OT_SelectCollectionBones(bpy.types.Operator):
    """
    Select all the bones of the specified layer.
    """
    bl_idname = "tgr.select_layer_bones"
    bl_label = "Select Layer Bones"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(name="Collection Name", default="")

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

        # Select all the bones of the specified collection
        # Hack for now, try something else later
        # Store current armature mode
        current_mode = context.mode
        # BoneCollection.bones doesn't work in Edit Mode, change to Pose Mode
        if not current_mode == 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        # Select all the bones of the specified collection
        for bone in context.object.tgr_props.armature.data.collections[self.name].bones:
            bone.select = True
        
        # Restore the previous armature mode
        if not current_mode == 'POSE':
            mode = 'EDIT' if current_mode == 'EDIT_ARMATURE' else 'OBJECT'
            bpy.ops.object.mode_set(mode=mode)
        

        return {"FINISHED"}

    def invoke(self, context, event):
        # Check if the shift key is pressed
        self.shift = event.shift
        return self.execute(context)


# ------------- LAYERS -------------
class TGR_OT_AssignBonesToCollection(bpy.types.Operator):
    """Assign the selected bones to the specified collection, press shift to keep the previous collections"""
    bl_idname = "tgr.assign_bones_to_collection"
    bl_label = "Assign Bones to Collection"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(name="Collection Name", default="")

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
        collections = context.object.tgr_props.armature.data.collections

        if context.mode == 'EDIT_ARMATURE':
            # Set the layer of the selected bones
            for bone in context.selected_bones:
                collections[self.name].assign(bone)
                if not self.shift:
                    for collection in collections:
                        if collection.name == self.name:
                            continue
                        collection.unassign(bone)
                
        elif context.mode == 'POSE':
            # Set the layer of the selected bones
            for bone in context.selected_pose_bones:
                collections[self.name].assign(bone.bone)
                if not self.shift:
                    for collection in collections:
                        if collection.name == self.name:
                            continue
                        collection.unassign(bone)
                        
        return {"FINISHED"}

    def invoke(self, context, event):
        # Check if the shift key is pressed
        self.shift = event.shift
        return self.execute(context)


class TGR_OT_LockBonesFromCollection(bpy.types.Operator):
    """Lock all bones that belongs to the specified collection"""
    bl_idname = "tgr.lock_bones_from_collection"
    bl_label = "Lock Bones From Layer"
    bl_options = {"REGISTER", "UNDO"}

    collection_name: bpy.props.StringProperty(name="Collection Name", default="")

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
        collection = context.object.tgr_props.armature.data.collections[self.collection_name]

        # Get bones to lock
        # Hack for now, try something else later
        # Store current armature mode
        current_mode = context.mode
        # BoneCollection.bones doesn't work in Edit Mode, change to Pose Mode
        if not current_mode == 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        # Select all the bones of the specified collection
        bones = collection.bones

        collection["locked"] = not collection["locked"]

        for bone in bones:
            bone.hide_select = collection["locked"]

        # Deselect all bones
        bpy.ops.pose.select_all(action='DESELECT')
        
        # Restore the previous armature mode
        if not current_mode == 'POSE':
            mode = 'EDIT' if current_mode == 'EDIT_ARMATURE' else 'OBJECT'
            bpy.ops.object.mode_set(mode=mode)

        return {"FINISHED"}


class TGR_OT_NewCollection(bpy.types.Operator):
    """Create a new bone collection with the specified name"""
    bl_idname = "tgr.new_collection"
    bl_label = "New Collection"
    bl_options = {"REGISTER", "UNDO"}

    # Layer attributes
    name: bpy.props.StringProperty(name="Name", default="Bones")
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
        # Create a new collection
        collection = context.object.tgr_props.armature.data.collections.new(self.name)
        collection["locked"] = self.lock_selection
        # update the view layer
        context.view_layer.update()

        return {"FINISHED"}


class TGR_OT_RemoveCollection(bpy.types.Operator):
    """Remove the selected collection"""

    bl_idname = "tgr.remove_collection"
    bl_label = "Remove Collection"
    bl_options = {"REGISTER", "UNDO"}

    def get_collection_names(self, context):
        return [(collection.name, collection.name, "") for collection in context.object.tgr_props.armature.data.collections]

    collections: bpy.props.EnumProperty(name="Collections", items=get_collection_names)

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
        row.label(text="Choose the collection to remove:")

        row = layout.row()
        row.prop(self, "collections", text="")

    def execute(self, context):
        # Remove the collection
        collections = context.object.tgr_props.armature.data.collections
        collections.remove(collections[self.collections])
        # update the view layer
        context.view_layer.update()

        return {"FINISHED"}


class TGR_OT_RenameCollection(bpy.types.Operator):
    """Rename the selected collection"""
    bl_idname = "tgr.edit_layer"
    bl_label = "Edit Layer"
    bl_options = {"REGISTER", "UNDO"}

    def get_collection_names(self, context):
        return [(collection.name, collection.name, "") for collection in context.object.tgr_props.armature.data.collections]

    # Layer parameters
    collections: bpy.props.EnumProperty(name="Layer", items=get_collection_names)

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
        # Choose the collection to edit
        layout = self.layout

        row = layout.row()
        row.label(text="Choose the collection to rename:")
        row = layout.row()
        row.prop(self, "collections", text="")

        # Return if no layer is selected
        if self.collections == "":
            return
        
        # Get the selected collection
        collection = context.object.tgr_props.armature.data.collections[self.collections]

        # Draw the collection rename parameters
        row = layout.row()
        row.label(text="New name:")
        row = layout.row()
        row.prop(collection, "name", text="Name")


    def execute(self, context):

        return {"FINISHED"}
