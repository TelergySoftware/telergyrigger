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
        # - Pie Menu UP item
        pie = layout.menu_pie()
        pie.operator("pose.constraint_add_with_targets", text="Copy Transforms", icon='CON_TRANSLIKE').type='COPY_TRANSFORMS'
        # - Pie Menu RIGHT item
        pie = layout.menu_pie()
        pie.operator("pose.constraint_add_with_targets", text="Copy Rotation", icon='CON_ROTLIKE').type='COPY_ROTATION'
        # - Pie Menu DOWN item
        pie = layout.menu_pie()
        pie.operator("pose.constraint_add_with_targets", text="Copy Location", icon='CON_LOCLIKE').type='COPY_LOCATION'
        # - Pie Menu TOP item
        pie = layout.menu_pie()
        pie.operator("pose.constraint_add_with_targets", text="Copy Scale", icon='CON_SIZELIKE').type='COPY_SCALE'
        # - Pie Menu TOP item
        pie = layout.menu_pie()
        pie.operator("pose.constraint_add_with_targets", text="Stretch To", icon='CON_STRETCHTO').type='STRETCH_TO'
        # - Pie Menu BOTTOM item
        pie = layout.menu_pie()
        pie.operator("pose.constraint_add_with_targets", text="Inverse Kinematics", icon='CON_KINEMATIC').type='IK'
