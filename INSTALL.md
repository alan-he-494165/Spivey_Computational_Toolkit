# Installation Guide for Spivey-computational-toolkit

## Quick Installation

### Option 1: Install in Development Mode (Recommended for local use)

This allows you to edit the code and see changes immediately without reinstalling:

```bash
cd /Users/alan/Spivey_Computational_Toolkit
pip install -e .
```

### Option 2: Install as a Regular Package

```bash
cd /Users/alan/Spivey_Computational_Toolkit
pip install .
```

### Option 3: Install with Development Dependencies

For development and testing:

```bash
cd /Users/alan/Spivey_Computational_Toolkit
pip install -e .[dev]
```

## Verify Installation

After installation, test it in Python:

```python
from spivey_computational_toolkit.pygmx import Gmx_Xvg
print("Installation successful!")
```

## Usage Example

```python
from spivey_computational_toolkit.pygmx import Gmx_Xvg

# Load and analyze XVG file
xvg = Gmx_Xvg('your_file.xvg')
xvg.get_summary()
xvg.plot_separate()

# Get cumulative averages
cum_avg = xvg.get_cumulative_average('Temperature')
final_avg = xvg.get_final_cumulative_average('Temperature')
```

## Uninstall

```bash
pip uninstall Spivey-computational-toolkit
```

## Troubleshooting

### Import Error
If you get an import error, make sure:
1. You're in the correct Python environment
2. The package is installed: `pip list | grep Spivey`
3. Try reinstalling: `pip uninstall Spivey-computational-toolkit && pip install -e .`

### Dependencies
If matplotlib or numpy are missing:
```bash
pip install numpy matplotlib
```
