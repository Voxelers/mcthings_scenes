#!/usr/bin/env python3

# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0
# Author (©): Alvaro del Castillo

import sys
import time

import mcpi.block
import mcpi.minecraft

from mcthings.scene import Scene
from mcthings.server import Server
from mcthings.world import World

BUILDER_NAME = "ElasticExplorer"

MC_SEVER_HOST = "localhost"
MC_SEVER_PORT = 4711


def main():
    try:
        World.connect(Server(MC_SEVER_HOST, MC_SEVER_PORT))
        scene_path = "scene_basic.mct"
        World.server.postToChat("Building a scene from " + scene_path)
        pos = World.server.entity.getTilePos(World.server.getPlayerEntityId(BUILDER_NAME))
        pos.z += 10

        World.server.postToChat("Cleaning a scene")

        # Let's load the scene and build it
        scene = Scene()
        scene.load(scene_path)
        # Move the scene to the player position
        scene.reposition(pos)
        scene.build()
        scene.unbuild()

    except mcpi.connection.RequestError:
        print("Can't connect to Minecraft server " + MC_SEVER_HOST)


if __name__ == "__main__":
    main()
    sys.exit(0)
