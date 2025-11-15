import bpy


class TGR_OT_GenerateUI(bpy.types.Operator):
    """
    Generate the UI python script
    """

    bl_idname = "tgr.generate_ui"
    bl_label = "Generate UI"
    bl_options = {'REGISTER', 'UNDO'}

    panel_name: bpy.props.StringProperty(
        name="Panel Name",
        description="Name that will show on the N panel tab",
        default="Rig UI"
    )
    
    file_name: bpy.props.StringProperty(
        name="File Name",
        description="Name of the generated UI python script",
        default="TGR_RigUI.py"
    )

    @classmethod
    def poll(cls, context):
        is_armature = context.active_object.type == 'ARMATURE'
        is_pose_mode = context.active_object.mode == 'POSE'
        is_edit_mode = context.active_object.mode == 'EDIT'
        return is_armature and (is_pose_mode or is_edit_mode)

    def execute(self, context):
        components = context.active_object.tgr_ui_components
        self.file_name = self.file_name if self.file_name.endswith(".py") else self.file_name + ".py"
        try:
            text = bpy.data.texts[self.file_name]
            text.clear()
        except KeyError:
            text = bpy.data.texts.new(self.file_name)

        # Header comments
        text.write("# ----- RIG UI Created by TelergyRigger -----\n")
        # Imports
        text.write("import bpy\n")
        text.write("\n\n")
        # Properties class
        text.write(
            "class TGR_RIG_Properties(bpy.types.PropertyGroup):\n"
            "\tpass\n"
        )
        text.write("\n\n")
        # Rig layers panel
        text.write(
            "class TGR_RIG_PT_Layers_Panel(bpy.types.Panel):\n"
            "\tbl_label = 'Bone Layers'\n"
            "\tbl_idname = 'TGR_RIG_PT_Layers_Panel'\n"
            "\tbl_space_type = 'VIEW_3D'\n"
            "\tbl_region_type = 'UI'\n"
            f"\tbl_category = '{self.panel_name}'\n"
            "\n"
            "\tdef draw(self, context):\n"
            "\t\tarmature = context.active_object.data\n"
            "\t\tlayout = self.layout\n"
            "\t\t# Toggle bone layer visibility\n"
            "\n"
        )
        current_line = -1
        for component in components:
            if component.line > current_line:
                text.write(
                    "\t\trow = layout.row(align=True)\n"
                )
                current_line = component.line
            if component.component_type == "LAYER":
                text.write(
                    f"\t\trow.prop(armature, 'layers', index={component.layer_index},"
                    f" toggle=True, text='{component.value}')\n"
                )
            elif component.component_type == "LABEL":
                text.write(
                    f"\t\trow.label(text='{component.value}')\n"
                )
        text.write("\n\n")
        # Rig properties panel
        text.write(
            "class TGR_RIG_PT_Properties_Panel(bpy.types.Panel):\n"
            "\tbl_label = 'Rig Properties'\n"
            "\tbl_idname = 'TGR_RIG_PT_Properties_Panel'\n"
            "\tbl_space_type = 'VIEW_3D'\n"
            "\tbl_region_type = 'UI'\n"
            f"\tbl_category = '{self.panel_name}'\n"
            "\n"
            "\tdef draw(self, context):\n"
            "\t\tlayout = self.layout\n"
            "\t\tarmature = context.active_object\n"
            "\t\tif context.mode == 'EDIT':\n"
            "\t\t\tbones = armature.edit_bones\n"
            "\t\t\tbone_names = [bone.name for bone in bones]\n"
            "\t\telif context.mode == 'POSE':\n"
            "\t\t\tbones = armature.pose.bones\n"
            "\t\t\tbone_names = [bone.name for bone in bones]\n"
            "\t\telse:\n"
            "\t\t\treturn\n"
            "\n"
            "\t\tfor bone_name in bone_names:\n"
            "\t\t\tbone = bones[bone_name]\n"
            "\t\t\tif len(bone.keys()) == 0:\n"
            "\t\t\t\tcontinue\n"
            "\t\t\tbox = layout.box()\n"
            "\t\t\tbox.label(text=bone_name)\n"
            "\t\t\tfor key in bone.keys():\n"
            "\t\t\t\tbox.prop(bone, f'[\"{key}\"]')\n"
        )
        text.write("\n\n")
        # Register classes and properties
        text.write(
            "def register():\n"
            "\tbpy.utils.register_class(TGR_RIG_PT_Layers_Panel)\n"
            "\tbpy.utils.register_class(TGR_RIG_Properties)\n"
            "\tbpy.utils.register_class(TGR_RIG_PT_Properties_Panel)\n"
            "\n"
            "\tbpy.types.Scene.rig_ui_properties = bpy.props.PointerProperty(type=TGR_RIG_Properties)\n"
            "\n"
            "\tbpy.types.Scene.rig_props = bpy.props.PointerProperty(type=TGR_RIG_Properties)\n"
        )
        text.write("\n\n")
        # Unregister classes and properties
        text.write(
            "def unregister():\n"
            "\tdel bpy.types.Scene.rig_props\n"
            "\n"
            "\tbpy.utils.unregister_class(TGR_RIG_PT_Layers_Panel)\n"
            "\tbpy.utils.unregister_class(TGR_RIG_Properties)\n"
            "\tbpy.utils.unregister_class(TGR_RIG_PT_Properties_Panel)\n"
        )
        text.write("\n\n")
        # Relink drivers
        text.write(
            "def relink_drivers():\n"
            "\t'''Update dependencies of drivers'''\n"
            "\tfor obj in bpy.data.objects:\n"
            "\t\tif obj.animation_data:\n"
            "\t\t\tfor driver in obj.animation_data.drivers:\n"
            "\t\t\t\tdriver.driver.expression = driver.driver.expression\n"
        )
        text.write("\n\n")
        # Main
        text.write(
            "if __name__ == '__main__':\n"
            "\tregister()\n"
            "\trelink_drivers()\n"
        )

        return {"FINISHED"}


class TGR_OT_UI_AddPanel(bpy.types.Operator):
    """ Add a new panel to the Rig UI components list """
    
    bl_idname = "tgr.ui_add_panel"
    bl_label = "Add UI Panel"
    bl_options = {'REGISTER', 'UNDO'}
    
    name: bpy.props.StringProperty(
        name="Panel Name",
        default="New Panel"
    )

    def execute(self, context):
        rig_ui_props = context.object.tgr_rig_ui_props
        rig_ui_props.ui_structure[self.name] = []
        return {'FINISHED'}


class TGR_OT_UI_AddRow(bpy.types.Operator):
    """ Add a new row to the Rig UI components list """
    
    bl_idname = "tgr.ui_add_row"
    bl_label = "Add UI Row"
    bl_options = {'REGISTER', 'UNDO'}
    
    path: bpy.props.StringProperty(
        name="Panel Path",
        default="",
        description="Path to the panel in the collections_panel_structure dict separated by dots"
    )

    def execute(self, context):
        rig_ui_props = context.object.tgr_rig_ui_props
        panel = rig_ui_props.ui_structure
        # Try to add a dictionary with the name ROW:1 under the specified path
        # Don't add if the path is invalid
        try:
            for part in self.path.split('.'):
                panel = panel[part]
            row_index = len([item for item in panel if isinstance(item, dict) and 'ROW' in item])
            panel.append({f'ROW:{row_index}': []})
        except KeyError:
            self.report({'ERROR'}, "Invalid panel path")
            return {'CANCELLED'}
            
        return {'FINISHED'}
    

def add_ui_component(context, component_type, value, path: str) -> bool:
    """ Helper function to add a UI component to the Rig UI structure """
    rig_ui_props = context.object.tgr_rig_ui_props
    panel = rig_ui_props.ui_structure
    # Try to add the component under the specified path
    # Don't add if the path is invalid
    try:
        for part in path.split('.'):
            panel = panel[part]
        panel.append({
            'type': component_type,
            'value': value
        })
    except KeyError:
        print("Invalid panel path")
        return False
        
    return True


class TGR_OT_UI_AddCollection(bpy.types.Operator):
    """ Add a new collection to the Rig UI components list """
    
    bl_idname = "tgr.ui_add_collection"
    bl_label = "Add UI Collection"
    bl_options = {'REGISTER', 'UNDO'}
    
    path: bpy.props.StringProperty(
        name="Panel Path",
        default="",
        description="Path to the panel in the ui_structure dict separated by dots"
    )
    collection_name: bpy.props.StringProperty(
        name="Collection Name",
        default=""
    )
    
    def execute(self, context):
        success = add_ui_component(context, "COLLECTION", self.collection_name, self.path)
        
        return {'FINISHED'} if success else {'CANCELLED'}


class TGR_OT_UI_AddLabel(bpy.types.Operator):
    """ Add a new label to the Rig UI components list """
    
    bl_idname = "tgr.ui_add_label"
    bl_label = "Add UI Label"
    bl_options = {'REGISTER', 'UNDO'}
    
    path: bpy.props.StringProperty(
        name="Panel Path",
        default="",
        description="Path to the panel in the ui_structure dict separated by dots"
    )
    label_text: bpy.props.StringProperty(
        name="Label Text",
        default=""
    )

    def execute(self, context):
        success = add_ui_component(context, "LABEL", self.label_text, self.path)
        
        return {'FINISHED'} if success else {'CANCELLED'}


class TGR_OT_UI_RemoveComponent(bpy.types.Operator):
    """ Remove the component from the Rig UI components list by index """
    
    bl_idname = "tgr.ui_remove_component"
    bl_label = "Remove UI Component"
    bl_options = {'REGISTER', 'UNDO'}
    
    path: bpy.props.StringProperty(
        name="Panel Path",
        default="",
        description="Path to the panel in the ui_structure dict separated by dots"
    )

    def execute(self, context):
        rig_ui_props = context.object.tgr_rig_ui_props
        component = rig_ui_props.ui_structure
        # Try to remove the component under the specified path
        try:
            parts = self.path.split('.')
            for part in parts[:-1]:
                component = component[part]
            del component
        except KeyError:
            self.report({'ERROR'}, "Invalid panel path")
            return {'CANCELLED'}
        
        return {'FINISHED'}

