#!/usr/bin/env python3
"""
Example: Aligning atom indices between two XYZ files

This example demonstrates how to use the align_atoms() function to reorder
atoms in one molecule to match the ordering of a reference molecule.

This is useful when:
- Comparing structures from different software packages
- Analyzing structures with different atom orderings
- Preparing structures for RMSD calculations
- Ensuring consistent atom indexing across multiple files
"""

from spivey_computational_toolkit.orca_py import xyz_molecule

# Example 1: Align two water molecules with different atom orderings
print("="*60)
print("Example 1: Aligning water molecules")
print("="*60)

# Create reference water molecule
ref = xyz_molecule()
ref.comment = "Reference water"
ref.add_atom("O", 0.0, 0.0, 0.0)
ref.add_atom("H", 0.757, 0.586, 0.0)
ref.add_atom("H", -0.757, 0.586, 0.0)

# Create misaligned water (same structure, different order)
misaligned = xyz_molecule()
misaligned.comment = "Misaligned water"
misaligned.add_atom("H", 0.757, 0.586, 0.0)  # Should be index 1
misaligned.add_atom("H", -0.757, 0.586, 0.0) # Should be index 2
misaligned.add_atom("O", 0.0, 0.0, 0.0)       # Should be index 0

print("\nBefore alignment:")
print("Reference:   O(0,0,0) H(0.757,0.586,0) H(-0.757,0.586,0)")
print("Misaligned:  ", end="")
for atom in misaligned.atom_list:
    print(f"{atom.atom_type}({atom.x:.3f},{atom.y:.3f},{atom.z:.3f}) ", end="")
print()

# Align the misaligned molecule
mapping = misaligned.align_atoms(ref)

print("\nAfter alignment:")
print("Aligned:     ", end="")
for atom in misaligned.atom_list:
    print(f"{atom.atom_type}({atom.x:.3f},{atom.y:.3f},{atom.z:.3f}) ", end="")
print()
print(f"\nMapping: {mapping}")
print("(This means: ref atom 0 -> original misaligned atom 2,")
print("             ref atom 1 -> original misaligned atom 0,")
print("             ref atom 2 -> original misaligned atom 1)")

# Example 2: Using align_atoms with a custom tolerance
print("\n" + "="*60)
print("Example 2: Using custom tolerance")
print("="*60)

# Create a slightly displaced structure
displaced = xyz_molecule()
displaced.comment = "Slightly displaced"
displaced.add_atom("H", 0.760, 0.590, 0.001)  # Slightly different position
displaced.add_atom("O", 0.002, 0.001, 0.001)
displaced.add_atom("H", -0.755, 0.585, 0.002)

print("\nWith default tolerance (0.5 Angstrom):")
try:
    mapping = displaced.align_atoms(ref)
    print("✓ Alignment successful")
    print(f"  Mapping: {mapping}")
except ValueError as e:
    print(f"✗ Alignment failed: {e}")

# Try with stricter tolerance
displaced2 = xyz_molecule()
displaced2.add_atom("H", 0.760, 0.590, 0.001)
displaced2.add_atom("O", 0.002, 0.001, 0.001)
displaced2.add_atom("H", -0.755, 0.585, 0.002)

print("\nWith stricter tolerance (0.001 Angstrom):")
try:
    mapping = displaced2.align_atoms(ref, tolerance=0.001)
    print("✓ Alignment successful (with warnings expected)")
except ValueError as e:
    print(f"✗ Alignment failed: {e}")

# Example 3: Practical use case - comparing energies after alignment
print("\n" + "="*60)
print("Example 3: Comparing bond lengths after alignment")
print("="*60)

# After alignment, we can reliably compare bond lengths
ref_oh_dist1 = ref.get_distance(0, 1)
aligned_oh_dist1 = misaligned.get_distance(0, 1)

print(f"\nO-H bond 1 distance:")
print(f"  Reference: {ref_oh_dist1:.4f} Å")
print(f"  Aligned:   {aligned_oh_dist1:.4f} Å")
print(f"  Match: {'✓' if abs(ref_oh_dist1 - aligned_oh_dist1) < 0.001 else '✗'}")

ref_oh_dist2 = ref.get_distance(0, 2)
aligned_oh_dist2 = misaligned.get_distance(0, 2)

print(f"\nO-H bond 2 distance:")
print(f"  Reference: {ref_oh_dist2:.4f} Å")
print(f"  Aligned:   {aligned_oh_dist2:.4f} Å")
print(f"  Match: {'✓' if abs(ref_oh_dist2 - aligned_oh_dist2) < 0.001 else '✗'}")

print("\n" + "="*60)
print("Alignment complete!")
print("="*60)
