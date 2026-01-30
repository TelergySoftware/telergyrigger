# ========================================
# TGR UI - Import Module
# ========================================

# Menu components
from .menus import (
    TGR_MT_EditMode_PieMenu,
    TGR_MT_PoseMode_Constraints_PieMenu,
    TGR_MT_EditMode_AddBone,
    TGR_MT_TrackNewLayer,
)

# Node editor system
from .node_editor import (
    # Core system
    TGR_RigNodeTree,
    TGR_UISocket,
    TGR_PropertySocket,
    TGR_EnumItemSocket,
    
    # Node classes
    
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

# Panel components
from .panels import (
    # Base Panel
    TGR_PT_BASE,
    
    # Edit Mode panels
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities,
    
    # Pose Mode panels
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_PoseMode_ORG,
    TGR_PT_View3D_Panel_PoseMode_Constraints,
    
    # Utilities panels
    TGR_PT_View3D_Panel_Utilities,
    TGR_PT_View3D_Panel_Utilities_Naming,
    TGR_PT_View3D_Panel_Utilities_Selection,
    
    # Specialized panels
    TGR_PT_View3D_Panel_BoneCollections,
    TGR_PT_View3D_Panel_CustomProperties,
)

# Export all classes for external imports
__all__ = [
    # Menu components
    "TGR_MT_EditMode_PieMenu",
    "TGR_MT_PoseMode_Constraints_PieMenu",
    "TGR_MT_EditMode_AddBone",
    "TGR_MT_TrackNewLayer",
    
    # Node editor system
    "TGR_RigNodeTree",
    "TGR_UISocket",
    "TGR_PropertySocket",
    "TGR_EnumItemSocket",
    "TGR_OutputNode",
    "TGR_PanelNode",
    "TGR_RowNode",
    "TGR_ColumnNode",
    "TGR_BoxNode",
    "TGR_ValueNode",
    "TGR_IntegerNode",
    "TGR_BooleanNode",
    "TGR_StringNode",
    "TGR_VectorNode",
    "TGR_ColorNode",
    "TGR_ObjectNode",
    "TGR_EnumItemNode",
    "TGR_PropertiesNode",
    "TGR_FloatPropertyNode",
    "TGR_IntegerPropertyNode",
    "TGR_BooleanPropertyNode",
    "TGR_StringPropertyNode",
    "TGR_VectorPropertyNode",
    "TGR_ColorPropertyNode",
    "TGR_EnumPropertyNode",
    
    # Panel components
    "TGR_PT_BASE",
    "TGR_PT_View3D_Panel_EditMode",
    "TGR_PT_View3D_Panel_EditMode_Create",
    "TGR_PT_View3D_Panel_EditMode_Parenting",
    "TGR_PT_View3D_Panel_EditMode_Utilities",
    "TGR_PT_View3D_Panel_PoseMode",
    "TGR_PT_View3D_Panel_PoseMode_ORG",
    "TGR_PT_View3D_Panel_PoseMode_Constraints",
    "TGR_PT_View3D_Panel_Utilities",
    "TGR_PT_View3D_Panel_Utilities_Naming",
    "TGR_PT_View3D_Panel_Utilities_Selection",
    "TGR_PT_View3D_Panel_BoneCollections",
    "TGR_PT_View3D_Panel_CustomProperties",
]