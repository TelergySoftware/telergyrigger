import bpy


class TGR_MT_PoseMode_Constraints_PieMenu(bpy.types.Menu):
    """
    Pose Mode Pie Menu.
    """
    bl_idname = "TGR_MT_PoseMode_Constraints_PieMenu"
    bl_label = "Constraints"

    @classmethod
    def poll(cls, context):
        is_armature = context.object.type == 'ARMATURE'
        is_pose_mode = context.mode == 'POSE'
        return is_armature and is_pose_mode

    def draw(self, context):
        bones_selected = len(context.selected_pose_bones) > 0
        if not bones_selected:
            # Warning message
            self.layout.label(text="No bones selected", icon='ERROR')
            return
        layout = self.layout
        # - Pie menu LEFT
        pie = layout.menu_pie()
        col = pie.column()
        col.label(text="Copy Constraints")
        col.operator("pose.constraint_add_with_targets", text="Copy Transforms",
                     icon='CON_TRANSLIKE').type = 'COPY_TRANSFORMS'
        col.separator()
        col.operator("pose.constraint_add_with_targets", text="Copy Rotation",
                     icon='CON_ROTLIKE').type = 'COPY_ROTATION'
        col.operator("pose.constraint_add_with_targets", text="Copy Location",
                     icon='CON_LOCLIKE').type = 'COPY_LOCATION'
        col.operator("pose.constraint_add_with_targets", text="Copy Scale", icon='CON_SIZELIKE').type = 'COPY_SCALE'
        # - Pie menu RIGHT
        pie = layout.menu_pie()
        col = pie.column()
        col.label(text="Limit Constraints")
        col.operator("pose.constraint_add_with_targets", text="Limit Distance",
                     icon='CON_DISTLIMIT').type = 'LIMIT_DISTANCE'
        col.separator()
        col.operator("pose.constraint_add_with_targets", text="Limit Location",
                     icon='CON_LOCLIMIT').type = 'LIMIT_LOCATION'
        col.operator("pose.constraint_add_with_targets", text="Limit Rotation",
                     icon='CON_ROTLIMIT').type = 'LIMIT_ROTATION'
        col.operator("pose.constraint_add_with_targets", text="Limit Scale",
                     icon='CON_SIZELIMIT').type = 'LIMIT_SCALE'

        pie = layout.menu_pie()
        col = pie.column()
        col.operator("pose.constraint_add_with_targets", text="Damped Track",
                     icon="CON_TRACKTO").type = 'DAMPED_TRACK'
        col.operator("pose.constraint_add_with_targets", text="Stretch To", icon='CON_STRETCHTO').type = 'STRETCH_TO'

        pie.operator("pose.constraint_add_with_targets", text="Inverse Kinematics", icon='CON_KINEMATIC').type = 'IK'
