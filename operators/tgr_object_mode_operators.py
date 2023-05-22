import bpy


class TGR_OT_AddTGRArmature(bpy.types.Operator):
    """
    Add a TGR Armature to the scene.
    """
    bl_idname = "tgr.add_tgr_armature"
    bl_label = "TGR Armature"
    bl_options = {'REGISTER', 'UNDO'}
    
    # axes_position: bpy.props.FloatProperty(name="Axes Position", default=1.0, min=0.0, max=1.0)

    @classmethod
    def poll(cls, context):
        is_object_mode = context.mode == 'OBJECT'
        return is_object_mode

    def execute(self, context):
        # Set up the root bone
        bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.tgr.align_bone_to_world()
        root = context.selected_editable_bones[0]
        root.name = 'ROOT'
        root.use_deform = False
        
        # Set up the tgr armature
        tgr_props = context.object.tgr_props
        tgr_props.armature = context.active_object
        
        # Set Armature view mode
        bpy.context.object.display_type = 'WIRE'
        bpy.context.object.show_in_front = True
        bpy.context.object.data.show_names = True
        bpy.context.object.data.show_axes = True
        
        # Update the armature
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'}
