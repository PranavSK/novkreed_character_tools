import bpy

from bpy.props import (
    IntProperty,
    StringProperty,
    PointerProperty,
    BoolVectorProperty,
    EnumProperty,
    BoolProperty
)
from bpy.types import PropertyGroup
from ..utils.armature import validate_target_armature


def on_update_selected_action_index(self, context):
    if not validate_target_armature(context.scene):
        self.report({'WARN'}, "No target armature.")
        return

    tool = context.scene.novkreed_character_tools
    idx = tool.selected_action_index
    if idx is None or not (0 <= idx < len(bpy.data.actions)):
        self.report({'INFO'}, "Nothing selected in the list.")
        return

    target_armature = tool.target_object
    selected_action = bpy.data.actions[idx]
    target_armature.animation_data.action = selected_action
    context.scene.frame_current = 1
    context.scene.frame_end = selected_action.frame_range[1]


class NCT_AddonProperties(PropertyGroup):
    '''Property container for options and paths of Mixamo Tools'''
    target_object: PointerProperty(
        name="Armature",
        description="The target armature into which the animations are merged",
        type=bpy.types.Object
    )
    # Exporters
    character_export_character_name: StringProperty(
        name="Character Name",
        description="The name of the character, used as name of the export",
        default="CharacterName"
    )
    character_export_path: StringProperty(
        name="Export Path",
        description="The path for quick character export",
        subtype="DIR_PATH",
        default="//"
    )
    character_export_format: EnumProperty(
        name="Export Format",
        description="Choose format for quick export",
        items=[
            ("GLTF", "GLTF", "", 0),
            ("GLB", "GLB", "", 1)
        ],
        default=None,
    )
    # Animations
    selected_action_index: IntProperty(
        name="Active Index",
        description="The index of the active animation in list",
        update=on_update_selected_action_index
    )
    trim_animation_from: IntProperty(
        name="From Frame",
        description="The desired start trim frame",
        default=1,
        min=0,
        max=1024
    )
    trim_animation_to: IntProperty(
        name="To Frame",
        description="The desired end trim frame",
        default=1,
        min=0,
        max=1024
    )
    # RootMotion Variables
    rootmotion_name: StringProperty(
        name="Root Bone Name",
        description="Choose name you want for the RootMotion Bone",
        maxlen=1024,
        default="root"
    )
    is_rootmotion_all: BoolProperty(
        name="Apply Rootmotion To All",
        description="Apply rootmotion to all animations",
        default=False
    )
    rootmotion_hip_bone: StringProperty(
        name="Hip Bone",
        description=(
            "Bone which will used to bake the root motion." +
            " Usually hips or pelvis"
        ),
        default="pelvis"
    )
    rootmotion_start_frame: IntProperty(
        name="Rootmotion Start Frame",
        description="The initial frame for rootmotion bake",
        default=1,
        min=-1,
        max=1024
    )
    rootmotion_use_translation: BoolVectorProperty(
        name="Bake Translation",
        description="Process the selected axes for rootmotion bake.",
        subtype='XYZ',
        size=3,
        default=(True, True, True)
    )
    rootmotion_on_ground: BoolProperty(
        name="On Ground",
        description="Keep the Z axis +ve for rootmotion bake.",
        default=True
    )
    rootmotion_use_rotation: BoolProperty(
        name="Bake Rotation",
        description=(
            "Process the rotation about Z axes" +
            " for rootmotion bake."
        ),
        default=True
    )
    rootmotion_use_rest_pose: BoolProperty(
        name="Use Rest Pose",
        description=(
            "Use rest pose as reference for calculating the change of" +
            " transforms for the hip. This is useful when animation starts" +
            " in air etc."
        ),
        default=False
    )