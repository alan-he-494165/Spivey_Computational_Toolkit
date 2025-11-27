import matplotlib.pyplot as plt
import numpy as np

class Gmx_Xvg:
    """
    Read and visualize XVG files from GROMACS or similar MD software
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.time = []
        self.data = {}  # Dictionary to store data columns
        self.column_names = []
        self.legends = {}  # Dictionary to store legend labels
        self.comments = []
        self.cumulative_averages = {}  # Store cumulative averages
        self.parse_xvg()
    
    def parse_xvg(self):
        """Parse XVG file and extract data"""
        with open(self.filepath, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
        
        data_lines = []
        
        for line in lines:
            # Skip comment lines
            if line.startswith('#'):
                self.comments.append(line)
                continue
            elif line.startswith('@'):
                # Parse legend labels
                if 'legend' in line:
                    # Format: @ s0 legend "Label Name"
                    parts = line.split()
                    if len(parts) >= 4:
                        col_id = parts[1]  # e.g., 's0', 's1'
                        # Extract legend text between quotes
                        legend_text = line.split('"')[1] if '"' in line else col_id
                        self.legends[col_id] = legend_text
                self.comments.append(line)
                continue
            elif line.strip() == '':
                continue
            else:
                # This is a data line
                data_lines.append(line)
        
        # Parse data lines
        for line in data_lines:
            values = line.split()
            if len(values) >= 2:
                values_float = [float(v) for v in values]
                self.time.append(values_float[0])
                
                # Store each column (s0, s1, s2, etc.)
                for i in range(1, len(values_float)):
                    col_name = f's{i-1}'
                    if col_name not in self.data:
                        self.data[col_name] = []
                        self.column_names.append(col_name)
                        # Set default legend if not found
                        if col_name not in self.legends:
                            self.legends[col_name] = col_name
                    self.data[col_name].append(values_float[i])
        
        # Calculate cumulative averages for all columns
        self._calculate_all_cumulative_averages()
    
    def calculate_cumulative_average(self, data_list):
        """Calculate cumulative average of a data list"""
        cumulative_avg = []
        cumsum = 0.0
        for i, val in enumerate(data_list, 1):
            cumsum += val
            cumulative_avg.append(cumsum / i)
        return cumulative_avg
    
    def _calculate_all_cumulative_averages(self):
        """Calculate cumulative averages for all data columns"""
        for col_name in self.column_names:
            self.cumulative_averages[col_name] = self.calculate_cumulative_average(self.data[col_name])
    
    def get_cumulative_average(self, column):
        """
        Get cumulative average for a specific column
        
        Parameters:
        -----------
        column : str
            Column name (e.g., 's0', 's1') or legend name
        
        Returns:
        --------
        list : Cumulative average values
        """
        # Check if column is a legend name
        if column in self.legends.values():
            # Find the column name from legend
            for col_name, legend in self.legends.items():
                if legend == column:
                    column = col_name
                    break
        
        if column in self.cumulative_averages:
            return self.cumulative_averages[column]
        else:
            raise ValueError(f"Column '{column}' not found. Available columns: {', '.join(self.column_names)}")
    
    def get_final_cumulative_average(self, column):
        """
        Get the final (converged) cumulative average value for a column
        
        Parameters:
        -----------
        column : str
            Column name (e.g., 's0', 's1') or legend name
        
        Returns:
        --------
        float : Final cumulative average value
        """
        cum_avg = self.get_cumulative_average(column)
        return cum_avg[-1]
    
    def get_all_final_cumulative_averages(self):
        """
        Get final cumulative average values for all columns
        
        Returns:
        --------
        dict : Dictionary mapping column names to their final cumulative averages
        """
        final_avgs = {}
        for col_name in self.column_names:
            legend_name = self.legends[col_name]
            final_avgs[legend_name] = self.cumulative_averages[col_name][-1]
        return final_avgs
    
    def plot_separate(self, time_start=None, time_end=None):
        """
        Plot each data column in separate subplots with cumulative average
        
        Parameters:
        -----------
        time_start : float, optional
            Start time for plotting
        time_end : float, optional
            End time for plotting
        """
        if time_start is None:
            time_start = self.time[0]
        if time_end is None:
            time_end = self.time[-1]
        
        # Filter data by time range
        indices = [i for i, t in enumerate(self.time) if time_start <= t <= time_end]
        time_filtered = [self.time[i] for i in indices]
        
        n_cols = len(self.column_names)
        
        # Create subplots (2 columns: raw data and cumulative average)
        fig, axes = plt.subplots(n_cols, 2, figsize=(16, 4 * n_cols))
        if n_cols == 1:
            axes = axes.reshape(1, -1)
        
        filename = self.filepath.split('/')[-1]
        fig.suptitle(f'XVG Visualization: {filename}', fontsize=16, fontweight='bold')
        
        for idx, col_name in enumerate(self.column_names):
            data_filtered = [self.data[col_name][i] for i in indices]
            cumulative_avg_filtered = [self.cumulative_averages[col_name][i] for i in indices]
            legend_name = self.legends[col_name]
            
            # Plot raw data
            axes[idx, 0].plot(time_filtered, data_filtered, linewidth=1.5, color='blue')
            axes[idx, 0].set_xlabel('Time', fontsize=11)
            axes[idx, 0].set_ylabel(legend_name, fontsize=11)
            axes[idx, 0].set_title(f'{legend_name} vs Time', fontsize=12, fontweight='bold')
            axes[idx, 0].grid(True, alpha=0.3)
            
            # Plot cumulative average
            axes[idx, 1].plot(time_filtered, cumulative_avg_filtered, linewidth=1.5, color='red')
            axes[idx, 1].set_xlabel('Time', fontsize=11)
            axes[idx, 1].set_ylabel(f'{legend_name} (Cumulative Avg)', fontsize=11)
            axes[idx, 1].set_title(f'{legend_name} - Cumulative Average vs Time', fontsize=12, fontweight='bold')
            axes[idx, 1].grid(True, alpha=0.3)
            
            # Add final value annotation
            final_val = cumulative_avg_filtered[-1]
            axes[idx, 1].axhline(y=final_val, color='green', linestyle='--', linewidth=1, alpha=0.7)
            axes[idx, 1].text(0.98, 0.98, f'Final: {final_val:.6f}', 
                            transform=axes[idx, 1].transAxes, 
                            fontsize=10, verticalalignment='top', horizontalalignment='right',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.show()
    
    def get_summary(self):
        """Print summary of the XVG file"""
        print("=" * 70)
        print("XVG FILE SUMMARY")
        print("=" * 70)
        print(f"File: {self.filepath}")
        print(f"Number of data points: {len(self.time)}")
        print(f"Time range: {self.time[0]:.2f} to {self.time[-1]:.2f}")
        print(f"\nColumns found:")
        for col_name in self.column_names:
            print(f"  {col_name}: {self.legends[col_name]}")
        print(f"Total columns: {len(self.column_names)}")
        
        print("\n" + "=" * 70)
        print("DATA STATISTICS")
        print("=" * 70)
        for col_name in self.column_names:
            data_array = np.array(self.data[col_name])
            legend_name = self.legends[col_name]
            final_cum_avg = self.cumulative_averages[col_name][-1]
            print(f"\n{legend_name} ({col_name}):")
            print(f"  Mean: {np.mean(data_array):.6f}")
            print(f"  Std Dev: {np.std(data_array):.6f}")
            print(f"  Min: {np.min(data_array):.6f}")
            print(f"  Max: {np.max(data_array):.6f}")
            print(f"  Final Cumulative Average: {final_cum_avg:.6f}")
        print("=" * 70)


if __name__ == "__main__":
    # Example usage
    vis = Gmx_Xvg('temperature.xvg')
    vis.get_summary()
    vis.plot_separate()
    
    # Get cumulative average for a specific column using legend name
    cum_avg = vis.get_cumulative_average('Energy')  # Or use 's0' for column name
    
    # Get final cumulative average value
    final_avg = vis.get_final_cumulative_average('Energy')
    
    # Get all final cumulative averages
    all_finals = vis.get_all_final_cumulative_averages()
    print(all_finals)
