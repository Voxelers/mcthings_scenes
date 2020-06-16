#!/usr/bin/env python3

# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0
# Author (©): Alvaro del Castillo
import logging
import sys
import time

import mcpi.block
import mcpi.minecraft
from mcpi.vec3 import Vec3

from mcthings.schematic import Schematic
from mcthings.server import Server
from mcthings.world import World

BUILDER_NAME = "ElasticExplorer"

MC_SEVER_HOST = "localhost"
MC_SEVER_PORT = 4711

SPACESHIP_INITIAL_HEIGHT = 15
MOVE_UPDATES_TIME = 0.5
MOVE_DISTANCE = 1
GROUND_HEIGHT = 0


class SceneSpaceShip:
    """
    Scene Space Ship

    A space ship lands in the earth with a mysterious guest

    The movement of the spaceship will be update each
    MOVE_UPDATES_TIME
    """

    spaceship = None

    @classmethod
    def move_spaceship(cls):
        """ Move spaceship approaching the surface """
        ship = cls.spaceship
        p = ship.position
        if p.y - MOVE_DISTANCE >= GROUND_HEIGHT:
            ship.move(Vec3(p.x, p.y - MOVE_DISTANCE, p.z))
        elif p.y >= GROUND_HEIGHT:
            ship.move(Vec3(p.x, p.y - 1, p.z))
        else:
            logging.info("Spaceship hits surface")
            sys.exit(0)

    @classmethod
    def build_ship(cls):
        p = cls.pos
        p = Vec3(p.x, p.y + SPACESHIP_INITIAL_HEIGHT, p.z)
        ship = Schematic(p)
        ship.file_path = "schematics/ship2.schematic"
        ship.change_blocks = {mcpi.block.ICE.id: mcpi.block.GLASS.id}
        ship.build()
        cls.spaceship = ship

    @classmethod
    def build_scene(cls):
        cls.build_ship()

    @classmethod
    def main(cls):
        try:
            World.connect(Server(MC_SEVER_HOST, MC_SEVER_PORT))

            World.server.postToChat("Building Spaceship Scene")
            cls.pos = World.server.entity.getTilePos(World.server.getPlayerEntityId(BUILDER_NAME))
            cls.pos.x += 1

            cls.build_scene()

            while True:
                # The spaceship approach the world and land on it
                logging.debug("Updating spaceship position")
                cls.move_spaceship()
                time.sleep(MOVE_UPDATES_TIME)

        except mcpi.connection.RequestError:
            print("Can't connect to Minecraft server " + MC_SEVER_HOST)


if __name__ == "__main__":
    SceneSpaceShip.main()
    sys.exit(0)
