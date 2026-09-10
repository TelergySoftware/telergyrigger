import bpy


def update_armature(context):
    # Hack to update the armature
    context.object.data.bones.update()
    context.scene.view_layers.update()


class TGR_OT_Create_Tweak_FK_Chain(bpy.types.Operator):
    """
    Binds the ORG bones to the DEF bones.
    """
    bl_idname = "tgr.create_tweak_fk_chain"
    bl_label = "Tweak FK Chain"
    bl_options = {'REGISTER', 'UNDO'}

    scale: bpy.props.FloatProperty(name="Scale", default=0.5, description="Scale of the created FK Bones")
    use_stretch: bpy.props.BoolProperty(name="Use Stretch", default=False, description="Use damped track constraint if turned off and stretch to if turned on")

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def execute(self, context):
        armature = context.object.tgr_props.armature
        selected_bone_names = [bone.name for bone in context.selected_pose_bones]
        bpy.ops.tgr.create_tweak_chain(use_stretch=self.use_stretch)
        bpy.ops.pose.select_all(action='DESELECT')
        update_armature(context=context)
        for name in selected_bone_names:
            pbone = armature.pose.bones[name]
            pbone.select = True
        bpy.ops.tgr.fk_from_tweak_chain(scale=self.scale)

        return {'FINISHED'}

