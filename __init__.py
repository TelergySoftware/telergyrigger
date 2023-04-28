# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

bl_info = {
    "name" : "Telergy Rigger",
    "author" : "Telergy Studio",
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Rigging"
}

# Import operators, panels, menus and properties
from .operators import (TGR_OT_AddPrefix,
                        TGR_OT_AddSuffix,
                        TGR_OT_CleanNameUp,
                        TGR_OT_EditLayer,
                        TGR_OT_LockBonesFromLayer,
                        TGR_OT_RemoveLayer,
                        TGR_OT_RemovePrefix,
                        TGR_OT_RemoveSuffix,
                        TGR_OT_SelectBonesByName,
                        TGR_OT_SelectLayerBones,
                        TGR_OT_SetBonesLayer,
                        TGR_OT_TrackNewLayer)

from .operators import (TGR_OT_AddDeformBone,
                        TGR_OT_AddNonDeformBone,
                        TGR_OT_AlignBoneToWorld,
                        TGR_OT_BoneOnPoints,
                        TGR_OT_ConnectBones,
                        TGR_OT_CreateTGT,
                        TGR_OT_RemoveTGT,
                        TGR_OT_ParentToRoot)

from .operators import (TGR_OT_BindTGT,
                        TGR_OT_CopyTransformsToChain,
                        TGR_OT_CreateIkFkSwichChain,
                        TGR_OT_CreateRotationChain,
                        TGR_OT_CreateStretchToChain,
                        TGR_OT_IsolateBoneRotation,
                        TGR_OT_UnbindTGT)

from .operators import (TGR_OT_AddTGRArmature)

from .ui import TGR_PT_View3D_Panel_EditMode, TGR_PT_View3D_Panel_PoseMode, TGR_PT_View3D_Panel_Utilities
# Edit Mode Subpanels
from .ui import TGR_PT_View3D_Panel_EditMode_Create, TGR_PT_View3D_Panel_EditMode_Parenting, TGR_PT_View3D_Panel_EditMode_Utilities
# Pose Mode Subpanels
from .ui import TGR_PT_View3D_Panel_PoseMode_TGT, TGR_PT_View3D_Panel_PoseMode_Constraints
# Utilities Subpanels
from .ui import TGR_PT_View3D_Panel_Utilities_Naming, TGR_PT_View3D_Panel_Utilities_Selection
# Bone Layers Subpanels
from .ui import TGR_PT_View3D_Panel_BoneLayers
# Menus
from .ui import TGR_MT_EditMode_PieMenu, TGR_MT_PoseMode_Constraints_PieMenu, TGR_MT_EditMode_AddBone, TGR_MT_TrackNewLayer

# Properties
from .properties import TGR_Properties, TGR_LayerProperties

# Classes to register
CLASSES_TO_REGISTER = (
    # Operators
    TGR_OT_AddDeformBone,
    TGR_OT_AddNonDeformBone,
    TGR_OT_AddPrefix,
    TGR_OT_AddSuffix,
    TGR_OT_AddTGRArmature,
    TGR_OT_AlignBoneToWorld,
    TGR_OT_BindTGT,
    TGR_OT_BoneOnPoints,
    TGR_OT_CleanNameUp,
    TGR_OT_ConnectBones,
    TGR_OT_CreateIkFkSwichChain,
    TGR_OT_CreateRotationChain,
    TGR_OT_CreateStretchToChain,
    TGR_OT_CreateTGT,
    TGR_OT_CopyTransformsToChain,
    TGR_OT_EditLayer,
    TGR_OT_IsolateBoneRotation,
    TGR_OT_LockBonesFromLayer,
    TGR_OT_ParentToRoot,
    TGR_OT_RemoveLayer,
    TGR_OT_RemovePrefix,
    TGR_OT_RemoveTGT,
    TGR_OT_RemoveSuffix,
    TGR_OT_SelectBonesByName,
    TGR_OT_SelectLayerBones,
    TGR_OT_SetBonesLayer,
    TGR_OT_TrackNewLayer,
    TGR_OT_UnbindTGT,
    # Panels
    TGR_PT_View3D_Panel_BoneLayers,
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities,
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_PoseMode_Constraints,
    TGR_PT_View3D_Panel_PoseMode_TGT,
    TGR_PT_View3D_Panel_Utilities,
    TGR_PT_View3D_Panel_Utilities_Naming,
    TGR_PT_View3D_Panel_Utilities_Selection,
    # Menus
    TGR_MT_EditMode_PieMenu,
    TGR_MT_EditMode_AddBone,
    TGR_MT_TrackNewLayer,
    TGR_MT_PoseMode_Constraints_PieMenu,
    # Properties
    TGR_LayerProperties,
    TGR_Properties,
)

# Keymaps reference
keymaps = []

# Object Mode Add menu appendix
def object_add_draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("tgr.add_tgr_armature", text="TGR Armature", icon="OUTLINER_OB_ARMATURE")

def register():
    # Register classes
    for cls in CLASSES_TO_REGISTER:
        bpy.utils.register_class(cls)
    
    # Add properties to the armature object
    bpy.types.Object.tgr_props = bpy.props.PointerProperty(type=TGR_Properties)
    bpy.types.Object.tgr_layer_collection = bpy.props.CollectionProperty(type=TGR_LayerProperties)
    
    # Append the default layers

    wm = bpy.context.window_manager
    # Add new Keymap
    km = wm.keyconfigs.addon.keymaps.new(name='Armature', space_type='EMPTY')
    # Add new Keymap items to call the TGR_MT_EditMode_PieMenu pie menu
    kmi = km.keymap_items.new('wm.call_menu_pie', 'D', 'PRESS')
    kmi.properties.name = 'TGR_MT_EditMode_PieMenu'
    kmi.active = True
    keymaps.append((km, kmi))
    
    # Add new Keymap
    km = wm.keyconfigs.addon.keymaps.new(name='Pose', space_type='EMPTY')
    # Add new Keymap items to call the TGR_MT_PoseMode_Constraints_PieMenu pie menu
    kmi = km.keymap_items.new('wm.call_menu_pie', 'D', 'PRESS')
    kmi.properties.name = 'TGR_MT_PoseMode_Constraints_PieMenu'
    kmi.active = True
    keymaps.append((km, kmi))
    
    # Add new Keymap
    km = wm.keyconfigs.addon.keymaps.new(name='Armature', space_type='EMPTY')
    # Add new Keymap items to call the TGR_MT_EditMode_AddBone pie menu
    kmi = km.keymap_items.new('wm.call_menu', 'A', 'PRESS', shift=True)
    kmi.properties.name = 'TGR_MT_EditMode_AddBone'
    kmi.active = True
    keymaps.append((km, kmi))
    
    # Append the Add TGR rig to the add menu
    bpy.types.VIEW3D_MT_add.append(object_add_draw_menu)
    

def unregister():
    # Remove the Add TGR rig from the add menu
    bpy.types.VIEW3D_MT_add.remove(object_add_draw_menu)
    
    # Clear keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

    # Remove properties from the armature object
    del bpy.types.Object.tgr_props
    del bpy.types.Object.tgr_layer_collection

    # Unregister classes
    for cls in CLASSES_TO_REGISTER:
        bpy.utils.unregister_class(cls)
