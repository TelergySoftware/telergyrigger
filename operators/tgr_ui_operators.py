import bpy
from dataclasses import dataclass, field


class TGR_OT_UIPicker(bpy.types.Operator):
    """Hover over any UI area to detect the area and region. Click to select it"""

    bl_idname = "tgr.ui_picker"
    bl_label = "UI Picker"
    bl_options = {'REGISTER', 'UNDO'}
    
    def modal(self, context, event):
        # Cancel on right click or escape
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_set('DEFAULT')
            context.workspace.status_text_set(None)
            return {'CANCELLED'}
        
        # Logic to detect UI area under mouse cursor
        found_area = None
        found_region = None
        
        for area in context.window.screen.areas:
            for region in area.regions:
                if (region.x <= event.mouse_x <= region.x + region.width and
                    region.y <= event.mouse_y <= region.y + region.height):
                    found_area = area
                    found_region = region
                    break
            if found_area:
                break
        
        # Update status text while hovering
        if event.type == 'MOUSEMOVE':
            if found_area and found_region:
                context.workspace.status_text_set(f"Area: {found_area.type}, Region: {found_region.type}")
            else:
                context.workspace.status_text_set("Hover over a UI area...")
        
        # Confirm selection on left click
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if found_area and found_region:
                self.view_node.space_type = found_area.type
                self.view_node.region_type = found_region.type
                # Redraw the node editor to reflect changes
                for area in context.window.screen.areas:
                    if area.type == 'NODE_EDITOR':
                        area.tag_redraw()
                self.report({'INFO'}, f"Selected Area: {found_area.type}, Region: {found_region.type}")
            else:
                self.report({'WARNING'}, "No UI area detected under cursor")
            context.window.cursor_set('DEFAULT')
            context.workspace.status_text_set(None)
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        self.view_node = context.active_node
        context.window.cursor_set('EYEDROPPER')
        context.window_manager.modal_handler_add(self)
        context.workspace.status_text_set("Hover over a UI area and click to select. Right click or Esc to cancel.")
        return {'RUNNING_MODAL'}       



@dataclass
class Panel:
    """Data class to represent a UI panel"""
    name: str
    space_type: str
    region_type: str
    category: str = ""
    parent_id: str = ""
    draw_code: list = field(default_factory=list)
    code_lines: list = field(default_factory=list)
    indent_level: int = 0
    
    def _add_line(self, line):
        """Add a line of code with proper indentation"""
        indent = "    " * self.indent_level
        self.code_lines.append(f"{indent}{line}")
    
    @property
    def class_name(self):
        """Generate a valid class name based on the panel name"""
        return f"TGR_PT_{self.name.replace(' ', '_')}"

@dataclass
class PropertyGroup:
    """Data class to represent a property group"""
    name: str
    properties: list = field(default_factory=list)
    code_lines: list = field(default_factory=list)
    indent_level: int = 0
    
    def _add_line(self, line):
        """Add a line of code with proper indentation"""
        indent = "    " * self.indent_level
        self.code_lines.append(f"{indent}{line}")
    
    @property
    def class_name(self):
        """Generate a valid class name based on the property group name"""
        return f"TGR_PG_{self.name.replace(' ', '_')}"


class NodeTreeCompiler:
    """Compiler for TGR node trees to generate UI code"""
    
    def __init__(self, node_tree, armature):
        self.node_tree = node_tree
        self.armature = armature
        self.panels = {}
        self.property_groups = {}
        self.output_lines = []
        self.indent_level = 0
        self.visited_nodes = set()
        self.compilers = {
            "TGR_ViewNode": self._compile_view_node,
            "TGR_PanelNode": self._compile_panel_node,}
    
    def compile(self):
        """Main compilation method"""
        self.output_lines = [
            "# ===== GENERATED UI SCRIPT BY TELERGY RIGGER =====",
            "import bpy",
            "",
            "",
            "# ===== RIG CONSTANTS =====",
            f"ARMATURE_NAME = '{self.armature.name}'",
            "",
            "# ===== UI CLASSES =====",
            "",
        ]
        
        # Find output nodes (nodes with no outputs connected)
        output_nodes = self._find_output_nodes()
        
        # Find 3D View nodes to generate panels
        view_nodes = [node for node in output_nodes if node.bl_idname == "TGR_ViewNode"]
        properties_nodes = [node for node in output_nodes if node.bl_idname == "TGR_PropertiesNode"]
        
        if view_nodes:
            for view_node in view_nodes:
                self._compile_view_node(view_node)
        else:
            # If no view nodes found, raise an error
            raise RuntimeError("No TGR_ViewNode found in the node tree.")
        
        if properties_nodes:
            for prop_node in properties_nodes:
                self._compile_properties_node(prop_node)
        
        # Add registration code
        self._add_registration_code()
        
        return "\n".join(self.output_lines)
    
    def _add_line(self, line):
        """Add a line to the output with proper indentation"""
        indent = "    " * self.indent_level
        self.output_lines.append(f"{indent}{line}")
    
    def _find_output_nodes(self):
        """Find nodes that have no output connections"""
        output_nodes = []
        for node in self.node_tree.nodes:
            has_output_connection = False
            for output in node.outputs:
                if output.links:
                    has_output_connection = True
                    break
            if not has_output_connection:
                output_nodes.append(node)
        return output_nodes
    
    def _compile_view_node(self, node):
        """Compile a View Node into a Blender panel class"""
        for ui_socket in node.inputs:
            if ui_socket.type == 'CUSTOM' and ui_socket.is_linked:
                for link in ui_socket.links:
                    panel_node = link.from_node
                    self.compilers[panel_node.bl_idname](panel_node, node)
    
    def _compile_panel_node(self, panel_node, node):
        """Compile a Panel Node into a Blender panel class"""
        panel_name = ""
        if panel_node.inputs['Name'].is_linked:
            from_node = panel_node.inputs['Name'].links[0].from_node
            if from_node.bl_idname == "TGR_StringNode":
                panel_name = from_node.value
        else:
            panel_name = panel_node.inputs['Name'].default_value
            

        class_name = f"TGR_PT_{panel_name.replace(' ', '_')}"
        self.output_lines.append(f"class {class_name}(bpy.types.Panel):")
        self.indent_level += 1
        self._add_line(f'bl_idname = "{class_name}"')
        self._add_line(f'bl_label = "{panel_name}"')
        self._add_line(f'bl_space_type = "{node.space_type}"')
        self._add_line(f'bl_region_type = "{node.region_type}"')
        self._add_line(f'bl_category = "{node.inputs["Category"].default_value}"')
        if node.bl_idname == "TGR_PanelNode":
            parent_id = ""
            if node.inputs['Name'].is_linked:
                from_node = node.inputs['Name'].links[0].from_node
            if from_node.bl_idname == "TGR_StringNode":
                parent_id = from_node.value
            else:
                parent_id = node.inputs['Name'].default_value
            self._add_line(f"bl_parent_id = '{parent_id}'")
        
        self._add_line("")
        self._add_line("def draw(self, context):")
        self.indent_level += 1
        self._add_line("layout = self.layout")
        for ui_socket in panel_node.inputs:
            if ui_socket.type == 'CUSTOM' and ui_socket.is_linked:
                for link in ui_socket.links:
                    from_node = link.from_node
                    self.compilers[from_node.bl_idname](from_node, node)
        self.indent_level -= 2
        self._add_line("")
        self._add_line("")

    def _add_registration_code(self):
        """Add registration code for all generated classes"""
        self.output_lines.append("")
        self.output_lines.append("classes = [")
        for line in self.output_lines:
            if line.startswith("class TGR_PT_") or line.startswith("class TGR_OT_"):
                class_name = line.split()[1].split("(")[0]
                self.output_lines.append(f"    {class_name},")
        self.output_lines.append("]")
        self.output_lines.append("")
        self.output_lines.append("def register():")
        self.indent_level += 1
        self._add_line("for cls in classes:")
        self.indent_level += 1
        self._add_line("bpy.utils.register_class(cls)")
        self.indent_level -= 2
        self.output_lines.append("")
        self.output_lines.append("def unregister():")
        self.indent_level += 1
        self._add_line("for cls in reversed(classes):")
        self.indent_level += 1
        self._add_line("bpy.utils.unregister_class(cls)")
        self.indent_level -= 2
        self.output_lines.append("")
        self.output_lines.append("if __name__ == '__main__':")
        self.indent_level += 1
        self._add_line("register()")
        self.indent_level -= 1
        

class TGR_OT_GenerateUI(bpy.types.Operator):
    """Generate the UI python script"""

    bl_idname = "tgr.generate_ui"
    bl_label = "Generate UI"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.active_object is None or context.space_data is None:
            return False
        is_armature = context.active_object.type == 'ARMATURE'
        is_node_tree_active = context.space_data.tree_type == 'TGR_RigNodeTree'
        return is_armature and is_node_tree_active

    def execute(self, context):
        node_tree = context.space_data.node_tree
        armature = context.active_object
        
        if not node_tree:
            self.report({'ERROR'}, "No active node tree found")
            return {"CANCELLED"}
        
        print("Compiling UI script:", node_tree.name, "for armature:", armature.name)
        
        # Create or overwrite the text block for the UI script
        script_name = f"{node_tree.name.replace(' ', '_').lower()}.py"
        if script_name in bpy.data.texts:
            text_block = bpy.data.texts[script_name]
            text_block.clear()
        else:
            text_block = bpy.data.texts.new(script_name)
        
        # Compile the node tree
        try:
            compiler = NodeTreeCompiler(node_tree, armature)
            generated_code = compiler.compile()
        except RuntimeError:
            self.report({'ERROR'}, "No Area Node found in the node tree.")
            return {"CANCELLED"}
        
        # Write the generated code to the text block
        text_block.write(generated_code)
        
        # Execute the generated script
        try:
            exec(text_block.as_string())
            self.report({'INFO'}, f"UI script '{script_name}' compiled and executed successfully.")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing compiled UI script: {e}")
        
        return {"FINISHED"}


class TGR_OT_CreateExecutable(bpy.types.Operator):
    """Create a new operator entry and execute function on the tgr_operators.py text block"""
    
    bl_idname = "tgr.create_executable"
    bl_label = "Create Executable"
    bl_options = {'REGISTER', 'UNDO'}
    
    name: bpy.props.StringProperty(name="Operator Name", default="")
    exec_type: bpy.props.StringProperty(name="Executable Type", default="OPERATOR")

    def execute(self, context):
        if not self.name.strip():
            self.report({'ERROR'}, "Operator name cannot be empty")
            return {'CANCELLED'}
        
        if not self.exec_type in ["OPERATOR", "CALLBACK"]:
            self.report({'ERROR'}, "Executable type must be either 'OPERATOR' or 'CALLBACK'")
            return {'CANCELLED'}
        
        text_block_name = "tgr_executables.py"
        if text_block_name not in bpy.data.texts:
            text_block = bpy.data.texts.new(text_block_name)
            text_block.write("# This is the tgr_executables.py text block. It contains executable definitions for Telergy Rigger.\n\n")
        else:
            text_block = bpy.data.texts[text_block_name]

        # Generate a unique executable name
        executable_name = ""
        if self.exec_type == "OPERATOR":
            executable_name = f"TGR_OT_{self.name.capitalize().replace(' ', '_')}"
        elif self.exec_type == "CALLBACK":
            executable_name = f"tgr_{self.name.lower().replace(' ', '_')}"
            
        if f"{self.exec_type}: {self.name}" in text_block.as_string():
            self.report({'ERROR'}, f"An executable with the same name '{self.name}' and type '{self.exec_type}' already exists.")
            return {'CANCELLED'}
        
        # Create the operator execute function template
        executable_code = f"""
# {self.exec_type}: {self.name}
def {"execute_" + executable_name if self.exec_type == "OPERATOR" else executable_name}({"self, context" if self.exec_type == "OPERATOR" else ""}):
    # TODO: Implement the functionality for this {self.exec_type.lower()}
    return {{'FINISHED'}}\n
"""
     
        text_block.write(executable_code)
        
        # Find a text editor area to display the new executable code
        for area in context.window.screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.spaces.active.text = text_block
                break
        
        return {'FINISHED'}
