import sys
import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")


def apply_pose_asset(override_context: typing.
                     Union[typing.Dict, 'bpy.types.Context'] = None,
                     execution_context: typing.Union[str, int] = None,
                     undo: bool = None,
                     *,
                     blend_factor: float = 1.0,
                     flipped: bool = False):
    ''' Apply the given Pose Action to the rig

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses
    :type blend_factor: float
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: bool
    '''

    pass


def apply_pose_asset_for_keymap(
        override_context: typing.Union[typing.
                                       Dict, 'bpy.types.Context'] = None,
        execution_context: typing.Union[str, int] = None,
        undo: bool = None):
    ''' Apply the given Pose Action to the rig :file: `addons/pose_library/operators.py\:438 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$438>`_

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    '''

    pass


def blend_pose_asset(override_context: typing.
                     Union[typing.Dict, 'bpy.types.Context'] = None,
                     execution_context: typing.Union[str, int] = None,
                     undo: bool = None,
                     *,
                     blend_factor: float = 0.0,
                     flipped: bool = False,
                     release_confirm: bool = False):
    ''' Blend the given Pose Action to the rig

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses
    :type blend_factor: float
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: bool
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button
    :type release_confirm: bool
    '''

    pass


def blend_pose_asset_for_keymap(
        override_context: typing.Union[typing.
                                       Dict, 'bpy.types.Context'] = None,
        execution_context: typing.Union[str, int] = None,
        undo: bool = None):
    ''' Blend the given Pose Action to the rig :file: `addons/pose_library/operators.py\:406 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$406>`_

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    '''

    pass


def convert_old_object_poselib(
        override_context: typing.Union[typing.
                                       Dict, 'bpy.types.Context'] = None,
        execution_context: typing.Union[str, int] = None,
        undo: bool = None):
    ''' Create a pose asset for each pose marker in this legacy pose library data-block :file: `addons/pose_library/operators.py\:494 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$494>`_

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    '''

    pass


def convert_old_poselib(override_context: typing.
                        Union[typing.Dict, 'bpy.types.Context'] = None,
                        execution_context: typing.Union[str, int] = None,
                        undo: bool = None):
    ''' Create a pose asset for each pose marker in the current action :file: `addons/pose_library/operators.py\:460 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$460>`_

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    '''

    pass


def copy_as_asset(override_context: typing.
                  Union[typing.Dict, 'bpy.types.Context'] = None,
                  execution_context: typing.Union[str, int] = None,
                  undo: bool = None):
    ''' Create a new pose asset on the clipboard, to be pasted into an Asset Browser :file: `addons/pose_library/operators.py\:211 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$211>`_

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    '''

    pass


def create_pose_asset(override_context: typing.
                      Union[typing.Dict, 'bpy.types.Context'] = None,
                      execution_context: typing.Union[str, int] = None,
                      undo: bool = None,
                      *,
                      pose_name: str = "",
                      activate_new_action: bool = True):
    ''' Create a new Action that contains the pose of the selected bones, and mark it as Asset. The asset will be stored in the current blend file

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param pose_name: Pose Name
    :type pose_name: str
    :param activate_new_action: Activate New Action
    :type activate_new_action: bool
    '''

    pass


def paste_asset(override_context: typing.
                Union[typing.Dict, 'bpy.types.Context'] = None,
                execution_context: typing.Union[str, int] = None,
                undo: bool = None):
    ''' Paste the Asset that was previously copied using Copy As Asset :file: `addons/pose_library/operators.py\:286 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$286>`_

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    '''

    pass


def pose_asset_select_bones(override_context: typing.
                            Union[typing.Dict, 'bpy.types.Context'] = None,
                            execution_context: typing.Union[str, int] = None,
                            undo: bool = None,
                            *,
                            select: bool = True,
                            flipped: bool = False):
    ''' Select those bones that are used in this pose

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param select: Select
    :type select: bool
    :param flipped: Flipped
    :type flipped: bool
    '''

    pass


def restore_previous_action(override_context: typing.
                            Union[typing.Dict, 'bpy.types.Context'] = None,
                            execution_context: typing.Union[str, int] = None,
                            undo: bool = None):
    ''' Switch back to the previous Action, after creating a pose asset :file: `addons/pose_library/operators.py\:164 <https://developer.blender.org/diffusion/BA/addons/pose_library/operators.py$164>`_

    :type override_context: typing.Union[typing.Dict, 'bpy.types.Context']
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    '''

    pass
