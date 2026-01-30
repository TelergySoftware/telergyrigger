import bpy
from bpy.types import Node


# ================ UI Area Nodes ==================

class TGR_ViewNode(Node):
    bl_idname = "TGR_ViewNode"
    bl_label = "View Area"
    bl_icon = "VIEW3D"
    
    space_type: bpy.props.EnumProperty(
        name="View Type",
        description="Type of the UI view area",
        items=[
            ("VIEW_3D", "3D View", "3D Viewport"),
            ("IMAGE_EDITOR", "Image Editor", "Image Editor"),
            ("NODE_EDITOR", "Node Editor", "Node Editor"),
            ("SEQUENCE_EDITOR", "Video Sequence Editor", "Video Sequence Editor"),
            ("CLIP_EDITOR", "Movie Clip Editor", "Movie Clip Editor"),
            ("DOPESHEET_EDITOR", "Dope Sheet", "Dope Sheet Editor"),
            ("GRAPH_EDITOR", "Graph Editor", "Graph Editor"),
            ("NLA_EDITOR", "NLA Editor", "Non-Linear Animation Editor"),
            ("TEXT_EDITOR", "Text Editor", "Text Editor"),
            ("CONSOLE", "Python Console", "Python Console"),
            ("INFO", "Info", "Info Editor"),
            ("OUTLINER", "Outliner", "Outliner"),
            ("PROPERTIES", "Properties", "Properties Editor"),
            ("FILE_BROWSER", "File Browser", "File Browser"),
            ("PREFERENCES", "Preferences", "User Preferences"),
            ("TIMELINE", "Timeline", "Timeline"),
            ("LOGIC_EDITOR", "Logic Editor", "Logic Editor"),
            ("ASSET_BROWSER", "Asset Browser", "Asset Browser"),
        ]
    )
    
    region_type: bpy.props.EnumProperty(
        name="Region Type",
        description="Type of the UI region",
        items=[
            ("WINDOW", "Window", "Window Region"),
            ("HEADER", "Header", "Header Region"),
            ("CHANNELS", "Channels", "Channels Region"),
            ("TOOLS", "Tools", "Tools Region"),
            ("UI", "UI", "UI Region"),
            ("TOOL_PROPS", "Tool Properties", "Tool Properties Region"),
            ("PREVIEW", "Preview", "Preview Region"),
            ("HUD", "HUD", "Heads-Up Display Region"),
        ]
    )
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Category")
        # Add initial empty socket for dynamic input
        self._add_empty_socket()
    
    def _add_empty_socket(self):
        """Add an empty socket for new connections"""
        socket = self.inputs.new("TGR_UISocket", "")
        socket.name = f"UI Element {len(self.inputs) - 1}"  # Don't count the Tab Name socket
        return socket
    
    def _remove_empty_sockets(self):
        """Remove unconnected empty sockets (except the last one)"""
        empty_sockets = []
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element") and socket.name != "Tab Name":
                empty_sockets.append(socket)
        
        # Always keep at least one empty socket for new connections
        if len(empty_sockets) > 1:
            for socket in empty_sockets[:-1]:
                self.inputs.remove(socket)
    
    def _update_socket_names(self):
        """Update socket names to maintain proper numbering"""
        input_count = 1
        for socket in self.inputs:
            if socket.name != "Category":
                if socket.is_linked:
                    socket.name = f"UI Element {input_count}"
                    input_count += 1
                else:
                    socket.name = f"UI Element {input_count}"
    
    def update(self):
        """Called when the node or its connections change"""
        # Check if we need to add a new empty socket
        has_empty_socket = False
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                has_empty_socket = True
                break
        
        if not has_empty_socket:
            # All sockets are connected, add a new empty one
            self._add_empty_socket()
        
        # Clean up unused empty sockets
        self._remove_empty_sockets()
        
        # Update socket names
        self._update_socket_names()
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        col = layout.column()
        col.operator("tgr.ui_picker", text="UI Picker", icon="EYEDROPPER")
        col.prop(self, "space_type", text="View Type")
        col.prop(self, "region_type", text="Region Type")
    
    def draw_label(self):
        return self.space_type

# ================ UI Nodes ==================

class TGR_PanelNode(Node):
    bl_idname = "TGR_PanelNode"
    bl_label = "Panel"
    bl_icon = "NONE"
    
    def init(self, context):
        # Inputs: String -> Name,
        self.inputs.new("NodeSocketString", "Name")
        self.outputs.new("TGR_UISocket", "UI")
        # Add initial empty socket for dynamic input
        self._add_empty_socket()
    
    def _add_empty_socket(self):
        """Add an empty socket for new connections"""
        socket = self.inputs.new("TGR_UISocket", "")
        socket.name = f"UI Element {len(self.inputs) - 1}"  # Don't count the Name socket
        return socket
    
    def _remove_empty_sockets(self):
        """Remove unconnected empty sockets (except the last one)"""
        empty_sockets = []
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element") and socket.name != "Name":
                empty_sockets.append(socket)
        
        # Always keep at least one empty socket for new connections
        if len(empty_sockets) > 1:
            for socket in empty_sockets[:-1]:
                self.inputs.remove(socket)
    
    def _update_socket_names(self):
        """Update socket names to maintain proper numbering"""
        input_count = 1
        for socket in self.inputs:
            if socket.name != "Name":
                if socket.is_linked:
                    socket.name = f"UI Element {input_count}"
                    input_count += 1
                else:
                    socket.name = f"UI Element {input_count}"
    
    def update(self):
        """Called when the node or its connections change"""
        # Check if we need to add a new empty socket
        has_empty_socket = False
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                has_empty_socket = True
                break
        
        if not has_empty_socket:
            # All sockets are connected, add a new empty one
            self._add_empty_socket()
        
        # Clean up unused empty sockets
        self._remove_empty_sockets()
        
        # Update socket names
        self._update_socket_names()
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Panel"


class TGR_RowNode(Node):
    bl_idname = "TGR_RowNode"
    bl_label = "Row"
    bl_icon = "NONE"
    
    def init(self, context):
        self.outputs.new("TGR_UISocket", "UI")
        # Add initial empty socket for dynamic input
        self._add_empty_socket()
    
    def _add_empty_socket(self):
        """Add an empty socket for new connections"""
        socket = self.inputs.new("TGR_UISocket", "")
        socket.name = f"UI Element {len(self.inputs)}"
        return socket
    
    def _remove_empty_sockets(self):
        """Remove unconnected empty sockets (except the last one)"""
        empty_sockets = []
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                empty_sockets.append(socket)
        
        # Always keep at least one empty socket for new connections
        if len(empty_sockets) > 1:
            for socket in empty_sockets[:-1]:
                self.inputs.remove(socket)
    
    def _update_socket_names(self):
        """Update socket names to maintain proper numbering"""
        input_count = 1
        for socket in self.inputs:
            socket.name = f"UI Element {input_count}"
            input_count += 1
    
    def update(self):
        """Called when the node or its connections change"""
        # Check if we need to add a new empty socket
        has_empty_socket = False
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                has_empty_socket = True
                break
        
        if not has_empty_socket:
            # All sockets are connected, add a new empty one
            self._add_empty_socket()
        
        # Clean up unused empty sockets
        self._remove_empty_sockets()
        
        # Update socket names
        self._update_socket_names()
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Row"


class TGR_ColumnNode(Node):
    bl_idname = "TGR_ColumnNode"
    bl_label = "Column"
    bl_icon = "NONE"
    
    def init(self, context):
        self.outputs.new("TGR_UISocket", "UI")
        # Add initial empty socket for dynamic input
        self._add_empty_socket()
    
    def _add_empty_socket(self):
        """Add an empty socket for new connections"""
        socket = self.inputs.new("TGR_UISocket", "")
        socket.name = f"UI Element {len(self.inputs)}"
        return socket
    
    def _remove_empty_sockets(self):
        """Remove unconnected empty sockets (except the last one)"""
        empty_sockets = []
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                empty_sockets.append(socket)
        
        # Always keep at least one empty socket for new connections
        if len(empty_sockets) > 1:
            for socket in empty_sockets[:-1]:
                self.inputs.remove(socket)
    
    def _update_socket_names(self):
        """Update socket names to maintain proper numbering"""
        input_count = 1
        for socket in self.inputs:
            socket.name = f"UI Element {input_count}"
            input_count += 1
    
    def update(self):
        """Called when the node or its connections change"""
        # Check if we need to add a new empty socket
        has_empty_socket = False
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                has_empty_socket = True
                break
        
        if not has_empty_socket:
            # All sockets are connected, add a new empty one
            self._add_empty_socket()
        
        # Clean up unused empty sockets
        self._remove_empty_sockets()
        
        # Update socket names
        self._update_socket_names()
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Column"


class TGR_BoxNode(Node):
    bl_idname = "TGR_BoxNode"
    bl_label = "Box"
    bl_icon = "NONE"
    
    def init(self, context):
        self.outputs.new("TGR_UISocket", "UI")
        # Add initial empty socket for dynamic input
        self._add_empty_socket()
    
    def _add_empty_socket(self):
        """Add an empty socket for new connections"""
        socket = self.inputs.new("TGR_UISocket", "")
        socket.name = f"UI Element {len(self.inputs)}"
        return socket
    
    def _remove_empty_sockets(self):
        """Remove unconnected empty sockets (except the last one)"""
        empty_sockets = []
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                empty_sockets.append(socket)
        
        # Always keep at least one empty socket for new connections
        if len(empty_sockets) > 1:
            for socket in empty_sockets[:-1]:
                self.inputs.remove(socket)
    
    def _update_socket_names(self):
        """Update socket names to maintain proper numbering"""
        input_count = 1
        for socket in self.inputs:
            socket.name = f"UI Element {input_count}"
            input_count += 1
    
    def update(self):
        """Called when the node or its connections change"""
        # Check if we need to add a new empty socket
        has_empty_socket = False
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("UI Element"):
                has_empty_socket = True
                break
        
        if not has_empty_socket:
            # All sockets are connected, add a new empty one
            self._add_empty_socket()
        
        # Clean up unused empty sockets
        self._remove_empty_sockets()
        
        # Update socket names
        self._update_socket_names()
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Box"


# ================ Input Nodes ==================

class TGR_ValueNode(Node):
    """Simple float value input node"""
    bl_idname = "TGR_ValueNode"
    bl_label = "Value"
    bl_icon = "NONE"
    
    value: bpy.props.FloatProperty(name="Value", default=0.0)
    
    def init(self, context):
        self.outputs.new("NodeSocketFloat", "Value")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="")
    
    def draw_label(self):
        return "Value"


class TGR_IntegerNode(Node):
    """Integer input node"""
    bl_idname = "TGR_IntegerNode"
    bl_label = "Integer"
    bl_icon = "NONE"
    
    value: bpy.props.IntProperty(name="Integer", default=0)
    
    def init(self, context):
        self.outputs.new("NodeSocketInt", "Integer")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="")
    
    def draw_label(self):
        return "Integer"


class TGR_BooleanNode(Node):
    """Boolean input node"""
    bl_idname = "TGR_BooleanNode"
    bl_label = "Boolean"
    bl_icon = "NONE"
    
    value: bpy.props.BoolProperty(name="Boolean", default=False)
    
    def init(self, context):
        self.outputs.new("NodeSocketBool", "Boolean")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="")
    
    def draw_label(self):
        return "Boolean"


class TGR_StringNode(Node):
    """String input node"""
    bl_idname = "TGR_StringNode"
    bl_label = "String"
    bl_icon = "NONE"
    
    value: bpy.props.StringProperty(name="String", default="")
    
    def init(self, context):
        self.outputs.new("NodeSocketString", "String")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="")
    
    def draw_label(self):
        return "String"


class TGR_VectorNode(Node):
    """Vector input node"""
    bl_idname = "TGR_VectorNode"
    bl_label = "Vector"
    bl_icon = "NONE"
    
    value: bpy.props.FloatVectorProperty(
        name="Vector",
        description="Vector value",
        default=(0.0, 0.0, 0.0),
        size=3
    )
    
    def init(self, context):
        self.outputs.new("NodeSocketVector", "Vector")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="")
    
    def draw_label(self):
        return "Vector"


class TGR_ColorNode(Node):
    """Color input node"""
    bl_idname = "TGR_ColorNode"
    bl_label = "Color"
    bl_icon = "NONE"
    
    value: bpy.props.FloatVectorProperty(
        name="Color",
        description="Color value",
        default=(1.0, 1.0, 1.0, 1.0),
        size=4,
        subtype='COLOR'
    )
    
    def init(self, context):
        self.outputs.new("NodeSocketColor", "Color")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="")
    
    def draw_label(self):
        return "Color"


class TGR_ObjectNode(Node):
    """Object reference input node"""
    bl_idname = "TGR_ObjectNode"
    bl_label = "Object"
    bl_icon = "NONE"
    
    value: bpy.props.PointerProperty(
        name="Object",
        description="Object reference",
        type=bpy.types.Object
    )
    
    def init(self, context):
        self.outputs.new("NodeSocketObject", "Object")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value", text="", placeholder="Select Object...")
    
    def draw_label(self):
        return "Object"


class TGR_EnumItemNode(Node):
    """Enum item node for enum properties"""
    bl_idname = "TGR_EnumItemNode"
    bl_label = "Enum Item"
    bl_icon = "NONE"
    
    name: bpy.props.StringProperty(
        name="Name",
        description="Display name for the enum item",
        default=""
    )
    
    description: bpy.props.StringProperty(
        name="Description",
        description="Tooltip description for the enum item",
        default=""
    )
    
    def init(self, context):
        self.outputs.new("TGR_EnumItemSocket", "Enum Item")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, "name", text="", placeholder="Item name...")
        col.prop(self, "description", text="", placeholder="Description...")
    
    def draw_label(self):
        return "Enum Item"


# ================ Property Nodes ==================
class TGR_PropertiesNode(Node):
    """Properties container node"""
    bl_idname = "TGR_PropertiesNode"
    bl_label = "Properties"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        # Add initial empty socket for dynamic input
        self._add_empty_socket()
    
    def _add_empty_socket(self):
        """Add an empty socket for new connections"""
        socket = self.inputs.new("TGR_PropertySocket", "")
        socket.name = f"Property {len(self.inputs) - 1}"  # Don't count the Name socket
        return socket
    
    def _remove_empty_sockets(self):
        """Remove unconnected empty sockets (except the last one)"""
        empty_sockets = []
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("Property") and socket.name != "Name":
                empty_sockets.append(socket)
        
        # Always keep at least one empty socket for new connections
        if len(empty_sockets) > 1:
            for socket in empty_sockets[:-1]:
                self.inputs.remove(socket)
    
    def _update_socket_names(self):
        """Update socket names to maintain proper numbering"""
        input_count = 1
        for socket in self.inputs:
            if socket.name != "Name":
                if socket.is_linked:
                    socket.name = f"Property {input_count}"
                    input_count += 1
                else:
                    socket.name = f"Property {input_count}"
    
    def update(self):
        """Called when the node or its connections change"""
        # Check if we need to add a new empty socket
        has_empty_socket = False
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("Property"):
                has_empty_socket = True
                break
        
        if not has_empty_socket:
            # All sockets are connected, add a new empty one
            self._add_empty_socket()
        
        # Clean up unused empty sockets
        self._remove_empty_sockets()
        
        # Update socket names
        self._update_socket_names()
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Properties"


class TGR_FloatPropertyNode(Node):
    """Float property node"""
    bl_idname = "TGR_FloatPropertyNode"
    bl_label = "Float Property"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        self.inputs.new("NodeSocketString", "Description")
        self.inputs.new("NodeSocketFloat", "Value")
        self.inputs.new("NodeSocketFloat", "Min")
        self.inputs.new("NodeSocketFloat", "Max")
        self.outputs.new("TGR_PropertySocket", "Property")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Float Property"


class TGR_IntegerPropertyNode(Node):
    """Integer property node"""
    bl_idname = "TGR_IntegerPropertyNode"
    bl_label = "Integer Property"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        self.inputs.new("NodeSocketString", "Description")
        self.inputs.new("NodeSocketInt", "Default Value")
        self.inputs.new("NodeSocketInt", "Min")
        self.inputs.new("NodeSocketInt", "Max")
        self.outputs.new("TGR_PropertySocket", "Property")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Integer Property"


class TGR_BooleanPropertyNode(Node):
    """Boolean property node"""
    bl_idname = "TGR_BooleanPropertyNode"
    bl_label = "Boolean Property"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        self.inputs.new("NodeSocketString", "Description")
        self.inputs.new("NodeSocketBool", "Default Value")
        self.outputs.new("TGR_PropertySocket", "Property")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Boolean Property"


class TGR_StringPropertyNode(Node):
    """String property node"""
    bl_idname = "TGR_StringPropertyNode"
    bl_label = "String Property"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        self.inputs.new("NodeSocketString", "Description")
        self.inputs.new("NodeSocketString", "Default Value")
        self.outputs.new("TGR_PropertySocket", "Property")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "String Property"


class TGR_VectorPropertyNode(Node):
    """Vector property node"""
    bl_idname = "TGR_VectorPropertyNode"
    bl_label = "Vector Property"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        self.inputs.new("NodeSocketString", "Description")
        self.inputs.new("NodeSocketVector", "Default Value")
        self.inputs.new("NodeSocketVector", "Min")
        self.inputs.new("NodeSocketVector", "Max")
        self.outputs.new("TGR_PropertySocket", "Property")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Vector Property"


class TGR_ColorPropertyNode(Node):
    """Color property node"""
    bl_idname = "TGR_ColorPropertyNode"
    bl_label = "Color Property"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        self.inputs.new("NodeSocketString", "Description")
        self.inputs.new("NodeSocketColor", "Default Value")
        self.outputs.new("TGR_PropertySocket", "Property")
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Color Property"


class TGR_EnumPropertyNode(Node):
    """Enum property node with dynamic enum items"""
    bl_idname = "TGR_EnumPropertyNode"
    bl_label = "Enum Property"
    bl_icon = "NONE"
    
    def init(self, context):
        self.inputs.new("NodeSocketString", "Name")
        self.inputs.new("NodeSocketString", "Description")
        self.outputs.new("TGR_PropertySocket", "Property")
        # Add initial empty socket for dynamic input
        self._add_empty_socket()
    
    def _add_empty_socket(self):
        """Add an empty socket for new connections"""
        socket = self.inputs.new("TGR_EnumItemSocket", "")
        socket.name = f"Enum Item {len(self.inputs) - 2}"  # Don't count Name and Description sockets
        return socket
    
    def _remove_empty_sockets(self):
        """Remove unconnected empty sockets (except the last one)"""
        empty_sockets = []
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("Enum Item") and socket.name not in ["Name", "Description"]:
                empty_sockets.append(socket)
        
        # Always keep at least one empty socket for new connections
        if len(empty_sockets) > 1:
            for socket in empty_sockets[:-1]:
                self.inputs.remove(socket)
    
    def _update_socket_names(self):
        """Update socket names to maintain proper numbering"""
        input_count = 1
        for socket in self.inputs:
            if socket.name not in ["Name", "Description"]:
                if socket.is_linked:
                    socket.name = f"Enum Item {input_count}"
                    input_count += 1
                else:
                    socket.name = f"Enum Item {input_count}"
    
    def update(self):
        """Called when the node or its connections change"""
        # Check if we need to add a new empty socket
        has_empty_socket = False
        for socket in self.inputs:
            if not socket.is_linked and socket.name.startswith("Enum Item"):
                has_empty_socket = True
                break
        
        if not has_empty_socket:
            # All sockets are connected, add a new empty one
            self._add_empty_socket()
        
        # Clean up unused empty sockets
        self._remove_empty_sockets()
        
        # Update socket names
        self._update_socket_names()
    
    def copy(self, node):
        print("Copied node ", node)
    
    def free(self):
        print("Node removed", self)
    
    def draw_buttons(self, context, layout):
        pass
    
    def draw_label(self):
        return "Enum Property"
        