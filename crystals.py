from utils import *
from main import *

import io
import numpy as np

class CrystalGenetic(GenericGenetic):
    """Représente un individu de cristal avec son génotype"""

    def __init__(self, parent=None):
        GenericGenetic.__init__(self, parent)

    def random_genotype(self):
        """génère un génotype random. Composition du génotype d'un crystal :
           [subcrytals (1-4):
                Cuts: [Cuts (0 - 50):
                    (phi, theta, r)
                ]
                Scale : (x, y, z)
                Orientation : (phi, theta)
                Offset : (w)
           ]
           """
        return [{
            'cuts': [(
                random.random() * 2 * math.pi,
                random.random() * 2 * math.pi,
                random.uniform(0.5, 0.9)
            ) for b in range(0, random.randint(1, 51))],
            'scale': (
                random.uniform(0.5, 1),
                random.uniform(0.5, 1),
                random.uniform(1, 3)
            ),
            'orientation': (
                random.uniform(0, math.pi * 2),
                random.uniform(0, math.pi / 2),  # ici c'est seulement un quart de cercle
            ),
            'offset': random.uniform(-2, 0)  # c'est en gros l'enfoncement du crystal dans le sol (donc négatif)
        } for a in range(1, random.randint(2, 5))]

    def genotype_as_string(self):
        buf = io.StringIO()
        for subcrystal in self.genotype:
            buf.write("#[\ncuts: [\n")
            for cut in subcrystal['cuts']:
                buf.write("\t" + str(cut[0]) + " " + str(cut[1]) + " " + str(cut[2]) + "\n")
            buf.write("]\nscale: "
                      + str(subcrystal['scale'][0]) + " "
                      + str(subcrystal['scale'][1]) + " "
                      + str(subcrystal['scale'][2])
                      + "\n")
            buf.write("orientation: "
                      + str(subcrystal['orientation'][0]) + " "
                      + str(subcrystal['orientation'][1]) + "\n")
            buf.write("offset: " + str(subcrystal['offset']) + "\n")
        buf.write("]")

        ret = buf.getvalue()
        buf.close()
        return ret

    def compute_individual(self, location):
        """Génère un cristal"""

        bpy.ops.object.add(type='EMPTY')
        bpy.context.object.name = "Crystal" + str(GenericGenetic.bobject_unique_id())
        self.generated = bpy.context.object.name
        parent_obj = bpy.context.object

        for idx, subcrystal in enumerate(self.genotype):

            # Etape 1 : on crée l'icosphere
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,
                                                  size=1,
                                                  view_align=False,
                                                  location=location,
                                                  enter_editmode=False)
            bpy.context.scene.objects.active.parent = parent_obj
            bpy.context.object.name = "Sub" + parent_obj.name + "-" + str(idx)
            object_center = list(bpy.context.object.location)
            object_ref = bpy.context.object

            # Etape 2 : on cutte
            for cut in subcrystal['cuts']:
                plane_co = spherical_to_xyz(cut[0], cut[1], cut[2])  # point sur le plan de coupe
                plane_no = np.subtract(plane_co, object_center)  # normale du plan de coupe (pointe vers l'extérieur)
                plane_no_magnitude = math.sqrt((plane_no ** 2).sum())
                plane_no /= plane_no_magnitude
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(plane_co=plane_co,
                                    plane_no=plane_no,
                                    use_fill=True, clear_inner=False, clear_outer=True,
                                    xstart=-100, xend=100,
                                    ystart=-100, yend=100)
                bpy.ops.object.mode_set(mode='OBJECT')

            # Etape 3 : on scale l'objet
            object_ref.scale = (
                subcrystal['scale'][0],
                subcrystal['scale'][1],
                subcrystal['scale'][2]
            )

            # Etape 4 : on tourne et on positionne
            bpy.context.object.rotation_euler[0] = subcrystal['orientation'][1]
            bpy.context.object.rotation_euler[2] = subcrystal['orientation'][0]
            object_ref.location = (
                (subcrystal['scale'][2] + subcrystal['offset']) * math.sin(subcrystal['orientation'][0]) * math.sin(subcrystal['orientation'][1]),
                (subcrystal['scale'][2] + subcrystal['offset']) * -math.cos(subcrystal['orientation'][0]) * math.sin(subcrystal['orientation'][1]),
                (subcrystal['scale'][2] + subcrystal['offset']) * math.cos(subcrystal['orientation'][1])
            )


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
