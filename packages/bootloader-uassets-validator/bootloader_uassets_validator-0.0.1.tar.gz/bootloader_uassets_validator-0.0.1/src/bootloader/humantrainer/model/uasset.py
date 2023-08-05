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


class UAsset:
    """
    An asset is any piece of content in an Unreal Engine project.  Assets
    are like building blocks that are used to create a game or an
    application.

    Assets can be of many types, such as Static Meshes, Materials, particle
    systems, and sound cues.  Some Assets are created outside Unreal Engine
    (for example, in other 3D applications like Maya or 3ds Max).  Other
    Assets, such as Blueprints, are created directly inside the engine.

    In Unreal Editor, Assets are stored in `.uasset` files, each of which
    typically contains only a single Asset.  Each Asset reference contains
    a directory-style path that uniquely identifies any Asset in the game.
    """


class UAssetAnimationBlueprint(UAsset):
    """
    Animation Blueprints are specialized Blueprints that control the
    animation of a Skeletal Mesh during simulation or gameplay.  Graphs
    are edited inside the Animation Blueprint Editor, where you can blend
    animation, control the bones of a Skeleton, or create logic that will
    define the final animation pose for a Skeletal Mesh to use per frame.
    """


class UAssetAnimationSequence(UAsset):
    """
    An Animation Sequence is an animation asset that contains animation
    data that can be played on a Skeletal Mesh to animate a character.  An
    Animation Sequence contains keyframes that specify the position,
    rotation, and scale of the Skeletal Mesh's Skeleton at specific points
    in time.  By blending between keyframes during sequential playback,
    the Skeleton's motion animates the Mesh.
    """


class UAssetMaterial(UAsset):
    """
    Materials in Unreal Engine define the surface properties of the
    objects in your scene.  In the broadest sense, you can think of a
    Material as the "paint" that is applied to a mesh to control its
    visual appearance.
    """


class UAssetMaterialInstance(UAsset):
    """
    Material Instances allow artists to quickly and easily customize
    Materials to produce multiple variations (or instances) from a single
    parent Material.

    Material instancing is used to change the appearance of a Material
    without incurring an expensive recompilation of the Material.
    """


class UAssetPhysicsAsset(UAsset):
    """
    A Physics Asset is used to define the physics and collision used by a
    Skeletal Mesh.  These contain a set of rigid bodies and constraints
    that make up a single ragdoll, which is not limited to humanoid
    ragdolls.  They can be used for any physical simulation using bodies
    and constraints.  Because only a single Physics Asset is allowed for a
    Skeletal Mesh, they can be turned on or off for many Skeletal Mesh
    components.
    """


class UAssetSkeletalMesh(UAsset):
    """
    Skeletal Meshes are made up of two parts: A set of polygons composed
    to make up the surface of the Skeletal Mesh, and a hierarchical set of
    interconnected bones which can be used to animate the vertices of the
    polygons.
    """


class UAssetTexture(UAsset):
    """
    Textures are image assets that are primarily used in Materials but can
    also be directly applied outside of Materials, like when using an
    texture for a heads up display (HUD).
    """