import bpy


def init_tgr_collections():
    """ Initialize the TGR collections """
    preferences = bpy.context.preferences.addons["telergyrigger"].preferences
    armature = bpy.context.active_object
    collections = armature.data.collections
    # Collection names
    def_prefix = preferences.def_prefix
    org_prefix = preferences.org_prefix
    mch_prefix = preferences.mch_prefix
    
    # Change the name of the default collection to "DEF"
    # and set the locked property to False
    collections[0].name = def_prefix
    collections[0]["locked"] = False
    
    # Create the "ORG", "MCH" and "ROOT" collections
    collections.new(name=org_prefix)["locked"] = False
    collections.new(name=mch_prefix)["locked"] = False
    collections.new(name="ROOT")["locked"] = False
    

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
        
        # Initialize the TGR collections
        init_tgr_collections()
        
        # Move the root bone to the ROOT collection
        bpy.ops.armature.move_to_collection(collection_index=3)
        
        # Set up the tgr armature
        tgr_props = context.object.tgr_props
        tgr_props.armature = context.active_object
        
        # Set Armature view mode
        bpy.context.object.display_type = 'WIRE'
        bpy.context.object.show_in_front = True
        bpy.context.object.data.show_names = True
        bpy.context.object.data.show_axes = True
        
        # Set pivot point to individual origins
        bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
        # Set orientation to normal
        bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'
        
        # Update the armature
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'}
