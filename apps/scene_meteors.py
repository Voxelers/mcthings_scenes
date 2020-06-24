#!/usr/bin/env python3

# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0
# Author (©): Alvaro del Castillo

import logging
import sys
import time

import mcpi.block
import mcpi.minecraft
from mcpi.vec3 import Vec3
from mcthings.renderers.raspberry_pi import RaspberryPi

from mcthings.sphere import SphereHollow
from mcthings.world import World

BUILDER_NAME = "ElasticExplorer"

MC_SEVER_HOST = "localhost"
MC_SEVER_PORT = 4711

METEORS_INITIAL_HEIGHT = 50
MOVE_UPDATES_TIME = 0.3
MOVE_DISTANCE = 10
DEEP_SURFACE = 5
METEOR_DISTANCE = 20
MAX_METEORS = 5


class SceneMeteors:
    """
    Scene Meteors

    A meteors storm will arrive the world and hit the surface.
    In the meteors entities will live inside.

    The movement of the meteors, spheres, will be update each
    MOVE_UPDATES_TIME
    """

    meteors = []

    @classmethod
    def move_meteors(cls):
        """ Move meteors approaching the surface """
        for meteor in cls.meteors:
            p = meteor.position
            if p.y >= -DEEP_SURFACE:
                meteor.move(Vec3(p.x, p.y - 1, p.z))
            else:
                logging.info("Meteor hits surface")
                sys.exit(0)

    @classmethod
    def build_meteors(cls):

        for i in range(1, MAX_METEORS + 1):
            p = cls.pos
            radius = 5
            meteor = SphereHollow(Vec3(p.x + i * METEOR_DISTANCE, p.y + METEORS_INITIAL_HEIGHT, p.z))
            meteor.radius = radius
            meteor.block = mcpi.block.BEDROCK
            meteor.build()
            cls.meteors.append(meteor)

    @classmethod
    def build_scene(cls):
        cls.build_meteors()

    @classmethod
    def main(cls):
        try:
            World.renderer = RaspberryPi(MC_SEVER_HOST, MC_SEVER_PORT)

            World.renderer.post_to_chat("Building Meteors Scene")
            cls.pos = World.renderer.server.mc.entity.getTilePos(World.renderer.server.mc.getPlayerEntityId(BUILDER_NAME))
            cls.pos.x += 1

            cls.build_scene()

            while True:
                # The meteors approach the world and go deep
                # inside it
                logging.debug("Updating meteor position")
                cls.move_meteors()
                time.sleep(MOVE_UPDATES_TIME)

        except mcpi.connection.RequestError:
            print("Can't connect to Minecraft server " + MC_SEVER_HOST)


if __name__ == "__main__":
    SceneMeteors.main()
    sys.exit(0)
