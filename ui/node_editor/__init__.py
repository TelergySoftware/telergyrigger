import bpy
# Core node system components
from .tgr_node_tree import TGR_NT_Data, TGR_NT_UI
from .tgr_socket import (
    TGR_SKT_EnumItem,
    TGR_SKT_Enum,
    TGR_SKT_Property,
    TGR_SKT_Executable,
    TGR_SKT_Layout,
    TGR_SKT_SplitItem,
    TGR_SKT_Any,
)

# Node classes
from .tgr_nodes import (
    # Output nodes
    
    
    # UI layout nodes
    TGR_LY_ND_Empty,
    TGR_LY_ND_Row,
    TGR_LY_ND_Column,
    TGR_LY_ND_Box,
    TGR_LY_ND_SplitItem,
    TGR_LY_ND_Split,
    TGR_LY_ND_Grid,
    TGR_LY_ND_Panel,
    TGR_LY_ND_Separator,
    TGR_LY_ND_BoneCollection,
    TGR_LY_ND_Prop,
    TGR_LY_ND_CustomProp,
    TGR_LY_ND_Operator,
    TGR_LY_ND_Label,
    # Data nodes
    TGR_DT_ND_Float,
    TGR_DT_ND_Integer,
    TGR_DT_ND_Boolean,
    TGR_DT_ND_String,
    TGR_DT_ND_Vector,
    TGR_DT_ND_Color,
    TGR_DT_ND_Object,
    TGR_DT_ND_Enum,
    TGR_DT_ND_EnumItem,
    TGR_DT_ND_PropertyGroup,
    # Operator nodes
    TGR_OP_ND_Executable,
    # Flow control nodes
    TGR_FC_ND_If,
    TGR_FC_ND_Compare,
)


NODE_CLASSES = [
    # Core node system components
    TGR_NT_Data,
    TGR_NT_UI,
    # Socket classes
    TGR_SKT_EnumItem,
    TGR_SKT_Enum,
    TGR_SKT_Property,
    TGR_SKT_Executable,
    TGR_SKT_Layout,
    TGR_SKT_SplitItem,
    TGR_SKT_Any,
    # Layout nodes
    TGR_LY_ND_Empty,
    TGR_LY_ND_Row,
    TGR_LY_ND_Column,
    TGR_LY_ND_Box,
    TGR_LY_ND_SplitItem,
    TGR_LY_ND_Split,
    TGR_LY_ND_Grid,
    TGR_LY_ND_Panel,
    TGR_LY_ND_Separator,
    TGR_LY_ND_BoneCollection,
    TGR_LY_ND_Prop,
    TGR_LY_ND_CustomProp,
    TGR_LY_ND_Operator,
    TGR_LY_ND_Label,
    # Data nodes
    TGR_DT_ND_Float,
    TGR_DT_ND_Integer,
    TGR_DT_ND_Boolean,
    TGR_DT_ND_String,
    TGR_DT_ND_Vector,
    TGR_DT_ND_Color,
    TGR_DT_ND_Object,
    TGR_DT_ND_Enum,
    TGR_DT_ND_EnumItem,
    TGR_DT_ND_PropertyGroup,
    # Operator nodes
    TGR_OP_ND_Executable,
    # Flow control nodes
    TGR_FC_ND_If,
    TGR_FC_ND_Compare,
]


def register():
    for cls in NODE_CLASSES:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(NODE_CLASSES):
        bpy.utils.unregister_class(cls)
