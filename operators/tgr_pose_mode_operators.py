import bpy
from mathutils import Vector

def update_armature(context):
    # Hack to update the armature
    context.object.data.bones.update()
    context.scene.view_layers.update()


class TGR_OT_BindTGT(bpy.types.Operator):
    """
    Binds the TGT bones to the DEF bones.

    conditions:
        - Active object is an armature:
            - Is pose mode:
                - TGT bones exist.
    """
    bl_idname = "tgr.bind_tgt"
    bl_label = "Bind TGT"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        # Check if there is any selected bones
        bones_to_bind = None
        if len(context.selected_pose_bones) > 0:
            bones_to_bind = context.selected_pose_bones
        else:
            bones_to_bind = context.object.pose.bones
        # Check if there are TGT bones for each DEF bone
        for bone in bones_to_bind:
            if bone.name.startswith('TGT-') or bone.name.startswith('CTRL-'):
                # Check if there's a DEF bone with the same name
                if (bone.name.replace('TGT-', 'DEF-') not in context.object.pose.bones) and (bone.name.replace('CTRL-', 'DEF-') not in context.object.pose.bones):
                    self.report({"ERROR"}, "No TGT or CTRL bone for DEF bone: " + bone.name)
                    return {"CANCELLED"}
        
        # Bind the TGT bones to the DEF bones
        for bone in bones_to_bind:
            if bone.name.startswith('TGT-') or bone.name.startswith('DEF-'):
                # Get the DEF bone
                try:
                    def_bone = context.object.pose.bones[bone.name.replace('TGT-', 'DEF-')]
                except KeyError:
                    def_bone = context.object.pose.bones[bone.name.replace('CTRL-', 'DEF-')]
                # Bind the TGT bone to the DEF bone
                if 'TGT' in bone.constraints:
                    def_bone.constraints['TGT'].subtarget = bone.name
                else:
                    constraint = def_bone.constraints.new('COPY_TRANSFORMS')
                    constraint.target = context.object.tgr_props.armature
                    constraint.subtarget = bone.name
                    constraint.name = 'TGT'
                    # Ensure this constraint is the first one
                    def_bone.constraints.move(len(def_bone.constraints) - 1, 0)
        
        # Update the view layer
        update_armature(context)
        return {'FINISHED'}


class TGR_OT_UnbindTGT(bpy.types.Operator):
    """
    Unbinds the TGT bones from the DEF bones.

    conditions:
        - Active object is an armature:
            - Is pose mode:
                - TGT bones exist.
    """
    bl_idname = "tgr.unbind_tgt"
    bl_label = "Unbind TGT"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        # Unbind the TGT bones from the DEF bones
        for bone in context.object.pose.bones:
            if bone.name.startswith('DEF-'):
                # Unbind the TGT bone from the DEF bone
                if 'TGT' in bone.constraints:
                    bone.constraints.remove(bone.constraints['TGT'])

        # Update the view layer
        update_armature(context)
        return {'FINISHED'}


class TGR_OT_IsolateBoneRotation(bpy.types.Operator):
    """
    Isolate the rotation of the selected bone.
    """
    bl_idname = "tgr.isolate_bone_rotation"
    bl_label = "Isolate Bone Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        # Check if at least one bone is selected
        if not context.selected_pose_bones:
            self.report({"ERROR"}, "No bones selected")
            return {"CANCELLED"}
        
        # Change the mode to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get current mirror mode
        mirror_mode = bpy.context.object.data.use_mirror_x
        
        # Set the mirror mode to off
        bpy.context.object.data.use_mirror_x = False
        
        # Get the selected bones
        selected_bones = context.selected_bones
        
        # Duplicate the selected bones and resize them to 50%
        bpy.ops.armature.duplicate()
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))

        # Replace the TGT- prefix for MCH-INT- prefix and remove the .001 suffix
        mch_int_bone_names = []
        for bone in context.selected_bones:
            if bone.name.startswith('TGT-'):
                bone.name = bone.name.replace('TGT-', 'MCH-INT-')
                bone.name = bone.name.replace('.001', '')
                mch_int_bone_names.append(bone.name)
            
        
        # Duplicate the selected bones and resize them to 50%
        bpy.ops.armature.duplicate()
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
        
        # Replace the MCH-INT- prefix for MCH- prefix and remove the .001 suffix
        mch_bones_names = []
        for bone in context.selected_bones:
            if bone.name.startswith('MCH-INT-'):
                bone.name = bone.name.replace('MCH-INT-', 'MCH-')
                bone.name = bone.name.replace('.001', '')
                mch_bones_names.append(bone.name)

        # Change the TGT- prefix for CTRL- prefix and parent them to the MCH-INT- bones
        for bone in selected_bones:
            bone.use_connect = False
            bone.parent = context.object.data.edit_bones[bone.name.replace('TGT-', 'MCH-INT-')]

        # Parent the MCH-INT- bones to the ROOT bone
        root_bone = context.object.tgr_props.root_bone
        for bone_name in mch_int_bone_names:
            bone = context.object.data.edit_bones[bone_name]
            bone.use_connect = False
            bone.parent = context.object.data.edit_bones[root_bone]
        
        # Change mirror mode to the original value
        bpy.context.object.data.use_mirror_x = mirror_mode
        
        # Change back to pose mode
        bpy.ops.object.mode_set(mode='POSE')
        
        # Add copy location and rotation constraints to the MCH-INT- bones, and set the target to the MCH- bones
        for bone_name in mch_int_bone_names:
            # Get the pose bone
            pose_bone = context.object.pose.bones[bone_name]
            # Add copy location constraint
            constraint = pose_bone.constraints.new('COPY_LOCATION')
            constraint.target = context.object
            constraint.subtarget = pose_bone.name.replace('MCH-INT-', 'MCH-')
            constraint.name = 'ISOLATE ROTATION LOC'
            # Add copy rotation constraint
            constraint = pose_bone.constraints.new('COPY_ROTATION')
            constraint.target = context.object
            constraint.subtarget = pose_bone.name.replace('MCH-INT-', 'MCH-')
            constraint.name = 'ISOLATE ROTATION ROT'
            constraint.influence = 0.0
            # Send the MCH-INT- and MCH- bones to the layer 2
            pose_bone.bone.layers = [i == 2 for i in range(len(pose_bone.bone.layers))]
            mch_bone = context.object.pose.bones[bone_name.replace('MCH-INT-', 'MCH-')]
            mch_bone.bone.layers = [i == 2 for i in range(len(mch_bone.bone.layers))]

        return {'FINISHED'}


class TGR_OT_CreateIkFkSwichChain(bpy.types.Operator):
    """
    Create an IK/FK switch chain.

    conditions:
        - Active object is an armature:
            - Is pose mode:
                - At least two bones are selected.
    """
    bl_idname = "tgr.create_ikfk_switch_chain"
    bl_label = "Create IK/FK Switch Chain"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        # Check if at least one bone is selected
        if not len(context.selected_pose_bones) > 1:
            self.report({"ERROR"}, "Not enough bones selected. Select at least two bones.")
            return {"CANCELLED"}
        
        # Change the mode to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get current mirror mode
        mirror_mode = bpy.context.object.data.use_mirror_x
        # Set the mirror mode to off
        bpy.context.object.data.use_mirror_x = False

        # Get the selected bones
        selected_bones = context.selected_bones
        
        
        # Duplicate the selected bones
        bpy.ops.armature.duplicate()

        # Replace the TGT- prefix for CTRL-FK- prefix and remove the .001 suffix
        fk_bone_names = []
        for bone in context.selected_bones:
            if bone.name.startswith('TGT-'):
                bone.name = bone.name.replace('TGT-', 'CTRL-FK-')
                bone.name = bone.name.replace('.001', '')
                fk_bone_names.append(bone.name)
        
        # Duplicate the selected bones
        bpy.ops.armature.duplicate()

        # Replace the CTRL-FK- prefix for MCH-IK- prefix if at least one child bone is in
        # the selected bones, else change the prefix to CTRL-IK- instead and remove the .001 suffix
        ik_bone_names = []
        for bone in context.selected_bones:
            if bone.name.startswith('CTRL-FK-'):
                if any(child in context.selected_bones for child in bone.children): 
                    bone.name = bone.name.replace('CTRL-FK-', 'MCH-IK-')
                    bone.name = bone.name.replace('.001', '')
                    ik_bone_names.append(bone.name)
                else:
                    bone.name = bone.name.replace('CTRL-FK-', 'CTRL-IK-')
                    bone.name = bone.name.replace('.001', '')
                    ik_bone_names.append(bone.name)        

        # Change mirror mode to the original value
        bpy.context.object.data.use_mirror_x = mirror_mode

        # Change back to pose mode
        bpy.ops.object.mode_set(mode='POSE')

        print(fk_bone_names, ik_bone_names)

        # Add copy location, rotation and scale in the Y axis constraints to the TGT- selected bones
        # and set the target to the MCH-IK- bones or CTRL-IK- bone if no child bones are selected
        for bone, ik_bone_name, fk_bone_name in zip(selected_bones, ik_bone_names, fk_bone_names):
            # Get the pose bone
            pose_bone = context.object.pose.bones[bone.name]
            # Set ik_stretch to 0.05 to the ik_bones
            context.object.pose.bones[ik_bone_name].ik_stretch = 0.05
            # Add copy location constraint
            constraint = pose_bone.constraints.new('COPY_LOCATION')
            constraint.target = context.object
            constraint.subtarget = ik_bone_name
            constraint.name = 'IK COPY LOCATION'
            # Add copy rotation constraint
            constraint = pose_bone.constraints.new('COPY_ROTATION')
            constraint.target = context.object
            constraint.subtarget = ik_bone_name
            constraint.name = 'IK COPY ROTATION'
            # Add copy scale constraint (in Y axis only) in local space
            constraint = pose_bone.constraints.new('COPY_SCALE')
            constraint.target = context.object
            constraint.subtarget = ik_bone_name
            constraint.target_space = 'LOCAL'
            constraint.owner_space = 'LOCAL'
            constraint.name = 'IK COPY SCALE'
            constraint.use_x = False
            constraint.use_z = False
            
            if ik_bone_name.startswith('CTRL-IK-'):
                # Change the parent prefix from MCH-IK to CTRL-IK-
                ik_bone = context.object.pose.bones[ik_bone_name]
                ik_bone.bone.parent.name = ik_bone.bone.parent.name.replace('MCH-IK-', 'CTRL-IK-')
                # Deselect all bones
                bpy.ops.pose.select_all(action='DESELECT')
                # Change to Edit mode
                bpy.ops.object.mode_set(mode='EDIT')
                # Get current mirror mode
                mirror_mode = bpy.context.object.data.use_mirror_x
                # Set the mirror mode to off
                bpy.context.object.data.use_mirror_x = False
                # Select the bone
                ik_edit_bone = context.object.data.edit_bones[ik_bone_name]
                ik_edit_bone.select = True
                if ik_edit_bone.use_connect:
                    ik_edit_bone.parent.select_tail = True
                else:
                    ik_edit_bone.select_head = True
                ik_edit_bone.select_tail = True
                # Store parent bone name for later reference
                target_bone_name = ik_edit_bone.parent.name
                # Duplicate the CTRL-IK- bone and resize it to 50%
                bpy.ops.armature.duplicate()
                bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
                # Replace the selected bone prefix from CTRL-IK for MCH-IK-
                mch_ik_bone = context.selected_bones[0]
                mch_ik_bone_name = mch_ik_bone.name = ik_bone_name.replace('CTRL-IK-', 'MCH-IK-')
                # Remove the .001 suffix
                mch_ik_bone.name = mch_ik_bone.name.replace('.001', '')
                # Parent the CTRL-IK- bone to the MCH-IK- bone
                ik_edit_bone.use_connect = False
                ik_edit_bone.parent = context.object.data.edit_bones[mch_ik_bone_name]
                # Duplicate the current selected bone
                bpy.ops.armature.duplicate()
                # Replace the selected bone prefix from CTRL-IK for CTRL-IK-CHAIN-
                ctrl_ik_chain_bone = context.selected_bones[0]
                ctrl_ik_chain_bone.use_connect = False
                ctrl_ik_chain_bone.name = ik_bone_name.replace('CTRL-IK-', 'CTRL-IK-CHAIN-')
                # Remove the .001 suffix
                ctrl_ik_chain_bone.name = ctrl_ik_chain_bone.name.replace('.001', '')
                # Align current selected bone to the world
                bpy.ops.tgr.align_bone_to_world()
                # Set CTRL-IK-CHAIN- bone as the parent of the MCK-IK- bone
                mch_ik_bone.parent = ctrl_ik_chain_bone
                # Set the ROOT bone as the parent of the CTRL-IK-CHAIN- bone
                ctrl_ik_chain_bone.parent = context.object.data.edit_bones[context.object.tgr_props.root_bone]
                # Resize it to 3 times the current size
                bpy.ops.transform.resize(value=(3, 3, 3))
                # Add a new non-deform bone to the same location as the target bone's head
                bpy.ops.tgr.add_non_deform_bone()
                pole_tgt_bone = context.selected_bones[0]
                pole_tgt_bone_name = pole_tgt_bone.name = pole_tgt_bone.name.replace('MCH-BONE', 'CTRL-POLE-TGT')
                pole_tgt_bone.head = context.object.data.edit_bones[target_bone_name].head + Vector((0, ctrl_ik_chain_bone.length * 3, 0.0))
                pole_tgt_bone.tail = pole_tgt_bone.head + Vector((0, ctrl_ik_chain_bone.length * 4, 0))
                # Set the pole target bone's parent to the CTRL-IK-CHAIN- bone
                pole_tgt_bone.parent = ctrl_ik_chain_bone
                # Return the mirror mode to the original value
                bpy.context.object.data.use_mirror_x = mirror_mode
                # Change back to pose mode
                bpy.ops.object.mode_set(mode='POSE')
                # Add the IK constraint to the parent bone and set the current armature as target
                # and the current bone as subtarget.
                constraint = context.object.pose.bones[target_bone_name].constraints.new('IK')
                constraint.target = context.object
                constraint.subtarget = mch_ik_bone_name
                constraint.pole_target = context.object
                constraint.pole_subtarget = pole_tgt_bone_name
                constraint.name = 'IK CHAIN'
                # Set the IK chain number to be the length of the ik_bone_names list - 1
                constraint.chain_count = len(ik_bone_names) - 1
                # Send the mch_ik_bone to the layer 2
                mch_ik_bone.layers = [i == 2 for i in range(len(mch_ik_bone.layers))]
            
            # Send the MCH-IK bones to the layer 2
            pose_bone.bone.layers = [i == 2 for i in range(len(pose_bone.bone.layers))]

            # Add copy transform constraint to the TGT- selected bones and set the target to the CTRL-FK- bones
            # with the influence of 0.0
            constraint = pose_bone.constraints.new('COPY_TRANSFORMS')
            constraint.target = context.object
            constraint.subtarget = fk_bone_name
            constraint.name = 'FK COPY TRANSFORM'
            constraint.influence = 0.0

        # Finish by deselecting all bones
        bpy.ops.pose.select_all(action='DESELECT')
        return {'FINISHED'}


class TGR_OT_CreateRotationChain(bpy.types.Operator):
    """
    Create a rotation chain with the selected bones
    """
    
    bl_idname = "tgr.create_rotation_chain"
    bl_label = "Create Rotation Chain"
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        return is_armature and is_pose_mode
    
    def execute(self, context):
        tgr_props = context.object.tgr_props
        # Must not stretch DEF- bones
        for bone in context.selected_pose_bones:
            if bone.name.startswith(tgr_props.def_prefix):
                self.report({'ERROR'}, 'Cannot use rotation chains on DEF- bones')
                return {'CANCELLED'}
        
        bpy.ops.object.mode_set(mode='EDIT')
        for bone in context.selected_bones:
            bone.use_connect = False
            split_name = bone.name.split('-')
            bone_name = "CTRL-"
            
            for name_part in split_name[1:]:
                bone_name += f"{name_part}"
            
            bone.name = bone_name
        ctrl_bone_names = [bone.name for bone in context.selected_bones]
        
        bpy.ops.armature.duplicate()
        for bone in context.selected_bones:
            bone.name = bone.name.replace("CTRL-", "CTRL-TWEAK-")
            bone.name = bone.name.replace(".001", "")
        ctrl_tweak_bone_names = [bone.name for bone in context.selected_bones]
            
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
        first_bones = True
        for ctrl, tweak in zip(ctrl_bone_names, ctrl_tweak_bone_names):
            ctrl_edit_bone = context.object.data.edit_bones[ctrl]
            ctrl_tweak_edit_bone = context.object.data.edit_bones[tweak]
            
            ctrl_edit_bone.parent = ctrl_tweak_edit_bone
            if first_bones:
                first_bones = False
                tweak_parent = ctrl_edit_bone
                continue
            
            ctrl_tweak_edit_bone.parent = tweak_parent
            tweak_parent = ctrl_edit_bone
        
        bpy.ops.object.mode_set(mode='POSE')
        first_bone = True
        for ctrl in ctrl_bone_names:
            ctrl_pose_bone = context.object.pose.bones[ctrl]
            
            if first_bone:
                first_bone = False
                target_bone = ctrl
                continue
            
            constraint = ctrl_pose_bone.constraints.new(type="COPY_ROTATION")
            constraint.name = "TGR Rotation Chain"
            constraint.target = context.object
            constraint.subtarget = target_bone
            constraint.mix_mode = 'AFTER'
            constraint.target_space = 'LOCAL'
            constraint.owner_space = 'LOCAL'
            
            target_bone = ctrl
        
        
        return {"FINISHED"}


class TGR_OT_CreateStretchToChain(bpy.types.Operator):
    """
    Create a stretch to constraint chain for the selected bones.
    The active bone will be the parent of the chain.
    """
    bl_idname = "tgr.create_stretch_to_chain"
    bl_label = "Create Stretch To Chain"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        return is_armature and is_pose_mode
    
    def execute(self, context):
        tgr_props = context.object.tgr_props
        # Must not stretch DEF- bones
        selected_bones = [bone for bone in context.selected_pose_bones]
        for bone in selected_bones:
            if bone.name.startswith(tgr_props.def_prefix):
                self.report({'ERROR'}, 'Cannot stretch DEF- bones')
                return {'CANCELLED'}
        
        previous_bone = None
        for i, bone in enumerate(selected_bones):
            # Enter edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            edit_bone = context.object.data.edit_bones[bone.name]
            last_bone = i == len(selected_bones) - 1
            
            # Add a new non-deform bone
            bpy.ops.tgr.add_non_deform_bone()
            # Move the new bone to the first bone's head
            new_bone = context.selected_bones[0]
            new_bone.name = f'CTRL-TWEAK-{"-".join(bone.name.split("-")[1:])}'
            new_bone.head = bone.head
            new_bone.tail = new_bone.head + Vector((0, bone.length / 3, 0))
            # Set the new bone as the parent of the first bone
            edit_bone.parent = new_bone
            
            if last_bone:
                # Add a new non-deform bone
                bpy.ops.tgr.add_non_deform_bone()
                # Move the new bone to the first bone's head
                new_bone = context.selected_bones[0]
                new_bone.name = f'CTRL-TWEAK-END-{"-".join(bone.name.split("-")[1:])}'
                new_bone.head = bone.tail
                new_bone.tail = new_bone.head + Vector((0, bone.length / 3, 0))
            
            if previous_bone is not None:
                # Go back to pose mode
                bpy.ops.object.mode_set(mode='POSE')
                # Add the stretch to constraint to the current bone with the new bone as the target
                tgt_name = new_bone.name
                if last_bone:
                    # Add the constraints to the current bone as well
                    constraint = bone.constraints.new('STRETCH_TO')
                    constraint.target = context.object
                    constraint.subtarget = tgt_name
                    constraint.name = "TGR-STRETCH"
                    tgt_name = tgt_name.replace("END-", "")
                
                constraint = previous_bone.constraints.new('STRETCH_TO')
                constraint.target = context.object
                constraint.subtarget = tgt_name
                constraint.name = "TGR-STRETCH"
                

            previous_bone = bone
        
        # Finish the operation 
        return {'FINISHED'}
    
    
class TGR_OT_CopyTransformsToChain(bpy.types.Operator):
    """
    Create a copy transforms chain considering two given names.
    """
    bl_idname = "tgr.copy_transforms_to_chain"
    bl_label = "Create Stretch To Chain"
    bl_options = {'REGISTER', 'UNDO'}
    
    from_prefix: bpy.props.StringProperty(name="From Prefix")
    to_prefix: bpy.props.StringProperty(name="To Prefix")
    constraint_name: bpy.props.StringProperty(name="Constraint Name")
    
    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        return is_armature and is_pose_mode
    
    def execute(self, context):
        for pose_bone in context.selected_pose_bones:
            constraint = pose_bone.constraints.new('COPY_TRANSFORMS')
            constraint.target = context.active_object
            
            from_bone_name = pose_bone.name.replace(self.to_prefix, self.from_prefix)
            try:
                _ = context.active_object.pose.bones[from_bone_name]
            except KeyError:
                self.report({'ERROR'}, f'{from_bone_name} not found!')
                return {'CANCELLED'}
            
            constraint.subtarget = from_bone_name
            if not self.constraint_name == '':
                constraint.name = self.constraint_name

        return {'FINISHED'}