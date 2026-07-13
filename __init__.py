import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem, NodeItemCustom

from . import properties, operators, ui
from .properties import TGR_Properties, TGR_Collection_Properties

# ----- PREFERENCES -----
from .tgr_preferences import TGR_Preferences


# Node Editor categories
class TGR_DT_NodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'TGR_NT_Data'


class TGR_UI_NodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'TGR_NT_UI'

def tgr_node_separator(self, layout, context):
    layout.separator()

node_categories = [
    TGR_DT_NodeCategory("DATA_NODES", "Data", items=[
        NodeItem("TGR_DT_ND_Float"),
        NodeItem("TGR_DT_ND_Integer"),
        NodeItem("TGR_DT_ND_Boolean"),
        NodeItem("TGR_DT_ND_String"),
        NodeItem("TGR_DT_ND_Vector"),
        NodeItem("TGR_DT_ND_Color"),
        NodeItem("TGR_DT_ND_Object"),
        NodeItem("TGR_DT_ND_Enum"),
        NodeItem("TGR_DT_ND_EnumItem"),
        # Spacer
        NodeItemCustom(draw=tgr_node_separator),
        NodeItem("TGR_DT_ND_PropertyGroup"),
    ]),
    
    TGR_DT_NodeCategory("EXECUTABLE_NODES", "Executable", items=[
        NodeItem("TGR_OP_ND_Executable"),
    ]),
    
    TGR_UI_NodeCategory("UI_NODES", "Layout", items=[
        NodeItem("TGR_LY_ND_Panel"),
        NodeItemCustom(draw=tgr_node_separator),
        NodeItem("TGR_LY_ND_Row"),
        NodeItem("TGR_LY_ND_Column"),
        NodeItem("TGR_LY_ND_Box"),
        NodeItem("TGR_LY_ND_Grid"),
        NodeItemCustom(draw=tgr_node_separator),
        NodeItem("TGR_LY_ND_Separator"),
        NodeItemCustom(draw=tgr_node_separator),
        NodeItem("TGR_LY_ND_SplitItem"),
        NodeItem("TGR_LY_ND_Split"),
    ]),
    
    TGR_UI_NodeCategory("UI_OPERATOR", "Operator", items=[
        NodeItem("TGR_LY_ND_Operator"),
    ]),
    
    TGR_UI_NodeCategory("UI_ELEMENTS", "Elements", items=[
        NodeItem("TGR_LY_ND_Prop"),
        NodeItem("TGR_LY_ND_BoneCollection"),
        NodeItem("TGR_LY_ND_Label"),
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
    properties.register()
    operators.register()
    ui.register()
        
    # Register node categories
    nodeitems_utils.register_node_categories("TGR_NODE_CATEGORIES", node_categories)

    # Add properties to the armature object
    bpy.types.Object.tgr_props = bpy.props.PointerProperty(type=TGR_Properties)
    bpy.types.Object.tgr_collections = bpy.props.PointerProperty(type=TGR_Collection_Properties)
    # bpy.types.Object.tgr_rig_ui_props = bpy.props.PointerProperty(type=TGR_RIG_UI_Properties)

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
    # # Append the Generate UI button to the node editor header
    # bpy.types.NODE_HT_header.append(header_draw_menu)


def unregister():
    # Unregister node categories
    nodeitems_utils.unregister_node_categories("TGR_NODE_CATEGORIES")
    # Remove the Add TGR rig from the add menu
    bpy.types.VIEW3D_MT_add.remove(object_add_draw_menu)
    # Remove the Generate UI button from the node editor header
    # bpy.types.NODE_HT_header.remove(header_draw_menu)

    # Clear keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

    # Remove properties from the armature object
    del bpy.types.Object.tgr_collections
    del bpy.types.Object.tgr_props
    
    ui.unregister()
    operators.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()
