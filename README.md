# Spivey-computational-toolkit

A Python toolkit for computational chemistry and molecular dynamics analysis from the Spivey Group.

## Features

### pygmx submodule
- **XVG File Parsing**: Automatically parse GROMACS XVG files with support for multiple data columns
- **Data Visualization**: Plot raw data and cumulative averages side-by-side
- **Statistical Analysis**: Calculate mean, std dev, min, max, and cumulative averages
- **Flexible Access**: Retrieve data using column names (s0, s1, etc.) or legend labels
- **Time Range Filtering**: Focus on specific time windows for analysis

## Installation

### From PyPI (when published)
```bash
pip install Spivey-computational-toolkit
```

### From source
```bash
git clone https://github.com/SpiveyGroup/Spivey-computational-toolkit.git
cd Spivey-computational-toolkit
pip install -e .
```

### Development installation
```bash
pip install -e .[dev]
```

## Quick Start

### Using pygmx for GROMACS XVG analysis

```python
from spivey_computational_toolkit.pygmx import Gmx_Xvg

# Load XVG file
xvg = Gmx_Xvg('energy.xvg')

# Print summary statistics
xvg.get_summary()

# Plot all data with cumulative averages
xvg.plot_separate()

# Plot specific time range
xvg.plot_separate(time_start=1000, time_end=5000)

# Get cumulative average for a column
cum_avg = xvg.get_cumulative_average('Temperature')

# Get final converged value
final_value = xvg.get_final_cumulative_average('Temperature')

# Get all final cumulative averages
all_finals = xvg.get_all_final_cumulative_averages()
print(all_finals)
```

## Requirements

- Python >= 3.7
- numpy >= 1.19.0
- matplotlib >= 3.3.0

## License

MIT License

## Author

Alan He from Spivey Group

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
