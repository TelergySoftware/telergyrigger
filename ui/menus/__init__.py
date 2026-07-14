import bpy
# Add classes from tgr_edit_mode_pie_menu
from .tgr_edit_mode_pie_menu import TGR_MT_EditMode_PieMenu
# Add classes from tgr_pose_mode_pie_menu
from .tgr_pose_mode_pie_menu import TGR_MT_PoseMode_Constraints_PieMenu
# Add classes from tgr_edit_mode_menu
from .tgr_edit_mode_menu import TGR_MT_EditMode_AddBone
# Add classes from tgr_layers_menu
from .tgr_layers_menu import TGR_MT_TrackNewLayer
# Add classes from tgr_weight_paint_pie_menu
from .tgr_weight_paint_pie_menu import TGR_MT_WP_PieMenu

MENU_CLASSES = [TGR_MT_EditMode_PieMenu,
                TGR_MT_PoseMode_Constraints_PieMenu,
                TGR_MT_EditMode_AddBone,
                TGR_MT_TrackNewLayer,
                TGR_MT_WP_PieMenu
                ]

def register():
    for cls in MENU_CLASSES:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in reversed(MENU_CLASSES):
        bpy.utils.unregister_class(cls)