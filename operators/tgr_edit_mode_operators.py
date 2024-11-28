import bpy
from mathutils import Vector

from ..utils import change_bones_prefix, set_bones_deform


def update_armature(context):
    # Hack to update the armature bones list
    context.active_object.data.bones.update()


def create_org(context):
    tgr_props = context.object.tgr_props
    collections = context.object.tgr_props.armature.data.collections
    preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
    # Get armature
    armature = context.object.tgr_props.armature
    # Deselect the ROOT bone, just to be sure
    root_bone = armature.data.edit_bones[tgr_props.root_bone]
    root_bone.select = False
    root_bone.select_head = False
    root_bone.select_tail = False
    # Duplicate selected bones
    bpy.ops.armature.duplicate()
    # Change bone prefix to the org_prefix
    def_prefix = preferences.def_prefix + preferences.separator
    org_prefix = preferences.org_prefix + preferences.separator
    change_bones_prefix(context.selected_bones, def_prefix, org_prefix)
    # Move the duplicated bones to the org_layer
    org_collection = collections[preferences.org_prefix]
    # Set bones deform to False
    set_bones_deform(context.selected_bones, False)
    bpy.ops.tgr.assign_bones_to_collection(name=org_collection.name)
    update_armature(context)


def create_org_with_selection(self, context):
    """
    Create ORG bones strategy for selected bones.
    """
    preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
    # Get armature
    armature = context.object.tgr_props.armature
    # Create the ORG bones
    create_org(context)
    def_prefix = preferences.def_prefix + preferences.separator
    org_prefix = preferences.org_prefix + preferences.separator
    # Check bones parents to see if they are all ORG bones
    # Also check the children of the ORG bones
    for bone in context.selected_bones:
        if not bone.parent:
            continue
        if not bone.parent.name.startswith(org_prefix):
            # Check if there is a ORG bone with the same name
            try:
                bone_name = bone.parent.name.replace(def_prefix, org_prefix)
                new_parent = armature.data.edit_bones[bone_name]
                bone.parent = new_parent
            except KeyError:
                # If there is no ORG bone with the same name, then keep the original parent
                pass
        if not bone.children:
            # Check if the DEF bone has a child
            def_bone_name = bone.name.replace(org_prefix, def_prefix)
            def_bone = armature.data.edit_bones[def_bone_name]
            for child in def_bone.children:
                try:
                    child_name = child.name.replace(def_prefix, org_prefix)
                    child = armature.data.edit_bones[child_name]
                    child.parent = bone
                except KeyError:
                    # If there is no child, then keep it as it is
                    pass
    return


def create_org_with_all(self, context):
    """
    Create ORG bones strategy for all bones.
    """
    preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
    def_prefix = preferences.def_prefix + preferences.separator
    # Get armature
    armature = context.object.tgr_props.armature
    # Deselect all bones
    bpy.ops.armature.select_all(action='DESELECT')
    # Select all def bones
    for bone in armature.data.edit_bones:
        if bone.name.startswith(def_prefix):
            bone.select = True
            bone.select_head = True
            bone.select_tail = True
    # Create the ORG bones
    create_org(context)
    return


class TGR_OT_CreateORG(bpy.types.Operator):
    """Create the ORG bones for the selected armature"""
    
    bl_idname = "tgr.create_org"
    bl_label = "Create ORG"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        armature = context.object.tgr_props.armature
        if not armature:
            self.report({"ERROR"}, "Armature not set")
            return {"CANCELLED"}
        if context.selected_bones:
            create_org_with_selection(self, context)
        else:
            create_org_with_all(self, context)
        # Deselect all bones
        bpy.ops.armature.select_all(action='DESELECT')
        # Update the armature
        update_armature(context)
        # Finish
        return {"FINISHED"}


class TGR_OT_RemoveORG(bpy.types.Operator):
    """
    Remove the ORG bones from the selected armature.
    """
    bl_idname = "tgr.remove_org"
    bl_label = "Remove ORG"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
        org_prefix = preferences.org_prefix + preferences.separator
        # Deselect all bones
        bpy.ops.armature.select_all(action='DESELECT')
        # Select all ORG bones
        armature = context.object.tgr_props.armature
        if not armature:
            self.report({"ERROR"}, "Armature not set")
            return {"CANCELLED"}

        for bone in armature.data.edit_bones:
            if bone.name.startswith(org_prefix):
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
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
        mch_prefix = preferences.mch_prefix + preferences.separator
        if self.bone_name == "":
            self.bone_name = f"{mch_prefix}BONE"
        # Add a new bone
        bpy.ops.armature.bone_primitive_add(name=self.bone_name)
        # Get the new bone
        bone = context.object.data.edit_bones[-1]
        # Set the bone use_connect
        bone.use_connect = False
        try:
            # Set the bone parent to the root
            bone.parent = context.object.data.edit_bones[context.object.tgr_props.root_bone]
        except KeyError:
            # Trigger a warning if the root bone is not set
            self.report({"WARNING"}, "Root bone not set")
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
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_edit_mode = context.mode == 'EDIT_ARMATURE'
        return is_armature and is_edit_mode

    def execute(self, context):
        preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
        def_prefix = preferences.def_prefix + preferences.separator
        # Add a new bone
        bpy.ops.armature.bone_primitive_add(name=f"{def_prefix}BONE")
        # Get the new bone
        bone = context.object.data.edit_bones[-1]
        # Set the bone use_connect
        bone.use_connect = False
        try:
            # Set the bone parent to the root
            bone.parent = context.object.data.edit_bones[context.object.tgr_props.root_bone]
        except KeyError:
            # Trigger a warning if the root bone is not set
            self.report({"WARNING"}, "Root bone not set")
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
        if not context.object:
            return False
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
        if not context.object:
            return False
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
        if not context.object:
            return False
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

    bone_scale: bpy.props.FloatProperty(name="Bone Scale", description="Bone Scale to be applied to each added bone.",
                                        default=1.0)
    deform: bpy.props.BoolProperty(name="Deform", description="Choose whether the added bones are deform or not.")

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.active_object.type == 'ARMATURE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and is_edit_mode

    def execute(self, context):
        
        if len(selected_bones := context.selected_editable_bones) > 0:
            # Set active bone collection active
            active_bone = context.active_bone
            context.object.tgr_props.armature.data.collections.active_name = active_bone.collections[0].name
            # Check if the active bone colection is visible and store its current state
            active_collection = context.object.tgr_props.armature.data.collections.active
            active_collection_state = active_collection.is_visible
            # Set it to visible
            active_collection.is_visible = True
            
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
            
            # Restore the active collection state
            active_collection.is_visible = active_collection_state
            
            return {'FINISHED'}

        else:
            return {'CANCELLED'}


class TGR_OT_CopyTransforms(bpy.types.Operator):
    """Copy the active bone transforms to the selected bones"""
    bl_idname = "tgr.copy_transforms"
    bl_label = "Copy Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    copy_location: bpy.props.BoolProperty(name="Copy Location",
                                          description=
                                          "Choose whether the location of the active bone will be copied or not.",
                                          default=True)
    copy_rotation: bpy.props.BoolProperty(name="Copy Rotation",
                                          description=
                                          "Choose whether the rotation of the active bone will be copied or not.",
                                          default=True)
    copy_scale: bpy.props.BoolProperty(name="Copy Scale",
                                       description=
                                       "Choose whether the scale of the active bone will be copied or not.",
                                       default=True)

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.active_object.type == 'ARMATURE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and is_edit_mode

    def execute(self, context):
        if len(selected_bones := context.selected_editable_bones) > 0:
            active_bone = context.active_bone
            for bone in selected_bones:
                if bone == active_bone:
                    continue
                if self.copy_location:
                    distance_vector = (bone.head - active_bone.head)
                    bone.head -= distance_vector
                    bone.tail -= distance_vector
                if self.copy_rotation:
                    active_head_tail_vector = (active_bone.head - active_bone.tail).normalized()
                    bone.tail = bone.head - active_head_tail_vector * bone.length
                    bone.roll = active_bone.roll
                if self.copy_scale:
                    bone.length = active_bone.length
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class TGR_OT_CreateSwitchChains(bpy.types.Operator):
    """
    Create switch chains for the selected bones.
    """
    bl_idname = "tgr.create_switch_chains"
    bl_label = "Create Switch Chains"
    bl_options = {'REGISTER', 'UNDO'}
    
    separation: bpy.props.FloatVectorProperty(name="Separation", description="Separation between the bones",
                                              default=(1.0, 0, 0), size=3)
    
    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.active_object.type == 'ARMATURE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and is_edit_mode

    def execute(self, context):
        preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
        def_prefix = preferences.def_prefix + preferences.separator
        mch_prefix = preferences.mch_prefix + preferences.separator
        org_prefix = preferences.org_prefix + preferences.separator
        ctrl_prefix = preferences.ctrl_prefix + preferences.separator
        
        separation = Vector(self.separation)

        # Get the selected bones
        selected_bones = context.selected_bones
        # Check if there are at least two bones selected
        if len(selected_bones) < 2:
            self.report({"ERROR"}, "Select at least two bones")
            return {"CANCELLED"}
        # Loop through the selected bones
        for bone in selected_bones:
            # Check if the bone is a DEF bone
            if bone.name.startswith(def_prefix):
                self.report({"ERROR"}, "Cannot create switch chains for DEF bones")
                return {"CANCELLED"}
        
        # Duplicate the selected bones
        bpy.ops.armature.duplicate()
        # Change bone prefix to the mch_prefix + "SWITCH" and move them using the separation
        for bone in context.selected_bones:
            if bone.name.startswith(org_prefix):
                bone.name = bone.name.replace(org_prefix, mch_prefix + "SWITCH" + preferences.separator)
            elif bone.name.startswith(ctrl_prefix):
                bone.name = bone.name.replace(ctrl_prefix, mch_prefix + "SWITCH" + preferences.separator)
            elif bone.name.startswith(mch_prefix):
                bone.name = bone.name.replace(mch_prefix, mch_prefix + "SWITCH" + preferences.separator)
            
            # Remove the .### from the bone name
            bone.name = bone.name[:-4]
            
            bone.head += separation
            if len(bone.children) == 0 or not bone.children[0].use_connect:
                bone.tail += separation 
        
        # Duplicate the selected bones
        bpy.ops.armature.duplicate()
        # Change bone prefix to the ctrl_prefix + "FK" and move them using the separation
        for bone in context.selected_bones:
           
            bone.name = bone.name.replace(mch_prefix + "SWITCH", ctrl_prefix + "FK")
            
            # Remove the .### from the bone name
            bone.name = bone.name[:-4]
            
            bone.head += separation
            if len(bone.children) == 0 or not bone.children[0].use_connect:
                bone.tail += separation
        
        # Duplicate the selected bones
        bpy.ops.armature.duplicate()
        # Change bone prefix to the mch_prefix + "IK" and move them using the separation
        for bone in context.selected_bones:
            bone.name = bone.name.replace(ctrl_prefix + "FK", mch_prefix + "IK")
            
            # Remove the .### from the bone name
            bone.name = bone.name[:-4]
            
            bone.head += separation
            if len(bone.children) == 0 or not bone.children[0].use_connect:
                bone.tail += separation
            
        
        # Update the armature
        update_armature(context)
        # Finish
        return {"FINISHED"}
        
    
class TGR_OT_CreateIntermediateBone(bpy.types.Operator):
    """Creates an MCH bone that acts as an intermediate bone"""
    
    bl_idname = "tgr.create_intermediate_bone"
    bl_label = "Create Intermediate Bone"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.active_object.type == 'ARMATURE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and is_edit_mode
    
    def execute(self, context):
        preferences = context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
        def_prefix = preferences.def_prefix + preferences.separator
        org_prefix = preferences.org_prefix + preferences.separator
        mch_prefix = preferences.mch_prefix + preferences.separator
        ctrl_prefix = preferences.ctrl_prefix + preferences.separator
        
        # It doesn't make sense to create an intermediate bone for a DEF bone
        if context.active_bone.name.startswith(def_prefix):
            self.report({"ERROR"}, "Cannot create an intermediate bone for a DEF bone")
            return {"CANCELLED"}
        
        # Duplicate the active bones
        bpy.ops.armature.duplicate()
        # Scale bones to 0.5
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
        # Change bone prefix to the mch_prefix or mch_prefix + "INT" if the selected bone is already an MCH bone and remove the .### from the bone name
        for bone in context.selected_editable_bones:
            # Set the current bone as the parent of the original bone
            context.active_object.data.edit_bones[bone.name[:-4]].parent = bone
            if bone.name.startswith(org_prefix):
                bone.name = bone.name.replace(org_prefix, mch_prefix)
            elif bone.name.startswith(ctrl_prefix):
                bone.name = bone.name.replace(ctrl_prefix, mch_prefix)
            elif bone.name.startswith(mch_prefix):
                bone.name = bone.name.replace(mch_prefix, mch_prefix + "INT_")
            bone.name = bone.name[:-4]
            
        # Update the armature
        update_armature(context)
        # Finish
        return {"FINISHED"}
                
                