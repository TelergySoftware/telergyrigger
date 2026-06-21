import bpy
from bpy.types import Node

from .tgr_node_tree import TGR_NT_Data, TGR_NT_UI


# ===========================================================
# DATA TREE NODES
# ===========================================================
class TGR_DT_ND_Float(Node):
    bl_idname = "TGR_DT_ND_Float"
    bl_label = "Float"
    bl_icon = 'EVENT_F'
    
    name: bpy.props.StringProperty(name="Name", default="")
    default_value: bpy.props.FloatProperty(name="Value", default=0.0, description="Default value for the float output")
    min_value: bpy.props.FloatProperty(name="Min Value", default=0.0, description="Minimum value for the float output")
    max_value: bpy.props.FloatProperty(name="Max Value", default=1.0, description="Maximum value for the float output")
    
    def init(self, context):
        self.outputs.new('NodeSocketFloat', "Float")
        self.inputs.new('TGR_SKT_Executable', "Update")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "default_value", text="Value")
        layout.prop(self, "min_value", text="Min")
        layout.prop(self, "max_value", text="Max")


class TGR_DT_ND_Integer(Node):
    bl_idname = "TGR_DT_ND_Integer"
    bl_label = "Integer"
    bl_icon = 'EVENT_I'
    
    name: bpy.props.StringProperty(name="Name", default="")
    default_value: bpy.props.IntProperty(name="Value", default=0, description="Default value for the integer output")
    min_value: bpy.props.IntProperty(name="Min Value", default=0, description="Minimum value for the integer output")
    max_value: bpy.props.IntProperty(name="Max Value", default=100, description="Maximum value for the integer output")
    
    def init(self, context):
        self.outputs.new('NodeSocketInt', "Integer")
        self.inputs.new('TGR_SKT_Executable', "Update")
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "default_value", text="Value")
        layout.prop(self, "min_value", text="Min")
        layout.prop(self, "max_value", text="Max")


class TGR_DT_ND_String(Node):
    bl_idname = "TGR_DT_ND_String"
    bl_label = "String"
    bl_icon = 'EVENT_S'
    
    name: bpy.props.StringProperty(name="Name", default="")
    default_value: bpy.props.StringProperty(name="Value", default="", description="Default value for the string output")
    
    def init(self, context):
        self.outputs.new('NodeSocketString', "String")
        self.inputs.new('TGR_SKT_Executable', "Update")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "default_value", text="", placeholder="String Value")


class TGR_DT_ND_Boolean(Node):
    bl_idname = "TGR_DT_ND_Boolean"
    bl_label = "Boolean"
    bl_icon = 'EVENT_B'
    
    name: bpy.props.StringProperty(name="Name", default="")
    default_value: bpy.props.BoolProperty(name="Value", default=False, description="Default value for the boolean output")
    
    def init(self, context):
        self.outputs.new('NodeSocketBool', "Boolean")
        self.inputs.new('TGR_SKT_Executable', "Update")
        
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "default_value", text="Value")


class TGR_DT_ND_Vector(Node):
    bl_idname = "TGR_DT_ND_Vector"
    bl_label = "Vector"
    bl_icon = 'EVENT_V'
    
    name: bpy.props.StringProperty(name="Name", default="")
    default_value: bpy.props.FloatVectorProperty(name="Value", default=(0.0, 0.0, 0.0), description="Default value for the vector output")
    min_value: bpy.props.FloatVectorProperty(name="Min Value", default=(0.0, 0.0, 0.0), description="Minimum value for the vector output")
    max_value: bpy.props.FloatVectorProperty(name="Max Value", default=(1.0, 1.0, 1.0), description="Maximum value for the vector output")
    
    def init(self, context):
        self.outputs.new('NodeSocketVector', "Vector")
        self.inputs.new('TGR_SKT_Executable', "Update")
        
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        col = layout.column(align=True)
        col.prop(self, "default_value")
        col.prop(self, "min_value")
        col.prop(self, "max_value")


class TGR_DT_ND_Color(Node):
    bl_idname = "TGR_DT_ND_Color"
    bl_label = "Color"
    bl_icon = 'IMAGE_RGB_ALPHA'
    
    name: bpy.props.StringProperty(name="Name", default="")
    default_value: bpy.props.FloatVectorProperty(name="Value", subtype='COLOR', default=(1.0, 1.0, 1.0), description="Default value for the color output")
    
    def init(self, context):
        self.outputs.new('NodeSocketColor', "Color")
        self.inputs.new('TGR_SKT_Executable', "Update")
        
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "default_value", text="")
        

class TGR_DT_ND_Enum(Node):
    bl_idname = "TGR_DT_ND_Enum"
    bl_label = "Enum"
    bl_icon = 'LINENUMBERS_OFF'
    
    name: bpy.props.StringProperty(name="Name", default="")
    
    def init(self, context):
        self.inputs.new('TGR_SKT_Executable', "Update")
        self.inputs.new('TGR_SKT_EnumItem', "Item 001")
        self.outputs.new('TGR_SKT_Enum', "Enum")
    
    def update(self):
        if not self.inputs:
            return
        
        if self.inputs[-1].is_linked:
            new_index = len(self.inputs) + 1
            self.inputs.new('TGR_SKT_EnumItem', f"Item {new_index:03d}")
        
        while len(self.inputs) > 2 and not self.inputs[-2].is_linked:
            self.inputs.remove(self.inputs[-1])
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")


class TGR_DT_ND_EnumItem(Node):
    bl_idname = "TGR_DT_ND_EnumItem"
    bl_label = "Enum Item"
    bl_icon = 'LINENUMBERS_ON'
    
    name: bpy.props.StringProperty(name="Name", default="")
    description: bpy.props.StringProperty(name="Description", default="", description="Description for the enum item")
    
    def init(self, context):
        self.outputs.new('TGR_SKT_EnumItem', "Enum")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "description", text="", placeholder="Description")


class TGR_DT_ND_Object(Node):
    bl_idname = "TGR_DT_ND_Object"
    bl_label = "Object"
    bl_icon = 'OBJECT_DATAMODE'
    
    name: bpy.props.StringProperty(name="Name", default="")
    default_value: bpy.props.PointerProperty(name="Value", type=bpy.types.Object, description="Default value for the object output")
    
    def init(self, context):
        self.outputs.new('NodeSocketObject', "Object")
        self.inputs.new('TGR_SKT_Executable', "Update")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "default_value", text="", placeholder="Object Value")

# ===========================================================
# PROPERTY GROUP NODES
# ===========================================================
class TGR_DT_ND_PropertyGroup(Node):
    bl_idname = "TGR_DT_ND_PropertyGroup"
    bl_label = "Property Group"
    bl_icon = 'GROUP'
    
    name: bpy.props.StringProperty(name="Name", default="")
    target: bpy.props.PointerProperty(name="Target Object", type=bpy.types.Object, description="Object that contains the property group")
    bone: bpy.props.StringProperty(name="Bone", default="", description="Name of the bone that contains the property group (optional)")
    
    def init(self, context):
        self.inputs.new('TGR_SKT_Property', "Property 001")
    
    def update(self):
        if not self.inputs:
            return
        
        if self.inputs[-1].is_linked:
            new_index = len(self.inputs) + 1
            self.inputs.new('TGR_SKT_Property', f"Property {new_index:03d}")
        
        while len(self.inputs) > 1 and not self.inputs[-2].is_linked:
            self.inputs.remove(self.inputs[-1])
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "target", text="", placeholder="Target Object")
        if self.target and self.target.type == 'ARMATURE':
            layout.prop_search(self, "bone", self.target.data, "bones", text="Bone", icon='BONE_DATA')

# ===========================================================
# OPERATOR NODES
# ===========================================================
class TGR_OP_ND_Executable(Node):
    bl_idname = "TGR_OP_ND_Executable"
    bl_label = "Executable"
    bl_icon = 'NODE'
    
    name: bpy.props.StringProperty(name="Name", default="")
    node_type: bpy.props.EnumProperty(name="Type", items=[('OPERATOR', "Operator", "Blender Operator"), ('CALLBACK', "Callback", "Custom Callback Function")], default='OPERATOR')
    
    def _check_operator_exists(self):
        try:
            text_block = bpy.data.texts["tgr_executables.py"]
        except KeyError:
            return False
        return f"{self.node_type}: {self.name}" in text_block.as_string()
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Executable', "Executable")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Name")
        layout.prop(self, "node_type", text="", placeholder="Type")
        if not self._check_operator_exists():
            operator = layout.operator("tgr.create_executable", text="Create Executable", icon='ADD')
            operator.name = self.name
            operator.exec_type = self.node_type

# ==========================================================
# Layout Nodes
# ==========================================================
class BaseDynamicLayoutNode(Node):
    
    default_input_type = 'TGR_SKT_Layout'
    
    def update(self):
        if not self.inputs:
            return
        
        if self.inputs[-1].is_linked:
            new_index = len(self.inputs) + 1
            self.inputs.new(self.default_input_type, f"Item {new_index:03d}")
        
        while len(self.inputs) > 1 and not self.inputs[-2].is_linked:
            self.inputs.remove(self.inputs[-1])


class TGR_LY_ND_Row(BaseDynamicLayoutNode):
    bl_idname = "TGR_LY_ND_Row"
    bl_label = "Row"
    bl_icon = 'ALIGN_JUSTIFY'
    
    align: bpy.props.BoolProperty(name="Align", default=False, description="Align items in the row")
    height: bpy.props.IntProperty(name="Height", default=0, min=0, description="Height of the row (0 for automatic)")
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
        self.inputs.new('TGR_SKT_Layout', "Item 001")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "align", text="Align", toggle=True)
        layout.prop(self, "height", text="Height")


class TGR_LY_ND_Column(BaseDynamicLayoutNode):
    bl_idname = "TGR_LY_ND_Column"
    bl_label = "Column"
    bl_icon = 'ALIGN_JUSTIFY'
    
    align: bpy.props.BoolProperty(name="Align", default=False, description="Align items in the column")
    height: bpy.props.IntProperty(name="Height", default=0, min=0, description="Height of the column (0 for automatic)")
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
        self.inputs.new('TGR_SKT_Layout', "Item 001")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "align", text="Align", toggle=True)
        layout.prop(self, "height", text="Height")

class TGR_LY_ND_Box(BaseDynamicLayoutNode):
    bl_idname = "TGR_LY_ND_Box"
    bl_label = "Box"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
        self.inputs.new('TGR_SKT_Layout', "Item 001")
        
        
class TGR_LY_ND_SplitItem(Node):
    bl_idname = "TGR_LY_ND_SplitItem"
    bl_label = "Split Item"
    bl_icon = 'ALIGN_JUSTIFY'
    
    label: bpy.props.StringProperty(name="Label", default="", description="Label for the split item (optional)")
    factor: bpy.props.FloatProperty(name="Factor", default=0.5, min=0.0, max=1.0, description="Split factor between 0 and 1")
    
    def init(self, context):
        self.inputs.new('TGR_SKT_Layout', "Input")
        self.outputs.new('TGR_SKT_SplitItem', "Layout")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "label", text="", placeholder="Label")
        layout.prop(self, "factor", text="Factor")


class TGR_LY_ND_Split(Node):
    bl_idname = "TGR_LY_ND_Split"
    bl_label = "Split"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def _check_invalid_links(self):
        for input in self.inputs:
            for link in input.links:
                if link.from_socket.bl_idname != 'TGR_SKT_SplitItem':
                    return True
        return False
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
        self.inputs.new('TGR_SKT_SplitItem', "Item 001")
    
    def insert_link(self, link):
        if link.to_node != self:
            return
        # Show an error message if the user tries to connect something that is not a Split Item socket to the Split node
        if link.from_socket.bl_idname != 'TGR_SKT_SplitItem' and link.from_socket:
            self["_link_error"] = "Only Split Item sockets can be connected to the Split node"
        else:
            if "_link_error" in self:
                del self["_link_error"]
    
    def update(self):
        if self._check_invalid_links():
            self["_link_error"] = "Only Split Item sockets can be connected to the Split node"
        else:
            if "_link_error" in self:
                del self["_link_error"]
        
        if not self.inputs:
            return
        
        if self.inputs[-1].is_linked:
            new_index = len(self.inputs) + 1
            self.inputs.new('TGR_SKT_SplitItem', f"Item {new_index:03d}")
        
        while len(self.inputs) > 1 and not self.inputs[-2].is_linked:
            self.inputs.remove(self.inputs[-1])
        
    
    def draw_buttons(self, context, layout):
        if "_link_error" in self and self["_link_error"]:
            layout.label(text=self["_link_error"], icon='ERROR')


class TGR_LY_ND_Grid(BaseDynamicLayoutNode):
    bl_idname = "TGR_LY_ND_Grid"
    bl_label = "Grid"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
        self.inputs.new('TGR_SKT_Layout', "Item 001")


class TGR_LY_ND_Panel(BaseDynamicLayoutNode):
    bl_idname = "TGR_LY_ND_Panel"
    bl_label = "Panel"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def _get_panel_enum_items(self, context):
        """Dynamically generate enum items based on the panels available in the current UI tree"""
        items = [("NONE", "None", "No parent panel")]
        ui_node_tree = None
        for node_group in bpy.data.node_groups:
            if isinstance(node_group, TGR_NT_UI):
                ui_node_tree = node_group
                break
        if ui_node_tree:
            for node in ui_node_tree.nodes:
                if isinstance(node, TGR_LY_ND_Panel) and node != self:
                    items.append((node.name, node.name, ""))
        return items
    
    name: bpy.props.StringProperty(name="Panel Name", default="", description="Name of the panel")
    parent: bpy.props.EnumProperty(name="Parent Panel", items=_get_panel_enum_items, description="Parent panel for nesting (optional)")
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
        self.inputs.new('TGR_SKT_Layout', "Item 001")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "name", text="", placeholder="Panel Name")
        layout.prop(self, "parent", text="Parent Panel")


class TGR_LY_ND_Separator(Node):
    bl_idname = "TGR_LY_ND_Separator"
    bl_label = "Separator"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")


class TGR_LY_ND_Prop(Node):
    bl_idname = "TGR_LY_ND_Prop"
    bl_label = "Property"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def _draw_float(self, context, layout):
        layout.prop(self, "property_name", text="Property")
        layout.prop(self, "use_slider", text="Use Slider")
        layout.prop(self, "subtype", text="Subtype")
    
    def _draw_boolean(self, context, layout):
        layout.prop(self, "property_name", text="Property")
        layout.prop(self, "toggle", text="Toggle")
        layout.prop(self, "invert_boolean", text="Invert Boolean")
    
    def _draw_vector(self, context, layout):
        layout.prop(self, "property_name", text="Property")
        layout.prop(self, "subtype", text="Subtype")
        layout.prop(self, "orientation", text="Orientation")
    
    def _draw_default(self, context, layout):
        layout.prop(self, "property_name", text="Property")
        
    
    def _get_property_enum_items(self, context):
        """Dynamically generate enum items based on the property nodes available in the data tree"""
        items = []
        data_node_tree = None
        for node_group in bpy.data.node_groups:
            if isinstance(node_group, TGR_NT_Data):
                data_node_tree = node_group
                break
        if data_node_tree:
            for node in data_node_tree.nodes:
                if isinstance(node, (TGR_DT_ND_Float, TGR_DT_ND_Integer, TGR_DT_ND_String, TGR_DT_ND_Boolean, TGR_DT_ND_Vector, TGR_DT_ND_Color, TGR_DT_ND_Enum, TGR_DT_ND_Object)):
                    # Don't add to the enum if they are not linked to the Property Group node
                    if not any(isinstance(link.to_node, TGR_DT_ND_PropertyGroup) for link in node.outputs[0].links):
                        continue
                    items.append((node.name, node.name, ""))
        return items
    
    def _get_property_type(self):
        data_node_tree = None
        for node_group in bpy.data.node_groups:
            if isinstance(node_group, TGR_NT_Data):
                data_node_tree = node_group
                break
        if data_node_tree:
            for node in data_node_tree.nodes:
                if node.name == self.property_name:
                    return type(node)
        return None
    
    property_name: bpy.props.EnumProperty(name="Property", items=_get_property_enum_items)
    
    # Float, Int
    use_slider: bpy.props.BoolProperty(name="Use Slider", default=False, description="Display a slider for numeric properties")
    subtype: bpy.props.EnumProperty(name="Unit",
                                 items=[
                                     ('NONE', "None", "No subtype"),
                                     ('LENGTH', "Length", "Display as length"),
                                     ('ANGLE', "Angle", "Display as angle"),
                                     ('TIME', "Time", "Display as time"),
                                     ('PERCENTAGE', "Percentage", "Display as percentage"),
                                     ('PIXELS', "Pixels", "Display as pixels"),],
                                 default='NONE', description="Subtype to display for numeric properties")
    
    # Boolean
    toggle: bpy.props.BoolProperty(name="Toggle", default=False, description="Display boolean property as a toggle button")
    invert_boolean: bpy.props.BoolProperty(name="Invert Boolean", default=False, description="Invert the value of the boolean property")
    
    # Vector
    orientation: bpy.props.EnumProperty(name="Orientation",
                                        items=[
                                            ('HORIZONTAL', "Horizontal", "Arrange vector components horizontally"),
                                            ('VERTICAL', "Vertical", "Arrange vector components vertically")],
                                        default='HORIZONTAL')

    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
    
    def draw_buttons(self, context, layout):
        property_type = self._get_property_type()
        if property_type == TGR_DT_ND_Float:
            self._draw_float(context, layout)
        elif property_type == TGR_DT_ND_Integer:
            self._draw_float(context, layout)
        elif property_type == TGR_DT_ND_Boolean:
            self._draw_boolean(context, layout)
        elif property_type == TGR_DT_ND_Vector:
            self._draw_vector(context, layout)
        else:
            self._draw_default(context, layout)

class TGR_LY_ND_Operator(Node):
    bl_idname = "TGR_LY_ND_Operator"
    bl_label = "Operator"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def _get_operator_enum_items(self, context):
        """Dynamically generate enum items based on the operators defined in the Data Tree's Executable nodes"""
        items = []
        data_node_tree = None
        for node_group in bpy.data.node_groups:
            if isinstance(node_group, TGR_NT_Data):
                data_node_tree = node_group
                break
        if data_node_tree:
            for node in data_node_tree.nodes:
                if isinstance(node, TGR_OP_ND_Executable) and node.node_type == 'OPERATOR':
                    items.append((node.name, node.name, ""))
        return items
    
    operator_name: bpy.props.EnumProperty(name="Operator", items=_get_operator_enum_items)
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "operator_name", text="Operator")


class TGR_LY_ND_Label(Node):
    bl_idname = "TGR_LY_ND_Label"
    bl_label = "Label"
    bl_icon = 'ALIGN_JUSTIFY'
    
    text: bpy.props.StringProperty(name="Text", default="")
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "text", text="", placeholder="Text")


class TGR_LY_ND_BoneCollection(Node):
    bl_idname = "TGR_LY_ND_BoneCollection"
    bl_label = "Bone Collection"
    bl_icon = 'ALIGN_JUSTIFY'
    
    def _get_bone_collection_items(self, context):
        """Dynamically generate enum items based on the bone collections available in the armature"""
        items = []
        obj = context.object
        if obj and obj.type == 'ARMATURE':
            for collection in obj.data.collections_all:
                items.append((collection.name, collection.name, ""))
        return items
    
    collection_name: bpy.props.EnumProperty(name="Bone Collection", items=_get_bone_collection_items)
    property: bpy.props.EnumProperty(name="Property", items=[("VISIBILITY", "Visibility", "Control the visibility of the bone collection"), ("SOLO", "Solo", "Control the solo state of the bone collection")], default="VISIBILITY")
    
    def init(self, context):
        self.outputs.new('TGR_SKT_Layout', "Layout")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "property", text="Property")
        layout.prop(self, "collection_name", text="Collection")
