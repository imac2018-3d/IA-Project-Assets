class GenericGenetic:
    """Classe abstraite pour gérer les individus"""

    def __init__(self, parent=None):
        """Crée un individu. Son génotype st alors aléatoirement généré"""
        self.genotype = self.random_genotype()  # genotype de l'individu
        self.generated = None  # Nom de l'objet généré. None sinon.
        self.fitness = None  # Valeur de fitness (entre 0 et 1) calculée. None sinon.
        self.parentName = parent  # Nom blender de l'objet parent

    def random_genotype(self):
        """Doit être redéfinie. Génère un génotype aléatoirement"""
        return None

    def compute_fitness(self):
        """Doit être redéfinie. Calcule et retourne la valeur de fitness (entre 0 et 1)"""
        return None

    def compute_individual(self, location):
        """Doit être redéfinie si un object 3D représente l'individu.
           Calcule le phénotype (l'individu). Doit retourner le nom de l'objet 3D"""
        return None

    def genotype_as_string(self):
        """Doit être réimplémentée. Retourna une version string du génotype."""

    def __str__(self):
        return str(self.generated)

    def __repr__(self):
        return str(self.genotype_as_string()) + " (" + str(self.generated) + ")"

    last_unique_boject_id = None
    @staticmethod
    def bobject_unique_id():
        if GenericGenetic.last_unique_boject_id is None:
            GenericGenetic.last_unique_boject_id = 0
        else:
            GenericGenetic.last_unique_boject_id += 1
        return GenericGenetic.last_unique_boject_id
