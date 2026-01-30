# ========================================
# TGR Node Editor - Import Module
# ========================================

# Core node system components
from .tgr_node_tree import TGR_RigNodeTree
from .tgr_socket import TGR_UISocket, TGR_PropertySocket, TGR_EnumItemSocket

# Node classes
from .tgr_nodes import (
    # Output nodes
    TGR_ViewNode,
    
    # UI layout nodes
    TGR_PanelNode,
    TGR_RowNode,
    TGR_ColumnNode,
    TGR_BoxNode,
    
    # Input/value nodes
    TGR_ValueNode,
    TGR_IntegerNode,
    TGR_BooleanNode,
    TGR_StringNode,
    TGR_VectorNode,
    TGR_ColorNode,
    TGR_ObjectNode,
    TGR_EnumItemNode,
    
    # Property nodes
    TGR_PropertiesNode,
    TGR_FloatPropertyNode,
    TGR_IntegerPropertyNode,
    TGR_BooleanPropertyNode,
    TGR_StringPropertyNode,
    TGR_VectorPropertyNode,
    TGR_ColorPropertyNode,
    TGR_EnumPropertyNode,
)

# Export all classes for external imports
__all__ = [
    # Core system
    "TGR_RigNodeTree",
    "TGR_UISocket",
    "TGR_PropertySocket",
    "TGR_EnumItemSocket",
    
    # Output nodes
    "TGR_OutputNode",
    
    # UI layout nodes
    "TGR_PanelNode",
    "TGR_RowNode",
    "TGR_ColumnNode",
    "TGR_BoxNode",
    
    # Input/value nodes
    "TGR_ValueNode",
    "TGR_IntegerNode",
    "TGR_BooleanNode",
    "TGR_StringNode",
    "TGR_VectorNode",
    "TGR_ColorNode",
    "TGR_ObjectNode",
    "TGR_EnumItemNode",
    
    # Property nodes
    "TGR_PropertiesNode",
    "TGR_FloatPropertyNode",
    "TGR_IntegerPropertyNode",
    "TGR_BooleanPropertyNode",
    "TGR_StringPropertyNode",
    "TGR_VectorPropertyNode",
    "TGR_ColorPropertyNode",
    "TGR_EnumPropertyNode",
]