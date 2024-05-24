"""
Utility functions
"""
import os
import bpy

def get_collection_index(name: str) -> tuple[int, bool]:
    """
    Return the index of a collection by name.
    """
    try:
        collection = bpy.context.active_object.data.collections_all[name]
        return collection.index, True
    except KeyError:
        return -1, False


def get_addon_name():
    return os.path.basename(os.path.dirname(__file__))


def change_bones_prefix(bones, old_prefix: str = "", prefix: str = ""):
    """
    Change the prefix of all bones.
    """
    if old_prefix == prefix:
        return
    if old_prefix == "":
        for bone in bones:
            bone.name = prefix + bone.name
            # Remove the .### suffix if any
            bone.name = bone.name.split(".")[:-1].join(".")
    else:
        for bone in bones:
            if bone.name.startswith(old_prefix):
                bone.name = bone.name.replace(old_prefix, prefix)

            # Remove the .### suffix if any
            split_name = bone.name.split(".")[:-1]
            new_name = ""
            if len(split_name) > 1:
                for i in range(len(split_name)):
                    new_name += split_name[i] + "." if i < len(split_name) - 1 else split_name[i]
            else:
                new_name = split_name[0]
            bone.name = new_name


def set_bones_deform(bones, deform: bool):
    """
    Set the deform property of all bones.
    """
    for bone in bones:
        bone.use_deform = deform
