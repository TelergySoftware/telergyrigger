import bpy

# ----- OPERATORS -----
from .operators import (
    TGR_OT_AddPrefix,
    TGR_OT_AddSuffix,
    TGR_OT_CleanNameUp,
    TGR_OT_RenameCollection,
    TGR_OT_LockBonesFromCollection,
    TGR_OT_RemoveCollection,
    TGR_OT_RemovePrefix,
    TGR_OT_RemoveSuffix,
    TGR_OT_SelectBonesByName,
    TGR_OT_SelectCollectionBones,
    TGR_OT_AssignBonesToCollection,
    TGR_OT_NewCollection
)

from .operators import (
    TGR_OT_AddDeformBone,
    TGR_OT_AddNonDeformBone,
    TGR_OT_AlignBoneToWorld,
    TGR_OT_BoneOnPoints,
    TGR_OT_ConnectBones,
    TGR_OT_CreateTGT,
    TGR_OT_RemoveTGT,
    TGR_OT_ParentToRoot,
    TGR_OT_CopyTransforms,
)

from .operators import (
    TGR_OT_BindTGT,
    TGR_OT_CopyTransformsToChain,
    TGR_OT_CreateIkFkSwitchChain,
    TGR_OT_CreateIKPoleTarget,
    TGR_OT_CreateRotationChain,
    TGR_OT_CreateStretchToChain,
    TGR_OT_IsolateBoneRotation,
    TGR_OT_UnbindTGT
)

from .operators import (
    TGR_OT_GenerateUI,
    TGR_OT_RIG_UI_AddComponent,
    TGR_OT_RIG_UI_ModifyItem,
    TGR_OT_RIG_UI_RemoveItem,
    TGR_OT_RIG_UI_Clear
)

from .operators import TGR_OT_AddTGRArmature

# ----- UI -----
from .ui import (
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_Utilities
)
# Edit Mode panels
from .ui import (
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities
)
# Pose Mode panels
from .ui import (
    TGR_PT_View3D_Panel_PoseMode_TGT,
    TGR_PT_View3D_Panel_PoseMode_Constraints
)
# Utilities panel
from .ui import (
    TGR_PT_View3D_Panel_Utilities_Naming,
    TGR_PT_View3D_Panel_Utilities_Selection
)
# Bone Layers panel
from .ui import TGR_PT_View3D_Panel_BoneCollections
# Rig UI
# from .ui import TGR_PT_View3D_Panel_RigUI
# Custom Properties
from .ui import TGR_PT_View3D_Panel_CustomProperties
# Menus
from .ui import (
    TGR_MT_EditMode_PieMenu,
    TGR_MT_PoseMode_Constraints_PieMenu,
    TGR_MT_EditMode_AddBone,
    TGR_MT_TrackNewLayer
)

# ----- PROPERTIES -----
from .properties import (
    TGR_Properties,
    TGR_UI_Components
)

# ----- PREFERENCES -----
from .tgr_preferences import TGR_Preferences

bl_info = {
    "name": "Telergy Rigger",
    "author": "Telergy Studio",
    "description": "Supercharge your rigging workflow! Accelerate the process, automate tasks, and unleash your"
                   " creative potential like never before.",
    "blender": (3, 0, 0),
    "version": (0, 1, 0),
    "location": "",
    "warning": "Under Heavy Development",
    "category": "Rigging"
}

# Classes to register
CLASSES_TO_REGISTER = (
    # Preferences
    TGR_Preferences,
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
    TGR_OT_CopyTransforms,
    TGR_OT_CopyTransformsToChain,
    TGR_OT_CreateIKPoleTarget,
    TGR_OT_CreateIkFkSwitchChain,
    TGR_OT_CreateRotationChain,
    TGR_OT_CreateStretchToChain,
    TGR_OT_CreateTGT,
    TGR_OT_RenameCollection,
    TGR_OT_GenerateUI,
    TGR_OT_IsolateBoneRotation,
    TGR_OT_LockBonesFromCollection,
    TGR_OT_ParentToRoot,
    TGR_OT_RIG_UI_AddComponent,
    TGR_OT_RIG_UI_Clear,
    TGR_OT_RIG_UI_ModifyItem,
    TGR_OT_RIG_UI_RemoveItem,
    TGR_OT_RemoveCollection,
    TGR_OT_RemovePrefix,
    TGR_OT_RemoveSuffix,
    TGR_OT_RemoveTGT,
    TGR_OT_SelectBonesByName,
    TGR_OT_SelectCollectionBones,
    TGR_OT_AssignBonesToCollection,
    TGR_OT_NewCollection,
    TGR_OT_UnbindTGT,
    # Panels
    TGR_PT_View3D_Panel_BoneCollections,
    TGR_PT_View3D_Panel_CustomProperties,
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities,
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_PoseMode_Constraints,
    TGR_PT_View3D_Panel_PoseMode_TGT,
    # TGR_PT_View3D_Panel_RigUI,
    TGR_PT_View3D_Panel_Utilities,
    TGR_PT_View3D_Panel_Utilities_Naming,
    TGR_PT_View3D_Panel_Utilities_Selection,
    # Menus
    TGR_MT_EditMode_PieMenu,
    TGR_MT_EditMode_AddBone,
    TGR_MT_TrackNewLayer,
    TGR_MT_PoseMode_Constraints_PieMenu,
    # Properties
    TGR_Properties,
    TGR_UI_Components,
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
    bpy.types.Object.tgr_ui_components = bpy.props.CollectionProperty(type=TGR_UI_Components)

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

    # Add new Keymap
    km = wm.keyconfigs.addon.keymaps.new(name='Pose', space_type='EMPTY')
    # Add new Keymap items to call the TGR_OT_SelectBonesByName operator
    kmi = km.keymap_items.new('tgr.select_bones_by_name', 'F', 'PRESS', ctrl=True)
    kmi.active = True
    keymaps.append((km, kmi))

    # Add new Keymap
    km = wm.keyconfigs.addon.keymaps.new(name='Armature', space_type='EMPTY')
    # Add new Keymap items to call the TGR_OT_SelectBonesByName operator
    kmi = km.keymap_items.new('tgr.select_bones_by_name', 'F', 'PRESS', ctrl=True)
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
    del bpy.types.Object.tgr_ui_components
    del bpy.types.Object.tgr_props

    # Unregister classes
    for cls in CLASSES_TO_REGISTER:
        bpy.utils.unregister_class(cls)
