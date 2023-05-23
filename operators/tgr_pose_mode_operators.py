import bpy
import math
from mathutils import Vector
from ..utils import bone_layers_by_number, get_addon_name


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
        preferences = context.preferences.addons[get_addon_name()].preferences
        def_prefix = preferences.def_prefix + preferences.separator
        tgt_prefix = preferences.tgt_prefix + preferences.separator
        ctrl_prefix = preferences.ctrl_prefix + preferences.separator
        # Check if there is any selected bones
        if len(context.selected_pose_bones) > 0:
            bones_to_bind = context.selected_pose_bones
        else:
            bones_to_bind = context.object.pose.bones
        # Check if there are TGT bones for each DEF bone
        for bone in bones_to_bind:
            if bone.name.startswith(tgt_prefix) or bone.name.startswith(ctrl_prefix):
                # Check if there's a DEF bone with the same name
                if (bone.name.replace(tgt_prefix, def_prefix) not in context.object.pose.bones) and (
                        bone.name.replace(ctrl_prefix, def_prefix) not in context.object.pose.bones):
                    self.report({"ERROR"}, "No TGT or CTRL bone for DEF bone: " + bone.name)
                    return {"CANCELLED"}

        # Bind the TGT bones to the DEF bones
        for bone in bones_to_bind:
            if bone.name.startswith(tgt_prefix) or bone.name.startswith(def_prefix):
                # Get the DEF bone
                try:
                    def_bone = context.object.pose.bones[bone.name.replace(tgt_prefix, def_prefix)]
                except KeyError:
                    def_bone = context.object.pose.bones[bone.name.replace(ctrl_prefix, def_prefix)]
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
    Unbinds the TGT bones from the DEF bones
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
        preferences = context.preferences.addons[get_addon_name()].preferences
        def_prefix = preferences.def_prefix + preferences.separator
        # Unbind the TGT bones from the DEF bones
        for bone in context.object.pose.bones:
            if bone.name.startswith(def_prefix):
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
        preferences = context.preferences.addons[get_addon_name()].preferences
        tgt_prefix = preferences.tgt_prefix + preferences.separator
        mch_prefix = preferences.mch_prefix + preferences.separator
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
            if bone.name.startswith(tgt_prefix):
                bone.name = bone.name.replace(tgt_prefix, f'{mch_prefix}INT{preferences.separator}')
                bone.name = bone.name.replace('.001', '')
                mch_int_bone_names.append(bone.name)

        # Duplicate the selected bones and resize them to 50%
        bpy.ops.armature.duplicate()
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))

        # Replace the MCH-INT- prefix for MCH- prefix and remove the .001 suffix
        mch_bones_names = []
        for bone in context.selected_bones:
            if bone.name.startswith(f'{mch_prefix}INT{preferences.separator}'):
                bone.name = bone.name.replace(f'{mch_prefix}INT{preferences.separator}', mch_prefix)
                bone.name = bone.name.replace('.001', '')
                mch_bones_names.append(bone.name)

        # Change the TGT- prefix for CTRL- prefix and parent them to the MCH-INT- bones
        for bone in selected_bones:
            bone.use_connect = False
            bone.parent = context.object.data.edit_bones[
                bone.name.replace(tgt_prefix, f'{mch_prefix}INT{preferences.separator}')]

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
            constraint.subtarget = pose_bone.name.replace(f'{mch_prefix}INT{preferences.separator}', mch_prefix)
            constraint.name = 'ISOLATE ROTATION LOC'
            # Add copy rotation constraint
            constraint = pose_bone.constraints.new('COPY_ROTATION')
            constraint.target = context.object
            constraint.subtarget = pose_bone.name.replace(f'{mch_prefix}INT{preferences.separator}', mch_prefix)
            constraint.name = 'ISOLATE ROTATION ROT'
            constraint.influence = 0.0
            # Send the MCH-INT- and MCH- bones to the layer 2
            pose_bone.bone.layers = [i == 2 for i in range(len(pose_bone.bone.layers))]
            mch_bone = context.object.pose.bones[
                bone_name.replace(f'{mch_prefix}INT{preferences.separator}', mch_prefix)]
            mch_bone.bone.layers = [i == 2 for i in range(len(mch_bone.bone.layers))]

        return {'FINISHED'}


class TGR_OT_CreateIkFkSwitchChain(bpy.types.Operator):
    """
    Create an IK/FK switch chain.
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
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout


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
        preferences = context.preferences.addons[get_addon_name()].preferences
        ctrl_prefix = preferences.ctrl_prefix + preferences.separator
        tgr_props = context.object.tgr_props
        # Must not rotate DEF bones
        for bone in context.selected_pose_bones:
            if bone.name.startswith(tgr_props.def_prefix):
                self.report({'ERROR'}, 'Cannot use rotation chains on DEF- bones')
                return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        for bone in context.selected_bones:
            bone.use_connect = False
            split_name = bone.name.split(preferences.separator)
            bone_name = ctrl_prefix

            for name_part in split_name[1:]:
                bone_name += f"{name_part}"

            bone.name = bone_name
        ctrl_bone_names = [bone.name for bone in context.selected_bones]

        bpy.ops.armature.duplicate()
        for bone in context.selected_bones:
            bone.name = bone.name.replace(ctrl_prefix, f"{ctrl_prefix}TWEAK{preferences.separator}")
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
    The active bone will be the parent of the chain
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
        # Finish the operation 
        return {'FINISHED'}


class TGR_OT_CopyTransformsToChain(bpy.types.Operator):
    """
    Create a copy transforms chain considering two given names
    """
    bl_idname = "tgr.copy_transforms_to_chain"
    bl_label = "Copy Transforms To Chain"
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

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="From and To Prefixes:")

        row = layout.row()
        row.prop(self, "from_prefix")

        row = layout.row()
        row.prop(self, "to_prefix")

        row = layout.row()
        row.label(text="Constraint Name")

        row = layout.row()
        row.prop(self, "constraint_name")


class TGR_OT_CreateIKPoleTarget(bpy.types.Operator):
    """
    Create the IK Pole target by selecting the IK chain first and last bone, and choosing a bone to place the Pole bone.
    """
    bl_idname = "tgr.create_ik_pole_target"
    bl_label = "Create IK Pole target "
    bl_options = {'REGISTER', 'UNDO'}

    first_bone_name: bpy.props.StringProperty(name="First Bone", description="First bone of the IK chain")
    last_bone_name: bpy.props.StringProperty(name="To Prefix", description="Last bone of the IK chain")
    placement_bone_name: bpy.props.StringProperty(name="Constraint Name",
                                                  description="Bone used to get the pole placement")
    chain_name: bpy.props.StringProperty(name="Chain Name", description="Name of this IK chain")
    pole_distance: bpy.props.FloatVectorProperty(name="Pole Distance",
                                                 description="Distance from the pole bole to the placement bone",
                                                 default=[0.0, -0.5, 0.0])
    pole_angle: bpy.props.FloatProperty(name="Pole Angle", min=-180, max=180)
    adjust_pole: bpy.props.BoolProperty(name="Adjust Pole")
    offset_pole: bpy.props.FloatVectorProperty(name="Offset Pole Position",
                                               description="Offset the pole position to the place of your liking")

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        preferences = context.preferences.addons[get_addon_name()].preferences
        mch_prefix = preferences.mch_prefix + preferences.separator
        ctrl_prefix = preferences.ctrl_prefix + preferences.separator
        armature = context.active_object
        tgr_props = context.object.tgr_props
        mch_bones = []
        old_cursor_location = context.scene.cursor.location

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        # Deselect all bones
        bpy.ops.armature.select_all(action="DESELECT")
        # Duplicate de first bone of the chain to be used as the stretch helper
        first_bone = armature.data.edit_bones[self.first_bone_name]

        first_bone.select = True
        first_bone.select_head = True
        first_bone.select_tail = True

        bpy.ops.armature.duplicate()

        # Set the duplicated bone tail to the same location as the last bone tail
        stretch_helper = context.selected_editable_bones[0]
        stretch_helper.name = f"{mch_prefix}{self.chain_name}{preferences.separator}STRETCH{preferences.separator}HELPER"
        last_bone = armature.data.edit_bones[self.last_bone_name]

        stretch_helper.tail = last_bone.tail
        # Add it to the mch_bones list
        mch_bones.append(stretch_helper)

        # Get the number of bones in the chain and the placement bone index
        placement_bone = armature.data.edit_bones[self.placement_bone_name]
        placement_bone_index = 0
        num_of_bones = 1
        first_bone_children = first_bone.children_recursive
        for bone in first_bone_children:
            num_of_bones += 1
            if bone.name == placement_bone.name:
                placement_bone_index = num_of_bones
            if bone.name == last_bone.name:
                break

        # Duplicate the stretch bone and scale it to be (placement_bone_index - 1) / num_of_bones
        bpy.ops.armature.duplicate()
        int_bone = context.selected_editable_bones[0]
        int_bone.name = f"{mch_prefix}{self.chain_name}{preferences.separator}INT{preferences.separator}HELPER"
        int_bone.length *= (placement_bone_index - 1) / num_of_bones

        # Offset int bone to be placed on the current tail position
        bpy.ops.transform.translate(value=[0, int_bone.length, 0], orient_type="NORMAL")
        # Orient it with the world
        bpy.ops.tgr.align_bone_to_world()
        # Clear all parenting
        int_bone.parent = None
        # Add it to the mch bones list
        mch_bones.append(int_bone)

        # Add the pole target bone to the placement bone head
        context.scene.cursor.location = placement_bone.head
        bpy.ops.tgr.add_non_deform_bone()
        pole_bone = context.selected_editable_bones[0]
        pole_bone.length = int_bone.length / 2

        # Set the distance of the pole from the placement bone
        pole_distance = Vector(self.pole_distance[:3])
        pole_bone.head += pole_distance
        pole_bone.tail += pole_distance
        # Set the parent to be the int bone
        pole_bone.parent = int_bone
        # Rename it accordingly
        pole_bone.name = f"{ctrl_prefix}{self.chain_name}{preferences.separator}POLE{preferences.separator}TGT"

        # Remove deform from mch bones
        for layer in armature.tgr_layer_collection:
            if layer.ui_name == "MCH":
                mch_layer_index = layer.index
                break
        else:
            self.report({'ERROR'}, 'MCH layer not found')
            return {'CANCELLED'}

        for bone in mch_bones:
            bone.use_deform = False
            # Send mch bones to the appropriated layer
            bone.layers = bone_layers_by_number(mch_layer_index)

        # Store bones names to avoid key not found
        stretch_helper_name = stretch_helper.name
        pole_bone_name = pole_bone.name
        int_bone_name = int_bone.name

        # Return to pose mode
        bpy.ops.object.mode_set(mode="POSE")

        # Add stretch to constraint to the stretch helper with the last bone tail as the target
        stretch_helper = armature.pose.bones[stretch_helper_name]
        last_bone = armature.pose.bones[self.last_bone_name]

        for constraint in last_bone.constraints:
            if constraint.type == "IK":
                ik_constraint = constraint
                break
        else:
            self.report({'ERROR'}, 'IK constraint not found')
            return {'CANCELLED'}

        stretch_constraint = stretch_helper.constraints.new(type="STRETCH_TO")
        stretch_constraint.target = armature
        stretch_constraint.subtarget = ik_constraint.subtarget

        # Add copy location to the int bone with the stretch helper as the target
        int_bone = armature.pose.bones[int_bone_name]

        copy_loc_constraint = int_bone.constraints.new(type="COPY_LOCATION")
        copy_loc_constraint.target = armature
        copy_loc_constraint.subtarget = stretch_helper.name
        copy_loc_constraint.head_tail = (placement_bone_index - 1) / num_of_bones

        # Add copy rotation and copy scale to the int bone with the root as the target
        copy_rot_constraint = int_bone.constraints.new(type="COPY_ROTATION")
        copy_rot_constraint.target = armature
        copy_rot_constraint.subtarget = tgr_props.root_bone

        copy_scale_constraint = int_bone.constraints.new(type="COPY_SCALE")
        copy_scale_constraint.target = armature
        copy_scale_constraint.subtarget = tgr_props.root_bone

        # Add pole bone as the pole target of the ik chain
        pole_bone = armature.pose.bones[pole_bone_name]

        ik_constraint.pole_target = armature
        ik_constraint.pole_subtarget = pole_bone.name
        ik_constraint.pole_angle = math.radians(self.pole_angle)

        context.scene.cursor.location = old_cursor_location

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        armature = context.active_object
        layout = self.layout

        row = layout.row()
        row.prop(self, "chain_name")

        row = layout.row()
        row.label(text="Bones Info:")

        row = layout.row()
        row.prop_search(self, "first_bone_name", armature.data, "bones", text="First Bone", icon='BONE_DATA')

        row = layout.row()
        row.prop_search(self, "last_bone_name", armature.data, "bones", text="Last Bone", icon='BONE_DATA')

        row = layout.row()
        row.prop_search(self, "placement_bone_name", armature.data, "bones", text="Placement Bone", icon='BONE_DATA')

        row = layout.row()
        row.label(text="Pole Target Settings:")

        row = layout.row()
        row.prop(self, "pole_distance")

        row = layout.row()
        row.prop(self, "pole_angle", text="Pole Angle")
