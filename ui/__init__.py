# Add classes from menus and panels
from .menus import TGR_MT_EditMode_PieMenu, TGR_MT_PoseMode_Constraints_PieMenu, TGR_MT_EditMode_AddBone, TGR_MT_TrackNewLayer
from .panels import (
    # Base Panel
    TGR_PT_BASE,
    # Edit Mode
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities,
    # Pose Mode
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_PoseMode_TGT,
    TGR_PT_View3D_Panel_PoseMode_Constraints,
    # Utilities
    TGR_PT_View3D_Panel_Utilities,
    TGR_PT_View3D_Panel_Utilities_Naming,
    TGR_PT_View3D_Panel_Utilities_Selection,
    # Bone Layers
    TGR_PT_View3D_Panel_BoneLayers,
    # Rig UI
    TGR_PT_View3D_Panel_RigUI,
)

__all__ = [
    # Menus
    TGR_MT_EditMode_PieMenu,
    TGR_MT_EditMode_AddBone,
    TGR_MT_PoseMode_Constraints_PieMenu,
    TGR_MT_TrackNewLayer,
    # Panels
    TGR_PT_BASE,
    # - EDIT MODE PANELS -
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities,
    # - POSE MODE PANELS -
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_PoseMode_TGT,
    # - UTILITIES PANELS -
    TGR_PT_View3D_Panel_Utilities,
    TGR_PT_View3D_Panel_Utilities_Naming,
    # - BONE LAYERS PANELS -
    TGR_PT_View3D_Panel_BoneLayers,
]