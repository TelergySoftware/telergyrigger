import bpy
from utils import TGR_EditModeUtils


# ------------- ADD PREFIX OR SUFFIX -------------

class TGR_OT_AddPrefix(bpy.types.Operator):
    """
    Add a prefix to the selected bone.
    """
    bl_idname = "tgr.add_prefix"
    bl_label = "Add Prefix"
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
        tgr_props = context.object.tgr_props
        
        if context.mode == 'EDIT_ARMATURE':
            # Check if there are any bones selected
            if len(edit_bones := context.selected_bones) > 0:
                for bone in edit_bones:
                    # Root bone doesn't need a prefix
                    if bone.name == tgr_props.root_bone:
                        continue
                    # Check if the prefix is already in the name
                    if not bone.name.startswith(tgr_props.prefix):
                        # Add the prefix to the name
                        bone.name = tgr_props.prefix + bone.name
            else:
                # Add the prefix to all bones
                edit_bones = context.object.data.edit_bones
                for bone in edit_bones:
                    # Root bone doesn't need a prefix
                    if bone.name == tgr_props.root_bone:
                        continue
                    # Check if the prefix is already in the name
                    if not bone.name.startswith(tgr_props.prefix):
                        # Add the prefix to the name
                        bone.name = tgr_props.prefix + bone.name
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones:= context.selected_pose_bones) > 0:
                for bone in pose_bones:
                    # Root bone doesn't need a prefix
                    if bone.name == tgr_props.root_bone:
                        continue
                    # Check if the prefix is already in the name
                    if not bone.name.startswith(tgr_props.prefix):
                        # Add the prefix to the name
                        bone.name = tgr_props.prefix + bone.name
            else:
                # Add the prefix to all bones
                pose_bones = context.object.pose.bones
                for bone in pose_bones:
                    # Root bone doesn't need a prefix
                    if bone.name == tgr_props.root_bone:
                        continue
                    # Check if the prefix is already in the name
                    if not bone.name.startswith(tgr_props.prefix):
                        # Add the prefix to the name
                        bone.name = tgr_props.prefix + bone.name
        return {"FINISHED"}


class TGR_OT_AddSuffix(bpy.types.Operator):
    """
    Add a suffix to the selected bone.
    """
    bl_idname = "tgr.add_suffix"
    bl_label = "Add Suffix"
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
                    # Root bone does not need a suffix
                    if bone.name == context.object.tgr_props.root_bone:
                        continue
                    # Check if the suffix is already in the name
                    if not bone.name.endswith(context.object.tgr_props.suffix):
                        # Add the suffix to the name
                        bone.name = bone.name + context.object.tgr_props.suffix
            else:
                # Add the suffix to all bones
                edit_bones = context.object.data.edit_bones
                for bone in edit_bones:
                    # Root bone does not need a suffix
                    if bone.name == context.object.tgr_props.root_bone:
                        continue
                    # Check if the suffix is already in the name
                    if not bone.name.endswith(context.object.tgr_props.suffix):
                        # Add the suffix to the name
                        bone.name = bone.name + context.object.tgr_props.suffix
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones:= context.selected_pose_bones) > 0:
                for bone in pose_bones:
                    # Root bone does not need a suffix
                    if bone.name == context.object.tgr_props.root_bone:
                        continue
                    # Check if the suffix is already in the name
                    if not bone.name.endswith(context.object.tgr_props.suffix):
                        # Add the suffix to the name
                        bone.name = bone.name + context.object.tgr_props.suffix
            else:
                # Add the suffix to all bones
                pose_bones = context.object.pose.bones
                for bone in pose_bones:
                    # Root bone does not need a suffix
                    if bone.name == context.object.tgr_props.root_bone:
                        continue
                    # Check if the suffix is already in the name
                    if not bone.name.endswith(context.object.tgr_props.suffix):
                        # Add the suffix to the name
                        bone.name = bone.name + context.object.tgr_props.suffix
        return {"FINISHED"}


# ------------- REMOVE PREFIX OR SUFFIX -------------

class TGR_OT_RemovePrefix(bpy.types.Operator):
    """
    Remove the prefix from the selected bone.
    """
    bl_idname = "tgr.remove_prefix"
    bl_label = "Remove Prefix"
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
                    # Check if the prefix is in the name
                    if bone.name.startswith(context.object.tgr_props.prefix):
                        # Remove the prefix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.prefix, "")
            else:
                # Remove the prefix from all bones
                edit_bones = context.object.data.edit_bones
                for bone in edit_bones:
                    # Check if the prefix is in the name
                    if bone.name.startswith(context.object.tgr_props.prefix):
                        # Remove the prefix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.prefix, "")
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones:= context.selected_pose_bones) > 0:
                for bone in pose_bones:
                    # Check if the prefix is in the name
                    if bone.name.startswith(context.object.tgr_props.prefix):
                        # Remove the prefix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.prefix, "")
            else:
                # Remove the prefix from all bones
                pose_bones = context.object.pose.bones
                for bone in pose_bones:
                    # Check if the prefix is in the name
                    if bone.name.startswith(context.object.tgr_props.prefix):
                        # Remove the prefix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.prefix, "")
        return {"FINISHED"}


class TGR_OT_RemoveSuffix(bpy.types.Operator):
    """
    Remove the suffix from the selected bone.
    """
    bl_idname = "tgr.remove_suffix"
    bl_label = "Remove Suffix"
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
                    # Check if the suffix is in the name
                    if bone.name.endswith(context.object.tgr_props.suffix):
                        # Remove the suffix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.suffix, "")
            else:
                # Remove the suffix from all bones
                edit_bones = context.object.data.edit_bones
                for bone in edit_bones:
                    # Check if the suffix is in the name
                    if bone.name.endswith(context.object.tgr_props.suffix):
                        # Remove the suffix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.suffix, "")
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones:= context.selected_pose_bones) > 0:
                for bone in pose_bones:
                    # Check if the suffix is in the name
                    if bone.name.endswith(context.object.tgr_props.suffix):
                        # Remove the suffix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.suffix, "")
            else:
                # Remove the suffix from all bones
                pose_bones = context.object.pose.bones
                for bone in pose_bones:
                    # Check if the suffix is in the name
                    if bone.name.endswith(context.object.tgr_props.suffix):
                        # Remove the suffix from the name
                        bone.name = bone.name.replace(context.object.tgr_props.suffix, "")
        return {"FINISHED"}


# ------------- CLEAN UP -------------

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
                    bone.name = self.clean_up_name(bone.name)
            else:
                # Clean up the name of all bones
                edit_bones = context.object.data.edit_bones
                for bone in edit_bones:
                    # Clean up the name of the selected bone
                    bone.name = self.clean_up_name(bone.name)
        elif context.mode == 'POSE':
            # Check if there are any bones selected
            if len(pose_bones:= context.selected_pose_bones) > 0:
                for bone in pose_bones:
                    # Clean up the name of the selected bone
                    bone.name = self.clean_up_name(bone.name)
            else:
                # Clean up the name of all bones
                pose_bones = context.object.pose.bones
                for bone in pose_bones:
                    # Clean up the name of the selected bone
                    bone.name = self.clean_up_name(bone.name)
        return {"FINISHED"}
    
    def clean_up_name(self, name) -> str:
        """
        Change the .001, .002, .003, ... suffixes to be before the .L or .R suffixes if
        they exist and change the dots to dashs.
        """
        # Check if the last three characters are numbers
        if (digit := name[-3:]).isdigit():
            # Check if the name has Left or Right suffixes in it
            lr_suffix = ""
            for suffix in [".L", ".R", "-L", "-R", "_L", "_R"]:
                if suffix in name:
                    lr_suffix = suffix
                    break
            if lr_suffix != "":
                name = name.replace(lr_suffix, "")
                name = name + f"-{digit}" + lr_suffix
            else:
                name = name[:-4] + f"-{digit}"
        return name


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
        return self.execute(context)


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
        layers = TGR_EditModeUtils.bone_layers_by_number(self.layer)
        
        if context.mode == 'EDIT_ARMATURE':
            # Set the layer of the selected bones
            for bone in context.selected_bones:
                bone.layers = layers if not self.shift else [old or new for old, new in zip(bone.layers, layers)]
        elif context.mode == 'POSE':
            # Set the layer of the selected bones
            for bone in context.selected_pose_bones:
                bone.bone.layers = layers if not self.shift else [old or new for old, new in zip(bone.bone.layers, layers)]
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
        for bone in context.selected_bones:
            bone.hide_select = layer.lock_selection
        
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
