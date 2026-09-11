import bpy
# Add classes from tgr_edit_mode_operators
from .tgr_edit_mode_operators import (TGR_OT_AddDeformBone,
                                      TGR_OT_AddNonDeformBone,
                                      TGR_OT_AlignBoneToWorld,
                                      TGR_OT_BoneOnPoints,
                                      TGR_OT_BonesOnVertices,
                                      TGR_OT_ConnectBones,
                                      TGR_OT_CopyTransforms,
                                      TGR_OT_CreateIntermediateBone,
                                      TGR_OT_CreateORG,
                                      TGR_OT_CreateSwitchChains,
                                      TGR_OT_ParentToRoot,
                                      TGR_OT_RemoveORG,)
# Add classes from tgr_object_mode_operators
from .tgr_object_mode_operators import (TGR_OT_AddTGRArmature,)
# Add classes from tgr_pose_mode_operators
from .tgr_pose_mode_operators import (TGR_OT_AddPivotController,
                                      TGR_OT_BindORG,
                                      TGR_OT_BindSwitch,
                                      TGR_OT_CopyTransformsToChain,
                                      TGR_OT_CreateIKChain,
                                      TGR_OT_CreateIKPoleTarget,
                                      TGR_OT_CreateRotationChain,
                                      TGR_OT_CreateSingleControllerStretch,
                                      TGR_OT_CreateTweakChain,
                                      TGR_OT_FKFromTweakChain,
                                      TGR_OT_IsolateBone,
                                      TGR_OT_UnbindORG,
                                      TGR_OT_SampleTransforms,)
# Add classes from tgr_ui_operators
from .tgr_ui_operators import (
                               TGR_OT_CreateExecutable,
                               TGR_OT_GenerateUI,
                               )
# Add classes from tgr_utilities_operators
from .tgr_utilities_operators import (TGR_OT_AddPrefix,
                                      TGR_OT_AddSuffix,
                                      TGR_OT_AssignBonesToCollection,
                                      TGR_OT_AutoColorBones,
                                      TGR_OT_AutoCorrectUseDeform,
                                      TGR_OT_CleanNameUp,
                                      TGR_OT_LoadCollections,
                                      TGR_OT_LockBonesFromCollection,
                                      TGR_OT_NewCollection,
                                      TGR_OT_RemoveCollection,
                                      TGR_OT_RemovePrefix,
                                      TGR_OT_RemoveSuffix,
                                      TGR_OT_RenameCollection,
                                      TGR_OT_SaveCollections,
                                      TGR_OT_SelectBonesByName,
                                      TGR_OT_SelectCollectionBones,
                                      TGR_OT_SetCollectionActive,)
# Add classes from tgr_weight_paint_operators
from .tgr_weight_paint_operators import (TGR_OT_ToggleDeformerConstraint,
                                         TGR_OT_ActivateBrush,
                                         TGR_OT_LoadWPBrushes,
                                         TGR_OT_WP_CleanUp,)
# Add classes from tgr_presset_operators
from .tgr_presset_operators import (TGR_OT_Create_Tweak_FK_Chain,
                                    TGR_OT_Create_IKFK_Switch,)



OPERATOR_CLASSES = [
    # Edit Mode Operators
    TGR_OT_AddDeformBone,
    TGR_OT_AddNonDeformBone,
    TGR_OT_AlignBoneToWorld,
    TGR_OT_BoneOnPoints,
    TGR_OT_BonesOnVertices,
    TGR_OT_ConnectBones,
    TGR_OT_CopyTransforms,
    TGR_OT_CreateIntermediateBone,
    TGR_OT_CreateORG,
    TGR_OT_CreateSwitchChains,
    TGR_OT_ParentToRoot,
    TGR_OT_RemoveORG,

    # Object Mode Operators
    TGR_OT_AddTGRArmature,

    # Pose Mode Operators
    TGR_OT_AddPivotController,
    TGR_OT_BindORG,
    TGR_OT_BindSwitch,
    TGR_OT_CopyTransformsToChain,
    TGR_OT_CreateIKChain,
    TGR_OT_CreateIKPoleTarget,
    TGR_OT_CreateRotationChain,
    TGR_OT_CreateSingleControllerStretch,
    TGR_OT_CreateTweakChain,
    TGR_OT_FKFromTweakChain,
    TGR_OT_IsolateBone,
    TGR_OT_UnbindORG,
    TGR_OT_SampleTransforms,

    # UI Operators
    TGR_OT_CreateExecutable,
    TGR_OT_GenerateUI,

    # Utilities Operators
    TGR_OT_AddPrefix,
    TGR_OT_AddSuffix,
    TGR_OT_AssignBonesToCollection,
    TGR_OT_AutoColorBones,
    TGR_OT_AutoCorrectUseDeform,
    TGR_OT_CleanNameUp,
    TGR_OT_LoadCollections,
    TGR_OT_LockBonesFromCollection,
    TGR_OT_NewCollection,
    TGR_OT_RemoveCollection,
    TGR_OT_RemovePrefix,
    TGR_OT_RemoveSuffix,
    TGR_OT_RenameCollection,
    TGR_OT_SaveCollections,
    TGR_OT_SelectBonesByName,
    TGR_OT_SelectCollectionBones,
    TGR_OT_SetCollectionActive,

    # Weight Paint Operators
    TGR_OT_ToggleDeformerConstraint,
    TGR_OT_ActivateBrush,
    TGR_OT_LoadWPBrushes,
    TGR_OT_WP_CleanUp,

    # Presset Operators
    TGR_OT_Create_Tweak_FK_Chain,
    TGR_OT_Create_IKFK_Switch,
]


def register():
    for cls in OPERATOR_CLASSES:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(OPERATOR_CLASSES):
        bpy.utils.unregister_class(cls)


