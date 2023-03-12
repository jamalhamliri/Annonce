
from enum import Enum, IntEnum

class AnnonceTYPE(IntEnum):
    Offre = 0
    Demande = 1

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

