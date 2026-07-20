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
    

class TGR_OT_ActivateBrush(bpy.types.Operator):
    """Activate a specific weight paint brush"""
    bl_idname = "tgr.activate_brush"
    bl_label = "Activate Brush"
    bl_options = {'REGISTER', 'UNDO'}
    
    brush: bpy.props.EnumProperty(
        name="Brush",
        description="Brush to activate",
        items=[
            ("Average", "Average", "Average brush"),
            ("Paint", "Paint", "Paint brush"),
            ("Blur", "Blur", "Blur brush"),
            ("Smear", "Smear", "Smear brush")
        ],
        default="Average"
    )
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_WEIGHT'
    
    def execute(self, context):
        # Set brush
        match self.brush:
            case "Average":
                bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Average")
            case "Paint":
                bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Paint")
            case "Blur":
                bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Blur")
            case "Smear":
                bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Smear")
            case _:
                self.report({'ERROR'}, "Invalid brush type")
        
        return {'FINISHED'}
    

class TGR_OT_LoadWPBrushes(bpy.types.Operator):
    """Load the default weight paint brushes"""
    bl_idname = "tgr.load_wp_brushes"
    bl_label = "Load Weight Paint Brushes"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_WEIGHT'

    def execute(self, context):
        # Store the current brush to restore it later
        current_brush = context.tool_settings.weight_paint.brush.name if context.tool_settings.weight_paint.brush else None
        # Load the default weight paint brushes
        bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Average")
        bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Paint")
        bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Blur")
        bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Smear")
        # Restore the brush
        bpy.ops.tgr.activate_brush(brush=current_brush)
        return {'FINISHED'}


class TGR_OT_WP_CleanUp(bpy.types.Operator):
    """Clean on all bones and Normalize them. Current active bone is also normalized"""
    bl_idname = "tgr.wp_clean_up"
    bl_label = "Clean Up"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_WEIGHT'
    
    def execute(self, context):
        # Clean all
        bpy.ops.object.vertex_group_clean(group_select_mode='ALL')
        # Normalize All
        bpy.ops.object.vertex_group_normalize_all(group_select_mode='BONE_DEFORM', lock_active=False)

        return {'FINISHED'}