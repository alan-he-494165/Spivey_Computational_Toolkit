("""orca_py — helpers for reading and writing ORCA-style XYZ files.

This package exposes lightweight classes for working with single-frame
XYZ files and simple multi-frame trajectory formats.

Public symbols:
- `atom` — lightweight atom container
- `xyz_molecule` — single XYZ frame
- `mol_group` — collection of frames / trajectory - special for ORCA
""")

from .orca_xyz import atom, xyz_molecule, mol_group

__all__ = ["atom", "xyz_molecule", "mol_group"]

__version__ = "0.1.0"

