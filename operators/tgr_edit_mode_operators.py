import bpy

from ..utils.tgr_edit_mode_utils import change_bones_prefix, bone_layers_by_number, set_bones_deform

def update_armature(context):
    # Hack to update the armature bones list
    context.active_object.data.bones.update()


def createTGT(context):
    tgr_props = context.object.tgr_props
    tgr_layers = context.object.tgr_layer_collection
    # Get armature
    armature = context.object.tgr_props.armature
    # Desselect the ROOT bone, just to be sure
    root_bone = armature.data.edit_bones[tgr_props.root_bone]
    root_bone.select = False
    root_bone.select_head = False
    root_bone.select_tail = False
    # Duplicate selected bones
    bpy.ops.armature.duplicate()
    # Change bone prefix to the tgt_prefix
    change_bones_prefix(context.selected_bones, tgr_props.def_prefix, tgr_props.tgt_prefix)
    # Move the duplicated bones to the tgt_layer
    layers = bone_layers_by_number(tgr_layers[1].index)
    # Set bones deform to False
    set_bones_deform(context.selected_bones, False)
    bpy.ops.armature.bone_layers(layers=layers)
    # Make the tgt_layer visible
    armature.data.layers[tgr_layers[1].index] = True
    update_armature(context)


def createTGT_with_selection(self, context):
    """
    Create TGT bones strategy for selected bones.
    """
    tgr_props = context.object.tgr_props
    # Get armature
    armature = context.object.tgr_props.armature
    # Create the TGT bones
    createTGT(context)
    # Check bones parents to see if they are all TGT bones
    # Also check the children of the TGT bones
    for bone in context.selected_bones:
        if not bone.parent:
            continue
        if not bone.parent.name.startswith(tgr_props.tgt_prefix):
            # Check if there is a TGT bone with the same name
            try:
                bone_name = bone.parent.name.replace(tgr_props.def_prefix, tgr_props.tgt_prefix)
                new_parent = armature.data.edit_bones[bone_name]
                bone.parent = new_parent
            except KeyError:
                # If there is no TGT bone with the same name, then keep the original parent
                pass
        if not bone.children:
            # Check if the DEF bone has a child
            def_bone_name = bone.name.replace(tgr_props.tgt_prefix, tgr_props.def_prefix)
            def_bone = armature.data.edit_bones[def_bone_name]
            for child in def_bone.children:
                try:
                    child_name = child.name.replace(tgr_props.def_prefix, tgr_props.tgt_prefix)
                    child = armature.data.edit_bones[child_name]
                    child.parent = bone
                except KeyError:
                    # If there is no child, then keep it as it is
                    pass

    return


def createTGT_with_all(self, context):
    """
    Create TGT bones strategy for all bones.
    """
    # Get armature
    armature = context.object.tgr_props.armature
    # Deselect all bones
    bpy.ops.armature.select_all(action='DESELECT')
    # Select all def bones
    for bone in armature.data.edit_bones:
        if bone.name.startswith(armature.tgr_props.def_prefix):
            bone.select = True
            bone.select_head = True
            bone.select_tail = True
    # Create the TGT bones
    createTGT(context)
    return


class TGR_OT_CreateTGT(bpy.types.Operator):
    """
    Create the TGT bones for the selected armature.
    """
    bl_idname = "tgr.create_tgt"
    bl_label = "Create TGT"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        armature = context.object.tgr_props.armature
        if not armature:
            self.report({"ERROR"}, "Armature not set")
            return {"CANCELLED"}
        if context.selected_bones:
            createTGT_with_selection(self, context)
        else:
            createTGT_with_all(self, context)
        # Deselect all bones
        bpy.ops.armature.select_all(action='DESELECT')
        # Update the armature
        update_armature(context)
        # Finish
        return {"FINISHED"}


class TGR_OT_RemoveTGT(bpy.types.Operator):
    """
    Remove the TGT bones from the selected armature.
    """
    bl_idname = "tgr.remove_tgt"
    bl_label = "Remove TGT"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        # Deselect all bones
        bpy.ops.armature.select_all(action='DESELECT')
        # Select all TGT bones
        armature = context.object.tgr_props.armature
        if not armature:
            self.report({"ERROR"}, "Armature not set")
            return {"CANCELLED"}
        
        for bone in armature.data.edit_bones:
            if bone.name.startswith("TGT-"):
                bone.select = True
                bone.select_head = True
                bone.select_tail = True
        
        # Delete the selected bones
        bpy.ops.armature.delete()
        # Update the armature
        update_armature(context)
        # Finish
        return {"FINISHED"}


class TGR_OT_AddNonDeformBone(bpy.types.Operator):
    """
    Add a non-deforming bone to the selected armature.
    """
    bl_idname = "tgr.add_non_deform_bone"
    bl_label = "Add Non-Deform Bone"
    bl_options = {'REGISTER', 'UNDO'}
    
    bone_name: bpy.props.StringProperty(name="Bone Name", default="")

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        if self.bone_name == "":
            self.bone_name = f"{context.object.tgr_props.mch_prefix}BONE"
        # Add a new bone
        bpy.ops.armature.bone_primitive_add(name=self.bone_name)
        # Get the new bone
        bone = context.object.data.edit_bones[-1]
        # Set the bone use_connect
        bone.use_connect = False
        # Set the bone parent to the root
        bone.parent = context.object.data.edit_bones[context.object.tgr_props.root_bone]
        # Align the bone rotation to the world
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        context.object.data.edit_bones.active = bone
        bpy.ops.tgr.align_bone_to_world()
        # Set the bone use_deform
        bone.use_deform = False
        # Update the armature
        update_armature(context)
        # Finish
        return {"FINISHED"}
    

class TGR_OT_AddDeformBone(bpy.types.Operator):
    """
    Add a deform bone to the selected armature.
    """
    bl_idname = "tgr.add_deform_bone"
    bl_label = "Add Deform Bone"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        # Add a new bone
        bpy.ops.armature.bone_primitive_add(name=f"{context.object.tgr_props.mch_prefix}BONE")
        # Get the new bone
        bone = context.object.data.edit_bones[-1]
        # Set the bone use_connect
        bone.use_connect = False
        # Set the bone parent to the root
        bone.parent = context.object.data.edit_bones[context.object.tgr_props.root_bone]
        # Align the bone rotation to the world
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        context.object.data.edit_bones.active = bone
        bpy.ops.tgr.align_bone_to_world()
        # Set the bone use_deform
        bone.use_deform = True
        # Update the armature
        update_armature(context)
        # Finish
        return {"FINISHED"}



class TGR_OT_ParentToRoot(bpy.types.Operator):
    """
    Parent the selected bones to the root bone.
    """
    bl_idname = "tgr.parent_to_root"
    bl_label = "Parent to Root"
    bl_description = "Parent selected bones to the root bone"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        root_bone = context.object.tgr_props.root_bone
        if root_bone is None:
            self.report({"ERROR"}, "Root bone not set")
            return {"CANCELLED"}
        if not context.selected_bones:
            self.report({"ERROR"}, "No bones selected")
            return {"CANCELLED"}
        # Loop through the selected edit bones
        for bone in context.selected_bones:
            bone.use_connect = False
            bone.parent = context.object.data.edit_bones[root_bone]
        # Update the armature
        update_armature(context)
        return {'FINISHED'}


class TGR_OT_ConnectBones(bpy.types.Operator):
    """
    Connect the selected bones to their parent
    without moving their head.
    """
    bl_idname = "tgr.connect_bones"
    bl_label = "Connect Bones"
    bl_description = "Connect selected bones to their parent"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        # Check if at least one bone is selected
        if not context.selected_bones:
            self.report({"ERROR"}, "No bones selected")
            return {"CANCELLED"}
        # Loop through the selected edit bones
        for bone in context.selected_bones:
            # Skip if the bone's parent is not selected
            if bone.parent not in context.selected_bones:
                continue
            # Move the tail of the parent bone to the head of the current bone
            bone.parent.tail = bone.head
            # Connect the current bone to its parent
            bone.use_connect = True
        # Update the armature
        update_armature(context)
        return {'FINISHED'}


class TGR_OT_AlignBoneToWorld(bpy.types.Operator):
    """
    Align bone rotation to world.
    """
    bl_idname = "tgr.align_bone_to_world"
    bl_label = "Align Rotation to World"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and is_edit_mode

    def execute(self, context):
        if len(selected_bones := context.selected_bones) > 0:
            for bone in selected_bones:
                # Disconnect the bone's children from the bone.
                for child in bone.children:
                    child.use_connect = False
                # Get the bone's matrix
                bone_matrix = bone.matrix
                # Set the bone's matrix rotation part to [1, 0, 0, 0, 1, 0, 0, 0, 1]
                bone_matrix.col[0].xyz = (1, 0, 0)
                bone_matrix.col[1].xyz = (0, 1, 0)
                bone_matrix.col[2].xyz = (0, 0, 1)
                # Set the bone's roll to 0
                bone.roll = 0
                # Set the bone's matrix to the new matrix
                bone.matrix = bone_matrix
            # Update the armature
            update_armature(context)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
        

class TGR_OT_BoneOnPoints(bpy.types.Operator):
    """
    Add bones on selected bones points (Head and Tail).
    """
    bl_idname = "tgr.bones_on_points"
    bl_label = "Bones on Points"
    bl_options = {'REGISTER', 'UNDO'}
    
    bone_scale: bpy.props.FloatProperty(name="Bone Scale", description="Bone Scale to be applied to each added bone.", default=1.0)
    deform: bpy.props.BoolProperty(name="Deform", description="Choose wether the added bones are deform or not.")

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and is_edit_mode

    def execute(self, context):
        if len(selected_bones := context.selected_editable_bones) > 0:
            current_3d_cursor_pos = context.scene.cursor.location
            for bone in selected_bones:
                context.scene.cursor.location = bone.head
                if self.deform:
                    bpy.ops.tgr.add_deform_bone()
                else:
                    bpy.ops.tgr.add_non_deform_bone()
                
                added_bone = context.selected_editable_bones[0]
                added_bone.length = self.bone_scale
                
                is_children_in_selection = any([child in selected_bones for child in bone.children])
                
                if not is_children_in_selection:
                    context.scene.cursor.location = bone.tail
                    if self.deform:
                        bpy.ops.tgr.add_deform_bone()
                    else:
                        bpy.ops.tgr.add_non_deform_bone()
                    added_bone = context.selected_editable_bones[0]
                    added_bone.length = self.bone_scale
            
            context.scene.cursor.location = current_3d_cursor_pos
            return {'FINISHED'}
        
        else:
            return {'CANCELLED'}