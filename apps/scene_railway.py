#!/usr/bin/env python3

# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0
# Author (©): Alvaro del Castillo
import sys

import mcpi.block
import mcpi.minecraft

from mcthings.decorators.border_decorator import BorderDecorator
from mcthings.server import Server
from mcthings.world import World

from apps.scene_interactive import SceneInteractive

BUILDER_NAME = "ElasticExplorer"

MC_SEVER_HOST = "localhost"
MC_SEVER_PORT = 4711
EVENTS_PER_CLICK = 3
CHECK_EVENTS_TIME = 2


class SceneRailway(SceneInteractive):
    """
    Scene Railway

    A complex Scene with a railway around it
    """

    @classmethod
    def add_railway(cls):
        scene = World.first_scene()
        # Add a Railway around the scene
        border = BorderDecorator
        border.block = mcpi.block.RAIL
        border.margin = 5
        scene.add_decorator(border)
        scene.decorate()

    @classmethod
    def build_scene(cls):
        cls.build_river()
        cls.build_bridges()
        cls.build_paths()
        cls.build_houses()
        cls.build_temple()
        cls.build_jail()
        cls.build_buildings()
        cls.build_stadium()
        cls.add_railway()

    @classmethod
    def main(cls):
        try:
            World.connect(Server(MC_SEVER_HOST, MC_SEVER_PORT))

            World.server.postToChat("Checking railway in a big Scene")
            cls.pos = World.server.entity.getTilePos(World.server.getPlayerEntityId(BUILDER_NAME))
            cls.pos.x += 1

            cls.build_scene()

        except mcpi.connection.RequestError:
            print("Can't connect to Minecraft server " + MC_SEVER_HOST)


if __name__ == "__main__":
    SceneRailway.main()
    sys.exit(0)
