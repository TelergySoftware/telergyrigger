# Add Classes from tgr_view3d_panels
from .tgr_base_panel import TGR_PT_BASE
# Edit Mode panels
from .tgr_edit_mode_panels import TGR_PT_View3D_Panel_EditMode, TGR_PT_View3D_Panel_EditMode_Create, TGR_PT_View3D_Panel_EditMode_Parenting, TGR_PT_View3D_Panel_EditMode_Utilities
# Pose Mode panels
from .tgr_pose_mode_panels import TGR_PT_View3D_Panel_PoseMode, TGR_PT_View3D_Panel_PoseMode_TGT, TGR_PT_View3D_Panel_PoseMode_Constraints
# Utilities panels
from .tgr_utilities_panels import TGR_PT_View3D_Panel_Utilities, TGR_PT_View3D_Panel_Utilities_Naming, TGR_PT_View3D_Panel_Utilities_Selection
# Bone Layers panels
from .tgr_bone_layers_panels import TGR_PT_View3D_Panel_BoneLayers
# Rig UI panels
from .tgr_rig_ui_panels import TGR_PT_View3D_Panel_RigUI
# Custom Properties panels
from .tgr_custom_properties_panels import TGR_PT_View3D_Panel_CustomProperties

__all__ = [
    # Base Panel
    TGR_PT_BASE,
    # Edit Mode Panels
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities,
    # Pose Mode Panels
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_PoseMode_TGT,
    # Utilities Panels
    TGR_PT_View3D_Panel_Utilities,
    TGR_PT_View3D_Panel_Utilities_Naming,
]