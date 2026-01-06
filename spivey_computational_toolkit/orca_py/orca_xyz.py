class atom:
    """
    Class to represent an atom in an XYZ file
    """
    def __init__(self, atom_type:str, x, y, z):
        self.atom_type = atom_type
        self.x = x
        self.y = y
        self.z = z

class xyz_molecule:
    """
    Read and visualize XYZ files from ORCA or similar computational chemistry software
    """
    
    def __init__(self):
        self.comment = ""
        self.atom_list = []
        self.energy = 0.0
    
    @classmethod
    def from_xyz(cls,filepath):
        """Parse XYZ file and extract data"""
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

    def add_atom(self, atom_type:str, x, y, z):
        """Add an atom to the current frame"""
        self.atom_list.append(atom(atom_type, x, y, z))

    def to_xyz(self, filepath):
        """Write the molecule to an XYZ file"""
        with open(filepath, 'w') as f:
            f.write(f"{len(self.atom_list)}\n")
            f.write(f"{self.comment}\n")
            for atom in self.atom_list:
                f.write(f"{atom.atom_type}  {atom.x:.6f}    {atom.y:.6f}    {atom.z:.6f}\n")

class mol_group:
    """
    Class to represent a group of molecules from an XYZ file
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
        """Write the molecule group to an XYZ trajectory file"""
        with open(filepath, 'w') as f:
            for mol in self.molecules:
                f.write(f"{len(mol.atom_list)}\n")
                f.write(f"{mol.comment}\n")
                for atom in mol.atom_list:
                    f.write(f"{atom.atom_type}  {atom.x:.6f}    {atom.y:.6f}    {atom.z:.6f}\n")
    def to_allxyz(self, filepath):
        """Write the molecule group to an allxyz file"""
        with open(filepath, 'w') as f:
            for mol in self.molecules:
                f.write(f"{len(mol.atom_list)}\n")
                f.write(f"{mol.comment}\n")
                for atom in mol.atom_list:
                    f.write(f"{atom.atom_type}  {atom.x:.6f}    {atom.y:.6f}    {atom.z:.6f}\n")
                f.write("\n")
                if mol != self.molecules[-1]:
                    f.write(">\n")
