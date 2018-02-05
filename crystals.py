import bpy
import os
import random
import numpy as np

from utils import *
from main import *


class CrystalGenetic(GenericGenetic):
    """Représente un individu de cristal avec son génotype"""

    def __init__(self, parent=None):
        GenericGenetic.__init__(self, parent)

    def random_genotype(self):
        """génère un génotype random. Composition du génotype d'un crystal :
           [subcrytals (1-4):
                [Cuts (0 - 50):
                    - phi, theta, r
                ]
                Scale : (x, y, z)
                Orientation : (phi, theta)
                Offset : (w)
           ]
           """
        return [random.getrandbits(32) for v in range(11)]

    def genotype_as_string(self):
        out = "#"
        for g in self.genotype:
            out += " " + hex(g)
        return out

    def compute_individual(self, location):
        """Génère un cristal"""

        nb_subcristals = int(self.genotype[0] / (2**32) * 3 + 1)
        print(nb_subcristals)

        for n in range(0, nb_subcristals):

            # Etape 1 : on crée l'objet (une icosphere)
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,
                                                  size=1,
                                                  view_align=False,
                                                  location=location,
                                                  enter_editmode=True)
            bpy.context.object.name = "Crystal" + str(GenericGenetic.bobject_unique_id())
            self.generated = bpy.context.object.name

            # Etape 2 : on cut l'objet avec bisect
            num_cuts = int(self.genotype[1 + n] / (2**32) * 64)
            object_center = list(bpy.data.objects[self.generated].location)

            for i in range (0, num_cuts):
                # Déterminons un plan aléatoire
                plane_co = spherical_to_xyz(
                    self.genotype[(i + n + 0) % 6 + 2] / (2 ** 32) * 2 * math.pi,
                    self.genotype[(i + n + 1) % 6 + 2] / (2 ** 32) * 2 * math.pi,
                    self.genotype[(i + n + 2) % 6 + 2] / (2 ** 32) * 0.9
                )  # point sur le plan de coupe
                plane_no = np.subtract(plane_co, object_center)  # normale du plan de coupe (pointe vers l'extérieur)
                plane_no_magnitude = math.sqrt((plane_no ** 2).sum())
                plane_no /= plane_no_magnitude
                # Coupons
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(plane_co=plane_co,
                                    plane_no=plane_no,
                                    use_fill=True, clear_inner=False, clear_outer=True,
                                    xstart=758, xend=818,
                                    ystart=550, yend=241)

            # Etape 3 : on scale l'objet
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.data.objects[self.generated].scale = (
                self.genotype[(8 + n) % 11] / (2 ** 32) * 2 + 1,
                self.genotype[(9 + n) % 11] / (2 ** 32) * 2 + 1,
                self.genotype[(10 + n) % 11] / (2 ** 32) * 2 + 1
            )

            # Etape 4 : on tourne et on positionne
            phi = self.genotype[(8 + n) % 11] / (2 ** 32) * 2 * math.pi
            theta = self.genotype[(9 + n) % 11] / (2 ** 32) * 2 * math.pi
            r = int(self.genotype[(10 + n) % 11] / (2 ** 32) * 3) + 1
            bpy.data.objects[self.generated].location = np.add(
                location,
                [r * math.sin(theta) * math.cos(phi),
                 r * math.sin(theta) * math.sin(phi),
                 r * math.cos(theta)]
            )
            bpy.context.object.rotation_euler[2] = phi
            bpy.context.object.rotation_euler[0] = theta


class AssetsGenerator:

    def __init__(self):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,  # l'ajout d'objet sert uniquement à ce que le reste ne
                                              size=1,          # plante pas si la scène est vide au départ.
                                              view_align=False,
                                              location=(0, 0, 0),
                                              enter_editmode=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpydeleteall()
        self.genotypes = []
        self.genotypes.append(CrystalGenetic())
        print(repr(self.genotypes[0]))
        self.genotypes[0].compute_individual((0, 0, 0))
        print(repr(self.genotypes[0]))


if __name__ == "__main__":
    assgen = AssetsGenerator()