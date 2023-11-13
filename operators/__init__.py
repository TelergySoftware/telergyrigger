# Add classes from tgr_object_mode_operators
from .tgr_object_mode_operators import (TGR_OT_AddTGRArmature)
# Add classes from tgr_utilities_operators
from .tgr_utilities_operators import (TGR_OT_AddPrefix,
                                      TGR_OT_AddSuffix,
                                      TGR_OT_CleanNameUp,
                                      TGR_OT_RenameCollection,
                                      TGR_OT_RemoveCollection,
                                      TGR_OT_RemovePrefix,
                                      TGR_OT_RemoveSuffix,
                                      TGR_OT_SelectBonesByName,
                                      TGR_OT_SelectCollectionBones,
                                      TGR_OT_AssignBonesToCollection,
                                      TGR_OT_LockBonesFromCollection,
                                      TGR_OT_NewCollection)
# Add classes from tgr_edit_mode_operators
from .tgr_edit_mode_operators import (TGR_OT_AddNonDeformBone,
                                      TGR_OT_AlignBoneToWorld,
                                      TGR_OT_BoneOnPoints,
                                      TGR_OT_ConnectBones,
                                      TGR_OT_CreateTGT,
                                      TGR_OT_RemoveTGT,
                                      TGR_OT_ParentToRoot,
                                      TGR_OT_AddDeformBone,
                                      TGR_OT_CopyTransforms)
# Add classes from tgr_pose_mode_operators
from .tgr_pose_mode_operators import (TGR_OT_BindTGT,
                                      TGR_OT_CopyTransformsToChain,
                                      TGR_OT_CreateIkFkSwitchChain,
                                      TGR_OT_CreateIKPoleTarget,
                                      TGR_OT_CreateRotationChain,
                                      TGR_OT_CreateStretchToChain,
                                      TGR_OT_IsolateBoneRotation,
                                      TGR_OT_UnbindTGT)
# Add classes from tgr_ui_operators
from .tgr_ui_operators import (TGR_OT_GenerateUI,
                               TGR_OT_RIG_UI_AddComponent,
                               TGR_OT_RIG_UI_ModifyItem,
                               TGR_OT_RIG_UI_RemoveItem,
                               TGR_OT_RIG_UI_Clear,)

__all__ = [
    # Edit Mode Operators
    TGR_OT_AddDeformBone,
    TGR_OT_AddNonDeformBone,
    TGR_OT_AlignBoneToWorld,
    TGR_OT_BoneOnPoints,
    TGR_OT_ConnectBones,
    TGR_OT_CreateTGT,
    TGR_OT_RemoveTGT,
    TGR_OT_ParentToRoot,
    # Object Mode Operators
    TGR_OT_AddTGRArmature,
    # Pose Mode Operators
    TGR_OT_BindTGT,
    TGR_OT_CreateIkFkSwitchChain,
    TGR_OT_CreateRotationChain,
    TGR_OT_CreateStretchToChain,
    TGR_OT_IsolateBoneRotation,
    TGR_OT_UnbindTGT,
    # Utilities Operators
    TGR_OT_AddPrefix,
    TGR_OT_AddSuffix,
    TGR_OT_CleanNameUp,
    TGR_OT_RenameCollection,
    TGR_OT_LockBonesFromCollection,
    TGR_OT_RemoveCollection,
    TGR_OT_RemovePrefix,
    TGR_OT_RemoveSuffix,
    TGR_OT_SelectCollectionBones,
    TGR_OT_AssignBonesToCollection,
    TGR_OT_NewCollection
]