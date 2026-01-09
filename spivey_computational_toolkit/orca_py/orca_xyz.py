import numpy as np
import math

class atom:
    """
    Class to represent an atom in an XYZ file
    PARAMETERS
    ----------
        atom_type (str): type of the atom (e.g., "C", "H", "O")
        x (float): x-coordinate
        y (float): y-coordinate
        z (float): z-coordinate 
    """
    def __init__(self, atom_type:str, x, y, z):
        self.atom_type = atom_type
        self.x = x
        self.y = y
        self.z = z

class xyz_molecule:
    """
    Read and visualize XYZ files from ORCA or similar computational chemistry software
    PARAMETERS
    ----------
        comment (str): comment line from the XYZ file
        atom_list (list): list of atom objects
        energy (float): energy extracted from the comment line if available

    METHODS
    -------
        from_xyz(filepath): class method to create an instance from an XYZ file
        add_atom(atom_type, x, y, z): add an atom to the molecule
        to_xyz(filepath): write the molecule to an XYZ file
        get_distance(atom_index1, atom_index2): calculate distance between two atoms
        get_bond_angle(atom_index1, atom_index2, atom_index3): calculate bond angle between three atoms
    """
    
    def __init__(self):
        self.comment = ""
        self.atom_list = []
        self.energy = 0.0
    
    @classmethod
    def from_xyz(cls,filepath):
        """Parse XYZ file and extract data
        PARAMETERS
        ----------
            filepath (str): path to the XYZ file

        RETURNS
        -------
            instance (xyz_molecule): instance of the xyz_molecule class
        """
        instance = cls()
        with open(filepath, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
        
            num_atoms = int(lines[0])
            instance.comment = lines[1]
            
            for i in range(2, 2 + num_atoms):
                atom_line = lines[i].split()
                atom_type = atom_line[0]
                x, y, z = map(float, atom_line[1:4])
                instance.atom_list.append(atom(atom_type, x, y, z))

            try:
                instance.energy = float(instance.comment.split()[-1])
            except:
                instance.energy = 0.0
                
            return instance

    def add_atom(self, atom_type:str = "C", x = 0, y = 0, z = 0):
        """Add an atom to the current frame"""
        self.atom_list.append(atom(atom_type, x, y, z))

    def to_xyz(self, filepath):
        """Write the molecule to an XYZ file
        PARAMETERS
        ----------
            filepath (str): path to the output XYZ file
        """
        with open(filepath, 'w') as f:
            f.write(f"{len(self.atom_list)}\n")
            f.write(f"{self.comment}\n")
            for atom in self.atom_list:
                f.write(f"{atom.atom_type}  {atom.x:.6f}    {atom.y:.6f}    {atom.z:.6f}\n")

    def get_distance(self, atom_index1:int, atom_index2:int) -> float:
        """Calculate the distance between two atoms in the molecule
        PARAMETERS
        ----------
            atom_index1 (int): index of the first atom
            atom_index2 (int): index of the second atom

        RETURNS
        -------
            distance (float): distance between the two atoms
        """
        import math
        atom1 = self.atom_list[atom_index1]
        atom2 = self.atom_list[atom_index2]
        dx = atom1.x - atom2.x
        dy = atom1.y - atom2.y
        dz = atom1.z - atom2.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def get_bond_angle(self, atom_index1:int, atom_index2:int, atom_index3:int) -> float:
        """
        Calculate the bond angle between three atoms in the molecule
        PARAMETERS
        ----------
            atom_index1 (int): index of the first atom
            atom_index2 (int): index of the second atom (vertex)
            atom_index3 (int): index of the third atom
        
        RETURNS
        -------
            angle (float): bond angle in degrees
        """
        
        atom1 = self.atom_list[atom_index1]
        atom2 = self.atom_list[atom_index2]
        atom3 = self.atom_list[atom_index3]
        
        v1 = np.array([atom1.x - atom2.x, atom1.y - atom2.y, atom1.z - atom2.z])
        v2 = np.array([atom3.x - atom2.x, atom3.y - atom2.y, atom3.z - atom2.z])

        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = math.acos(cos_angle)
        
        return math.degrees(angle)
    

class mol_group:
    """
    Class to represent a group of molecules from an XYZ file
    PARAMETERS
    ----------
        molecules (list): list of xyz_molecule objects
        n_mol (int): number of molecules in the group
        energy (list): list of energies for each molecule

    METHODS
    -------
        load_trj(filepath): class method to load a trajectory from an XYZ file
        load_allxyz(filepath): class method to load a trajectory from an allxyz file
        to_trj(filepath): write the molecule group to an XYZ trajectory file
        to_allxyz(filepath): write the molecule group to an allxyz file
    """
    def __init__(self):
        self.molecules = []
        self.n_mol = 0
        self.energy = []
    
    @classmethod
    def load_trj(cls, filepath):
        instance = cls()
        with open(filepath, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
        n_atoms = int(lines[0])
        instance.n_mol = int(len(lines) / (n_atoms + 2))
        
        for i in range(0, instance.n_mol):
            instance.molecules.append(xyz_molecule())
            start = i * (n_atoms + 2)
            end = start + n_atoms + 2
            instance.molecules[i].comment = lines[start + 1]
            try:
                instance.energy.append(float(lines[start + 1].split()[-1]))
            except:
                instance.energy.append(0.0)
            for j in range(start + 2, end):
                atom_line = lines[j].split()
                atom_type = atom_line[0]
                x, y, z = map(float, atom_line[1:4])
                instance.molecules[-1].add_atom(atom_type, x, y, z)
        return instance
    
    @classmethod
    def load_allxyz(cls, filepath):
        instance = cls()
        with open(filepath, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
        n_atoms = int(lines[0])
        instance.n_mol = int((len(lines)+1) / (n_atoms + 3))
        for i in range(0, instance.n_mol):
            instance.molecules.append(xyz_molecule())
            start = i * (n_atoms + 3)
            end = start + n_atoms + 3
            instance.molecules[i].comment = lines[start + 1]
            try:
                instance.energy.append(float(lines[start + 1].split()[-1]))
            except:
                instance.energy.append(0.0)
            for j in range(start + 2, end - 1):
                atom_line = lines[j].split()
                atom_type = atom_line[0]
                x, y, z = map(float, atom_line[1:4])
                instance.molecules[-1].add_atom(atom_type, x, y, z)
        return instance
    
    def to_trj(self, filepath):
        """Write the molecule group to an XYZ trajectory file
        PARAMETERS
        ----------
            filepath (str): path to the output XYZ trajectory file
        """
        with open(filepath, 'w') as f:
            for mol in self.molecules:
                f.write(f"{len(mol.atom_list)}\n")
                f.write(f"{mol.comment}\n")
                for atom in mol.atom_list:
                    f.write(f"{atom.atom_type}  {atom.x:.6f}    {atom.y:.6f}    {atom.z:.6f}\n")

    def to_allxyz(self, filepath):
        """Write the molecule group to an allxyz file
        PARAMETERS
        ----------
            filepath (str): path to the output allxyz file
        """
        with open(filepath, 'w') as f:
            for mol in self.molecules:
                f.write(f"{len(mol.atom_list)}\n")
                f.write(f"{mol.comment}\n")
                for atom in mol.atom_list:
                    f.write(f"{atom.atom_type}  {atom.x:.6f}    {atom.y:.6f}    {atom.z:.6f}\n")
                f.write("\n")
                if mol != self.molecules[-1]:
                    f.write(">\n")

    def sort_by_energy(self, overwrite:bool = False):
        """Sort the molecules in the group by their energy values
        PARAMETERS
        ----------
            overwrite (bool): if True, overwrite the current order of molecules

        RETURNS (if overwrite is False)
        -------------------------------
            index (list): list of indices that would sort the molecules by energy
            energy (list): sorted list of energies
        """
        if len(self.energy) != self.n_mol:
            raise ValueError("Energy list length does not match number of molecules.")
        elif self.n_mol == 0:
            raise ValueError("No molecules to sort.")
        if overwrite:
            sorted_molecules = [mol for _, mol in sorted(zip(self.energy, self.molecules), key=lambda x: x[0])]
            self.molecules = sorted_molecules
            self.energy.sort()
            return
        index, energy = zip(*sorted(enumerate(self.energy), key=lambda x: x[1]))
        return index, energy
    