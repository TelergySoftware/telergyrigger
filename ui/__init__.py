from . import panels, menus, node_editor


def register():
    panels.register()
    menus.register()
    node_editor.register()

def unregister():
    node_editor.unregister()
    menus.unregister()
    panels.unregister()