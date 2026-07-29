from __future__ import annotations
import bpy
from dataclasses import dataclass, field
import cattrs
import json


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
    instant: bpy.props.BoolProperty(
        name="Instant",
        description="Instantly add the prefix to the bones",
        default=False
    )

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
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
        if self.instant:
            return self.execute(context)
        
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
    
    instant: bpy.props.BoolProperty(
        name="Instant",
        description="Instantly add the suffix to the bones",
        default=False
    )

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
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
        if self.instant:
            return self.execute(context)
        
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
        if not context.object:
            return False
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
        if not context.object:
            return False
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
    preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
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
        if not context.object:
            return False
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
    Select all the bones that match the searched name.
    """
    bl_idname = "tgr.select_bones_by_name"
    bl_label = "Select Bones By Name"
    bl_options = {"REGISTER", "UNDO"}

    bone_name: bpy.props.StringProperty(name="Bone Name", description="Name of bones to be selected")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.shift = False

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
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
                    pose_bone.select = True

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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.shift = False

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
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
        for bone in context.object.tgr_props.armature.data.collections_all[self.name].bones:
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
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.shift = False

    name: bpy.props.StringProperty(name="Collection Name", default="")

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        collections = context.object.tgr_props.armature.data.collections_all

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
        if not context.object:
            return False
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        collection = context.object.tgr_props.armature.data.collections_all[self.collection_name]
        collection_props = context.object.tgr_collections

        # Get bones to lock
        # Hack for now, try something else later
        # Store current armature mode
        current_mode = context.mode
        # BoneCollection.bones doesn't work in Edit Mode, change to Pose Mode
        if not current_mode == 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        # Select all the bones of the specified collection
        bones = collection.bones

        # Check if the collection is locked and change its state
        if collection.name in collection_props.locked_collections:
            collection_props.locked_collections.remove(collection.name)
        else:
            collection_props.locked_collections.add(collection.name)

        for bone in bones:
            bone.hide_select = collection.name in collection_props.locked_collections

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
    parent: bpy.props.StringProperty(name="Parent", default="")
    lock_selection: bpy.props.BoolProperty(name="Lock Selection", default=False)

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
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
        row.prop(self, "name")
        row = layout.row()
        row.prop(self, "lock_selection")

    def execute(self, context):
        # Create a new collection
        collection = context.object.tgr_props.armature.data.collections.new(self.name)
        if not self.parent == "":
            collection.parent = context.object.tgr_props.armature.data.collections_all[self.parent]
        collection["locked"] = self.lock_selection
        # update the view layer
        context.view_layer.update()

        return {"FINISHED"}


class TGR_OT_RemoveCollection(bpy.types.Operator):
    """Remove the selected collection"""

    bl_idname = "tgr.remove_collection"
    bl_label = "Remove Collection"
    bl_options = {"REGISTER", "UNDO"}

    collection: bpy.props.StringProperty(name="Collection Name", default="")

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
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
        row.label(text="Remove This Collection?")

    def execute(self, context):
        # Remove the collection
        collections = context.object.tgr_props.armature.data.collections
        removed_collection = context.object.tgr_props.armature.data.collections_all[self.collection]
        collections.remove(removed_collection)
        # update the view layer
        context.view_layer.update()

        return {"FINISHED"}


class TGR_OT_RenameCollection(bpy.types.Operator):
    """Rename the selected collection"""
    bl_idname = "tgr.rename_collection"
    bl_label = "Rename Collection"
    bl_options = {"REGISTER", "UNDO"}

    # Layer parameters
    collection: bpy.props.StringProperty(name="Collection Name", default="")

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def invoke(self, context, event):
        self.renamed_collection = context.object.tgr_props.armature.data.collections_all[self.collection]
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        # Set the new name to the current collection
        layout = self.layout
        # Draw the collection rename parameters
        row = layout.row()
        row.prop(self, "collection", text="Name")


    def execute(self, context):
        self.renamed_collection.name = self.collection
        # update the view layer
        context.view_layer.update()
        
        return {"FINISHED"}


class TGR_OT_SetCollectionActive(bpy.types.Operator):
    """Set the selected collection as the active one"""
    bl_idname = "tgr.set_collection_active"
    bl_label = "Set Collection Active"
    bl_options = {"REGISTER", "UNDO"}

    collection: bpy.props.StringProperty(name="Collection Name", default="")

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the selected object is in Edit Mode or Pose Mode
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        # Check if the selected object is an Armature and in Edit Mode or Pose Mode
        return is_armature and (is_edit_mode or is_pose_mode)

    def execute(self, context):
        # Set the selected collection as the active one
        context.object.tgr_props.armature.data.collections.active = context.object.tgr_props.armature.data.collections_all[self.collection]
        # update the view layer
        context.view_layer.update()

        return {"FINISHED"}

class TGR_OT_AutoCorrectUseDeform(bpy.types.Operator):
    """Auto correct the Use Deform property of all bones in the armature"""
    bl_idname = "tgr.auto_correct_use_deform"
    bl_label = "Auto Correct Use Deform"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        # Check if the selected object is an Armature
        is_armature = context.object.type == 'ARMATURE'
        # Check if the armature is not in object mode
        not_object_mode = context.mode != 'OBJECT'
        # Check if the selected object is an Armature and not in object mode
        return is_armature and not_object_mode
    
    def execute(self, context):
        # Set the Use Deform property of all bones with DEF prefix to True
        # and all other bones to False
        preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
        def_prefix = preferences.def_prefix
        changed_bones = []
        for bone in context.object.data.bones:
            current_use_deform = bone.use_deform
            bone.use_deform = bone.name.startswith(def_prefix)
            if current_use_deform != bone.use_deform:
                changed_bones.append(bone.name)
        
        if changed_bones:
            self.report({"INFO"}, f"Use Deform property of {len(changed_bones)} bones changed: {', '.join(changed_bones)}")
        return {"FINISHED"}



class TGR_OT_AutoColorBones(bpy.types.Operator):
    """Automatically color the bones based on their name"""
    
    bl_idname = "tgr.auto_color_bones"
    bl_label = "Auto Color Bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        return is_armature and is_pose_mode
    
    def execute(self, context):
        
        armature = context.active_object
        
        for bone in armature.data.bones:
            if "TWEAK" in bone.name.upper():
                bone.color.palette = "THEME03"
            elif bone.name.endswith(".L"):
                bone.color.palette = "THEME01"
            elif bone.name.endswith(".R"):
                bone.color.palette = "THEME04"
            elif bone.name == "ROOT":
                bone.color.palette = "THEME10"
            else:
                bone.color.palette = "THEME09"
            
        return {"FINISHED"}


@dataclass
class BoneCollection:
    name: str
    is_visible: bool = True
    is_solo: bool = False
    children: list[BoneCollection] = field(default_factory=list)

class TGR_OT_SaveCollections(bpy.types.Operator):
    """Save all collections of this armature to a JSON file"""

    bl_idname = "tgr.save_collections"
    bl_label = "Save Collections"
    bl_options = {'REGISTER'}

    file_path: bpy.props.StringProperty(
        name="File Path",
        description="File path to save the collections",
        default="",
        subtype='FILE_PATH'
    )

    @classmethod
    def poll(cls, context):
        if not context.object:
            cls.poll_message_set("No active object found")
            return False
        if not context.active_object.type == 'ARMATURE':
            cls.poll_message_set("Active object is not an armature")
            return False
        if not context.active_object.data.collections_all:
            cls.poll_message_set("Armature has no collections")
            return False
        return True
    

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "file_path")
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def _populate_bone_collections(self, parent) -> list[BoneCollection]:
        if not parent.children:
            return []
        
        children = []
        for child in parent.children:
            collection = BoneCollection(name=child.name)
            collection.is_solo = child.is_solo
            collection.is_visible = child.is_visible
            if child.children:
                collection.children = self._populate_bone_collections(child)
            children.append(collection)

        return children

    def execute(self, context):
        armature = context.active_object
        collections = armature.data.collections

        collection_hierarchy = []
        for collection in collections:
            bone_collection = BoneCollection(name=collection.name)
            bone_collection.is_visible = collection.is_visible
            bone_collection.is_solo = collection.is_solo
            bone_collection.children = self._populate_bone_collections(collection)
            collection_hierarchy.append(bone_collection)

        converter = cattrs.preconf.json.JsonConverter(omit_if_default=True)
        with open(self.file_path, "w") as file:
            file.write(converter.dumps(collection_hierarchy, indent=2))
        
        return {'FINISHED'}


class TGR_OT_LoadCollections(bpy.types.Operator):
    """Load collections from a JSON file and apply them to the armature"""

    bl_idname = "tgr.load_collections"
    bl_label = "Load Collections"
    bl_options = {'REGISTER', 'UNDO'}

    file_path: bpy.props.StringProperty(
        name="File Path",
        description="File path to load the collections from",
        default="",
        subtype='FILE_PATH'
    )

    @classmethod
    def poll(cls, context):
        if not context.object:
            cls.poll_message_set("No active object found")
            return False
        if not context.active_object.type == 'ARMATURE':
            cls.poll_message_set("Active object is not an armature")
            return False
        return True

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "file_path")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def _recursive_dict_to_collection(self, bone_collections: list[BoneCollection], parent_collection=None):
        """Recursively create collections from a dictionary"""
        for collection in bone_collections:
            # Create a new collection if it doesn't exist
            new_collection = None
            if collection.name not in bpy.context.object.tgr_props.armature.data.collections_all:
                new_collection = bpy.context.object.tgr_props.armature.data.collections.new(collection.name)
            else:
                new_collection = bpy.context.object.tgr_props.armature.data.collections_all[collection.name]
            
            if parent_collection:
                new_collection.parent = parent_collection
            
            # Recursively create child collections
            if collection.children:
                self._recursive_dict_to_collection(collection.children, parent_collection=new_collection)

            new_collection.is_visible = collection.is_visible
            new_collection.is_solo = collection.is_solo

    def execute(self, context):
        armature = context.active_object

        # Load the collections hierarchy from the JSON file
        try:
            with open(self.file_path, 'r') as f:
                collections_hierarchy = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load collections: {e}")
            return {'CANCELLED'}

        converter = cattrs.preconf.json.JsonConverter(omit_if_default=True)
        loaded = converter.structure(collections_hierarchy, list[BoneCollection])
        self._recursive_dict_to_collection(loaded, parent_collection=None)

        return {'FINISHED'}