# Atom Alignment Feature

## Overview

The `align_atoms()` method has been added to the `xyz_molecule` class to solve the problem of misaligned atom indices when comparing molecular structures from different sources.

## Problem Statement

When working with molecular structures from different computational chemistry software packages or different calculation runs, the same molecule may have atoms listed in different orders. This makes direct comparison of structures (bond lengths, angles, RMSD, etc.) difficult or impossible.

## Solution

The `align_atoms()` method reorders the atoms in a molecule to match the ordering of a reference molecule. It uses a greedy algorithm that:

1. Matches atoms based on element type
2. Finds the closest spatial match for each atom
3. Ensures each atom is matched exactly once
4. Validates the alignment with a distance tolerance

## Method Signature

```python
xyz_molecule.align_atoms(reference_mol, tolerance=0.5)
```

**Parameters:**
- `reference_mol` (xyz_molecule): The reference molecule with the desired atom ordering
- `tolerance` (float): Maximum distance in Angstroms to consider atoms as matching (default: 0.5 Å)

**Returns:**
- `mapping` (list): List of indices showing the correspondence between reference and original molecule
  - `mapping[i]` gives the index in the original molecule that corresponds to atom `i` in the reference

**Raises:**
- `ValueError`: If molecules have different numbers of atoms or incompatible atom types

**Warnings:**
- Prints warnings to stdout if any atom match exceeds the tolerance threshold

## Usage Examples

### Basic Usage

```python
from spivey_computational_toolkit.orca_py import xyz_molecule

# Load two structures of the same molecule
reference = xyz_molecule.from_xyz('reference.xyz')
structure = xyz_molecule.from_xyz('structure.xyz')

# Align structure to match reference ordering
mapping = structure.align_atoms(reference)

# Now atoms are in the same order and can be compared directly
distance1 = structure.get_distance(0, 1)
distance2 = reference.get_distance(0, 1)
```

### With Custom Tolerance

```python
# Use stricter tolerance for high-precision matching
mapping = structure.align_atoms(reference, tolerance=0.1)
```

### Error Handling

```python
try:
    mapping = structure.align_atoms(reference)
    print(f"Alignment successful: {mapping}")
except ValueError as e:
    print(f"Alignment failed: {e}")
```

## Algorithm Details

The alignment algorithm works as follows:

1. **Validation**: Check that both molecules have the same number of atoms and the same composition of element types

2. **Greedy Matching**: For each atom in the reference molecule (in order):
   - Find all unused atoms in the target molecule with the same element type
   - Calculate Euclidean distances to each candidate
   - Select the closest match
   - Mark that atom as used

3. **Tolerance Check**: Issue warnings if any match exceeds the specified tolerance

4. **Reordering**: Reorder the target molecule's atom list according to the computed mapping

## Limitations

- **Algorithm**: Uses a greedy approach which may not find the globally optimal alignment in complex cases
- **Symmetry**: May not handle molecular symmetry optimally (e.g., equivalent hydrogen atoms)
- **Structural Similarity**: Requires structures to be spatially similar (within tolerance distance)
- **Exact Composition**: Requires identical atom type compositions

## Use Cases

1. **Multi-Software Workflows**: Aligning structures from different computational chemistry packages
2. **RMSD Calculations**: Preparing structures for accurate RMSD comparisons
3. **Trajectory Analysis**: Ensuring consistent atom ordering across trajectory frames
4. **Structure Comparison**: Comparing optimized structures from different starting points
5. **Database Matching**: Aligning downloaded structures to internal reference structures

## Testing

A comprehensive example script is provided in `examples/align_atoms_example.py` demonstrating:
- Basic alignment of water molecules
- Custom tolerance usage
- Bond length comparison after alignment
- Error handling

## Implementation Location

- **Module**: `spivey_computational_toolkit/orca_py/orca_xyz.py`
- **Class**: `xyz_molecule`
- **Method**: `align_atoms()`
- **Lines**: 136-203

## Related Methods

- `get_distance()`: Calculate distances between aligned atoms
- `get_bond_angle()`: Calculate angles using aligned atom indices
- `from_xyz()`: Load XYZ files for alignment
- `to_xyz()`: Save aligned structures

## Version

Added in version 0.1.0
