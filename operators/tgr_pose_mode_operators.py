import bpy
import math
from mathutils import Vector
from ..utils import get_addon_name, get_collection_index


def update_armature(context):
    # Hack to update the armature
    context.object.data.bones.update()
    context.scene.view_layers.update()


class TGR_OT_BindOGR(bpy.types.Operator):
    """
    Binds the OGR bones to the DEF bones.
    """
    bl_idname = "tgr.bind_ogr"
    bl_label = "Bind OGR"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        preferences = context.preferences.addons[get_addon_name()].preferences
        def_prefix = preferences.def_prefix + preferences.separator
        ogr_prefix = preferences.ogr_prefix + preferences.separator
        ctrl_prefix = preferences.ctrl_prefix + preferences.separator
        # Check if there is any selected bones
        if len(context.selected_pose_bones) > 0:
            bones_to_bind = context.selected_pose_bones
        else:
            bones_to_bind = context.object.pose.bones
        # Check if there are OGR bones for each DEF bone
        for bone in bones_to_bind:
            if bone.name.startswith(ogr_prefix) or bone.name.startswith(ctrl_prefix):
                # Check if there's a DEF bone with the same name
                if (bone.name.replace(ogr_prefix, def_prefix) not in context.object.pose.bones) and (
                        bone.name.replace(ctrl_prefix, def_prefix) not in context.object.pose.bones):
                    self.report({"ERROR"}, "No OGR or CTRL bone for DEF bone: " + bone.name)
                    return {"CANCELLED"}

        # Bind the OGR bones to the DEF bones
        failed_bones = []
        for bone in bones_to_bind:
            if bone.name.startswith(ogr_prefix) or bone.name.startswith(def_prefix) or \
                    (bone.name.startswith(ctrl_prefix) and not bone.name.startswith(f"{ctrl_prefix}TWEAK")):
                # Get the DEF bone
                try:
                    def_bone = context.object.pose.bones[bone.name.replace(ogr_prefix, def_prefix)]
                    def_bone = context.object.pose.bones[def_bone.name.replace(ctrl_prefix, def_prefix)]
                except KeyError:
                    failed_bone = bone.name.replace(ogr_prefix, def_prefix)
                    failed_bone = failed_bone.replace(ctrl_prefix, def_prefix)
                    failed_bones.append(failed_bone)
                    continue

                # Bind the OGR bone to the DEF bone
                if 'OGR' in def_bone.constraints:
                    def_bone.constraints['OGR'].subtarget = bone.name
                else:
                    constraint = def_bone.constraints.new('COPY_TRANSFORMS')
                    constraint.target = context.object.tgr_props.armature
                    constraint.subtarget = bone.name
                    constraint.name = 'OGR'
                    # Ensure this constraint is the first one
                    def_bone.constraints.move(len(def_bone.constraints) - 1, 0)

        # Update the view layer
        update_armature(context)
        if len(failed_bones) > 0:
            self.report(
                {"WARNING"},
                "The following bones could not be bound: " + ", ".join(failed_bones)
            )
        return {'FINISHED'}


class TGR_OT_UnbindOGR(bpy.types.Operator):
    """
    Unbinds the OGR bones from the DEF bones
    """
    bl_idname = "tgr.unbind_ogr"
    bl_label = "Unbind OGR"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        preferences = context.preferences.addons[get_addon_name()].preferences
        def_prefix = preferences.def_prefix + preferences.separator
        # Unbind the OGR bones from the DEF bones
        for bone in context.object.pose.bones:
            if bone.name.startswith(def_prefix):
                # Unbind the OGR bone from the DEF bone
                if 'OGR' in bone.constraints:
                    bone.constraints.remove(bone.constraints['OGR'])

        # Update the view layer
        update_armature(context)
        return {'FINISHED'}


class TGR_OT_IsolateBone(bpy.types.Operator):
    """Isolate the selected bones from their parent transforms"""
    
    bl_idname = "tgr.isolate_bone"
    bl_label = "Isolate Bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    isolate_location: bpy.props.BoolProperty(name="Isolate Location", default=False)
    isolate_rotation: bpy.props.BoolProperty(name="Isolate Rotation", default=True)
    isolate_scale: bpy.props.BoolProperty(name="Isolate Scale", default=True)

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        preferences = context.preferences.addons[get_addon_name()].preferences
        ogr_prefix = preferences.ogr_prefix + preferences.separator
        ctrl_prefix = preferences.ctrl_prefix + preferences.separator
        mch_prefix = preferences.mch_prefix + preferences.separator
        collections = context.object.tgr_props.armature.data.collections
        # Check if at least one bone is selected
        if not context.selected_pose_bones:
            self.report({"WARNING"}, "No bones selected")
            return {"CANCELLED"}

        # Change the mode to edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get current mirror mode
        mirror_mode = bpy.context.object.data.use_mirror_x

        # Set the mirror mode to off
        bpy.context.object.data.use_mirror_x = False

        # Duplicate the selected bones and resize them to 50%
        bpy.ops.armature.duplicate()
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))

        bone_pair_names = []
        for bone in context.selected_bones:
            # Get the parent bone
            ctrl_bone = context.object.data.edit_bones[bone.name[:-4]]
            parent = ctrl_bone.parent
            # Replace the OGR or CTRL prefix for MCH-INT- prefix and remove the .001 suffix,
            if bone.name.startswith(ogr_prefix):
                bone.name = bone.name.replace(ogr_prefix, f'{mch_prefix}INT{preferences.separator}')
                bone.name = bone.name.replace('.001', '')
            elif bone.name.startswith(ctrl_prefix):
                bone.name = bone.name.replace(ctrl_prefix, f'{mch_prefix}INT{preferences.separator}')
                bone.name = bone.name.replace('.001', '')
                
            # Add the bone pair to the list
            bone_pair_names.append({'mch': bone.name, 'parent': parent.name})
            
            # Set the parent of the MCH-INT- bone to be the root bone
            bpy.ops.tgr.parent_to_root()
            # Move the MCH-INT- bone to the tail of the parent bone
            distance_vector = bone.head - parent.tail
            bone.head -= distance_vector
            bone.tail -= distance_vector
            # Align the bone to the parent bone
            parent_head_tail_vector = (parent.head - parent.tail).normalized()
            bone.tail = bone.head - parent_head_tail_vector * bone.length
            bone.roll = parent.roll
            # Set the current bone as the partent of the ctrl bone
            ctrl_bone.use_connect = False
            ctrl_bone.parent = bone
            # Send the bone to the MCH collection
            collection_index, _ = get_collection_index(preferences.mch_prefix)
            bpy.ops.armature.move_to_collection(collection_index=collection_index)
        
        # Set mirror mode back to the original state
        bpy.context.object.data.use_mirror_x = mirror_mode
        # Change the mode to pose mode
        bpy.ops.object.mode_set(mode='POSE')
        
        # Add the constraints to the MCH-INT- bones
        for bone_pair in bone_pair_names:
            mch_bone = context.object.pose.bones[bone_pair['mch']]
            parent = context.object.pose.bones[bone_pair['parent']]
            
            # Add the copy location constraint
            constraint = mch_bone.constraints.new('COPY_LOCATION')
            constraint.target = context.object
            constraint.subtarget = parent.name
            constraint.head_tail = 1
            constraint.influence = 1 if not self.isolate_location else 0
            # Add the copy rotation constraint
            constraint = mch_bone.constraints.new('COPY_ROTATION')
            constraint.target = context.object
            constraint.subtarget = parent.name
            constraint.influence = 1 if not self.isolate_rotation else 0
            # Add the copy scale constraint
            constraint = mch_bone.constraints.new('COPY_SCALE')
            constraint.target = context.object
            constraint.subtarget = parent.name
            constraint.influence = 1 if not self.isolate_scale else 0

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
            bone_name = ctrl_prefix[:-1]

            for name_part in split_name[1:]:
                bone_name += f"{preferences.separator}{name_part}"

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
    """Create the IK Pole target by selecting the IK chain first and last bone, and choosing a bone to place the Pole bone"""
    bl_idname = "tgr.create_ik_pole_target"
    bl_label = "Create IK Pole target "
    bl_options = {'REGISTER', 'UNDO'}

    def get_collection_names(self, context):
        return [(collection.name, collection.name, "") for collection in context.object.tgr_props.armature.data.collections]
    
    last_bone_name: bpy.props.StringProperty(name="First Bone", description="Last bone of the IK chain")
    ik_bone_name: bpy.props.StringProperty(name="To Prefix", description="Bone containing the IK constraint")
    placement_bone_name: bpy.props.StringProperty(name="Constraint Name",
                                                  description="Bone used to get the pole placement")
    chain_name: bpy.props.StringProperty(name="Chain Name", description="Name of this IK chain")
    pole_distance: bpy.props.FloatVectorProperty(name="Pole Distance",
                                                 description="Distance from the pole bole to the placement bone",
                                                 default=[0.0, -0.5, 0.0])
    pole_angle: bpy.props.FloatProperty(name="Pole Angle", min=-180, max=180)
    collections: bpy.props.EnumProperty(name="Collections", items=get_collection_names)
    
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
        
        # Check if the active bone colection is visible and store its current state
        active_collection = armature.data.collections.active
        active_collection_state = active_collection.is_visible
        # Set it to visible
        active_collection.is_visible = True

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        # Deselect all bones
        bpy.ops.armature.select_all(action="DESELECT")
        # Duplicate de first bone of the chain to be used as the stretch helper
        first_bone = armature.data.edit_bones[self.last_bone_name]

        first_bone.select = True
        first_bone.select_head = True
        first_bone.select_tail = True

        bpy.ops.armature.duplicate()

        # Set the duplicated bone tail to the same location as the last bone tail
        stretch_helper = context.selected_editable_bones[0]
        stretch_helper.name = f"{mch_prefix}{self.chain_name}{preferences.separator}STRETCH{preferences.separator}HELPER"
        last_bone = armature.data.edit_bones[self.ik_bone_name]

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
        
        # Set MCH bones use_deform to False and send them to the MCH collection
        mch_collection = armature.data.collections[preferences.mch_prefix]
        bpy.ops.armature.select_all(action="DESELECT")
        for bone in mch_bones:
            bone.use_deform = False
            # Send mch bones to the appropriated collection
            bone.select = True
            bone.select_head = True
            bone.select_tail = True
        bpy.ops.armature.move_to_collection(collection=mch_collection.name)
        bpy.ops.armature.select_all(action="DESELECT")
        
        # Store bones names to avoid key not found
        stretch_helper_name = stretch_helper.name
        pole_bone_name = pole_bone.name
        int_bone_name = int_bone.name

        # Return to pose mode
        bpy.ops.object.mode_set(mode="POSE")

        # Add stretch to constraint to the stretch helper with the last bone tail as the target
        stretch_helper = armature.pose.bones[stretch_helper_name]
        last_bone = armature.pose.bones[self.ik_bone_name]

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
        
        # Send the pole bone to the selected collection
        bpy.ops.pose.select_all(action="DESELECT")
        pole_bone.bone.select = True
        bpy.ops.armature.move_to_collection(collection=self.collections)
        bpy.ops.pose.select_all(action="DESELECT")

        context.scene.cursor.location = old_cursor_location
        
        # Set the active collection to its previous state
        active_collection.is_visible = active_collection_state

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
        row.prop_search(self, "last_bone_name", armature.data, "bones", text="Last Bone", icon='BONE_DATA')

        row = layout.row()
        row.prop_search(self, "ik_bone_name", armature.data, "bones", text="IK Bone", icon='BONE_DATA')

        row = layout.row()
        row.prop_search(self, "placement_bone_name", armature.data, "bones", text="Placement Bone", icon='BONE_DATA')

        row = layout.row()
        row.label(text="Pole Target Settings:")

        row = layout.row()
        row.prop(self, "pole_distance")

        row = layout.row()
        row.prop(self, "pole_angle", text="Pole Angle")
        
        row = layout.row()
        row.label(text="Target Collection:")
        
        row = layout.row()
        row.prop(self, "collections")
