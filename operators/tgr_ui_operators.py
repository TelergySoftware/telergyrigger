import bpy
from bpy.types import Node
from dataclasses import dataclass, field
from ..node_tree_compilation import run_tgr_ui_generator


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
class TGR_Panel:
    """Data structure to hold panel information"""
    name: str
    category: str
    layout_inputs: list[Node] = field(default_factory=list)


@dataclass
class TGR_Row:
    """Data structure to hold row information"""
    aligned: bool = False
    height: int = 0
    parent: object = None
    layout_inputs: list[Node] = field(default_factory=list)


@dataclass
class TGR_Column:
    """Data structure to hold column information"""
    aligned: bool = False
    width: int = 0
    parent: object = None
    layout_inputs: list[Node] = field(default_factory=list)

@dataclass
class TGR_BoneCollection:
    """Data structure to hold bone collection information"""
    name: str
    use_visibility: bool = True
    use_solo: bool = False


class TGR_OT_GenerateUI(bpy.types.Operator):
    """Generate the UI python script"""

    bl_idname = "tgr.generate_ui"
    bl_label = "Generate UI"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.active_object is None or context.space_data is None:
            return False
        return context.active_object.type == 'ARMATURE'

    def execute(self, context):
        success = run_tgr_ui_generator(armature=context.active_object)
        if success:
            self.report({'INFO'}, "UI script compiled and active.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to generate UI script.")
            return {'CANCELLED'}


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
