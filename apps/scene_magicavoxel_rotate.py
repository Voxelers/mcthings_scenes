#!/usr/bin/env python3

# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0
# Author (©): Alvaro del Castillo

from os import listdir
from os.path import isdir, isfile, join
import time

import io, zipfile

import logging
import sys

import requests

import mcpi.block
import mcpi.minecraft
from mcpi.vec3 import Vec3
from mcthings.renderers.raspberry_pi import RaspberryPi

from mcthings.schematic import Schematic
from mcthings.vox import Vox
from mcthings.world import World

BUILDER_NAME = "ElasticExplorer"

MC_SEVER_HOST = "localhost"
MC_SEVER_PORT = 4711

MODELS_FOLDER = "scene-MagicaVoxel-models"
MODEL_MARGIN = 1  # blocks between models
MODELS_URL = "https://github.com/mikelovesrobots/mmmm/archive/master.zip"
MODELS_TOTAL = 487
MODELS_PER_ROW = 10


class SceneMagicaVoxelRotate:
    """
    Scene MagicaVoxel with models rotation

    Load the MODELS_TOTAL vox models from MODELS_URL and show them in Minecraft.

    """

    @classmethod
    def rotate_models(cls, thing1, thing2):
        # Let's rotate the things to simulate movement
        initial_pos1 = thing1.position
        initial_pos2 = thing2.position
        i = 0
        while True:
            time.sleep(1)
            thing1.unbuild()
            thing1._position = initial_pos1
            thing1.create()
            if i % 4 > 0:
                thing1.rotate((i % 4) * 90)
            thing1.render()

            time.sleep(1)
            thing2.unbuild()
            thing2._position = initial_pos2
            thing2.create()
            if i % 4 > 0:
                thing2.rotate((i % 4) * 90)
            thing2.render()

            i += 1

    @classmethod
    def rotate_model(cls, thing):
        # Let's rotate the thing to simulate movement
        initial_pos = thing.position
        i = 0
        while True:
            time.sleep(1)
            thing.unbuild()
            thing._position = initial_pos
            thing.create()
            if i % 4 > 0:
                thing.rotate((i % 4) * 90)
            thing.render()
            i += 1

    @classmethod
    def build_scene(cls):
        models_folder = join(MODELS_FOLDER, "mmmm-master", "vox")
        models_files = [f for f in listdir(models_folder) if isfile(join(models_folder, f))]
        logging.info("Number of models: %i " % len(models_files))
        if len(models_files) != MODELS_TOTAL:
            logging.error("Wrong number of models found: %i. Expected: %i" % (len(models_files), MODELS_TOTAL))

        init_pos = Vec3(cls.pos.x, cls.pos.y, cls.pos.z)
        models_files.sort()
        pos_z = init_pos.z
        max_row_length = 0
        pos = init_pos
        models = []
        for i in range(0, len(models_files)):
            model_file = models_files[i]
            if i % MODELS_PER_ROW == 0:
                pos = Vec3(init_pos.x, init_pos.y, pos.z + max_row_length)
            logging.debug("Creating model %s" % model_file)
            # Load the vox to get the dimensions
            vox = Vox(pos)
            vox.file_path = join(models_folder, model_file)
            vox.create()
            # Move to create space for the flip
            width = vox.end_position.x - pos.x
            length = vox.end_position.z - pos.z
            max_row_length = length if length > max_row_length else max_row_length
            vox = Vox(Vec3(pos.x + width, pos.y, pos.z))
            models.append(vox)
            vox.file_path = join(models_folder, model_file)
            vox.create()
            vox.flip_x()
            vox.render()
            if len(models) == 2:
                cls.rotate_models  (models[0], models[1])
            pos_x = vox.end_position.x + MODEL_MARGIN
            pos = Vec3(pos_x, pos.y, pos.z)

    @classmethod
    def main(cls):

        # Download all models (50MB aprox)
        if not isdir(MODELS_FOLDER):
            logging.info("Downloading all models (50MB) from " + MODELS_URL)
            r = requests.get(MODELS_URL)
            r.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(MODELS_FOLDER)
            logging.info("Models downloaded! Loading them ...")

        try:
            World.renderer = RaspberryPi(MC_SEVER_HOST, MC_SEVER_PORT)

            World.renderer.post_to_chat("Building MagicaVoxel Scene")
            cls.pos = World.renderer.get_pos(BUILDER_NAME)
            cls.pos.z += 20

            cls.build_scene()

        except mcpi.connection.RequestError:
            print("Can't connect to Minecraft server " + MC_SEVER_HOST)


if __name__ == "__main__":
    SceneMagicaVoxelRotate.main()
    sys.exit(0)
