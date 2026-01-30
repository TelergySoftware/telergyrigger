import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

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
    TGR_OT_SetCollectionActive,
    TGR_OT_AssignBonesToCollection,
    TGR_OT_NewCollection,
    TGR_OT_AutoCorrectUseDeform,
)

from .operators import (
    TGR_OT_AddDeformBone,
    TGR_OT_AddNonDeformBone,
    TGR_OT_AlignBoneToWorld,
    TGR_OT_BoneOnPoints,
    TGR_OT_BonesOnVertices,
    TGR_OT_ConnectBones,
    TGR_OT_CreateSwitchChains,
    TGR_OT_CreateORG,
    TGR_OT_RemoveORG,
    TGR_OT_ParentToRoot,
    TGR_OT_CopyTransforms,
    TGR_OT_CreateIntermediateBone,
)

from .operators import (
    TGR_OT_BindORG,
    TGR_OT_CopyTransformsToChain,
    TGR_OT_CreateIKChain,
    TGR_OT_CreateIKPoleTarget,
    TGR_OT_CreateRotationChain,
    TGR_OT_CreateTweakChain,
    TGR_OT_IsolateBone,
    TGR_OT_UnbindORG,
    TGR_OT_AddPivotController,
    TGR_OT_FKFromTweakChain,
    TGR_OT_CreateSingleControllerStretch,
)

from .operators import (
    TGR_OT_UIPicker,
    TGR_OT_GenerateUI,
)

from .operators import (
    TGR_OT_ToggleDeformerConstraint,
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
    TGR_PT_View3D_Panel_PoseMode_ORG,
    TGR_PT_View3D_Panel_PoseMode_Constraints
)
# Utilities panel
from .ui import (
    TGR_PT_View3D_Panel_Utilities_Naming,
    TGR_PT_View3D_Panel_Utilities_Selection
)
# Bone Layers panel
from .ui import TGR_PT_View3D_Panel_BoneCollections
# Custom Properties
from .ui import TGR_PT_View3D_Panel_CustomProperties
# Menus
from .ui import (
    TGR_MT_EditMode_PieMenu,
    TGR_MT_PoseMode_Constraints_PieMenu,
    TGR_MT_EditMode_AddBone,
    TGR_MT_TrackNewLayer
)
# Rig Node Editor
from .ui import (
    # Core node system components
    TGR_RigNodeTree,
    TGR_UISocket,
    TGR_PropertySocket,
    TGR_EnumItemSocket,
    
    # Node classes
    TGR_ViewNode,
    TGR_PanelNode,
    TGR_RowNode,
    TGR_ColumnNode,
    TGR_BoxNode,
    TGR_ValueNode,
    TGR_IntegerNode,
    TGR_BooleanNode,
    TGR_StringNode,
    TGR_VectorNode,
    TGR_ColorNode,
    TGR_ObjectNode,
    TGR_PropertiesNode,
    TGR_FloatPropertyNode,
    TGR_IntegerPropertyNode,
    TGR_BooleanPropertyNode,
    TGR_StringPropertyNode,
    TGR_VectorPropertyNode,
    TGR_ColorPropertyNode,
    TGR_EnumPropertyNode,
    TGR_EnumItemNode,
)

# ----- PROPERTIES -----
from .properties import (
    TGR_Properties,
    TGR_RIG_UI_Properties,
    TGR_Collection_Properties,
)

# ----- PREFERENCES -----
from .tgr_preferences import TGR_Preferences

# Classes to register
CLASSES_TO_REGISTER = (
    # Preferences
    TGR_Preferences,
    # Operators
    TGR_OT_AddDeformBone,
    TGR_OT_AddNonDeformBone,
    TGR_OT_AddPivotController,
    TGR_OT_AddPrefix,
    TGR_OT_AddSuffix,
    TGR_OT_AddTGRArmature,
    TGR_OT_AlignBoneToWorld,
    TGR_OT_AutoCorrectUseDeform,
    TGR_OT_BindORG,
    TGR_OT_BoneOnPoints,
    TGR_OT_BonesOnVertices,
    TGR_OT_CleanNameUp,
    TGR_OT_ConnectBones,
    TGR_OT_CopyTransforms,
    TGR_OT_CopyTransformsToChain,
    TGR_OT_CreateIKChain,
    TGR_OT_CreateIKPoleTarget,
    TGR_OT_CreateIntermediateBone,
    TGR_OT_CreateSingleControllerStretch,
    TGR_OT_CreateRotationChain,
    TGR_OT_CreateSwitchChains,
    TGR_OT_CreateTweakChain,
    TGR_OT_FKFromTweakChain,
    TGR_OT_CreateORG,
    TGR_OT_RenameCollection,
    TGR_OT_UIPicker,
    TGR_OT_GenerateUI,
    TGR_OT_IsolateBone,
    TGR_OT_LockBonesFromCollection,
    TGR_OT_ParentToRoot,
    TGR_OT_RemoveCollection,
    TGR_OT_RemovePrefix,
    TGR_OT_RemoveSuffix,
    TGR_OT_RemoveORG,
    TGR_OT_SelectBonesByName,
    TGR_OT_SelectCollectionBones,
    TGR_OT_SetCollectionActive,
    TGR_OT_ToggleDeformerConstraint,
    TGR_OT_AssignBonesToCollection,
    TGR_OT_NewCollection,
    TGR_OT_UnbindORG,
    # Panels
    TGR_PT_View3D_Panel_BoneCollections,
    TGR_PT_View3D_Panel_CustomProperties,
    TGR_PT_View3D_Panel_EditMode,
    TGR_PT_View3D_Panel_EditMode_Create,
    TGR_PT_View3D_Panel_EditMode_Parenting,
    TGR_PT_View3D_Panel_EditMode_Utilities,
    TGR_PT_View3D_Panel_PoseMode,
    TGR_PT_View3D_Panel_PoseMode_Constraints,
    TGR_PT_View3D_Panel_PoseMode_ORG,
    TGR_PT_View3D_Panel_Utilities,
    TGR_PT_View3D_Panel_Utilities_Naming,
    TGR_PT_View3D_Panel_Utilities_Selection,
    # Menus
    TGR_MT_EditMode_PieMenu,
    TGR_MT_EditMode_AddBone,
    TGR_MT_TrackNewLayer,
    TGR_MT_PoseMode_Constraints_PieMenu,
    # Node Editor
    TGR_RigNodeTree,
    TGR_PanelNode,
    TGR_ViewNode,
    TGR_RowNode,
    TGR_ColumnNode,
    TGR_BoxNode,
    TGR_UISocket,
    TGR_PropertySocket,
    TGR_EnumItemSocket,
    TGR_ValueNode,
    TGR_IntegerNode,
    TGR_BooleanNode,
    TGR_StringNode,
    TGR_VectorNode,
    TGR_ColorNode,
    TGR_ObjectNode,
    TGR_EnumItemNode,
    TGR_PropertiesNode,
    TGR_FloatPropertyNode,
    TGR_IntegerPropertyNode,
    TGR_BooleanPropertyNode,
    TGR_StringPropertyNode,
    TGR_VectorPropertyNode,
    TGR_ColorPropertyNode,
    TGR_EnumPropertyNode,
    # Properties
    TGR_Properties,
    TGR_RIG_UI_Properties,
    TGR_Collection_Properties,
)


# Node Editor categories
class TGR_NodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'TGR_RigNodeTree'

node_categories = [
    TGR_NodeCategory("TGR_OUTPUT", "Output", items=[
        NodeItem("TGR_ViewNode"),
    ]),
    TGR_NodeCategory("INPUT_NODES", "Input", items=[
        NodeItem("TGR_StringNode"),
        NodeItem("TGR_IntegerNode"),
        NodeItem("TGR_ValueNode"),
        NodeItem("TGR_BooleanNode"),
        NodeItem("TGR_VectorNode"),
        NodeItem("TGR_ColorNode"),
        NodeItem("TGR_ObjectNode"),
        NodeItem("TGR_EnumItemNode"),
    ]),
    TGR_NodeCategory("TGR_UI", "UI", items=[
        NodeItem("TGR_PanelNode"),
        NodeItem("TGR_RowNode"),
        NodeItem("TGR_ColumnNode"),
        NodeItem("TGR_BoxNode"),
    ]),
    TGR_NodeCategory("PROPERTY_NODES", "Property", items=[
        NodeItem("TGR_PropertiesNode"),
        NodeItem("TGR_FloatPropertyNode"),
        NodeItem("TGR_IntegerPropertyNode"),
        NodeItem("TGR_BooleanPropertyNode"),
        NodeItem("TGR_StringPropertyNode"),
        NodeItem("TGR_VectorPropertyNode"),
        NodeItem("TGR_ColorPropertyNode"),
        NodeItem("TGR_EnumPropertyNode"),
    ]),
]


# Keymaps reference
keymaps = []


# Object Mode Add menu appendix
def object_add_draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("tgr.add_tgr_armature", text="TGR Armature", icon="OUTLINER_OB_ARMATURE")


# Node Tree Header draw appendix
def header_draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("tgr.generate_ui", text="Generate UI", icon="PLAY")


def register():
    # Register classes
    for cls in CLASSES_TO_REGISTER:
        bpy.utils.register_class(cls)
        
    # Register node categories
    nodeitems_utils.register_node_categories("TGR_NODE_CATEGORIES", node_categories)

    # Add properties to the armature object
    bpy.types.Object.tgr_props = bpy.props.PointerProperty(type=TGR_Properties)
    bpy.types.Object.tgr_collections = bpy.props.PointerProperty(type=TGR_Collection_Properties)
    bpy.types.Object.tgr_rig_ui_props = bpy.props.PointerProperty(type=TGR_RIG_UI_Properties)

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
    # Append the Generate UI button to the node editor header
    bpy.types.NODE_HT_header.append(header_draw_menu)


def unregister():
    # Unregister node categories
    nodeitems_utils.unregister_node_categories("TGR_NODE_CATEGORIES")
    # Remove the Add TGR rig from the add menu
    bpy.types.VIEW3D_MT_add.remove(object_add_draw_menu)
    # Remove the Generate UI button from the node editor header
    bpy.types.NODE_HT_header.remove(header_draw_menu)

    # Clear keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

    # Remove properties from the armature object
    del bpy.types.Object.tgr_collections
    del bpy.types.Object.tgr_props

    # Unregister classes
    for cls in CLASSES_TO_REGISTER:
        bpy.utils.unregister_class(cls)
