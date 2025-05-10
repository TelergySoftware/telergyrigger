import bpy


class TGR_OT_ToggleDeformerConstraint(bpy.types.Operator):
    """Toggle the Deformer bones copy transforms constraint"""
    bl_idname = "tgr.toggle_deformer_constraint"
    bl_label = "Toggle Deformer Constraint"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        # Check if the active object is parented to an armature
        if context.object.parent and context.object.parent.type == 'ARMATURE':
            return True
        if context.object.type == 'ARMATURE':
            return True
        
    def execute(self, context):
        preferences = bpy.context.preferences.addons["bl_ext.user_default.telergyrigger"].preferences
        armature = context.object.parent if not context.object.type == 'ARMATURE' else context.object
        
        for bone in armature.pose.bones:
            if bone.name.startswith(preferences.def_prefix):
                # Check if the bone has a copy transforms constraint
                for constraint in bone.constraints:
                    if constraint.type == 'COPY_TRANSFORMS':
                        # Toggle the constraint
                        constraint.mute = not constraint.mute
                        break
        return {'FINISHED'}
