# Copyright (C) 2022 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import os
import re
from pathlib import Path
from typing import Iterator

from bootloader.humantrainer.constant.uasset import UAssetType
from bootloader.humantrainer.model.uasset import UAsset
from bootloader.humantrainer.model.uasset import UAssetAnimationSequence
from bootloader.humantrainer.model.uasset import UAssetMaterial
from bootloader.humantrainer.model.uasset import UAssetMaterialInstance
from bootloader.humantrainer.model.uasset import UAssetSkeletalMesh
from bootloader.humantrainer.model.uasset import UAssetTexture


# The default extension (suffix) of a Unreal Editor asset file.
UASSET_FILE_EXTENSION = '.uasset'

# List of the uasset file name prefixes for each type of asset.
BOOTLOADER_UASSET_FILE_NAME_PREFIX_ANIMATION_SEQUENCE = 'A_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_ANIMATION_BLUEPRINT = 'ABP_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_BLUEPRINT = 'BP_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_MATERIAL = 'M_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_MATERIAL_INSTANCE = 'MI_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_PHYSICS_ASSET = 'PA_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_SKELETAL_MESH = 'SK_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_SKELETON = 'S_'
BOOTLOADER_UASSET_FILE_NAME_PREFIX_TEXTURE = 'T_'


# The regular expression to match the uasset file name of an Unreal
# Engine animation blueprint.
REGEX_BOOTLOADER_UASSET_FILE_NAME_ANIMATION_BLUEPRINT = re.compile(
    rf'^{BOOTLOADER_UASSET_FILE_NAME_PREFIX_BLUEPRINT}$'
)

# The regular expression to match the uasset file name of an Unreal
# Engine animation sequence.
REGEX_BOOTLOADER_UASSET_FILE_NAME_ANIMATION_SEQUENCE = re.compile(
    rf'^{BOOTLOADER_UASSET_FILE_NAME_PREFIX_ANIMATION_SEQUENCE}'
    rf'(?P<CharacterName>[a-zA-Z0-9]+)_'
    rf'(?P<Location>[a-zA-Z]+)$'
)

# The regular expression to match the uasset file name of an Unreal
# Engine material.
REGEX_BOOTLOADER_UASSET_FILE_NAME_MATERIAL = re.compile(
    rf'^{BOOTLOADER_UASSET_FILE_NAME_PREFIX_MATERIAL}'
    rf'(?P<CharacterName>[a-zA-Z0-9]+)_'
    rf'(?P<Location>[a-zA-Z]+)$'
)

# The regular expression to match the uasset file name of an Unreal
# # Engine material instance.
REGEX_BOOTLOADER_UASSET_FILE_NAME_MATERIAL_INSTANCE = re.compile(
    rf'^{BOOTLOADER_UASSET_FILE_NAME_PREFIX_MATERIAL_INSTANCE}_'
    rf'(?P<CharacterName>[a-zA-Z0-9]+)_'
    rf'(?P<Location>[a-zA-Z]+)$'
)

# The regular expression to match the uasset file name of an Unreal
# Engine physics asset.
REGEX_BOOTLOADER_UASSET_FILE_NAME_PHYSICS_ASSET = re.compile(
    rf'^{BOOTLOADER_UASSET_FILE_NAME_PREFIX_PHYSICS_ASSET}$'
)

# The regular expression to match the uasset file name of an Unreal
# Engine skeletal mesh.
REGEX_BOOTLOADER_UASSET_FILE_NAME_SKELETAL_MESH = re.compile(
    rf'^{BOOTLOADER_UASSET_FILE_NAME_PREFIX_SKELETAL_MESH}'
    rf'(?P<CharacterName>[a-zA-Z0-9]+)_'
    rf'(?P<Location>[a-zA-Z0-9]+)_'
    rf'(?P<Base>[a-zA-Z]+)$'
)

# The regular expression to match the uasset file name of an Unreal
# Engine texture.
REGEX_BOOTLOADER_UASSET_FILE_NAME_TEXTURE = re.compile(
    rf'^{BOOTLOADER_UASSET_FILE_NAME_PREFIX_TEXTURE}'
    rf'(?P<CharacterName>[a-zA-Z0-9]+)_'
    rf'(?P<Location>[a-zA-Z]+)_'
    rf'(?P<MapType>[a-zA-Z0-9]+)_'
    rf'((?P<MapSubType>[a-zA-Z0-9]+)_)?'
    rf'(?P<Suffix>[a-zA-Z]+)$'
)


class BootloaderUAssetNamingConventionViolationException(Exception):
    """
    Indicate that the name of an Unreal Engine asset file is not
    respecting the established Bootloader's naming convention.
    """
    def __init__(self, file_path: Path, asset_type: UAssetType = None):
        self.__file_path = file_path
        self.__asset_type = asset_type

    @property
    def asset_type(self) -> UAssetType:
        return self.__asset_type

    @property
    def file_path(self) -> Path:
        return self.__file_path


def find_uasset_files(root_path: str) -> Iterator[Path]:
    """
    Return the list of Unreal Engine asset files


    @param root_path: The path to the root folder where to start searching
        for Unreal Engine asset files.


    @return: A generator iterator of Unreal Engine asset file's path and
        name.
    """
    for directory_path, directory_names, file_names in os.walk(os.path.expanduser(root_path)):
        for file_name in file_names:
            if file_name.endswith(UASSET_FILE_EXTENSION):
                yield Path(os.path.join(directory_path, file_name))


def is_uasset_file_animation_sequence(file_path: Path) -> bool:
    """
    Indicate whether the specified file corresponds to a Bootloader Unreal
    Engine animation sequence asset.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: `True` if the file corresponds to a Bootloader Unreal Engine
        animation sequence asset; `False` otherwise.
    """
    return file_path.stem.startswith(BOOTLOADER_UASSET_FILE_NAME_PREFIX_ANIMATION_SEQUENCE)


def is_uasset_file_material(file_path: Path) -> bool:
    """
    Indicate whether the specified file corresponds to a Bootloader Unreal
    Engine material asset.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: `True` if the file corresponds to a Bootloader Unreal Engine
        material asset; `False` otherwise.
    """
    return file_path.stem.startswith(BOOTLOADER_UASSET_FILE_NAME_PREFIX_MATERIAL)


def is_uasset_file_material_instance(file_path: Path) -> bool:
    """
    Indicate whether the specified file corresponds to a Bootloader Unreal
    Engine material instance asset.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: `True` if the file corresponds to a Bootloader Unreal Engine
        material instance asset; `False` otherwise.
    """
    return file_path.stem.startswith(BOOTLOADER_UASSET_FILE_NAME_PREFIX_MATERIAL_INSTANCE)


def is_uasset_file_skeletal_mesh(file_path: Path) -> bool:
    """
    Indicate whether the specified file corresponds to a Bootloader Unreal
    Engine skeletal mesh asset.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: `True` if the file corresponds to a Bootloader Unreal Engine
        skeletal mesh asset; `False` otherwise.
    """
    return file_path.stem.startswith(BOOTLOADER_UASSET_FILE_NAME_PREFIX_SKELETAL_MESH)


def is_uasset_file_texture(file_path: Path) -> bool:
    """
    Indicate whether the specified file corresponds to a Bootloader Unreal
    Engine texture asset.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: `True` if the file corresponds to a Bootloader Unreal Engine
        texture asset; `False` otherwise.
    """
    return file_path.stem.startswith(BOOTLOADER_UASSET_FILE_NAME_PREFIX_TEXTURE)


def parse_uasset_file(file_path: Path) -> UAsset:
    """
    Parse an Unreal Engine asset file

    @param file_path: The path and name of an Unreal Engine asset file.


    @return: An object representing an Unreal Engine asset.


    @raise BootloaderNamingConventionViolationException: If the name of
        the file doesn't respect the Bootloader's naming convention.
    """
    if is_uasset_file_animation_sequence(file_path):
        return parse_uasset_file_animation_sequence(file_path)
    elif is_uasset_file_material(file_path):
        return parse_uasset_file_material(file_path)
    elif is_uasset_file_material_instance(file_path):
        return parse_uasset_file_material_instance(file_path)
    elif is_uasset_file_skeletal_mesh(file_path):
        return parse_uasset_file_skeletal_mesh(file_path)
    elif is_uasset_file_texture(file_path):
        return parse_uasset_file_texture(file_path)
    else:
        raise BootloaderUAssetNamingConventionViolationException(file_path)


def parse_uasset_file_animation_sequence(file_path: Path) -> UAssetAnimationSequence:
    """
    Parse an Unreal Engine asset file representing an animation sequence.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: An object representing an Unreal Engine animation sequence.


    @raise BootloaderNamingConventionViolationException: If the name of
        the file doesn't respect the Bootloader's naming convention.
    """
    match = REGEX_BOOTLOADER_UASSET_FILE_NAME_ANIMATION_SEQUENCE.match(file_path.stem)
    if not match:
        raise BootloaderUAssetNamingConventionViolationException(file_path, asset_type=UAssetType.AnimationSequence)


def parse_uasset_file_material(file_path: Path) -> UAssetMaterial:
    """
    Parse an Unreal Engine asset file representing a material.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: An object representing an Unreal Engine material.


    @raise BootloaderNamingConventionViolationException: If the name of
        the file doesn't respect the Bootloader's naming convention.
    """
    match = REGEX_BOOTLOADER_UASSET_FILE_NAME_MATERIAL.match(file_path.stem)
    if not match:
        raise BootloaderUAssetNamingConventionViolationException(file_path, asset_type=UAssetType.Material)


def parse_uasset_file_material_instance(file_path: Path) -> UAssetMaterialInstance:
    """
    Parse an Unreal Engine asset file representing a material instance.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: An object representing an Unreal Engine material instance.


    @raise BootloaderNamingConventionViolationException: If the name of
        the file doesn't respect the Bootloader's naming convention.
    """
    match = REGEX_BOOTLOADER_UASSET_FILE_NAME_MATERIAL_INSTANCE.match(file_path.stem)
    if not match:
        raise BootloaderUAssetNamingConventionViolationException(file_path, asset_type=UAssetType.MaterialInstance)


def parse_uasset_file_skeletal_mesh(file_path: Path) -> UAssetSkeletalMesh:
    """
    Parse an Unreal Engine asset file representing a skeletal mesh.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: An object representing an Unreal Engine skeletal mesh.


    @raise BootloaderNamingConventionViolationException: If the name of
        the file doesn't respect the Bootloader's naming convention.
    """
    match = REGEX_BOOTLOADER_UASSET_FILE_NAME_SKELETAL_MESH.match(file_path.stem)
    if not match:
        raise BootloaderUAssetNamingConventionViolationException(file_path, asset_type=UAssetType.SkeletalMesh)


def parse_uasset_file_texture(file_path: Path) -> UAssetTexture:
    """
    Parse an Unreal Engine asset file representing a texture.


    @param file_path: The path and name of an Unreal Engine asset file.


    @return: An object representing an Unreal Engine texture.


    @raise BootloaderNamingConventionViolationException: If the name of
        the file doesn't respect the Bootloader's naming convention.
    """
    match = REGEX_BOOTLOADER_UASSET_FILE_NAME_TEXTURE.match(file_path.stem)
    if not match:
        raise BootloaderUAssetNamingConventionViolationException(file_path, asset_type=UAssetType.Texture)


def validate_uasset_file_name(file_path: Path) -> None:
    parse_uasset_file(file_path)  # @todo: Replace with a function that only checks
