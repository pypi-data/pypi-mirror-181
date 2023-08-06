from MDAnalysis.analysis import distances
from MDAnalysis.topology.guessers import guess_atom_element as guess_element

def guess_bonds(u, atoms, cutoff):
    id2index = {atomi.id : i for i, atomi in enumerate(u.atoms)}
    others = u.select_atoms("not (resname WAT or resname HOH or resname H2O)")
    waters = u.select_atoms("resname WAT or resname HOH or resname H2O")
    other_distances = distances.distance_array(others, others)
    mask = other_distances < cutoff
    for i, atomi in enumerate(others):
        for j in range(i + 1, len(others)):
            if mask[i][j]:
                atoms[id2index[atomi.id]]["bonds"].append(id2index[others[j].id])
    for residue in waters.residues:
        for i, o in enumerate(residue.atoms):
            for j in range(i+1, len(residue.atoms)):
                h = residue.atoms[j]
                atoms[id2index[o.id]]["bonds"].append(id2index[h.id])
