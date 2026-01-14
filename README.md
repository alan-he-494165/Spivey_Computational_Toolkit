# Spivey-computational-toolkit

A Python toolkit for computational chemistry and molecular dynamics analysis from the Spivey Group.

## Features

### pygmx submodule
- **XVG File Parsing**: Automatically parse GROMACS XVG files with support for multiple data columns
- **Data Visualization**: Plot raw data and cumulative averages side-by-side
- **Statistical Analysis**: Cumulative averages
- **Flexible Access**: Retrieve data using column names (s0, s1, etc.) or legend labels
- **Time Range Filtering**: Focus on specific time windows for analysis

## Installation

### From PyPI (recommended)
```bash
pip install Spivey-computational-toolkit
```

### From source
```bash
git clone https://github.com/alan-he-494165/Spivey_Computational_Toolkit.git
cd Spivey_Computational_Toolkit
pip install .
```

## Quick Start

### Using pygmx for GROMACS XVG analysis

```python
from spivey_computational_toolkit.pygmx import Gmx_Xvg

# Load XVG file
xvg = Gmx_Xvg('nvt.xvg')

# Print summary statistics
xvg.get_summary()

# Plot all data with cumulative averages
xvg.plot_separate()

# Plot specific time range
xvg.plot_separate(time_start=1000, time_end=5000)

# Get cumulative average for a column
cum_avg = xvg.get_cumulative_average('Potential')

# Get final converged value
final_value = xvg.get_final_cumulative_average('Potential')

# Get all final cumulative averages
all_finals = xvg.get_all_final_cumulative_averages()
print(all_finals)
```

## orca_py submodule

The `orca_py` submodule provides simple helpers for reading and writing ORCA-style XYZ files and trajectories, along with geometry calculation tools.

- `atom`: lightweight container for an atom (`atom_type`, `x`, `y`, `z`).
- `xyz_molecule`: represents a single XYZ frame with:
	- `from_xyz(filepath)` — classmethod to parse a single-frame XYZ file and extract `comment`, `atom_list`, and an optional energy parsed from the comment line.
	- `add_atom(atom_type, x, y, z)` — add an atom to the molecule.
	- `to_xyz(filepath)` — write the molecule out to an XYZ file.
	- `get_distance(atom_index1, atom_index2)` — calculate the distance between two atoms (in Angstroms).
	- `get_bond_angle(atom_index1, atom_index2, atom_index3)` — calculate the bond angle between three atoms in degrees (atom_index2 is the vertex).
	- `align_atoms(reference_mol, tolerance=0.5)` — align the atom ordering to match a reference molecule based on atom types and spatial proximity. Useful when comparing structures from different sources with different atom orderings.
- `mol_group`: container for multiple `xyz_molecule` frames with:
	- `load_trj(filepath)` — load a simple trajectory where frames are contiguous (no blank lines between frames).
	- `load_allxyz(filepath)` — load a file with a blank line and `>` separators between frames (allxyz format).
	- `to_trj(filepath)` — write frames in the simple trajectory format.
	- `to_allxyz(filepath)` — write frames in the allxyz format (blank line and `>` separators).
	- `sort_by_energy(overwrite=False)` — sort molecules by energy values. If `overwrite=True`, modifies the current group in place; otherwise returns sorted indices and energies.

Basic examples:

```python
from spivey_computational_toolkit.orca_py import xyz_molecule, mol_group, atom

# Read a single XYZ file
mol = xyz_molecule.from_xyz('sample.xyz')
print('atoms:', len(mol.atom_list), 'energy:', mol.energy)

# Calculate geometry parameters
distance = mol.get_distance(0, 1)  # Distance between atoms 0 and 1
print(f'Bond length: {distance:.3f} Angstroms')

angle = mol.get_bond_angle(0, 1, 2)  # Angle at atom 1
print(f'Bond angle: {angle:.2f} degrees')

# Align atoms to match a reference structure (useful when atom indices differ)
reference = xyz_molecule.from_xyz('reference.xyz')
mol2 = xyz_molecule.from_xyz('structure.xyz')
mapping = mol2.align_atoms(reference)  # Reorders mol2 atoms to match reference
print(f'Atom mapping: {mapping}')

# Read a trajectory
group = mol_group.load_trj('traj.xyz')
print('frames:', group.n_mol)
print('energies:', group.energy[:5])

# Sort structures by energy
sorted_indices, sorted_energies = group.sort_by_energy()
print(f'Lowest energy: {sorted_energies[0]:.6f}')

# Or sort in place
group.sort_by_energy(overwrite=True)

# Write back to disk
group.to_trj('out_traj.xyz')
group.to_allxyz('out_all.xyz')
```

## Requirements

- Python >= 3.7
- numpy >= 1.19.0
- matplotlib >= 3.3.0

## License

MIT License

## Author

Alan He from [Spivey Group](https://www.imperial.ac.uk/spivey-group/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
