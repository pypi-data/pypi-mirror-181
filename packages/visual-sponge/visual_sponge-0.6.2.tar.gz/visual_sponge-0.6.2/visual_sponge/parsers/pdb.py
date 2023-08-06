from pathlib import Path

from . import Parser
from .. import Model, mda
from ..utils import guess_bonds, guess_element

class PDBParser(Parser, formats="pdb"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        u = mda.Universe(m, topology_format="PDB", **kwargs)
        atoms = [{"elem": atom.element if hasattr(atom, "element") else guess_element(atom.name),
                  "atom": atom.name,
                  "resi": int(atom.resid),
                  "resn": atom.resname,
                  "x": float(atom.position[0]),
                  "y": float(atom.position[1]),
                  "z": float(atom.position[2]),
                  "bonds":[]} for atom in u.atoms]
        guess_bonds(u, atoms, 1.6)
        model = Model(name=Path(m).stem, u=u)
        model.traj_files.append((m, "PDB"))
        return atoms, model

    @staticmethod
    def Traj_Parse(traj):
        return "PDB"
